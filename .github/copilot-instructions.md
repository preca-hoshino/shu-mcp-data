# SHU MCP Data 开发指南

## 项目概述

这是一个 Python 爬虫项目，定时爬取上海大学各院系/部门网站新闻，产出结构化 JSON 数据，为 [shu-mcp](https://github.com/arts-amadeus/shu-mcp) MCP 服务提供数据源。

## 技术栈

- **语言**: Python 3.12+
- **网络请求**: requests (线程池 + Session 复用)
- **HTML 解析**: beautifulsoup4 (CSS 选择器)
- **并发模型**: ThreadPoolExecutor（栏目级 + 页码级双重并发）
- **进度显示**: rich (ANSI 进度条)
- **代码质量**: Ruff (Linter + Formatter)、mypy (类型检查)、pytest (测试)

## 目录结构

```
├── scheduler.py         # 启动器，将 src/ 加入 Python 路径后委托 src/scheduler.main()
├── src/
│   ├── scheduler.py     # CLI 逻辑，参数解析与流程编排
│   ├── crawler.py       # 主引擎，动态负载均衡 & 任务调度
│   ├── column.py        # 单栏目页面级并发爬取
│   ├── fetch.py         # 网络层：线程级 Session 池、UA 伪装、重试
│   ├── parser.py        # HTML 解析：文章提取、日期标准化、翻页检测
│   ├── writer.py        # JSON 输出：增量合并、签名去重
│   ├── whitelist.py     # 白名单管理与 domian.txt 解析
│   ├── config.py        # 全局配置常量（路径、并发、延迟）
│   ├── handlers/        # 39 种站点类型处理器 + 进度显示
│   │   ├── __init__.py  # 包导出（导入全部 handler 触发注册）
│   │   ├── p01_zhgy.py ~ p39_*.py  # 各站点类型选择器注册
│   │   ├── progress.py  # Rich ANSI 进度条
│   │   └── executor.py  # 向后兼容模块（已废弃）
│   └── whitelists/      # 各站点类型白名单 JSON
├── tests/               # 测试套件
├── output/              # 爬取结果（自动生成，每个部门一个 JSON）
└── domian.txt           # 白名单源文件
```

## 编码原则

以下规则适用于所有 Python 源文件：

1. **所有公共函数必须标注类型** — 参数类型 + 返回类型，使用 Python 3.12+ 内置泛型
2. **模块 docstring 必须存在** — 每个 `.py` 文件开头用 `"""..."""` 描述职责
3. **中文注释**用于业务逻辑说明，**英文术语**保留 Python 标准命名
4. **禁止裸 except** — 至少捕获 `Exception`，优先捕获具体异常
5. **禁止可变默认参数** — 使用 `None` + 函数内初始化
6. **库代码禁止 `print()`** — 使用 `logging` 或通过返回值向上传递（CLI 入口除外）
7. **预编译正则** — 全局常量级 `re.compile()`，避免循环内重复编译
8. **线程安全** — 共享状态加锁，线程局部变量用 `threading.local()`
9. **模块依赖单向** — `config` → `fetch/parser/whitelist` → `column` → `crawler` → `scheduler`

## 开发工作流

```bash
# 安装依赖
pip install -r requirements-dev.txt

# 全量检查（格式化 + Lint + 类型 + 测试）
just check

# 自动修复
just fix

# 快速运行测试
just run-quick
```

## 提交规范

提交信息格式：`[Type](scope): 描述`

| Type | 用途 |
|------|------|
| `[Add]` | 新增功能（handler、解析器等） |
| `[Fix]` | 修复 Bug |
| `[Ref]` | 代码重构 |
| `[Del]` | 删除冗余代码 |
| `[Doc]` | 文档修改 |
| `[Chore]` | 依赖更新、配置维护 |
| `[Style]` | 格式化、Lint 修复 |
| `[Test]` | 测试代码 |
| `[Merge]` | 分支合并 |

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。
