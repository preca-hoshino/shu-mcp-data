"""
处理器 18 — listPageList 型（采购与招标管理中心等站点）
———— 列表 ul.listPageList > li，标题 a（a>p 包含标题文本），日期 li>div，翻页 a.Next
CMS 特征: VSB 系统 + ul.listPageList 容器 + li>div 日期 + a.Next 翻页 + fanye td 总页数
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 18"""
    SITE_TYPES["18"] = {
        "name": "listPageList型",
        "list_selector": "ul.listPageList",
        "row_selector": "li",
        "title_selector": "",  # 取 a 标签文本（a>p 的文本）
        "date_selector": "",  # 回退到 date_tag
        "date_tag": "div",  # <div>2026/01/22</div> 直接子 div
        "pagination_selector": "td[id^='fanye']",  # 精确定位 VSB 分页 td（id=fanyeNNNNN）
        "next_page_selector": "a.Next",  # 精确 CSS: 下页链接带 class="Next"
        "next_page_texts": ["下页"],  # 文本回退
    }


_register()
