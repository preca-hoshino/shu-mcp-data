"""
shu-mcp 执行器 —— 向后兼容模块

⚠️ 此文件已废弃，所有功能已迁移至项目根目录的子模块：
    config.py     —— 全局配置 + SITE_TYPES 注册表
    fetch.py      —— 网络层（Session 复用 + 请求重试）
    parser.py     —— HTML 解析层（文章提取、翻页检测、页码推断）
    crawler.py    —— 爬取引擎（页面级并发 + 域名级并发）
    whitelist.py  —— 白名单管理（加载/保存/查看/domian.txt 解析）

保留此文件仅为向后兼容，直接导入新位置即可。
"""

# 从新位置导入所有公开符号
from config import (  # noqa: F401
    DEFAULT_WORKERS,
    DOMIAN_FILE,
    MAX_RETRIES,
    OUTPUT_DIR,
    REQUEST_DELAY_MAX,
    REQUEST_DELAY_MIN,
    RETRY_BACKOFF_BASE,
    ROOT_DIR,
    SITE_TYPES,
    WHITELIST_DIR,
)
from crawler import crawl_all_whitelist  # noqa: F401
from fetch import fetch  # noqa: F401
from parser import (  # noqa: F401
    build_page_urls,
    extract_articles,
    find_next_page_url,
    get_total_pages_from_html,
    normalize_date,
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
