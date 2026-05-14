"""
处理器 09 — div.listR-lb 型（继续教育学院、科技园区等站点）
———— 列表容器 div.listR-lb > ul > li，文章 li>a + li>i(日期)，翻页 "下页" 链接
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 09"""
    SITE_TYPES["09"] = {
        "name": "div.listR-lb型",
        "list_selector": "div.listR-lb",
        "row_selector": "li",
        "pagination_selector": "",
        "next_page_texts": ["下页"],
        "date_selector": "i",
    }


_register()
