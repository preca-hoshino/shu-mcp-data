"""
shu-mcp 白名单管理
———— 加载 / 保存 / 添加 / 查看 + domian.txt 解析
"""

import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from config import DOMIAN_FILE, WHITELIST_DIR

# ————————————————————————————————————————————————————————————
# 路径工具
# ————————————————————————————————————————————————————————————

_WL_DIR = Path(WHITELIST_DIR)


def _whitelist_path(type_name: str) -> Path:
    """根据类型名返回对应的白名单文件路径，如 '01' → whitelists/01.json"""
    return _WL_DIR / f"{type_name}.json"


# ————————————————————————————————————————————————————————————
# 白名单加载 / 保存
# ————————————————————————————————————————————————————————————


def load_whitelist(type_name: str | None = None) -> dict[str, Any]:
    """加载白名单。

    参数:
        type_name: '01'~'27' 加载单个类型文件；None 则合并全部文件。
    """
    if type_name is not None:
        path = _whitelist_path(type_name)
        if path.exists():
            with path.open(encoding="utf-8") as f:
                data: dict[str, Any] = json.load(f)
                return data
        return {}

    # 合并全部类型
    merged: dict[str, Any] = {}
    if _WL_DIR.is_dir():
        for child in sorted(_WL_DIR.iterdir()):
            if not child.name.endswith(".json"):
                continue
            with child.open(encoding="utf-8") as f:
                merged.update(json.load(f))
    return merged


def save_whitelist(wl: dict[str, Any], type_name: str) -> None:
    """按类型保存白名单文件（whitelists/{type_name}.json）"""
    _WL_DIR.mkdir(parents=True, exist_ok=True)
    path = _whitelist_path(type_name)
    with path.open("w", encoding="utf-8") as f:
        json.dump(wl, f, ensure_ascii=False, indent=2)


# ————————————————————————————————————————————————————————————
# 域名 / 路径提取
# ————————————————————————————————————————————————————————————


def domain_key(url: str) -> str:
    """提取域名作为白名单键"""
    return urlparse(url).netloc


def path_from_url(url: str) -> str:
    """提取路径部分（去掉开头 /），如 xwdt.htm 或 sylm/tzgg.htm"""
    p = urlparse(url).path.lstrip("/")
    return p or "index.htm"


# ————————————————————————————————————————————————————————————
# 添加至白名单
# ————————————————————————————————————————————————————————————


def add_to_whitelist(url: str, type_name: str, result: dict[str, Any], column: str = "") -> None:
    """将成功爬取的站点按域名加入对应类型的白名单文件"""
    wl = load_whitelist(type_name)
    domain = domain_key(url)
    path = path_from_url(url)
    existing = wl.get(domain, {})
    pages = existing.get("pages", {})
    old_entry = pages.get(path, {})
    if isinstance(old_entry, dict):
        old_pages = old_entry.get("pages", 1)
        old_column = old_entry.get("column", column)
    else:
        old_pages = old_entry
        old_column = column
    pages[path] = {
        "pages": result.get("total_pages", old_pages),
        "column": old_column or column,
    }
    wl[domain] = {
        "type": type_name,
        "department": existing.get("department", ""),
        "pages": pages,
    }
    save_whitelist(wl, type_name)


# ————————————————————————————————————————————————————————————
# domian.txt 解析
# ————————————————————————————————————————————————————————————


def parse_domian_txt() -> list[tuple[str, str, str]]:
    """解析 domian.txt → [(url, department, category), ...]"""
    entries: list[tuple[str, str, str]] = []
    current_dept = ""
    domian_path = Path(DOMIAN_FILE)
    with domian_path.open(encoding="utf-8") as f:
        for raw_line in f:
            stripped = raw_line.strip()
            if not stripped:
                continue
            if stripped.startswith("http"):
                parts = stripped.split(None, 1)
                url = parts[0]
                category = parts[1] if len(parts) > 1 else ""
                entries.append((url, current_dept, category))
            else:
                current_dept = stripped
    return entries


# ————————————————————————————————————————————————————————————
# 白名单查看
# ————————————————————————————————————————————————————————————


def show_whitelist() -> None:
    """打印白名单概览（域名型，含栏目名称）"""
    wl = load_whitelist()
    if not wl:
        return
    for info in wl.values():
        info.get("department", "")
        pages = info.get("pages", {})
        for _path, entry in sorted(pages.items()):
            if isinstance(entry, dict):
                entry.get("pages", "?")
                entry.get("column", "")
            else:
                pass
