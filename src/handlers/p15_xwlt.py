"""
处理器 15 — xw-lt 型（计算机学院等站点）
———— 列表 div.xw-lt 或 div.tzgg > ul > li，标题 h3，日期 span，翻页 span.p_pages
CMS 特征: VSB 系统 + div.xw-lt/div.tzgg 容器 + h3 标题 + span 日期 + span.p_pages 翻页
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 15"""
    SITE_TYPES["15"] = {
        "name": "xw-lt型",
        "list_selector": "div.xw-lt, div.tzgg",  # 新闻用 xw-lt，通知/学术用 tzgg
        "row_selector": "li",
        "title_selector": "h3",  # <h3>标题文本</h3>
        "date_selector": "",  # 留空，用默认 span 查找（第一个 span 即日期）
        "date_tag": "span",  # <span>2026-05</span> 年-月
        "pagination_selector": "span.p_pages",  # 翻页容器
        "next_page_texts": ["下页"],  # 下页链接文本
    }


_register()
