"""
shu-mcp 调度入口（启动器）
———— 将 src/ 加入 Python 路径后委托给 src/scheduler.main()
"""

from pathlib import Path
import sys

# 将 src/ 加入 Python 路径，使内部模块可正常导入
_src = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(_src))

# 修复 Windows GBK 编码下 emoji 输出问题
sys.stdout.reconfigure(encoding="utf-8")

from scheduler import main

if __name__ == "__main__":
    main()
