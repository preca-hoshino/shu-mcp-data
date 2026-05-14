"""
处理器 12 — list-rt-d 型（化学教学实验中心等站点）
———— 列表 div.list-rt-d > ul > li，标题 a > span，日期 a > i，翻页 table 内 class="Next"
CMS 特征: div.list-rt-d 容器 + span 标题 + i 日期 + 递减翻页偏移
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 12"""
    SITE_TYPES["12"] = {
        "name": "list-rt-d型",
        "list_selector": "div.list-rt-d",
        "row_selector": "li",
        "title_selector": "",  # 直接取 a 或其兄弟文本（兼容 gzc 无 span 的情况）
        "date_selector": "a i",
        "pagination_selector": "",
        "next_page_texts": ["下页", "下一页"],
    }


_register()
