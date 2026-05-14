"""
处理器 07 — only-list 型（本科生院等站点）
———— 列表容器 div.only-list，文章 li>a + 纯文本中文日期，翻页 "下页" 链接
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 07"""
    SITE_TYPES["07"] = {
        "name": "only-list型",
        "list_selector": "div.only-list, div.only-list1",
        "pagination_selector": "div.fanye",
        "next_page_texts": ["下页"],
        "date_regex": r"(\d{4}年\d{1,2}月\d{1,2}日)",
    }


_register()
