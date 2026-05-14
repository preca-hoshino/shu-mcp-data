"""
处理器 05 — VSb-only-list1 型（机电工程与自动化学院等站点）
———— 列表容器 div.only-list1，文章 li>a + li>span，翻页 div.fanye
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 05"""
    SITE_TYPES["05"] = {
        "name": "VSb-only-list1型",
        "list_selector": "div.only-list1",
        "pagination_selector": "div.fanye",
        "next_page_selector": "a.Next",  # 优先用 CSS class 定位（auto/law/schim 等）
        "next_page_texts": [
            "下页",
            "下一页",
            ">",
            "›",
            "»",
        ],  # fallback: 文字匹配（bio/baoweichu 等）
    }


_register()
