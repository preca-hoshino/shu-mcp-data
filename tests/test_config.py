"""config 模块测试"""

from pathlib import Path

from config import (
    DEFAULT_WORKERS,
    MAX_RETRIES,
    OUTPUT_DIR,
    REQUEST_TIMEOUT,
    ROOT_DIR,
    SITE_TYPES,
)


def test_default_workers_is_positive() -> None:
    """验证默认并发数为正整数值。"""
    assert DEFAULT_WORKERS > 0


def test_max_retries_is_positive() -> None:
    """验证最大重试次数为正整数值。"""
    assert MAX_RETRIES > 0


def test_request_timeout_is_positive() -> None:
    """验证请求超时为正整数值。"""
    assert REQUEST_TIMEOUT > 0


def test_site_types_is_dict() -> None:
    """验证 SITE_TYPES 为字典类型。"""
    assert isinstance(SITE_TYPES, dict)


def test_root_dir_exists() -> None:
    """验证项目根目录存在。"""
    assert Path(ROOT_DIR).is_dir()


def test_output_dir_exists() -> None:
    """验证输出目录存在。"""
    assert Path(OUTPUT_DIR).is_dir()
