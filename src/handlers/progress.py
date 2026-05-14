"""
进度显示模块（rich 版）
———— 顶部总进度行 + 每部门一行进度条

API:
    set_total(page_count, dept_count)   →  初始化总进度行
    register(dept, page_est)            →  注册一个部门行
    step_dept(dept, n_pages)            →  某部门完成 n 页
    finish_dept(dept)                   →  某部门完成（行消失）
    close()                             →  停止
"""

import sys
import threading
from typing import Self

from rich.progress import (
    BarColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
)
from rich.text import Text


class ProgressDisplay:
    """顶部总进度行 + 每部门一行进度条"""

    def __init__(self, enabled: bool = True) -> None:
        """初始化进度显示器。

        Args:
            enabled: 是否启用进度条。TTY 关闭时自动禁用。
        """
        self._enabled = enabled and sys.stdout.isatty()
        self._lock = threading.Lock()
        self._rich: Progress | None = None
        self._total_task_id: TaskID | None = None
        self._total_pages = 0
        self._total_depts = 0
        self._done_depts = 0
        self._dept_tasks: dict[str, TaskID] = {}
        self._dept_done: dict[str, int] = {}
        self._dept_total: dict[str, int] = {}

        if self._enabled:
            self._rich = Progress(
                TextColumn("{task.description}", justify="left"),
                BarColumn(bar_width=30, complete_style="green", finished_style="green"),
                TextColumn("{task.completed}/{task.total}", justify="right"),
                TextColumn("\u2022"),
                TimeElapsedColumn(),
                transient=True,
            )
            self._rich.start()

    # ------------------------------------------------------------------
    # 公共 API
    # ------------------------------------------------------------------

    def set_total(self, page_count: int, dept_count: int) -> None:
        """启动总进度行（置顶常驻）。"""
        if not self._enabled:
            return
        with self._lock:
            self._total_pages = max(page_count, 1)
            self._total_depts = dept_count
            desc = self._build_total_desc()
            self._total_task_id = self._rich.add_task(
                desc,
                total=self._total_pages,
                visible=True,
            )

    def register(self, dept: str, page_est: int) -> None:
        """注册一个部门进度行。"""
        if not self._enabled:
            return
        with self._lock:
            if dept in self._dept_tasks:
                return
            self._dept_done[dept] = 0
            self._dept_total[dept] = max(page_est, 1)
            desc = Text(f"  {dept}", style="bold cyan")
            task_id = self._rich.add_task(desc, total=max(page_est, 1))
            self._dept_tasks[dept] = task_id

    def step_dept(self, dept: str, n_pages: int = 1) -> None:
        """某部门完成 n 页，更新其进度条 + 总进度。"""
        if not self._enabled:
            return
        with self._lock:
            if dept not in self._dept_tasks:
                return
            self._dept_done[dept] = self._dept_done.get(dept, 0) + n_pages
            done = self._dept_done[dept]
            total = self._dept_total[dept]
            if done > total:
                self._dept_total[dept] = done
                total = done
            desc = Text(f"  {dept}", style="bold cyan")
            self._rich.update(self._dept_tasks[dept], description=desc, completed=done, total=total)
            self._update_total()

    def finish_dept(self, dept: str) -> None:
        """某部门完成 → 行消失，总进度更新。"""
        if not self._enabled:
            return
        with self._lock:
            task_id = self._dept_tasks.pop(dept, None)
            if task_id is None:
                return
            self._dept_done[dept] = self._dept_total.get(dept, self._dept_done.get(dept, 0))
            self._done_depts += 1
            self._update_total()
            self._rich.remove_task(task_id)

    def close(self) -> None:
        """关闭进度显示器（幂等，可安全重复调用）。"""
        if self._rich is not None:
            try:
                self._rich.stop()
            except (RuntimeError, OSError):
                pass
            finally:
                self._rich = None

    # ------------------------------------------------------------------
    # 内部
    # ------------------------------------------------------------------

    def _build_total_desc(self) -> Text:
        return Text.assemble(
            ("══ 总进度 ══", "bold yellow"),
            (f"  {self._done_depts}/{self._total_depts}学院", "bold cyan"),
        )

    def _update_total(self) -> None:
        """刷新总进度行。"""
        if self._total_task_id is None:
            return
        done_pages = sum(self._dept_done.values())
        self._rich.update(
            self._total_task_id,
            description=self._build_total_desc(),
            completed=min(done_pages, self._total_pages),
            total=max(self._total_pages, 1),
        )

    # ------------------------------------------------------------------
    # 上下文管理器
    # ------------------------------------------------------------------

    def __enter__(self) -> Self:
        """进入上下文管理器。"""
        return self

    def __exit__(self, *args: object) -> None:
        """退出上下文管理器，关闭进度显示。"""
        self.close()

    def __del__(self) -> None:
        """析构安全网：确保 rich 后台线程被停止。"""
        self.close()
