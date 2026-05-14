"""
处理器 25 — VSB 列表 li 型（后勤保障部等 VSB 站点）
———— 列表 li[id^="line_u"]，标题 a，日期 span，翻页 div.pb_sys_common + span.p_next>a
CMS 特征: VSB 系统 + li[id^="line_u"] 列表项 + a 标题 + span 日期 + span.p_pages 翻页 + 共N条总条数
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 25"""
    SITE_TYPES["25"] = {
        "name": "VSB列表li型",
        "list_selector": "",  # 全页搜索
        "row_selector": 'li[id^="line_u"]',  # VSB 文章行: <li id="line_u5_0">
        "title_selector": "",  # 直接取 li > a 标签文本
        "date_selector": "span",  # li > span: <span>2026-05-08</span>
        "pagination_selector": ".pb_sys_common",  # VSB 分页容器 div.pb_sys_common
        "next_page_selector": "span.p_next a",  # 活跃下页链接: span.p_next > a[href]
        "next_page_texts": ["下页"],  # 文本回退
    }


_register()
