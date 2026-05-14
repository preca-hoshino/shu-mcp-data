"""
处理器 33 — UTSEUS 自定义列表型 (div.right-content > div.right-title + div.right-data)
———— 列表 div.right-content（每篇文章块），
    标题 div.right-title（纯文本，非<a>标签），日期 div.right-data (YYYY年MM月DD日)，
    文章链接 div.learn-more > a，翻页 td[id^=fanye] + a.Next 下页

CMS 特征: Visual SiteBuilder (VSB) + 自定义模板
         + youare-content clearfix 内容区
         + div.right-content 单篇文章容器（重复）
         + div.right-title 标题（仅文本）
         + div.right-article 摘要
         + div.learn-more > a 文章详情链接（文本"详细页面 >"）
         + div.right-data 日期（格式：YYYY年MM月DD日）
         + td[id^=fanye] 分页信息（共X条 N/M）
         + a.Next 下页/尾页/首页/上页链接
         + 页码 URL 逆序: zyxw1.htm(第1页/最新) → zyxw1/22.htm(第2页) → zyxw1/1.htm(末页)

区分于:
  - Type 05 (vsbonlylist): 使用 div.fanye 翻页组件，列表为 div.right-list > ul > li
  - Type 32 (sjccustomlist): 使用 _simple_list_gotopage_fun JS 分页，列表为 li.clearfix
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 33"""
    SITE_TYPES["33"] = {
        "name": "UTSEUS自定义列表型",
        "list_selector": "",  # 文章列表无外层容器，直接匹配 div.right-content
        "row_selector": "div.right-content",  # 每篇文章: <div class="right-content">
        "title_selector": "div.right-title",  # 标题: <div class="right-title">（纯文本）
        "date_selector": "div.right-data",  # 日期: <div class="right-data">YYYY年MM月DD日
        "date_tag": "div",  # fallback
        "link_attr": "href",  # 链接在 div.learn-more > a[href] 中
        "pagination_selector": "td[id^='fanye']",  # 翻页容器: <td id="fanye189436">
        "next_page_selector": "a.Next",  # 下页链接: <a class="Next" href="...">下页</a>
        "next_page_texts": ["下页", "下一页"],  # 文本回退
    }


_register()
