"""
处理器 16 — shu-main 型（上海大学主站等站点）
———— 列表 div.list > ul > li，标题 p.bt，日期 p.sj，翻页 span.p_pages
CMS 特征: VSB 系统 + div.list 容器 + p.bt 标题 + p.sj 日期 + span.p_pages 翻页
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 16"""
    SITE_TYPES["16"] = {
        "name": "shu-main型",
        "list_selector": "div.list ul",  # div.list 内的 ul（跳过空 div.list）
        "row_selector": "li",
        "title_selector": "p.bt",  # <p class="bt">标题</p>
        "date_selector": "p.sj",  # <p class="sj">2026.05.07</p>
        "pagination_selector": "span.p_pages",  # 翻页容器
        "next_page_texts": ["下页"],  # 下页链接文本
    }


_register()
