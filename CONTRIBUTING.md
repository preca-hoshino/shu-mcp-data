# 贡献指南 (Contributing Guide)

> 项目概述、快速启动和 API 文档请参见 [README.md](README.md)。

## 开发流程

### 环境准备

在开始开发之前，请确保你已经安装了 Python 3.12+ 以及项目依赖：

```bash
# 安装运行依赖
pip install -r requirements.txt

# 安装开发依赖（含 Ruff、mypy、pytest）
pip install -r requirements-dev.txt
```

`just check` 还依赖以下外部工具，请一并安装：

```bash
pip install ruff mypy pytest pytest-cov
# 或直接
pip install -r requirements-dev.txt
```

### 代码质量工具

本项目使用以下工具链保证代码质量，全部配置集中在 [pyproject.toml](pyproject.toml)：

| 工具 | 用途 | 配置文件 |
|------|------|---------|
| **Ruff** | Linter + Formatter（替代 flake8/isort/black） | `[tool.ruff]` |
| **mypy** | 静态类型检查 | `[tool.mypy]` |
| **pytest** | 单元测试框架 | `[tool.pytest.ini_options]` |

### 提交前检查

在提交代码前，请务必运行以下命令以确保代码质量达到准入标准：

```bash
# 一键全量检查（格式化 + Lint + 类型 + 测试）
just check

# 或分步执行：
just check-format   # 格式检查
just check-lint     # Lint 检查
just check-types    # 类型检查
just check-test     # 运行测试

# 自动修复
just fix            # 一键格式化 + 安全修复
```

### 运行测试

```bash
# 快速测试（增量模式，仅前 1 页）
just run-quick

# 完整运行
python scheduler.py --no-progress --mode incremental -p 1
```

### 扩展项目

新增站点处理器时，请在 `src/handlers/` 下新建 `pxx_xxx.py` 文件并在其中注册 `SITE_TYPES`，同时在 `domian.txt` 中添加对应白名单条目。

---

## 提交与 PR 规范 (Commit & PR Convention)

### 提交信息规范

提交信息应遵循你专属的 **`[Type](scope):` 规范**，并且描述部分建议使用**简短的祈使句 (imperative mood)** （例如 `[Fix](crawler): Fix page parsing for site type 16` 或 `[Add](handler): 新增机电学院站点处理器`）。

提交信息应严格遵循以下格式：

```text
[Type](scope): 描述信息
```

**Type 类型列表：**

| Type      | 用途                                                         |
| --------- | ------------------------------------------------------------ |
| `[Add]`   | 新增功能或还原了某个缺失的特性                               |
| `[Fix]`   | 修复 Bug，或修复因还原回退导致的问题                         |
| `[Ref]`   | 代码重构（不改变外部逻辑）、或代码层面的性能/内存优化        |
| `[Del]`   | 删除冗余代码或文件                                           |
| `[Doc]`   | 修改文档或清晰化注释（例如编写 README、本规范指南等）        |
| `[Chore]` | 日常杂项维护（如更新 pip 依赖、修改自动化构建流、配置项）    |
| `[Style]` | 代码风格调整（如格式化、Lint修复等不影响逻辑运行的改动）     |
| `[Test]`  | 增补或修改测试代码/用例                                      |
| `[Merge]` | 分支合并记录                                                 |

### Pull Request (PR) 规范

提交 PR 时，请在描述中务必包含以下关键信息：

1. **用户可见影响 (User-visible impact)**：清晰说明该修改对爬取行为、数据产出或白名单产生了什么影响。
2. **技术重构与取舍说明 (Architecture & Tradeoffs)**：如果是针对爬取逻辑、并发策略、解析器或站点类型注册的变动，请说明采用该方案的背景及背后的取舍逻辑。
3. **验证步骤 (Validation steps)**：列出如何通过命令行运行爬虫、检查产出 JSON 或对比数据来验证本次修改。
4. **测试日志/截图**：涉及到新的站点处理器、逻辑调整或性能改进时，请提供终端运行输出或日志片段以供审核。

---

## 🌿 分支模型与镜像标签策略

本项目采用 **Git Flow 分支模型** 并配合 **语义化版本标签**，通过 GitHub Actions 自动化构建和发布流程。

### 分支说明

