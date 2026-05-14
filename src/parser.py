"""
shu-mcp 解析层
———— HTML 解析：文章提取、翻页检测、总页数估算、页码 URL 推断
"""

import re
from typing import Any
from urllib.parse import urljoin, urlparse, urlunparse

from bs4 import BeautifulSoup

_SECOND_PAGE = 2  # 翻页推断：检测「下一页」URL 是否指向第 2 页

# ————————————————————————————————————————————————————————————
# 日期标准化
# ————————————————————————————————————————————————————————————


def normalize_date(raw: str) -> str:  # noqa: PLR0911
    """将各种日期格式统一为 YYYY-MM-DD。

    支持格式:
        - 2026-04-16 / 2026/04/24 / 2019.11.13 / 20260416
        - 2023年10月16日 / 2023年04月
        - 2026-05（年-月，补 -01）
        - 20260508（纯8位数字）
    空字符串或无法解析时原样返回。
    """
    if not raw:
        return raw
    s = raw.strip()

    # 剥离时间部分: "2026/04/14 15:29:31" → "2026/04/14"
    s = re.split(r"\s+", s)[0]

    # 中文日期: 2023年10月16日 / 2023年04月
    m = re.match(r"(\d{4})年(\d{1,2})月(?:(\d{1,2})日?)?$", s)
    if m:
        y, mo = int(m.group(1)), int(m.group(2))
        d = int(m.group(3)) if m.group(3) else 1
        return f"{y:04d}-{mo:02d}-{d:02d}"

    # 纯8位数字  # noqa: ERA001
    m = re.match(r"^(\d{4})(\d{2})(\d{2})$", s)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"

    # 年-月-日: 2026-04-16 / 2026/04/24 / 2019.11.13 / 2026.05.07
    m = re.match(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})$", s)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return f"{y:04d}-{mo:02d}-{d:02d}"

    # 年 月-日（空格分隔）: 2025 09-29 / 2025 09/29
    m = re.match(r"(\d{4})\s+(\d{1,2})[-/.](\d{1,2})$", s)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return f"{y:04d}-{mo:02d}-{d:02d}"

    # DD20YY-MM 格式 (MBA页面 date-box 内联文本: "062026-05" = 日+年-月)
    # 限于 20xx 年份，避免将 2025-11 错解析为 DD=20 YYYY=2511
    m = re.match(r"(0[1-9]|[12]\d|3[01])(20\d{2})-(\d{1,2})$", s)
    if m:
        d, y, mo = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return f"{y:04d}-{mo:02d}-{d:02d}"

    # 年月-日（无分隔拼接）: 202509-29 / 202511-04（get_text(strip=True) 产出）
    m = re.match(r"(\d{4})(\d{2})[-/.](\d{2})$", s)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return f"{y:04d}-{mo:02d}-{d:02d}"

    # 年-月: 2026-05 / 2026/05 / 2026.05
    m = re.match(r"(\d{4})[-/.](\d{1,2})$", s)
    if m:
        y, mo = int(m.group(1)), int(m.group(2))
        return f"{y:04d}-{mo:02d}-01"

    # 无法解析，原样返回
    return s


# ————————————————————————————————————————————————————————————
# 文章提取
# ————————————————————————————————————————————————————————————

_BUTTON_TEXTS = {"了解更多", "详细", "查看详情", "more", "read more"}


def extract_articles(html: str, base_url: str, cfg: dict[str, Any]) -> list[dict[str, Any]]:  # noqa: C901, PLR0912, PLR0915
    """按站点配置从 HTML 提取文章列表

    配置项:
        list_selector: 列表容器 CSS 选择器（为空则全页搜索）
        row_selector:  每行元素 CSS 选择器（默认 "li"）
        title_selector: 标题元素 CSS 选择器（在行内），默认取 a 标签文本
        date_selector:  日期元素 CSS 选择器（在行内），默认 date_tag 指定的标签名
        date_tag:       日期标签名（fallback，默认 "span"）
        date_regex:     日期正则（fallback，用于从行文本提取特殊格式日期，如中文日期）
    """
    soup = BeautifulSoup(html, "html.parser")
    container = soup.select_one(cfg["list_selector"]) if cfg.get("list_selector") else soup
    if not container:
        return []

    title_sel = cfg.get("title_selector", "")
    date_sel = cfg.get("date_selector", "")
    date_tag = cfg.get("date_tag", "span")
    date_regex = cfg.get("date_regex", "")
    row_sel = cfg.get("row_selector", "li")
    link_attr = cfg.get("link_attr", "href")  # "href" (default) or "onclick"

    articles: list[dict[str, Any]] = []
    for row in container.select(row_sel):
        # 提取链接: 支持 href 和 onclick (window.open) 两种模式
        href = None
        if link_attr == "onclick":
            onclick_val = str(row.get("onclick", ""))
            if onclick_val:
                m = re.search(r"""window\.open\(['"]([^'"]+)['"]""", onclick_val)
                if m:
                    href = m.group(1)
        elif row.name == "a":
            href = row.get("href", "")
        else:
            a = row.find("a")
            if a:
                href = a.get("href", "")

        if not href:
            continue

        href = urljoin(base_url, href)

        # 日期：优先 date_selector（CSS），否则 date_tag（标签名）
        d_el = row.select_one(date_sel) if date_sel else row.find(date_tag)
        date_str = d_el.get_text(strip=True) if d_el else ""

        # 标题
        a_tag = row if row.name == "a" else row.find("a")
        if title_sel:
            t_el = row.select_one(title_sel)
            title = (
                t_el.get_text(strip=True) if t_el else (a_tag.get_text(strip=True) if a_tag else "")
            )
            if not title:  # 回退：标题选择器匹配到但文本为空
                row_text = row.get_text(strip=True)
                if d_el and date_str:
                    row_text = row_text.replace(date_str, "").strip()
                title = row_text or title
        else:
            title = a_tag.get_text(strip=True) if a_tag else ""
            if not title or title.lower().strip() in _BUTTON_TEXTS:
                title = row.get_text(strip=True)
            if d_el and date_str and a_tag and d_el in a_tag.descendants:
                title = title.replace(date_str, "").strip()
        # 标题为按钮占位文本时，回退到 <a> 的 title 属性
        if title.lower().strip() in _BUTTON_TEXTS and a_tag:
            attr_title = str(a_tag.get("title", "")).strip()
            if attr_title:
                title = attr_title

        if not date_str:
            full_text = row.get_text(" ", strip=True)
            if date_regex:
                m = re.search(date_regex, full_text)
            else:
                m = re.search(r"(\d{4}[-/.]\d{1,2}[-/.]\d{1,2})", full_text)
            date_str = m.group(1) if m else ""

        # 统一日期格式为 YYYY-MM-DD
        date_str = normalize_date(date_str)

        articles.append({"title": title, "url": href, "date": date_str})

    return articles


