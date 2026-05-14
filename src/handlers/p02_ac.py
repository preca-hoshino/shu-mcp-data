"""
处理器 02 — list-center-r-down 型（学术委员会等站点）
———— 列表容器 .list-center-r-down，文章 li>a + li>i，翻页在下方的 div[align=center] 中
"""

# 从 executor 导入公共基础设施并注册新类型
from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 02"""
    SITE_TYPES["02"] = {
        "name": "博达CMS-list-center-r-down型",
        "list_selector": ".list-center-r-down",
        "pagination_selector": ".list-center-r-down div[align='center']",
        "next_page_texts": ["下页", "下一页", ">", "›", "»"],
        "date_tag": "i",  # 日期在 <i> 标签中
    }


_register()
