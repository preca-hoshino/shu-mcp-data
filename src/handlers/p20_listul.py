"""
处理器 20 — listUL 型（电气工程系等站点）
———— 列表 ul.listUL > li，行 div.listItem > a > div.whitespace，标题文本在 a 内，日期 span 在 a 内深层嵌套
CMS 特征: VSB 系统 + ul.listUL 容器 + div.listItem 行 + span 日期（a>div.whitespace>span）+ a.Next 翻页 + fanye td 总页数
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 20"""
    SITE_TYPES["20"] = {
        "name": "listUL型",
        "list_selector": "ul.listUL",
        "row_selector": "li",
        "title_selector": "",  # 直接取 a 标签文本（executor 会自动去除嵌套的 span 日期）
        "date_selector": "",  # 回退到 date_tag
        "date_tag": "span",  # <span>2025-12-03</span> 在 a>div.whitespace>span 内
        "pagination_selector": "td[id^='fanye']",  # VSB 分页 td（id=fanyeNNNNN）
        "next_page_selector": "a.Next",  # 精确 CSS: 下页链接带 class="Next"
        "next_page_texts": ["下页"],  # 文本回退
    }


_register()
