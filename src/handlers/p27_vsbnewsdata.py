"""
处理器 27 — VSB 列表 li+news-data 型（全球问题研究院等 VSB 站点）
———— 列表 li[id^="line_u"]，标题 a，日期 span.news-data，翻页 a.Next（倒序翻页）
CMS 特征: VSB 系统 + li[id^="line_u"] 列表项 + div>a 标题 + span.news-data 日期 + a.Next 翻页 + 共N条总条数 + 倒序翻页
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 27"""
    SITE_TYPES["27"] = {
        "name": "VSB列表li+news-data型",
        "list_selector": "",  # 全页搜索
        "row_selector": 'li[id^="line_u"]',  # VSB 文章行: <li id="line_u12_0">
        "title_selector": "",  # 直接取 li > div > a 标签文本
        "date_selector": "span.news-data",  # <span class="news-data">2026-01-28</span>
        "pagination_selector": "",  # 空→全页搜索（翻页文本格式 "共N条  页码/总页" 全页可识别）
        "next_page_selector": "a.Next",  # 下页链接: a.Next[href]
        "next_page_texts": ["下页"],  # 文本回退
    }


_register()
