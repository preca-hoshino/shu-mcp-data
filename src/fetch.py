"""
shu-mcp 网络层
———— 线程级 Session 复用 + 浏览器全伪装 + 统一延迟 + 智能重试
"""

import atexit
from collections.abc import MutableMapping
import contextlib
import random
import threading
import time
from urllib.parse import urlparse
import weakref

import requests
import urllib3

from config import (
    MAX_RETRIES,
    REQUEST_DELAY,
    REQUEST_DELAY_MAX,
    REQUEST_DELAY_MIN,
    REQUEST_TIMEOUT,
    RETRY_BACKOFF_BASE,
    RETRY_DELAY,
    RETRY_STATUSES,
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HTTP_NOT_FOUND = 404  # 404 状态码，不重试直接返回 None

# =========================================================================
# 会话清理 —— 防止 urllib3 连接池阻塞进程退出
# =========================================================================

_sessions: weakref.WeakSet[requests.Session] = weakref.WeakSet()
_cleanup_lock = threading.Lock()


def _cleanup_sessions() -> None:
    """Atexit 钩子：强制关闭所有已知 Session，释放连接池。"""
    with _cleanup_lock:
        for sess in list(_sessions):
            with contextlib.suppress(Exception):
                sess.close()
        _sessions.clear()


atexit.register(_cleanup_sessions)

# =========================================================================
# UA 池 / Accept-Language 池
# =========================================================================

_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.205 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
]

_ACCEPT_LANGUAGES = [
    "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "zh-CN,zh;q=0.9,en;q=0.8",
    "zh-CN,zh-Hans;q=0.9,en;q=0.8,ja;q=0.7",
]

_BASE_ACCEPT = (
    "text/html,application/xhtml+xml,application/xml;q=0.9,"
    "image/avif,image/webp,image/apng,*/*;q=0.8,"
    "application/signed-exchange;v=b3;q=0.7"
)

# =========================================================================
# 线程级 Session
# =========================================================================

_thread_local = threading.local()


def _build_headers(url: str) -> MutableMapping[str, str | bytes]:
    """根据目标 URL 构建一次性的伪装请求头"""
    parsed = urlparse(url)
    return {
        "Accept": _BASE_ACCEPT,
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": random.choice(_ACCEPT_LANGUAGES),
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "DNT": "1",
        "Referer": f"{parsed.scheme}://{parsed.hostname}/",
        "Sec-Ch-Ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": random.choice(_USER_AGENTS),
    }


def _get_session() -> requests.Session:
    """获取当前线程的 Session（线程安全 + 连接池复用）。"""
    if not hasattr(_thread_local, "session"):
        sess = requests.Session()
        sess.verify = False
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=20,
            pool_maxsize=20,
            max_retries=0,
            pool_block=False,
        )
        sess.mount("https://", adapter)
        sess.mount("http://", adapter)
        _thread_local.session = sess
        _sessions.add(sess)
    session: requests.Session = _thread_local.session
    return session


def close_all_sessions() -> None:
    """关闭所有已知线程级 Session，释放连接池资源。"""
    _cleanup_sessions()


# =========================================================================
# 延迟控制
# =========================================================================


def _apply_delay() -> None:
    """按配置施加统一的请求间隔"""
    time.sleep(
        REQUEST_DELAY if REQUEST_DELAY > 0 else random.uniform(REQUEST_DELAY_MIN, REQUEST_DELAY_MAX)
    )


# =========================================================================
# 重试辅助
# =========================================================================


def _retry_wait(attempt: int, tag: str, url: str, verbose: bool, exc: str = "") -> bool:  # noqa: ARG001
    """统一重试等待逻辑。返回 True 表示应继续重试。"""
    if attempt >= MAX_RETRIES:
        return False
    wait = RETRY_DELAY * (RETRY_BACKOFF_BASE ** (attempt - 1)) * random.uniform(0.7, 1.3)
    time.sleep(wait)
    return True


# =========================================================================
# 网络请求
# =========================================================================


def fetch(url: str, verbose: bool = True) -> str | None:  # noqa: C901, PLR0911
    """GET 请求（浏览器全伪装 + 统一延迟 + 智能重试），返回 HTML 文本。

    verbose=False 时静默所有重试/错误日志（适合批量爬取）。
    """
    session = _get_session()
    headers = _build_headers(url)

    for attempt in range(1, MAX_RETRIES + 1):
        _apply_delay()
        try:
            r = session.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        except requests.exceptions.Timeout:
            if not _retry_wait(attempt, "TIMEOUT", url, verbose):
                return None
        except requests.exceptions.ConnectionError as e:
            if not _retry_wait(attempt, "CONN", url, verbose, str(e)):
                return None
        except requests.RequestException as e:
            if not _retry_wait(attempt, "ERROR", url, verbose, str(e)):
                return None
        else:
            if r.status_code in RETRY_STATUSES and _retry_wait(attempt, "RETRY", url, verbose):
                continue
            if r.status_code == HTTP_NOT_FOUND:
                return None
            if not r.ok:
                return None
            r.encoding = r.apparent_encoding or "utf-8"
            return r.text

    return None
