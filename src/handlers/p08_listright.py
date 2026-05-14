"""
处理器 08 — div.list-right 型（先进凝固技术中心等站点）
———— 列表容器 div.list-right > ul > li，文章 li>a + li>span，翻页 div.fanye "下页" 链接
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 08"""
    SITE_TYPES["08"] = {
        "name": "div.list-right型",
        "list_selector": "div.list-right",
        "row_selector": "li",
        "pagination_selector": "div.fanye",
        "next_page_texts": ["下页"],
        "date_selector": "span",
    }


_register()
