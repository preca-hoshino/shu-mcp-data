"""
handlers 包 —— 按站点类型收集所有处理器模块

架构:
    config.py     —— 全局配置 + SITE_TYPES 注册表
    fetch.py      —— 网络层
    parser.py     —— HTML 解析层
    column.py     —— 单栏目页面级并发爬取
    crawler.py    —— 动态部门均衡调度引擎
    whitelist.py  —— 白名单管理
    p01~p27       —— 包装器：各注册自己的 SITE_TYPES
    progress.py   —— 进度显示器
"""

from config import (  # noqa: F401
    DEFAULT_WORKERS,
    OUTPUT_DIR,
    SITE_TYPES,
)
from crawler import crawl_all_whitelist  # noqa: F401
from fetch import close_all_sessions, fetch  # noqa: F401
from parser import (  # noqa: F401
    extract_articles,
    find_next_page_url,
    get_total_pages_from_html,
)
from whitelist import (  # noqa: F401
    add_to_whitelist,
    domain_key,
    load_whitelist,
    parse_domian_txt,
    path_from_url,
    save_whitelist,
    show_whitelist,
)

# 注册各站点类型（仅需 import 即可触发 _register()）
from . import (
    p01_zhgy,  # noqa: F401  # 类型 01
    p02_ac,  # noqa: F401  # 类型 02
    p03_listul,  # noqa: F401  # 类型 03
    p04_artlist,  # noqa: F401  # 类型 04
    p05_vsbonlylist,  # noqa: F401  # 类型 05
    p06_rightlist,  # noqa: F401  # 类型 06
    p07_onlylist,  # noqa: F401  # 类型 07
    p08_listright,  # noqa: F401  # 类型 08
    p09_listrlb,  # noqa: F401  # 类型 09
    p10_vsbnewlist,  # noqa: F401  # 类型 10
    p11_textcontent,  # noqa: F401  # 类型 11
    p12_listrtd,  # noqa: F401  # 类型 12
    p13_listpage,  # noqa: F401  # 类型 13
    p14_sjlistul,  # noqa: F401  # 类型 14
    p15_xwlt,  # noqa: F401  # 类型 15
    p16_shumain,  # noqa: F401  # 类型 16
    p17_listcrd,  # noqa: F401  # 类型 17
    p18_listpagelist,  # noqa: F401  # 类型 18
    p19_listcentrerilb,  # noqa: F401  # 类型 19
    p20_listul,  # noqa: F401  # 类型 20
    p21_listul,  # noqa: F401  # 类型 21
    p22_listulabs,  # noqa: F401  # 类型 22
    p23_listbody,  # noqa: F401  # 类型 23
    p24_vsbtable,  # noqa: F401  # 类型 24
    p25_vsblistli,  # noqa: F401  # 类型 25
    p26_hrcmslist,  # noqa: F401  # 类型 26
    p27_vsbnewsdata,  # noqa: F401  # 类型 27
    p28_vsbbarespan,  # noqa: F401  # 类型 28
    p29_mbanewslist,  # noqa: F401  # 类型 29
    p30_vsbcardlist,  # noqa: F401  # 类型 30
    p31_sfavsblist,  # noqa: F401  # 类型 31
    p32_sjccustomlist,  # noqa: F401  # 类型 32
    p33_utseuslist,  # noqa: F401  # 类型 33
    p34_modartlist,  # noqa: F401  # 类型 34
    p35_nanolist,  # noqa: F401  # 类型 35
    p36_dnnarticles,  # noqa: F401  # 类型 36
    p37_physicslist,  # noqa: F401  # 类型 37
    p38_xyylist,  # noqa: F401  # 类型 38
)
from .progress import ProgressDisplay  # noqa: F401
