"""
处理器 22 — listUL-abstract 型（妇委 / 电站自动化等站点）
———— 列表 ul.listUL > li > div.listItem > a > div.whitespace（标题）+ div.abstract（日期）
日期格式: 中文 YYYY年MM月DD日，翻页 div.page + span.p_next > a，倒序页码
CMS 特征: VSB 系统 + ul.listUL 容器 + div.listItem 行 + div.whitespace 标题 + div.abstract 日期 + div.page 翻页
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 22"""
    SITE_TYPES["22"] = {
        "name": "listUL-abstract型",
        "list_selector": "ul.listUL",
        "row_selector": "li",
        "title_selector": "div.whitespace",  # a 标签内的 div.whitespace
        "date_selector": "div.abstract",  # div.listItem > a > div.abstract
        "date_tag": "div",  # fallback
        "date_regex": r"(\d{4}年\d{1,2}月\d{1,2}日)",  # 中文日期格式
        "pagination_selector": "div.page",  # 翻页容器
        "next_page_selector": "",  # 无特定 CSS，用文本回退
        "next_page_texts": ["下页"],  # 文本匹配
    }


_register()
