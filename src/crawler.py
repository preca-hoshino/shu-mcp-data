"""
shu-mcp 爬取引擎
———— 动态部门均衡调度 + 栏目任务编排
"""

from collections import deque
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
import threading
from typing import Any, Protocol, runtime_checkable

from column import crawl_one_column
from config import DEFAULT_WORKERS, OUTPUT_DIR, SITE_TYPES
from fetch import close_all_sessions
from whitelist import load_whitelist, save_whitelist
from writer import OutputMeta, merge_and_write_json, write_full_json

COLUMN_TIMEOUT = 1800  # 每栏目最大 30 分钟


@runtime_checkable
class ProgressProto(Protocol):
    """进度显示器协议。"""

    def set_total(self, page_count: int, dept_count: int) -> None: ...  # noqa: D102
    def register(self, dept: str, page_est: int) -> None: ...  # noqa: D102
    def step_dept(self, dept: str, n_pages: int = 1) -> None: ...  # noqa: D102
    def finish_dept(self, dept: str) -> None: ...  # noqa: D102
    def close(self) -> None: ...  # noqa: D102


# =========================================================================
# 写入调度
# =========================================================================


def _save_json(
    output_path: str,
    *,
    mode: str,
    meta: OutputMeta,
    new_articles: list[dict[str, Any]],
) -> tuple[bool, int, int]:
    """根据 mode 选择写入策略。"""
    if mode == "incremental":
        return merge_and_write_json(output_path, meta=meta, new_articles=new_articles)
    return write_full_json(output_path, meta=meta, articles=new_articles)


# =========================================================================
# 部门结果保存
# =========================================================================


def _save_dept_result(  # noqa: PLR0913
    domain: str,
    dept: str,
    type_name: str,
    crawl_ts: str,
    mode: str,
    domain_articles: dict[str, list[dict[str, Any]]],
    domain_page_counts: dict[str, dict[str, int]],
    progress: ProgressProto | None,
    result_set: set[str],
) -> tuple[int, int]:
    """保存部门结果到 JSON + 用实际页数更新白名单。返回 (total_articles, new_count)。"""
    arts = domain_articles.get(domain, [])
    jp = str(Path(OUTPUT_DIR) / f"{dept}.json")
    meta = OutputMeta(domain=domain, department=dept, site_type=type_name, crawl_time=crawl_ts)
    _written, total, new_cnt = _save_json(jp, mode=mode, meta=meta, new_articles=arts)
    # ---- 更新白名单页数记录 ----
    wlt = load_whitelist(type_name)
    ex = wlt.get(domain, {})
    ex["department"] = dept
    ex["type"] = type_name
    old_pages = ex.get("pages", {})
    actual_pages = domain_page_counts.get(domain, {})
    for path, count in actual_pages.items():
        old_entry = old_pages.get(path, {})
        if isinstance(old_entry, dict):
            old_entry["pages"] = count
        else:
            old_pages[path] = {"pages": count, "column": ""}
    ex["pages"] = old_pages
    wlt[domain] = ex
    save_whitelist(wlt, type_name)
    if progress:
        progress.finish_dept(dept)
    result_set.add(domain)
    return total, new_cnt


# =========================================================================
# 主入口
# =========================================================================


