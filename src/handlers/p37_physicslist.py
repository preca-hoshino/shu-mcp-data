"""
处理器 37 — VSB ul#newslist 列表型 (physics.shu.edu.cn 等站点)
———— 列表 ul#newslist（文章列表），
    标题 li.artlist > a.alistp（文章链接），
    日期 li.artlist > span.listdate (YYYY-MM-DD)，
    翻页 td[id^="fanye"] "共X条 N/M" + a.Next 下页/尾页

CMS 特征: 上海大学 VSB (Visual SiteBuilder) 标准列表模板
         + ul#newslist 文章列表主容器
         + li.artlist 每篇文章行（class="artlist"）
         + a.alistp 标题链接（class="alistp"）
         + span.listdate 日期（class="listdate"，格式: YYYY-MM-DD）
         + td[id^="fanye"] 翻页信息单元格（含"共X条  N/M"）
         + JS: _simple_list_gotopage_fun(总页数, ...)
         + a.Next=下页, span.PrevDisabled=首页/上页(禁用态)
         + a.Next(href="尾页URL")=尾页
         + 页码 URL 逆序: base.htm(第1页) → base/{总页数-1}.htm(第2页) → ... → base/1.htm(末页)

区分于:
  - Type 35 (nanolist): div.list-center-right-center ul, Next/Prev 有独立 class
  - Type 36 (DNNArticles): table.ArticleList 容器, tr 行, 不同选择器
  - Type 05 (vsbonlylist): div.fanye + div.right-list
  - Type 20 (listUL): ul.listUL + div.listItem
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 37"""
    SITE_TYPES["37"] = {
        "name": "VSB-newslist列表型",
        "list_selector": "ul#newslist",  # VSB 文章列表主容器
        "row_selector": "li.artlist",  # 文章行: <li class="artlist">
        "title_selector": "a.alistp",  # 标题链接: <a class="alistp" href="...">
        "date_selector": "span.listdate",  # 日期: <span class="listdate">YYYY-MM-DD</span>
        "date_tag": "span",
        "link_attr": "href",
        "pagination_selector": 'td[id^="fanye"]',  # 翻页信息单元格: "共X条  N/M"
        "next_page_selector": "a.Next",  # 下页链接: <a class="Next" href="...">下页</a>
        "next_page_texts": ["下页"],  # 文本回退
    }


_register()
