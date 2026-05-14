"""
处理器 32 — SJC 自定义分页列表型 (div.jjyRight.fr > div.article > ul > li.clearfix)
———— 列表 div.article > ul > li.clearfix，
    标题 a 标签文本，日期 span.fr (YYYY-MM-DD)，
    翻页 _simple_list_gotopage_fun(N, ...) JS 分页 + a.Next 下页链接

CMS 特征: 疑似博达 CMS 自定义模板
         + div.jjyRight.fr 内容容器（右侧主内容区）
         + div.article 文章列表容器
         + ul > li.clearfix 行元素
         + a 标签内标题文本
         + span.fr 日期（格式 YYYY-MM-DD）
         + 翻页: _simple_list_gotopage_fun(总页数, ...) JS 函数
         + 下页链接: a.Next (class="Next")
         + 页码 URL 逆序: zhxw.htm(第1页/最新) → zhxw/{N-1}.htm(第2页) → zhxw/1.htm(末页)
         + 分页信息: "共XX条  X/YY"

区分于:
  - Type 05 (vsbonlylist): 使用 div.fanye 翻页组件 + a.Next，列表为 div.right-list > ul > li
  - Type 31 (sfavsblist): 使用 div.pb_sys_common 翻页组件，列表为 ul.notice-list > li.notice-item
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 32"""
    SITE_TYPES["32"] = {
        "name": "SJC自定义分页列表型",
        "list_selector": "div.jjyRight.fr",  # 文章列表容器（右侧主内容区）
        "row_selector": "li.clearfix",  # 每行: <li class="clearfix">
        "title_selector": "",  # 标题: 取 li.clearfix > a 标签文本（默认行为）
        "date_selector": "span.fr",  # 日期: <span class="fr">YYYY-MM-DD</span>
        "date_tag": "span",  # fallback
        "link_attr": "href",  # 链接在 a[href] 中
        "pagination_selector": "div.article div[align='center']",  # 翻页容器: div.article 内的分页区域
        "next_page_selector": "a.Next",  # 下页链接: <a class="Next" href="...">下页</a>
        "next_page_texts": ["下页", "下一页"],  # 文本回退
    }


_register()
