"""
处理器 21 — second_artlist 型（新型显示技术实验室等站点）
———— 列表 ul#second_artlist > li，标题 a，日期 li 内纯文本（正则提取），翻页 a.Next
CMS 特征: 自建系统 + ul#second_artlist 容器 + li 内 a[href][title] + 日期纯文本 + a.Next 翻页 + N/M 总页数 + 倒序翻页
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 21"""
    SITE_TYPES["21"] = {
        "name": "second_artlist型",
        "list_selector": "ul#second_artlist",
        "row_selector": "li",
        "title_selector": "",  # 直接取 a 标签文本
        "date_selector": "",  # 回退到 date_tag → 正则
        "date_tag": "span",  # li 内无 span，触发 fallback 正则提取
        "date_regex": r"(\d{4}[-/.]\d{1,2}[-/.]\d{1,2})",  # YYYY-MM-DD 格式
        "pagination_selector": "",  # 无特定容器，全页搜索
        "next_page_selector": "a.Next",  # 精确 CSS: 下页链接带 class="Next"
        "next_page_texts": ["下页"],  # 文本回退
    }


_register()
