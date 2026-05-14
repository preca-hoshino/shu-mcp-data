# SHU MCP Data

上海大学新闻爬虫数据仓库 —— 定时爬取上海大学各院系/部门网站新闻，产出结构化 JSON 数据供 [shu-mcp](https://github.com/arts-amadeus/shu-mcp) 服务消费。

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 增量爬取（每天自动运行）
python scheduler.py --no-progress --mode incremental -p 1

# 全量爬取
python scheduler.py --no-progress --mode full

# 查看白名单
python scheduler.py --list
```

## 项目结构

```
scheduler.py         # 启动器（thin launcher）
src/                 # 业务源码
├── scheduler.py     # CLI 逻辑
├── crawler.py       # 爬取引擎
├── column.py        # 单栏目并发爬取
├── fetch.py         # 网络层
├── parser.py        # HTML 解析
├── writer.py        # JSON 输出
├── whitelist.py     # 白名单管理
├── config.py        # 全局配置
├── handlers/        # 39 种站点类型处理器
└── whitelists/      # 白名单 JSON 数据
output/              # 爬取结果
```

## 数据目录

爬取结果存放在 `output/` 目录，每个院系/部门对应一个 JSON 文件。

## 自动化

通过 GitHub Actions 每天定时增量爬取并自动提交更新。详见 `.github/workflows/crawl.yml`。