# ————————————————————————————————————————————————————————————
# 翻页
# ————————————————————————————————————————————————————————————


def find_next_page_url(html: str, base_url: str, cfg: dict[str, Any]) -> str | None:
    """从翻页容器中定位"下一页"链接

    配置项:
        pagination_selector: 翻页容器 CSS
        next_page_selector:  下一页链接 CSS（直接取 href），优先级最高
        next_page_texts:     下一页链接文本列表（fallback）
    """
    soup = BeautifulSoup(html, "html.parser")

    # 0) 优先：直接用 CSS 选择器定位"下一页"链接
    nps = cfg.get("next_page_selector", "")
    if nps:
        a = soup.select_one(nps)
        if a and a.get("href"):
            return urljoin(base_url, str(a["href"]))

    next_texts: list[str] = cfg.get("next_page_texts", [])

    # 1) 翻页容器选择器（跳过空字符串）
    pager_sel = cfg.get("pagination_selector", "")
    pager = soup.select_one(pager_sel) if pager_sel else None
    # 2) 回退：在列表容器父级中找
    if not pager:
        container = soup.select_one(cfg["list_selector"] or "body")
        if container and container.parent:
            pager = container.parent
    # 3) 最后回退：整页搜索
    if not pager:
        pager = soup

    for a in pager.find_all("a"):
        if a.get_text(strip=True) in next_texts:
            href: str = str(a.get("href", ""))
            if href:
                return urljoin(base_url, href)
    return None


# ————————————————————————————————————————————————————————————
# 总页数
# ————————————————————————————————————————————————————————————


