"""
shu-mcp 全局配置
———— 路径常量、请求参数、站点类型注册表
"""

from pathlib import Path

# ————————————————————————————————————————————————————————————
# 路径常量
# ————————————————————————————————————————————————————————————

_ROOT = Path(__file__).resolve().parent
ROOT_DIR = _ROOT.parent  # 项目根目录（src/ 的上级）

WHITELIST_DIR = str(_ROOT / "whitelists")
DOMIAN_FILE = str(ROOT_DIR / "domian.txt")
OUTPUT_DIR = str(ROOT_DIR / "output")

# ————————————————————————————————————————————————————————————
# 并发 / 延迟配置
# ————————————————————————————————————————————————————————————

DEFAULT_WORKERS = 3  # 统一并发数（栏目级 + 页码级）

# —— 统一请求延迟（秒）——
REQUEST_DELAY = 1.5  # 每次请求前固定等待（秒），设 0 则使用随机延迟
REQUEST_DELAY_MIN = 0.8  # 随机延迟下限（REQUEST_DELAY=0 时生效）
REQUEST_DELAY_MAX = 2.5  # 随机延迟上限（REQUEST_DELAY=0 时生效）
RETRY_DELAY = 3.0  # 重试退避基础间隔（秒）

# —— 重试 ——
MAX_RETRIES = 3  # 最大重试次数
RETRY_BACKOFF_BASE = 2.0  # 重试退避指数基数
RETRY_STATUSES = {429, 500, 502, 503, 504}  # 对这些状态码自动重试

# —— 超时 ——
REQUEST_TIMEOUT = 30  # 请求超时（秒），连接和读取共用此超时

# ————————————————————————————————————————————————————————————
# 站点类型配置 —— 各包装器（p01~p27）负责注册
# ————————————————————————————————————————————————————————————

SITE_TYPES: dict[str, dict[str, str | int | list[str]]] = {}
