"""
处理器 30 — VSB 卡片新闻列表型 (div.right-jjy > a[id^="line_u"])
———— 列表 div.right-jjy > a[id^="line_u"]（行即 a 标签），标题 p，无日期显示，
    翻页 div.pb_sys_common > .p_next > a

CMS 特征: Visual SiteBuilder (VSB) 9，卡片式新闻列表
         + div.right-jjy 容器（第二类名随栏目变化: kydt / zhaop）
         + a.kydtbox / a.zhaopbox 行元素（id=line_uX_Y）— 行即 <a> 标签
         + 标题 p 标签内
         + 无日期显示（仅图片+标题卡片布局）
         + div.pb_sys_common 翻页组件 + .p_next 下页链接
         + span.p_t 显示"共N条"
         + 页码 URL: kydt.htm(首页) → kydt/1.htm(第2页) → kydt/N.htm

区分于:
  - Type 24 (vsbtable): 使用 table 布局
  - Type 25 (vsblistli): 使用 ul/li 布局
  - Type 27 (vsbnewsdata): 含 span.news_metas 日期
  - Type 28 (vsbbarespan): 含裸 span 日期
  - Type 29 (mbanewslist): 自定义 ul.news-list，链接在 onclick 中
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 30"""
    SITE_TYPES["30"] = {
        "name": "VSB卡片新闻列表型",
        "list_selector": "div.right-jjy",  # 文章列表容器（共通）
        "row_selector": "a[id^='line_u']",  # 每行: <a id="line_uX_Y">（行即 a）
        "title_selector": ":scope > p",  # 标题: 直接子元素 <p>（跳过 div.zhaopdate 内的日期 p）
        "date_selector": "div.zhaopdate",  # 日期容器（仅 xwdt 有，kydt 无）
        "date_tag": "span",  # fallback（不会命中）
        "link_attr": "href",  # 链接在 a[href] 中（行即 a）
        "pagination_selector": "div.pb_sys_common",  # 翻页容器: VSB 标准分页
        "next_page_selector": "span.p_next a",  # 下页链接: <span class="p_next"><a>
        "next_page_texts": ["下页", "下一页"],  # 文本回退
    }


_register()