def crawl_all_whitelist(  # noqa: C901, PLR0912, PLR0915
    *,
    workers: int | None = None,
    progress: ProgressProto | None = None,
    verbose: bool = True,
    mode: str = "incremental",
    max_pages: int = 0,
) -> list[dict[str, Any]]:
    """主入口。

    Args:
        workers: 统一并发数（栏目级 + 页码级）。
        progress: None 时使用纯文本日志。
        verbose: 是否打印详细日志。
        mode: "incremental" 合并已有数据，"full" 全量覆盖。
        max_pages: 每栏目最大爬取页数，0 不限制。
    """
    if workers is None:
        workers = DEFAULT_WORKERS

    wl = load_whitelist()
    if not wl:
        return []

    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    crawl_ts = datetime.now(tz=UTC).strftime("%Y%m%d_%H%M%S")

    # ---- 构建栏目任务 ----
    domain_meta: dict[str, dict[str, str]] = {}
    column_tasks: list[tuple[str, str, str, str, dict[str, Any]]] = []
    domain_page_est: dict[str, int] = {}
    total_pages_est = 0

    for domain, info in wl.items():
        dept = info.get("department", "")
        type_name = info.get("type", "")
        pages_dict = info.get("pages", {})
        if not dept or not pages_dict or type_name not in SITE_TYPES:
            continue
        cfg = SITE_TYPES[type_name]
        domain_meta[domain] = {"dept": dept, "type_name": type_name}
        domain_page_est.setdefault(domain, 0)
        for path in sorted(pages_dict):
            entry = pages_dict[path]
            col_name = (
                (entry.get("column") or entry.get("name", "")) if isinstance(entry, dict) else ""
            )
            col_est = entry.get("pages", 1) if isinstance(entry, dict) else entry
            column_tasks.append((domain, dept, path, col_name, cfg))
            domain_page_est[domain] += col_est
            total_pages_est += col_est

    if not column_tasks:
        return []

    len(column_tasks)

    # ---- 进度条 ----
    if progress:
        progress.set_total(total_pages_est, len(domain_meta))
        for domain in sorted(domain_meta):
            progress.register(domain_meta[domain]["dept"], domain_page_est.get(domain, 1))

    # ---- 计数器（所有模式均追踪） ----
    col_done = 0
    col_fail = 0
    counter_lock = threading.Lock()

    # ---- 线程安全辅助 ----
    domain_articles: dict[str, list[dict[str, Any]]] = {}
    domain_page_counts: dict[str, dict[str, int]] = {}  # domain → {path: actual_pages}
    art_lock = threading.Lock()
    pc_lock = threading.Lock()
    saved_domains: set[str] = set()
    all_results: list[dict[str, Any]] = []

    # 每域名剩余栏目数
    domain_cols_remaining: dict[str, int] = {
        domain: sum(1 for d, *_ in column_tasks if d == domain) for domain in domain_meta
    }
    cols_remaining_lock = threading.Lock()

    # ---- 提交栏目任务 ----
    executor = ThreadPoolExecutor(max_workers=workers)
    try:
        dept_queues: dict[str, deque[tuple[str, str, str, str, dict[str, Any]]]] = {
            d: deque() for d in domain_cols_remaining
        }
        for domain, dept, path, col_name, cfg in column_tasks:
            dept_queues[domain].append((domain, dept, path, col_name, cfg))

        dept_active: dict[str, int] = dict.fromkeys(dept_queues, 0)
        active_total = 0
        dispatch_lock = threading.Lock()
        fm: dict[Future[tuple[int, list[dict[str, Any]], str]], tuple[str, str, str, str]] = {}
        all_done = threading.Event()

        def _pick_dept() -> str | None:
            """选择下一个调度部门：活跃数最少优先，剩余任务多者优先。"""
            best, best_score = None, (float("inf"), -1)
            for d, q in dept_queues.items():
                if q:
                    sc = (dept_active[d], -len(q))
                    if sc < best_score:
                        best_score, best = sc, d
            return best

        def _fill() -> None:
            """提交任务直到满额或无待办。"""
            nonlocal active_total
            while active_total < workers:
                d = _pick_dept()
                if d is None:
                    return
                domain, dept, path, col_name, cfg = dept_queues[d].popleft()
                dept_active[d] += 1
                active_total += 1
                fut = executor.submit(
                    crawl_one_column,
                    domain,
                    dept,
                    path,
                    col_name,
                    cfg,
                    progress,
                    workers,
                    verbose,
                    max_pages,
                )
                fm[fut] = (domain, dept, col_name, path)
                fut.add_done_callback(_on_done)

        def _on_done(fut: Future[tuple[int, list[dict[str, Any]], str]]) -> None:  # noqa: C901
            """任务完成回调。"""
            nonlocal active_total, col_done, col_fail
            domain_val, dept_val, _col_name, path = fm.pop(fut, (None, None, None, None))

            # --- 处理结果 ---
            try:
                page_count, arts, warning = fut.result(timeout=COLUMN_TIMEOUT)
                if domain_val:
                    with art_lock:
                        domain_articles.setdefault(domain_val, []).extend(arts)
                    # 记录每个栏目实际爬取的页数
                    if page_count and path:
                        with pc_lock:
                            domain_page_counts.setdefault(domain_val, {})[path] = page_count
                if warning and progress:
                    pass
                if not progress:
                    with counter_lock:
                        col_done += 1
                    if not arts and page_count > 0:
                        pass
                else:
                    with counter_lock:
                        col_done += 1
            except (RuntimeError, OSError, TimeoutError):
                with counter_lock:
                    col_fail += 1

            # --- 释放槽位 + 检查部门完成 ---
            with dispatch_lock:
                if domain_val:
                    dept_active[domain_val] -= 1
                active_total -= 1
                if domain_val:
                    with cols_remaining_lock:
                        domain_cols_remaining[domain_val] -= 1
                        if domain_cols_remaining[domain_val] == 0:
                            total, new_cnt = _save_dept_result(
                                domain_val,
                                dept_val or "",
                                domain_meta[domain_val]["type_name"],
                                crawl_ts,
                                mode,
                                domain_articles,
                                domain_page_counts,
                                progress,
                                saved_domains,
                            )
                            all_results.append(
                                {
                                    "domain": domain_val,
                                    "department": dept_val or "",
                                    "total_articles": total,
                                    "new_articles": new_cnt,
                                }
                            )
                _fill()
                if not fm:
                    all_done.set()

        # ---- 初始填充 + 等待完成 ----
        with dispatch_lock:
            _fill()
        all_done.wait()

        # ---- 收尾：保存未保存的部门 ----
        with dispatch_lock:
            for domain in domain_meta:
                if domain not in saved_domains:
                    dept = domain_meta[domain]["dept"]
                    tn = domain_meta[domain]["type_name"]
                    total, new_cnt = _save_dept_result(
                        domain,
                        dept,
                        tn,
                        crawl_ts,
                        mode,
                        domain_articles,
                        domain_page_counts,
                        progress,
                        saved_domains,
                    )
                    all_results.append(
                        {
                            "domain": domain,
                            "department": dept,
                            "total_articles": total,
                            "new_articles": new_cnt,
                        }
                    )

    finally:
        executor.shutdown(wait=False, cancel_futures=True)
        if progress:
            progress.close()
        close_all_sessions()

    return all_results