def get_total_pages_from_html(html: str, cfg: dict[str, Any]) -> int:  # noqa: C901
    """从首页 HTML 中提取总页数。

    支持多种格式（按优先级）：
        - '1/7'    当前页/总页数
        - '共62条'  总条数，按每页10条估算
        - '共5页'   直接标注总页数
        - 数页码链接  如 span.p_pages 中 .p_no 页码项
        - JS 函数签名  _simple_list_gotopage_fun(N, ...)
    """
    soup = BeautifulSoup(html, "html.parser")

    pager_sel = cfg.get("pagination_selector", "")
    pager = soup.select_one(pager_sel) if pager_sel else soup
    if not pager:
        pager = soup

    text = pager.get_text(" ", strip=True)

    # "1/7"
    m = re.search(r"(\d+)\s*/\s*(\d+)", text)
    if m:
        return int(m.group(2))

    # "共 62 条"
    m = re.search(r"共\s*(\d+)\s*条", text)
    if m:
        return max(1, (int(m.group(1)) + 9) // 10)

    # "共 5 页"
    m = re.search(r"共\s*(\d+)\s*页", text)
    if m:
        return int(m.group(1))

    # 数页码链接（Type 01: span.p_pages 中只有 1 2 3 等数字页码链接）
    page_nums: set[int] = set()
    for a in pager.find_all("a"):
        t = a.get_text(strip=True)
        if t.isdigit():
            page_nums.add(int(t))
    if page_nums:
        return max(page_nums)

    # JS 函数签名（Type 02: _simple_list_gotopage_fun(总页数, ...)）
    for script in soup.select("script"):
        if script.string:
            m = re.search(r"_simple_list_gotopage_fun\s*\(\s*(\d+)\s*,", script.string)
            if m:
                return int(m.group(1))

    return 1


# ————————————————————————————————————————————————————————————
# 页码 URL 推断（用于页面级并发爬取）
# ————————————————————————————————————————————————————————————


def build_page_urls(first_url: str, next_url: str | None, total_pages: int) -> list[str]:  # noqa: C901, PLR0915
    """根据首页 → 下一页的 URL 差异，推断第 2~N 页的 URL。

    支持的 URL 模式:
        - 路径插入: index.htm → index_2.htm → index_3.htm ...
        - 路径后缀: list_1.htm → list_2.htm → list_3.htm ...
        - 查询参数: ?page=1 → ?page=2 → ?page=3 ...
        - 查询参数: ?pagenumber=1 → ?pagenumber=2 ...
        - DNN逆序: base.htm → base/{T-1}.htm → base/{T-2}.htm → ... → base/1.htm

    如果无法推断模式，返回空列表。
    """
    if not next_url or total_pages <= 1:
        return []

    # 第一页的解析信息
    first_parsed = urlparse(first_url)
    root = f"{first_parsed.scheme}://{first_parsed.netloc}"
    first_path = first_parsed.path

    # 下一页：尝试两种解析方式
    #   A) 页面相对: urljoin(first_url, next_url)  — 适合 /dir/page.htm + next.htm 等
    #   B) 站点根相对: urljoin(root, '/' + next_url.lstrip('/')) — 适合 /dir/page.htm + dir/page2.htm
    next_page_rel = urljoin(first_url, next_url)
    next_root_rel = urljoin(root + "/", "/" + next_url.lstrip("/"))
    candidates = [next_page_rel]
    if next_root_rel != next_page_rel:
        candidates.append(next_root_rel)

    if all(c == first_url for c in candidates):
        return []

    # =====================================================================
    # 对每种候选 URL 依次尝试各模式
    # =====================================================================

    def _try_patterns(next_abs: str) -> list[str] | None:  # noqa: C901
        """尝试所有模式，成功返回 URL 列表，失败返回 None"""
        next_parsed = urlparse(next_abs)

        # —— 模式 A: 路径中 _2 后缀（博达 CMS） ——
        m = re.match(r"^(.+)_2(\.\w+)$", next_abs)
        if m:
            base, ext = m.groups()
            urls = [f"{base}_{pg}{ext}" for pg in range(3, total_pages + 1)]
            return [next_abs, *urls]

        # —— 模式 B: 路径中 _1 → _2 演变 ——
        m1 = re.match(r"^(.+)_(\d+)(\.\w+)$", first_path)
        m2 = re.match(r"^(.+)_(\d+)(\.\w+)$", next_parsed.path)
        if m1 and m2 and m1.group(1) == m2.group(1) and m1.group(3) == m2.group(3):
            base = m1.group(1)
            ext = m1.group(3)
            urls = []
            for pg in range(3, total_pages + 1):
                path = f"{base}_{pg}{ext}"
                urls.append(urlunparse(next_parsed._replace(path=path)))
            return [next_abs, *urls]

        # —— 模式 C: 查询参数 ?page=2 ——
        m = re.search(r"([?&])page=(\d+)", next_abs)
        if m and int(m.group(2)) == _SECOND_PAGE:
            prefix = m.group(1)
            urls = []
            for pg in range(2, total_pages + 1):
                urls.append(re.sub(r"([?&])page=\d+", f"{prefix}page={pg}", next_abs, count=1))
            return urls

        # —— 模式 D: 查询参数 ?pagenumber=2 ——
        m = re.search(r"([?&])pagenumber=(\d+)", next_abs)
        if m and int(m.group(2)) == _SECOND_PAGE:
            prefix = m.group(1)
            urls = []
            for pg in range(2, total_pages + 1):
                urls.append(
                    re.sub(r"([?&])pagenumber=\d+", f"{prefix}pagenumber={pg}", next_abs, count=1)
                )
            return urls

        # —— 模式 E: DNN/VSB 逆序翻页 ——
        # 第1页: base.htm, 第2页: base/{T-1}.htm, ..., 末页: base/1.htm
        m_first = re.match(r"^(.+)\.(\w+)$", first_path)
        m_next = re.match(r"^(.+)/(\d+)\.(\w+)$", next_parsed.path)
        if m_first and m_next:
            fb, fe = m_first.group(1), m_first.group(2)
            nb, nn, ne = m_next.group(1), int(m_next.group(2)), m_next.group(3)
            if fb == nb and fe == ne:
                urls = []
                # 确定起始递减值（通常 = total-1，但容错）
                start = min(nn, total_pages - 1)
                # 用 next_abs 的 scheme+netloc 构造绝对 URL
                base_prefix = f"{next_parsed.scheme}://{next_parsed.netloc}"
                for offset in range(1, min(start, total_pages - 1) + 1):
                    pg_num = start - offset
                    if pg_num < 1:
                        break
                    urls.append(f"{base_prefix}{nb}/{pg_num}.{ne}")
                return [next_abs, *urls]

        return None  # 所有模式都不匹配

    for cand in candidates:
        result = _try_patterns(cand)
        if result is not None:
            return result

    return []
