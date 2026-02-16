#!/usr/bin/env python3
"""
Flight Price Tracker (starter scaffold)

- Stores last observed price in state.json (so it can compare runs)
- Emits an "ALERT:" line when a price drop crosses the threshold
- Uses a placeholder fetch_price_aud() you can replace later
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Optional


DATA_FILE = "state.json"


def env_str(name: str, default: str) -> str:
    val = os.getenv(name)
    return val.strip() if val and val.strip() else default


def env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    try:
        return float(raw)
    except ValueError:
        raise ValueError(f"Invalid float for {name}: {raw!r}")


ROUTE = env_str("ROUTE", "SYD-DXB")
THRESHOLD_AUD = env_float("THRESHOLD_AUD", 1200.0)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_state() -> Dict[str, Any]:
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If the file somehow gets corrupted, don't crash the workflow
        return {}


def save_state(state: Dict[str, Any]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f_
