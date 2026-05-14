"""
shu-mcp 写入模块
———— 增量合并 + 全量覆盖，保证 git diff 只反映真实变更
"""

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class OutputMeta:
    """输出文件的公共元数据。"""

    domain: str
    department: str
    site_type: str
    crawl_time: str


def _article_key(a: dict[str, Any]) -> str:
    """文章唯一标识：URL 是唯一键"""
    return str(a.get("url", ""))


def _sort_articles(articles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """确定性排序：日期降序 → URL 升序（同日期内稳定排序）"""
    return sorted(articles, key=lambda a: (_neg_date_key(a), a.get("url", "")))


def _neg_date_key(a: dict[str, Any]) -> str:
    """将日期转为取反字符串，实现降序排列，空日期排最后"""
    d = str(a.get("date", ""))
    try:
        parts = d.split("-")
        y, m, day = int(parts[0]), int(parts[1]), int(parts[2])
        # 取反：用 9999-y 实现降序
        return f"{9999 - y:04d}-{12 - m:02d}-{31 - day:02d}"
    except (ValueError, IndexError):
        return "9999-99-99"


def _articles_signature(articles: list[dict[str, Any]]) -> set[str]:
    """文章集合签名：用于快速判断内容是否变化"""
    return {
        f"{a.get('url', '')}|{a.get('title', '')}|{a.get('date', '')}|{a.get('column', '')}"
        for a in articles
    }


def _build_record(meta: OutputMeta, articles: list[dict[str, Any]]) -> dict[str, Any]:
    """组装输出 JSON 记录。"""
    col_counts: dict[str, int] = {}
    for a in articles:
        cn = str(a.get("column", ""))
        col_counts[cn] = col_counts.get(cn, 0) + 1
    # 按字典序排列栏目，确保输出确定性
    sorted_col_counts = dict(sorted(col_counts.items()))
    return {
        "domain": meta.domain,
        "department": meta.department,
        "type": meta.site_type,
        "crawl_time": meta.crawl_time,
        "total_articles": len(articles),
        "columns": sorted_col_counts,
        "articles": articles,
    }


def _read_existing(path: Path) -> list[dict[str, Any]]:
    """读取已有 JSON 文件中的文章列表，读取失败返回空列表。"""
    try:
        with path.open(encoding="utf-8") as f:
            data: dict[str, Any] = json.load(f)
            return list(data.get("articles", []))
    except (json.JSONDecodeError, OSError):
        return []


def _write_json(path: Path, record: dict[str, Any]) -> None:
    """写入 JSON 文件。"""
    with path.open("w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)


def merge_and_write_json(
    output_path: str,
    *,
    meta: OutputMeta,
    new_articles: list[dict[str, Any]],
) -> tuple[bool, int, int]:
    """增量合并写入 JSON 文件。

    流程：
    1. 读取已有 JSON（如存在）
    2. 以 URL 为键合并：新文章覆盖旧文章，新增文章追加
    3. 确定性排序（日期降序 → URL 升序）
    4. 对比签名：仅在内容实际变化时写入文件
    5. 若文件不存在则直接写入

    Returns:
        (written, total_articles, new_count)
        written: 是否实际写入了文件
        total_articles: 合并后文章总数
        new_count: 本次新增的文章数
    """
    path = Path(output_path)

    # ---- 构建本次爬取的文章索引 ----
    new_index: dict[str, dict[str, Any]] = {}
    for a in new_articles:
        key = _article_key(a)
        if key:
            new_index[key] = a

    # ---- 读取已有文件 ----
    existing_articles = _read_existing(path) if path.exists() else []

    # ---- 合并：新覆盖旧，保留旧中不重复的 ----
    merged_index: dict[str, dict[str, Any]] = {}
    for a in existing_articles:
        key = _article_key(a)
        if key:
            merged_index[key] = a
    merged_index.update(new_index)  # 新文章覆盖旧文章

    merged_articles = _sort_articles(list(merged_index.values()))

    # ---- 新增计数：存在于 new_index 但不存在于 existing ----
    existing_keys = {_article_key(a) for a in existing_articles}
    new_count = sum(1 for k in new_index if k not in existing_keys)

    record = _build_record(meta, merged_articles)

    # ---- 对比签名，决定是否写入 ----
    if existing_articles:
        old_sig = _articles_signature(existing_articles)
        if old_sig == _articles_signature(merged_articles):
            return False, len(merged_articles), 0

    _write_json(path, record)
    return True, len(merged_articles), new_count


def write_full_json(
    output_path: str,
    *,
    meta: OutputMeta,
    articles: list[dict[str, Any]],
) -> tuple[bool, int, int]:
    """全量覆盖写入 JSON 文件。

    确定性排序后直接覆盖，不与已有数据合并。

    Returns:
        (written, total_articles, new_count)
        written: 是否实际写入了文件
        total_articles: 文章总数
        new_count: 本次写入的文章数（全量模式等于 total）
    """
    path = Path(output_path)
    sorted_articles = _sort_articles(articles)
    record = _build_record(meta, sorted_articles)

    # ---- 对比已有文件，跳过无变化写入 ----
    if path.exists():
        existing = _read_existing(path)
        if existing and _articles_signature(existing) == _articles_signature(sorted_articles):
            return False, len(sorted_articles), 0

    _write_json(path, record)
    return True, len(sorted_articles), len(sorted_articles)
