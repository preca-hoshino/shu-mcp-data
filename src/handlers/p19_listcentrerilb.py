"""
处理器 19 — list-center-ri-lb 型（党委教师工作部 / 党史学习教育专题网等站点）
———— 列表 div.list-center-ri-lb > ul > li，标题 a，日期 span，翻页 a.Next
CMS 特征: VSB 系统 + div.list-center-ri-lb 容器 + span 日期 + a.Next 翻页 + fanye td 总页数
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 19"""
    SITE_TYPES["19"] = {
        "name": "list-center-ri-lb型",
        "list_selector": "div.list-center-ri-lb",
        "row_selector": "li",
        "title_selector": "",  # 直接取 a 标签文本
        "date_selector": "",  # 回退到 date_tag
        "date_tag": "span",  # <span>2026/04/20</span>
        "pagination_selector": "td[id^='fanye']",  # VSB 分页 td（id=fanyeNNNNN）
        "next_page_selector": "a.Next",  # 精确 CSS: 下页链接带 class="Next"
        "next_page_texts": ["下页"],  # 文本回退
    }


_register()
