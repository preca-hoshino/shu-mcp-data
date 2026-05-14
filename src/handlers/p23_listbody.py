"""
处理器 23 — listBody 型（工程技术训练中心等站点）
———— 列表 ul.listBody > li，标题 p，日期 span.date，翻页 div.fanye + a.Next
CMS 特征: VSB 系统 + ul.listBody 容器 + p 标题 + span.date 日期 + a.Next 翻页 + fanye td 总页数 + 倒序翻页
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 23"""
    SITE_TYPES["23"] = {
        "name": "listBody型",
        "list_selector": "ul.listBody",
        "row_selector": "li",
        "title_selector": "p",  # li > a > div > p
        "date_selector": "span.date",  # li > a > span.date
        "pagination_selector": "div.fanye",  # 翻页容器
        "next_page_selector": "a.Next",  # 精确 CSS: 下页链接带 class="Next"
        "next_page_texts": ["下页"],  # 文本回退
    }


_register()
