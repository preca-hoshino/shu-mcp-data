"""
处理器 39 — PB CMS 列表型 (yjszs.shu.edu.cn 研究生招生网)
———— 列表 div.list-right > ul.clearfix > li.clearfix（文章列表），
    标题 li.clearfix > a > h3（文章标题），
    日期 li.clearfix > a > span ([YYYY/MM/DD])，
    翻页 span.p_pages（span.p_no_d=当前页, span.p_no=其他页, span.p_next a=下页）

CMS 特征: 上海大学 PB CMS (PowerBuilder Content Management System)
         + div.list-right 桌面端文章列表容器
         + div.mob-listPage 移动端文章列表容器
         + ul.clearfix > li.clearfix 每篇文章行
         + a > h3 标题链接
         + a > span 日期（格式: [YYYY/MM/DD]）
         + span.p_pages 翻页信息区域
         + span.p_no_d 当前页码（无链接，class=p_no_d）
         + span.p_no 可跳转页码（含 a 标签）
         + span.p_next a 下页链接
         + span.p_last a 尾页链接
         + span.p_first_d / span.p_prev_d 首页/上页（首页禁用态）
         + 页码 URL 逆序: base.htm(第1页) → base/{N}.htm (倒序: 第2页=N大值)

区别于:
  - Type 37 (physicslist): ul#newslist > li.artlist, 翻页 td[id^="fanye"]
  - Type 38 (xyylist): tr[id^="line_u"] 嵌套表格型
  - Type 05 (vsbonlylist): div.fanye + div.right-list
  - Type 20 (listUL): ul.listUL + div.listItem
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 39"""
    SITE_TYPES["39"] = {
        "name": "PB-CMS-clearfix列表型",
        "list_selector": "div.list-right, div.mob-listPage",  # 桌面端/移动端列表容器
        "row_selector": "ul.clearfix li.clearfix",  # 文章行: <li class="clearfix">
        "title_selector": "a h3",  # 标题: <a href="..."><h3>标题</h3></a>
        "date_selector": "a span",  # 日期: <a><span>[YYYY/MM/DD]</span></a>
        "date_tag": "span",
        "link_attr": "href",
        "pagination_selector": "span.p_pages",  # 翻页: <span class="p_pages">...</span>
        "next_page_selector": "span.p_next a",  # 下页链接: <span class="p_next"><a href="...">下页</a>
        "next_page_texts": ["下页"],  # 文本回退
    }


_register()
