---
description: "Use when writing or modifying Python source code in this project. Covers type hints, error handling, module organization, import ordering, and all Ruff-enforced rules."
applyTo:
  - "src/**/*.py"
  - "tests/**/*.py"
---

# Python 编码规范

本项目通过 `pyproject.toml` 中的 `[tool.ruff]` 配置强制执行代码质量标准。以下规则在所有 Python 源文件中**必须遵守**。

## 类型标注

### 所有公共函数必须标注类型

```python
# ✅ 正确
def crawl_one_column(domain: str, path: str, site_type: str,
                     max_pages: int = 1) -> list[dict]:
    """爬取单个栏目的所有文章。"""
    ...

# ❌ 错误 — 缺少参数类型和返回类型
def crawl_one_column(domain, path, site_type, max_pages=1):
    ...
```

### 使用现代类型语法（Python 3.12+）

```python
# ✅ 使用内置泛型
def group_by_domain(items: list[dict]) -> dict[str, list[dict]]:
    ...

# ❌ 避免旧式 typing 导入
from typing import List, Dict  # 不需要
```

### 类型标注例外

- 内部辅助函数（私有、不导出）可省略类型标注
- 变量类型可由类型检查器推断时不必显式标注

## 文档字符串

### 模块级 docstring

每个 `.py` 文件必须以描述模块职责的 docstring 开头：

```python
"""
shu-mcp 网络层
———— 线程级 Session 复用 + 浏览器全伪装 + 统一延迟 + 智能重试
"""
```

### 公共函数 docstring

```python
def fetch(url: str, timeout: int = 30) -> requests.Response | None:
    """发起 HTTP GET 请求，内置重试与伪装。

    Args:
        url: 目标 URL。
        timeout: 超时秒数，默认 30。

    Returns:
        成功时返回 Response 对象，全部重试失败返回 None。
    """
```

### 格式约定

- 使用 Google 风格 docstring（`Args:` / `Returns:` / `Raises:`）
- 中文描述业务逻辑，专有名词保留英文
- 第一行（summary line）使用 `"""` 同一行

## 导入顺序

使用 Ruff isort 规则强制排序，顺序为：**标准库 → 第三方库 → 本地模块**

```python
# ✅ 正确顺序
import atexit
import threading
import time
from urllib.parse import urlparse

import requests
import urllib3

from config import REQUEST_DELAY, MAX_RETRIES
```

## 错误处理

### 禁止裸 except

```python
# ❌ 禁止
try:
    do_something()
except:
    pass

# ✅ 至少捕获 Exception
try:
    do_something()
except Exception:
    pass

# ✅ 更好：捕获具体异常
try:
    response = requests.get(url, timeout=30)
except requests.Timeout:
    response = None
except requests.ConnectionError:
    response = None
```

### 网络/IO 操作必须处理异常

所有涉及网络请求、文件读写的操作必须有明确的异常处理路径。

```python
# ✅ 正确的网络请求模式
try:
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"[WARN] 请求失败: {e}")
    return None
```

## 禁止模式

### `print()` 在库代码中

```python
# ❌ 在库代码中使用 print
print("debug info")  # Ruff T20 会报错

# ✅ 使用 logging 或调度器内部控制台输出
import logging
logger = logging.getLogger(__name__)
logger.info("debug info")
```

例外：`scheduler.py`（CLI 入口）和 `progress.py`（终端 UI）可使用 `print()`。

### 可变默认参数

```python
# ❌ 禁止
def foo(items: list[str] = []) -> list[str]:
    ...

# ✅ 使用 None
def foo(items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    ...
```

### 无意义的 f-string

```python
# ❌
x = f"hello"

# ✅
x = "hello"
```

## 模块组织

本项目按**职责**拆分模块，依赖方向清晰：

```
scripts/
├── scheduler.py       ← CLI 入口，参数解析
├── crawler.py         ← 主引擎，任务调度 & 负载均衡
├── column.py          ← 单栏目页面级并发爬取
├── fetch.py           ← 网络层（线程安全）
├── parser.py          ← HTML 解析 & 日期标准化
├── writer.py          ← JSON 输出 & 增量合并
├── whitelist.py       ← 白名单管理
├── config.py          ← 全局常量 & 配置
└── handlers/          ← 站点类型处理器
    ├── __init__.py    ← 包导出 & 所有 handler 注册
    ├── p01_xxx.py     ← 处理器模块（仅注册 SITE_TYPES）
    ├── progress.py    ← 进度显示器
    └── executor.py    ← 进度聚合器
```

### 模块依赖规则

- `config.py` 无本地依赖（只有标准库 `os`）
- `fetch.py` / `parser.py` / `whitelist.py` 只依赖 `config.py`
- `column.py` 依赖 `fetch.py` + `parser.py`
- `crawler.py` 依赖 `column.py` + `writer.py` + `whitelist.py`
- `scheduler.py` 只依赖 `handlers` 包
- **禁止循环导入**

## 性能规范

### 避免循环中的重复计算

```python
# ❌ 每次循环重新编译正则
import re
for url in urls:
    if re.match(r"https?://", url):
        ...

# ✅ 预编译
import re
URL_RE = re.compile(r"https?://")

for url in urls:
    if URL_RE.match(url):
        ...
```

### 使用生成器处理大数据集

```python
# ✅ 惰性求值，节省内存
def iter_articles(articles: list[dict]) -> Generator[dict, None, None]:
    for article in articles:
        if article.get("date"):
            yield article
```

## 线程安全

本项目使用 `ThreadPoolExecutor` 实现并发爬取，所有跨线程共享的状态必须：

```python
import threading

# ✅ 线程级存储（每个线程独立）
_thread_local = threading.local()

# ✅ 共享数据结构加锁
_lock = threading.Lock()
with _lock:
    shared_dict[key] = value
```
