"""
处理器 28 — VSB 列表 li+裸span 日期型（智能制造实验室、图书情报档案系等 VSB 站点）
———— 列表 li[id^="line_u"]，标题 a，日期 span（无class），翻页 a.Next
CMS 特征: VSB 系统 + list.vsb.css/new-list.vsb.css + li[id^="line_u"] 列表项
         + li>a 标题 + li>span(无class) YYYY-MM-DD 日期 + table.headStyle* 翻页
         + "共N条 X/Y" 总页数 + a.Next/a.Prev 翻页链接
区分于:
  - 类型10: 日期在 <i> 标签中
  - 类型27: 日期在 span.news-data（有class）中
  - 类型25: 翻页用 span.p_next a
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 28"""
    SITE_TYPES["28"] = {
        "name": "VSB列表li+裸span日期型",
        "list_selector": "",  # 全页搜索
        "row_selector": 'li[id^="line_u"]',  # VSB 文章行: <li id="line_u2_0">
        "title_selector": "",  # 直接取 li > a 标签文本
        "date_selector": "span",  # <span>2026-05-09</span>（无class）
        "date_tag": "span",  # fallback
        "pagination_selector": "",  # 空→全页搜索（VSB table.headStyle*）
        "next_page_selector": "a.Next",  # 下页链接: a.Next[href]
        "next_page_texts": ["下页", "下一页"],  # 文本回退
    }


_register()
