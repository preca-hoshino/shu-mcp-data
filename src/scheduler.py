"""
shu-mcp 调度逻辑
———— 爬取白名单全部站点文章（由根目录 scheduler.py 启动）

用法:
    python scheduler.py                          # 增量爬取，每栏目前 1 页（默认）
    python scheduler.py --mode full               # 全量爬取，不限页数
    python scheduler.py --mode incremental -p 3   # 增量爬取，每栏目前 3 页
    python scheduler.py -c 5                      # 指定并发数
    python scheduler.py --progress                # 启用 ANSI 进度条（TTY 中默认开启）
    python scheduler.py --no-progress             # 关闭进度条（GitHub Actions 推荐）
    python scheduler.py --list                    # 查看白名单
    python scheduler.py --types                   # 查看已知站点类型

GitHub Actions 示例:
    python scheduler.py --no-progress --mode incremental -p 1
"""

import sys

from handlers import (
    DEFAULT_WORKERS,
    SITE_TYPES,
    ProgressDisplay,
    crawl_all_whitelist,
    show_whitelist,
)


def parse_args(argv: list[str]) -> dict:  # noqa: C901
    """简易参数解析 → {workers, progress, list, types, mode, max_pages}"""
    opts = {
        "workers": DEFAULT_WORKERS,
        "progress": sys.stdout.isatty(),  # 默认：TTY 下开，管道关
        "list": False,
        "types": False,
        "mode": "incremental",
        "max_pages": 0,  # 0 = 使用模式默认值
    }

    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "-c" and i + 1 < len(argv):
            try:
                opts["workers"] = int(argv[i + 1])
            except ValueError:
                print(f"[ERROR] -c 需要数字参数，得到: {argv[i + 1]}")
                sys.exit(1)
            i += 2
        elif a == "--mode" and i + 1 < len(argv):
            m = argv[i + 1].lower()
            if m not in ("incremental", "full"):
                print(f"[ERROR] --mode 需要 incremental 或 full，得到: {argv[i + 1]}")
                sys.exit(1)
            opts["mode"] = m
            i += 2
        elif a in ("-p", "--max-pages") and i + 1 < len(argv):
            try:
                opts["max_pages"] = int(argv[i + 1])
            except ValueError:
                print(f"[ERROR] {a} 需要数字参数，得到: {argv[i + 1]}")
                sys.exit(1)
            i += 2
        elif a == "--progress":
            opts["progress"] = True
            i += 1
        elif a == "--no-progress":
            opts["progress"] = False
            i += 1
        elif a == "--list":
            opts["list"] = True
            i += 1
        elif a == "--types":
            opts["types"] = True
            i += 1
        else:
            print(f"[ERROR] 未知参数: {a}")
            print_usage()
            sys.exit(1)

    return opts


def print_usage() -> None:
    """打印用法帮助信息。"""
    print("用法:")
    print("  python scheduler.py                          # 增量爬取，每栏目前 1 页")
    print("  python scheduler.py --mode full               # 全量爬取，不限页数")
    print("  python scheduler.py --mode incremental -p 3   # 增量，每栏目前 3 页")
    print("  python scheduler.py -c 5                      # 指定并发数")
    print("  python scheduler.py --progress                # 启用 ANSI 进度条")
    print("  python scheduler.py --no-progress             # 关闭进度条（CI 推荐）")
    print("  python scheduler.py --list                    # 查看白名单")
    print("  python scheduler.py --types                   # 查看站点类型")
    print(f"\n已知类型: {', '.join(SITE_TYPES.keys())}")
    print(f"默认并发: {DEFAULT_WORKERS}")


def cmd_list() -> None:
    """列出白名单。"""
    show_whitelist()


def cmd_types() -> None:
    """列出已知站点类型。"""
    print(f"\n{'=' * 60}")
    print(f"📦 已知站点类型 ({len(SITE_TYPES)})")
    print(f"{'=' * 60}")
    for name, cfg in SITE_TYPES.items():
        print(f"  🔧 {name}: {cfg['name']}")
        print(f"     list_selector:       {cfg['list_selector']}")
        print(f"     pagination_selector: {cfg['pagination_selector']}")
        print(f"     next_page_texts:     {cfg.get('next_page_texts', [])}")
    print(f"{'=' * 60}\n")


def main() -> None:
    """主入口。"""
    argv = sys.argv[1:]

    # 解析参数（无参数时使用默认值：TTY → 进度条，管道 → 文本）
    opts = parse_args(argv)

    if opts["list"]:
        cmd_list()
        return

    if opts["types"]:
        cmd_types()
        return

    # 主流程：并发爬取
    #  进度条模式 → 静默 fetch 日志，避免破坏 ANSI 显示
    #  无进度条模式 → 打印列级进度 + fetch 错误信息
    use_progress = opts["progress"]
    progress = ProgressDisplay(enabled=use_progress) if use_progress else None
    # 根据模式决定默认 max_pages
    max_pages = opts["max_pages"]
    if max_pages == 0:
        max_pages = 1 if opts["mode"] == "incremental" else 0

    crawl_all_whitelist(
        workers=opts["workers"],
        progress=progress,
        verbose=not use_progress,
        mode=opts["mode"],
        max_pages=max_pages,
    )
