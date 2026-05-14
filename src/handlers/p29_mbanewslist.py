"""
处理器 29 — MBA新闻列表型 (ul.news-list + li.news-item)
———— 列表 ul.news-list > li.news-item，标题 div.news-title，日期 div.date-box
    （span.date-day + span.date-ym），链接在 li[onclick] 中，翻页 div.pagination > a.Next

CMS 特征: 自定义设计（非VSB），ul.news-list 容器 + li.news-item 行
         + div.news-title 标题 + div.date-box > span.date-day + span.date-ym 日期
         + li[onclick]="window.open(...)" 文章链接（非<a href>）
         + div.pagination 翻页容器 + a.Next 翻页链接
         + "共N条 X/Y" 总页数

区分于:
  - 所有其他类型: 链接在 onclick 而非 <a href> 中
  - 类型28: 日期在裸 span 中
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 29"""
    SITE_TYPES["29"] = {
        "name": "MBA新闻列表型",
        "list_selector": "ul.news-list",  # 文章列表容器
        "row_selector": "li.news-item",  # 每行: <li class="news-item">
        "title_selector": "div.news-title",  # 标题: <div class="news-title">
        "date_selector": "div.date-box",  # 日期: <div class="date-box">（内含 span.date-day + span.date-ym）
        "date_tag": "span",  # fallback
        "link_attr": "onclick",  # 链接在 li[onclick]="window.open('url', '_self')"
        "pagination_selector": "div.pagination",  # 翻页容器
        "next_page_selector": "a.Next",  # 下页链接: <a class="Next" href="...">
        "next_page_texts": ["下页", "下一页"],  # 文本回退
    }


_register()
