"""
处理器 13 — listPage 型（国际教育学院等 VSB 站点）
———— 列表 ul.listPage > li，标题 a，日期 span，翻页 span.p_pages 内 p_next/p_no
CMS 特征: VSB 系统 + ul.listPage 容器 + span 日期 + span.p_pages 翻页
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 13"""
    SITE_TYPES["13"] = {
        "name": "listPage型",
        "list_selector": "ul.listPage",
        "row_selector": "li",
        "title_selector": "",  # 直接取 a 标签文本
        "date_selector": "span",  # <span>2026/04/24</span>
        "pagination_selector": "span.p_pages",  # 翻页容器
        "next_page_texts": ["下页"],  # 下页链接文本
    }


_register()
