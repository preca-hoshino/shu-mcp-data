"""
处理器 26 — HRCMS 表格型（人事处等 HRCMS 站点）
———— 列表 tr[id^="line_u"]，标题 td:first-child>a，日期 span.artdata，翻页 td[id^="fanye"] + a.Next
CMS 特征: HRCMS 系统 + tr[id^="line_u"] 行 + td 表格布局 + a.Next 翻页 + td[id^="fanye"] 总条数/总页数 + 倒序翻页
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 26"""
    SITE_TYPES["26"] = {
        "name": "HRCMS列表型",
        "list_selector": "",  # 全页搜索
        "row_selector": 'tr[id^="line_u"]',  # HRCMS 文章行: <tr id="line_u6_0">
        "title_selector": "",  # 直接取第一个 td > a 标签文本
        "date_selector": "span.artdata",  # <span class="linkfont1 artdata">2026-04-09</span>
        "pagination_selector": "",  # 空→全页搜索（翻页文本格式 "共N条  页码/总页" 全页可识别）
        "next_page_selector": "a.Next",  # 下页链接: a.Next[href]
        "next_page_texts": ["下页"],  # 文本回退
    }


_register()
