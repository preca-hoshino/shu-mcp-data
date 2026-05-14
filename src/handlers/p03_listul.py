"""
处理器 03 — listUL 型（未来技术学院等站点）
———— 列表容器 ul.listUL > ul.listUL，标题 .whitespace，日期 .day，翻页 ul.listUL > div.table
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 03"""
    SITE_TYPES["03"] = {
        "name": "博达CMS-listUL型",
        "list_selector": "ul.listUL ul.listUL",  # 内层 ul 含实际文章
        "pagination_selector": "ul.listUL",  # 外层 ul 含翻页 div.table
        "next_page_texts": ["下页", "下一页", ">", "›", "»"],
        "title_selector": ".whitespace",  # 标题在 .whitespace 中
        "date_selector": ".day",  # 日期在 .day 中
    }


_register()
