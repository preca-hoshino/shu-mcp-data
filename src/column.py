"""
shu-mcp 栏目爬取
———— 单栏目页面级并发，含 URL 推断与顺序回退
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import threading
from typing import TYPE_CHECKING, Any

from fetch import fetch
from parser import build_page_urls, extract_articles, find_next_page_url, get_total_pages_from_html

if TYPE_CHECKING:
    from crawler import ProgressProto

PAGE_TIMEOUT = 120


# =========================================================================
# 页面并发抓取（提取公共逻辑，消除重复）
# =========================================================================


def _concurrent_fetch_pages(  # noqa: PLR0913
    urls: list[str],
    all_articles: list[dict[str, Any]],
    column_name: str,
    cfg: dict[str, Any],
    dept: str,
    page_workers: int,
    verbose: bool,
    progress: ProgressProto | None,
) -> int:
    """并发抓取多个页面 URL，将文章追加到 all_articles。返回失败页数。"""
    if not urls:
        return 0

    failed_pages = 0
    lock = threading.Lock()
    failed_lock = threading.Lock()

    def _fetch_one(u: str) -> None:
        nonlocal failed_pages
        h = fetch(u, verbose=verbose)
        if not h:
            with failed_lock:
                failed_pages += 1
            return
        aa = extract_articles(h, u, cfg)
        for x in aa:
            x["column"] = column_name
        with lock:
            all_articles.extend(aa)

    pw = min(page_workers, len(urls))
    with ThreadPoolExecutor(max_workers=pw) as executor:
        futures = {executor.submit(_fetch_one, u): u for u in urls}
        for fut in futures:
            try:
                fut.result(timeout=PAGE_TIMEOUT)
            except (RuntimeError, OSError, TimeoutError):
                with failed_lock:
                    failed_pages += 1
            finally:
                if progress:
                    progress.step_dept(dept)
        executor.shutdown(wait=False, cancel_futures=True)
    return failed_pages


# =========================================================================
# 单栏目爬取
# =========================================================================


def crawl_one_column(  # noqa: C901, PLR0912, PLR0913, PLR0915
    domain: str,
    dept: str,
    path: str,
    column_name: str,
    cfg: dict[str, Any],
    progress: ProgressProto | None = None,
    page_workers: int = 3,
    verbose: bool = True,
    max_pages: int = 0,
) -> tuple[int, list[dict[str, Any]], str]:
    """爬取某个栏目的文章。

    返回: (总页数, 文章列表, 告警信息)
    """
    url = f"https://{domain}/{path}"
    all_articles: list[dict[str, Any]] = []
    failed_pages = 0

    # ---- 首页 ----
    html = fetch(url, verbose=verbose)
    if not html:
        msg = f"首页请求失败: {url}"
        raise RuntimeError(msg)

    total = get_total_pages_from_html(html, cfg) or 1
    arts = extract_articles(html, url, cfg)
    for a in arts:
        a["column"] = column_name
    all_articles.extend(arts)
    if progress:
        progress.step_dept(dept)

    # ---- 应用页数限制 ----
    if max_pages > 0:
        total = min(total, max_pages)
    if total <= 1:
        return total, all_articles, ""

    # ---- 尝试 URL 推断 → 并发 ----
    next_url = find_next_page_url(html, url, cfg)
    page_urls = build_page_urls(url, next_url, total)
    if max_pages > 0 and len(page_urls) > max_pages - 1:
        page_urls = page_urls[: max_pages - 1]

    if page_urls:
        failed_pages += _concurrent_fetch_pages(
            page_urls,
            all_articles,
            column_name,
            cfg,
            dept,
            page_workers,
            verbose,
            progress,
        )
    elif next_url:
        # URL 推断失败 → 探测第 2 页后再尝试推断
        pages_crawled = 1
        h2 = fetch(next_url, verbose=verbose)
        if h2:
            pages_crawled += 1
            nxt2 = find_next_page_url(h2, next_url, cfg)
            page_urls2 = build_page_urls(url, next_url, total)
            if not page_urls2 and nxt2 and nxt2 != next_url:
                page_urls2 = build_page_urls(next_url, nxt2, total)

            # 第 2 页文章先提取
            aa2 = extract_articles(h2, next_url, cfg)
            for x in aa2:
                x["column"] = column_name
            all_articles.extend(aa2)
            if progress:
                progress.step_dept(dept)

            if page_urls2:
                # 过滤掉已爬的第 2 页
                remaining = [u for u in page_urls2 if u != next_url]
                if max_pages > 0:
                    remaining = remaining[: max_pages - pages_crawled]
                failed_pages += _concurrent_fetch_pages(
                    remaining,
                    all_articles,
                    column_name,
                    cfg,
                    dept,
                    page_workers,
                    verbose,
                    progress,
                )
                return (
                    total,
                    all_articles,
                    _build_warning(dept, column_name, total, failed_pages, all_articles, verbose),
                )

            # 仍然不能推断 → 退回到顺序模式
            current = nxt2
        else:
            failed_pages += 1
            if progress:
                progress.step_dept(dept)
            current = None

        # ---- 最终回退：顺序爬取 ----
        visited: set[str] = {url, next_url} if next_url else {url}
        while current and current not in visited:
            if max_pages > 0 and pages_crawled >= max_pages:
                break
            visited.add(current)
            h = fetch(current, verbose=verbose)
            if not h:
                failed_pages += 1
                if progress:
                    progress.step_dept(dept)
                break
            aa = extract_articles(h, current, cfg)
            for x in aa:
                x["column"] = column_name
            all_articles.extend(aa)
            pages_crawled += 1
            if progress:
                progress.step_dept(dept)
            nxt = find_next_page_url(h, current, cfg)
            if nxt == current:
                break
            current = nxt

    return (
        total,
        all_articles,
        _build_warning(dept, column_name, total, failed_pages, all_articles, verbose),
    )


def _build_warning(  # noqa: PLR0913
    dept: str,
    column_name: str,
    total: int,
    failed_pages: int,
    all_articles: list[dict[str, Any]],
    verbose: bool,
) -> str:
    """构建诊断告警信息。"""
    if not all_articles:
        warning = f"{dept} · {column_name}: 0篇文章（{total}页）"
    elif failed_pages > 0:
        warning = f"{dept} · {column_name}: {failed_pages}/{total} 页请求失败"
    else:
        return ""
    if verbose:
        pass
    return warning
