"""
处理器 38 — HRCMS 嵌套表格列表型 (xyy.shu.edu.cn 等站点)
———— 列表 tr[id^="line_u"]（文章行），
    标题 tr[id^="line_u"] 内 a.linkfont1（文章链接），
    日期 tr[id^="line_u"] 内 span.linkfont1 (YYYY-MM-DD)，
    翻页 "共X条 Y/Z" + a.Next 下页/尾页

CMS 特征: 上海大学 HRCMS 系统（嵌套表格布局）
         + tr[id^="line_u"] 文章行（每行含嵌套3行表格）
         + a.linkfont1 标题链接（class="linkfont1"）
         + span.linkfont1 日期（class="linkfont1"，格式: YYYY-MM-DD）
         + "共X条  Y/Z" 翻页信息文本
         + a.Next=下页, span.PrevDisabled=首页/上页(禁用态)
         + a.Next(href="尾页URL")=尾页
         + 页码 URL 逆序: base.htm(第1页) → base/{N}.htm(第2页) → ... → base/1.htm(末页)

区别于:
  - Type 26 (hrcmslist): tr[id^="line_u"] 行，但日期是 span.artdata，标题/日期不在嵌套表格中
  - Type 37 (physicslist): ul#newslist > li.artlist 非表格型
  - Type 36 (dnnarticles): table.ArticleList 容器, tr 行
"""

from config import SITE_TYPES


def _register() -> None:
    """向 SITE_TYPES 注册类型 38"""
    SITE_TYPES["38"] = {
        "name": "HRCMS嵌套表格列表型",
        "list_selector": "",  # 全页搜索
        "row_selector": 'tr[id^="line_u"]',  # HRCMS 文章行: <tr id="line_u3_0">
        "title_selector": "",  # 直接取第一个 a 标签文本 (a.linkfont1)
        "date_selector": "span.linkfont1",  # <span class="linkfont1">YYYY-MM-DD</span>
        "date_tag": "span",
        "link_attr": "href",
        "pagination_selector": "",  # 空→全页搜索（翻页文本格式 "共N条  Y/Z" 全页可识别）
        "next_page_selector": "a.Next",  # 下页链接: <a class="Next" href="...">下页</a>
        "next_page_texts": ["下页"],  # 文本回退
    }


_register()
