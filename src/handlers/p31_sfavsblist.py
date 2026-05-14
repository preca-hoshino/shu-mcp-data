"""
处理器 31 — SFA VSB列表型 (div.right > ul.*-list > li.*-item)
———— 列表 ul.notice-list / ul.teacher-list > li.notice-item / li.teacher-item，
    标题 a 标签文本，无日期（WeChat链接），翻页 div.pb_sys_common > .p_next > a

CMS 特征: Visual SiteBuilder (VSB) + 自定义列表
         + div.right 内容容器
         + ul.notice-list 或 ul.teacher-list 列表容器
         + li.notice-item 或 li.teacher-item 行元素
         + 标题 a 标签内（链接目标为微信公众号 mp.weixin.qq.com）
         + 无日期显示
         + div.pb_sys_common 翻页组件 + span.p_next a 下页链接
         + span.p_t 显示"共N条"
         + 页码 URL 降序: tzgg.htm(首页) → tzgg/126.htm(第2页,总共127页)

区分于:
  - Type 29 (mbanewslist): ul.news-list > li.news-item，标题 div.news-title，有日期 div.date-box
  - Type 30 (vsbcardlist): a[id^='line_u'] 行即链接，div.right-jjy 容器
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 31"""
    SITE_TYPES["31"] = {
        "name": "SFA VSB列表型",
        "list_selector": "div.right",  # 文章列表容器（共通）
        "row_selector": "li.notice-item, li.teacher-item",  # 每行: <li class="notice-item"> 或 <li class="teacher-item">
        "title_selector": "",  # 标题: 取 a 标签文本（默认行为）
        "date_selector": "",  # 无日期显示
        "date_tag": "span",  # fallback（不会命中）
        "link_attr": "href",  # 链接在 a[href] 中（微信公众号链接）
        "pagination_selector": "div.pb_sys_common",  # 翻页容器: VSB 标准分页
        "next_page_selector": "span.p_next a",  # 下页链接: <span class="p_next"><a>
        "next_page_texts": ["下页", "下一页"],  # 文本回退
    }


_register()
