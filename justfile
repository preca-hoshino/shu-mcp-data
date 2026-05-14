# Justfile for shu-mcp-data
# Python 爬虫项目的开发脚本集
# 约定：check-* 系列只做检查不修改，fix-* 系列自动修复

set shell := ["powershell", "-c"]

# 默认显示任务列表
default:
    @just --list

# =========================================================================
# 运行
# =========================================================================

# [run] 增量爬取（默认 1 页，3 并发）
run:
    python scheduler.py -c 3

# [run-full] 全量爬取（不限页数）
run-full:
    python scheduler.py --mode full -c 3

# [run-quick] 快速测试（增量，1 页，CI 模式）
run-quick:
    python scheduler.py --no-progress --mode incremental -p 1 -c 3

# =========================================================================
# 质量检查（check-* 只读操作）
# =========================================================================

# [check-format] 检查代码格式（不修改）
check-format:
    ruff format --check .

# [check-lint] 静态 Lint 检查
check-lint:
    ruff check .

# [check-types] 静态类型检查
check-types:
    mypy .

# [check-test] 运行测试
check-test:
    pytest

# [check] 一键运行全部检查
check:
    @just check-format
    @just check-lint
    @just check-types
    @just check-test

# =========================================================================
# 自动修复（fix-* 会修改文件）
# =========================================================================

# [fix-format] 自动格式化代码
fix-format:
    ruff format .

# [fix-lint] 自动修复 Lint 问题（安全修复）
fix-lint:
    ruff check --fix .

# [fix] 一键自动修复
fix:
    @just fix-format
    @just fix-lint

# =========================================================================
# 依赖管理
# =========================================================================

# [install] 安装运行依赖
install:
    pip install -r requirements.txt

# [install-dev] 安装开发依赖（含 ruff, mypy, pytest）
install-dev:
    pip install -r requirements-dev.txt
