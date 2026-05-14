"""
处理器 24 — VSB 表格型（研究生院等 VSB 站点）
———— 列表 tr[id^="line_u"]，标题 td>a，日期 td:nth-of-type(2)，翻页 div.pb_sys_common + span.p_next>a
CMS 特征: VSB 系统 + tr[id^="line_u"] 行 + td 表格布局 + span.p_pages 翻页 + 共N条总条数
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 24"""
    SITE_TYPES["24"] = {
        "name": "VSB表格型",
        "list_selector": "",  # 全页搜索
        "row_selector": 'tr[id^="line_u"]',  # VSB 文章行: <tr id="line_u17_0">
        "title_selector": "",  # 直接取第一个 td > a 标签文本
        "date_selector": "td:nth-of-type(2)",  # 第二个 td: <td width="130">2026/04/14 15:29:31</td>
        "pagination_selector": ".pb_sys_common",  # VSB 分页容器 div.pb_sys_common
        "next_page_selector": "span.p_next a",  # 活跃下页链接: span.p_next > a[href]
        "next_page_texts": ["下页"],  # 文本回退
    }


_register()
