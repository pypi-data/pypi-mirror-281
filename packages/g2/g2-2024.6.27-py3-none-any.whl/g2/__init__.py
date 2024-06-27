# -*- coding: utf-8 -*-
#
# pyG2
#
# @Author: Lin, Max
# @Email : jason.max.lin@outlook.com
# @Time  : 2024/6/23 16:42
#
# =============================================================================
"""g2"""
from importlib import metadata
from datetime import datetime


def _get_version():
    try:
        # 安装完成后，获取安装的version
        version = metadata.version("g2")
    except metadata.PackageNotFoundError:
        # 发布或者开发时，当前日期作为发布版本
        now = datetime.now()
        version = f"{now.year}.{now.month}.{now.day}"
    return version


__version__ = _get_version()
