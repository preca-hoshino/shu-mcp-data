"""
处理器 36 — DNN Articles 列表型 (news.shu.edu.cn 等 DNN/VSB Articles 模块)
———— 列表 table.ArticleList（文章列表），
    标题 tr[id^="line_u5_"] > a[id*="titleLink"]，
    日期 span[id*="lblPublishDate"] (YYYY-MM-DD)，
    翻页 td[id^="fanye"] "共X条 N/M" + a.Next 下页/尾页

CMS 特征: DNN (DotNetNuke) + VSB (Visual SiteBuilder) Articles 模块
         + table.ArticleList 文章列表主容器（class="ArticleList"）
         + tr[id^="line_u5_"] 每篇文章行（如 line_u5_0）
         + 内嵌 table>tr>td 横向布局（标题左 + 日期右）
         + a[id*="titleLink"] 标题链接（也可能是 a.Normal）
         + span[id*="lblPublishDate"] 日期（格式: YYYY-MM-DD）
         + td[id^="fanye"] 翻页信息单元格
         + "共X条  N/M" 格式分页（N=当前页, M=总页数）
         + JS: _simple_list_gotopage_fun(总页数, ...)
         + a.Next=下页, span.PrevDisabled=首页/上页(禁用态)
         + 页码 URL 逆序: base.htm(第1页) → base/{总页数-1}.htm(第2页) → base/1.htm(末页)

区分于:
  - Type 24 (VSB表格型): 使用 tr[id^="line_u"] 无 table.ArticleList，翻页 span.p_next
  - Type 05 (vsbonlylist): 使用 div.fanye + div.right-list 翻页组件
  - Type 16 (shumain): 使用 div.list-container 翻页组件
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 36"""
    SITE_TYPES["36"] = {
        "name": "DNNArticles列表型",
        "list_selector": "table.ArticleList",  # DNN Articles 模块主容器
        "row_selector": 'tr[id^="line_u5_"]',  # 文章行: <tr id="line_u5_0">
        "title_selector": "",  # 标题取行内第一个 a 标签
        "date_selector": 'span[id*="lblPublishDate"]',  # 日期: <span id="...lblPublishDate">YYYY-MM-DD</span>
        "date_tag": "span",
        "link_attr": "href",
        "pagination_selector": 'td[id^="fanye"]',  # 翻页信息单元格: "共X条  N/M"
        "next_page_selector": "a.Next",  # 下页链接: <a class="Next" href="...">下页</a>
        "next_page_texts": ["下页", "下一页"],
    }


_register()
