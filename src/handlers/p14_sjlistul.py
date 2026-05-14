"""
处理器 14 — sj-list-ul 型（文学院等站点）
———— 列表 ul.sj-list-ul > li[id^="line_u"]，标题 a 文本，日期 a > p，翻页 a.Next
CMS 特征: VSB 系统 + ul.sj-list-ul 容器 + p 日期标签 + a.Next 翻页 + _simple_list_gotopage_fun 总页数
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 14"""
    SITE_TYPES["14"] = {
        "name": "sj-list-ul型",
        "list_selector": "ul.sj-list-ul",
        "row_selector": 'li[id^="line_u"]',
        "title_selector": "",  # 直接取 a 标签文本
        "date_selector": "p",  # <p>2026-04-23</p> 在 a 标签内
        "pagination_selector": "",  # 翻页容器由 find_next_page_url 回退处理
        "next_page_selector": "a.Next",  # 精确 CSS: 下页链接均带 class="Next"
        "next_page_texts": ["下页"],  # 文本回退
    }


_register()
