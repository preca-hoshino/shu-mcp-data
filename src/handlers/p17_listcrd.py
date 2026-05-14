"""
处理器 17 — list-centre-right-down 型（财务处等站点）
———— 列表 div.list-centre-right-down > ul > li.clearfix，标题 a，日期 p.list-centre-right-down-p，翻页 a.Next
CMS 特征: VSB 系统 + div.list-centre-right-down 容器 + p.list-centre-right-down-p 日期 + a.Next 翻页 + _simple_list_gotopage_fun 总页数
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 17"""
    SITE_TYPES["17"] = {
        "name": "list-centre-right-down型",
        "list_selector": "div.list-centre-right-down",
        "row_selector": "li.clearfix",
        "title_selector": "",  # 直接取 a 标签文本
        "date_selector": "p.list-centre-right-down-p",  # <p class="list-centre-right-down-p">2025-09-19</p>
        "pagination_selector": "",  # 翻页在容器内，由 next_page_selector 定位
        "next_page_selector": "a.Next",  # 精确 CSS: 下页链接带 class="Next"
        "next_page_texts": ["下页"],  # 文本回退
    }


_register()
