"""
处理器 04 — table.ArtList 型（亚洲人口研究中心等站点）
———— 文章行 table.ArtList，标题 a.linkfont1，日期 span.linkfont1，翻页 a.Next
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 04"""
    SITE_TYPES["04"] = {
        "name": "博达CMS-table.ArtList型",
        "list_selector": "",  # 全页搜索
        "row_selector": "table.ArtList",  # 每行是 table.ArtList
        "pagination_selector": "",  # 不指定容器
        "next_page_selector": "a.Next",  # 直接定位下一页链接（CSS class）
        "next_page_texts": ["下页", "下一页", ">"],  # fallback
        "title_selector": "a.linkfont1",  # 标题在 a.linkfont1
        "date_selector": "span.linkfont1",  # 日期在 span.linkfont1
    }


_register()