| 分支类型  | 命名示例      | 说明                                                                                   |
| --------- | ------------- | -------------------------------------------------------------------------------------- |
| `master`  | `master`      | 默认分支，始终对应最新稳定版本。只允许合并，不接受直接提交。**仅此分支可打版本标签。** |
| `develop` | `develop`     | 主要开发集成分支，所有功能、重构、修复分支都从此切出，并通过 PR 合并回来。             |
| `feat/*`  | `feat/handler-x` | 新站点处理器开发分支，从 `develop` 切出，完成后合并回 `develop`。                    |
| `ref/*`   | `ref/crawler` | 代码重构分支，从 `develop` 切出，完成后合并回 `develop`。                              |
| `fix/*`   | `fix/parse-bug` | 普通 bug 修复分支（非紧急），从 `develop` 切出，完成后合并回 `develop`。            |
| `release/*`| `release/v0.1.0-Amiya` | 发版预备分支，从 `develop` 切出，确认无误并改好版本号合进 `master` 触发发版。          |
| `docs/*`  | `docs/api`    | 纯文档修改的分支。                                                                     |
| `chore/*` | `chore/deps`  | 架构杂务或包依赖维护的分支。                                                           |
| `test/*`  | `test/crawl`  | 专用于补充测试脚本的无底层代码改动分支。                                               |

### 版本标签与发布标签

**正式发布标签**：`v<major>.<minor>.<patch>-<Codename>`，例如 `v0.1.0-Amiya`。

**版本命名规定**：
项目采用语义化版本规范 (Semantic Versioning) 加 代号 (Codename) 的规则。
**代号变更规范**：只有主版本号（Major，即 `A.B.C` 中的 `A`）变更时才需要更换代号；主版本不变时，代号保持不变。

⚠️ **重要**：**只有 `master` 分支上的提交才能打版本标签**。其他分支（包括 `develop`）都禁止打标签。标签打错后无法直接删除远程标签，必须通过团队负责人处理。

### 🤖 GitHub Actions CI/CD 工作流

本仓库通过 GitHub Actions 每天定时运行爬虫并自动提交产出数据。

- **`crawl.yml`**：定时爬取流水线，支持 `incremental`（增量）和 `full`（全量）两种模式
- **`pr-branch-check.yml`**：PR 分支命名与标题规范校验

### 🚀 全流程实操示例

以下是基于本项目规范的标准开发与发布闭环。**强烈推荐使用原生 [GitHub Web 网页端](https://github.com/) 或 [GitHub CLI (`gh`)](https://cli.github.com/) 处理 Pull Request (PR) 审核和合并**，这比纯本地合并更透明、也更容易触发自动化流水线。

#### 1. 日常功能开发 (Feature / Bugfix)

**步骤 1：从 `develop` 签出新分支**
始终保持你的本地 `develop` 为最新，然后再切出开发分支。
```bash
git checkout develop
git pull origin develop
git checkout -b feat/new-handler
```

**步骤 2：原子化提交 (Atomic Commits)**
开发中提倡小步快跑，多次原子化提交，让复盘和回退更清晰。
```bash
# 新增站点处理器时：
git add scripts/handlers/
git commit -m "[Add](handler): Add handler for site type 99"

# 修复解析 bug 时：
git add scripts/parser.py
git commit -m "[Fix](parser): Fix date parsing for pagelist layout"

# 更新白名单时：
git add domian.txt scripts/whitelists/
git commit -m "[Chore](whitelist): Add new department entries"
```

**步骤 3：推送到远程并创建 PR**
将分支推送到远程仓库。
```bash
git push -u origin feat/new-handler
```
> 💡 **推荐操作**：
> 1. 推送结束后点击终端中提示的 GitHub 链接直接在网页端创建 PR；
> 2. 或者使用 GitHub CLI 快速创建：
> ```bash
> gh pr create --base develop --title "[Add](handler): New Site Handler" --body "详见前述 PR 规范说明（影响、取舍、验证步骤）"
> ```

**步骤 4：CI 自动化验证与合并**
- 提交 PR 后，GitHub Actions 会自动对该分支进行检查。
- 团队或自行审核通过后，**请直接使用 `gh pr merge` 或者 GitHub 网页端点击 `Squash and merge` / `Merge pull request` 将其合并进 `develop`**（使用网页或CLI操作可以追溯完整的 PR 记录和讨论，请避免本地直接 merge）。

---

#### 2. 版本发布准备 (Release)

当 `develop` 分支集成了所有预定该版本发版的功能后，即可准备打版发布。

**步骤 1：切出发版分支并更新版本号**
严禁直接合并 `develop`，而是切出一个 `release/*` 分支来进行回归调测和版本更新。
