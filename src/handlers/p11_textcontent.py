"""
处理器 11 — textContent 型（土木工程系等站点）
———— 列表 div.textContent > ul > li，标题 a.myTitle，日期 span.eleLeft，翻页表格内"下页"
CMS 特征: div.textContent 容器 + span.eleLeft 日期 + a.myTitle 标题
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 11"""
    SITE_TYPES["11"] = {
        "name": "textContent型",
        "list_selector": "div.textContent",
        "row_selector": "li",
        "title_selector": "a.myTitle",
        "date_selector": "span.eleLeft",
        "pagination_selector": "",
        "next_page_texts": ["下页", "下一页"],
    }


_register()
