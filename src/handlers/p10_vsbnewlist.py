"""
处理器 10 — VSB new-list 型（本科招生网、理学院、通信学院、附属中学等站点）
———— 列表 li[id^="line_u"] > a(标题) + i(日期)，翻页 a.Next "下页"
VSB 标识: new-list.vsb.css + 分页 table.headStyle*
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 10"""
    SITE_TYPES["10"] = {
        "name": "VSB new-list型",
        "list_selector": "",  # 全页搜索
        "row_selector": 'li[id^="line_u"]',  # VSB 文章行: <li id="line_u5_0">
        "pagination_selector": "",  # 翻页容器在 table.headStyle* 中，由 find_next_page_url 回退处理
        "next_page_selector": "a.Next",  # 精确 CSS: 下页链接均带 class="Next"
        "next_page_texts": ["下页"],  # 文本回退
        "date_selector": "i",  # <i>2026-04-03</i>
    }


_register()
