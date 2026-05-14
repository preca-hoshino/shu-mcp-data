"""
处理器 06 — div.right-list 型（自动化系等站点）
———— 列表容器 div.right-list，文章 li>a + li>span，翻页 "下页" 链接
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 06"""
    SITE_TYPES["06"] = {
        "name": "div.right-list型",
        "list_selector": "div.right-list",
        "pagination_selector": "div.right-list",
        "next_page_texts": ["下页"],
        "date_selector": "span",
    }


_register()
