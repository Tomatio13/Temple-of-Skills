#!/usr/bin/env python3
"""
出力先の設定を読み込む
"""

import json
import os
from pathlib import Path

DEFAULT_OUTPUT_DIR = Path("~/ai_daily")


def _config_path():
    return Path(__file__).resolve().parent.parent / "config.json"


def get_output_dir():
    env_dir = os.getenv("DAILY_REPORT_OUTPUT_DIR")
    if env_dir:
        return Path(env_dir)

    path = _config_path()
    if not path.exists():
        return DEFAULT_OUTPUT_DIR

    try:
        with open(path, "r") as f:
            data = json.load(f)
        value = data.get("output_dir")
        if value:
            return Path(value)
    except (OSError, json.JSONDecodeError):
        return DEFAULT_OUTPUT_DIR

    return DEFAULT_OUTPUT_DIR
