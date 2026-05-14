"""
处理器 35 — nano 列表型 (div.list-center-right-center ul > li > a + span)
———— 列表 div.list-center-right-center ul（文章列表），
    标题 li > a（文章链接），日期 li > span (YYYY-MM-DD)，
    翻页 div.list-center-right-dwon "共X条 N/M" + a.Next 下页/尾页

CMS 特征: 上海大学纳米科学与技术研究中心自定义模板
         + div.list-center-right-down 页面布局层
         + div.list-center-right-center 文章列表主容器
         + ul > li 文章条目（a=标题链接，span=日期）
         + 条目间穿插 <span id="section_u3_X"> 隐藏占位（需过滤）
         + div.list-center-right-dwon 分页组件
         + "共X条  N/M" 格式分页信息
         + a.Next=下页, a.Prev=上页, span.PrevDisabled=首页/上页(禁用态)
         + 页码 URL: base.htm(第1页) → base/N.htm(第N+1页)

区分于:
  - Type 34 (modart): ul.rightList, 日期中文格式(YYYY年MM月DD日), 页码逆序
  - Type 05 (vsbonlylist): 使用 div.fanye 翻页组件
  - Type 06 (rightlist): 使用 div.right-list > ul > li, VSB fanye td
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 35"""
    SITE_TYPES["35"] = {
        "name": "nano列表型",
        "list_selector": "div.list-center-right-center ul",  # 文章列表容器（在list-center-right-down内）
        "row_selector": "li",  # 每篇文章: <li>
        "title_selector": "",  # 标题: 直接取 li > a 文本
        "date_selector": "span",  # 日期: <span>YYYY-MM-DD</span>
        "date_tag": "span",  # fallback
        "link_attr": "href",  # 链接在 li > a[href] 中
        "pagination_selector": "div.list-center-right-dwon",  # 翻页容器: 含"共X条 N/M"文本
        "next_page_selector": "a.Next",  # 下页链接: <a class="Next" href="...">下页</a>
        "next_page_texts": ["下页", "下一页"],  # 文本回退
    }


_register()
