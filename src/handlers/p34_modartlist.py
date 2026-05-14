"""
处理器 34 — modart 自定义列表型 (ul.rightList > li > a + span)
———— 列表 ul.rightList（文章列表），
    标题 li > a（文章链接），日期 li > span (YYYY年MM月DD日)，
    翻页 td "共X条 N/M" + a.Next 下页/尾页

CMS 特征: 自定义模板（非VSB）
         + div#rightPage 内容区
         + div#leftPage 侧边栏导航
         + ul.rightList 文章列表容器
         + li > a 标题链接（target=_blank 新窗口打开）
         + li > span 日期（格式：YYYY年MM月DD日）
         + table.headStyleXXX > td 分页信息（共X条 N/M）
         + a.Next 下页/尾页/首页/上页链接
         + 页码 URL 逆序: xyxw.htm(第1页) → xyxw/10.htm(第2页) → xyxw/1.htm(末页)

区分于:
  - Type 05 (vsbonlylist): 使用 div.fanye 翻页组件
  - Type 06 (rightlist): 使用 div.right-list > ul > li，VSB fanye td
  - Type 20 (listUL): 使用 ul.listUL 容器
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 34"""
    SITE_TYPES["34"] = {
        "name": "modart自定义列表型",
        "list_selector": "ul.rightList",  # 文章列表容器
        "row_selector": "li",  # 每篇文章: <li>
        "title_selector": "",  # 标题: 直接取 li > a 文本
        "date_selector": "span",  # 日期: <span>YYYY年MM月DD日</span>
        "date_tag": "span",  # fallback
        "link_attr": "href",  # 链接在 li > a[href] 中
        "pagination_selector": "td",  # 翻页容器: <td>（含"共X条 N/M"文本）
        "next_page_selector": "a.Next",  # 下页链接: <a class="Next" href="...">下页</a>
        "next_page_texts": ["下页", "下一页"],  # 文本回退
    }


_register()
