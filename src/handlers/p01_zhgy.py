"""
处理器 01 — ul.rightList 型（综合管理等站点）
———— 列表容器 ul.rightList，翻页 span.p_pages
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 01"""
    SITE_TYPES["01"] = {
        "name": "博达CMS-ul.rightList型",
        "list_selector": "ul.rightList",
        "pagination_selector": "span.p_pages",
        "next_page_texts": ["下页", "下一页", ">", "›", "»"],
    }


_register()
