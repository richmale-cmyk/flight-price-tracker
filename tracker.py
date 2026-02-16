#!/usr/bin/env python3
import os
import json
import sys
from datetime import datetime

# --- CONFIG ---
ROUTE = os.getenv("ROUTE", "SYD-DXB")
THRESHOLD_AUD = float(os.getenv("THRESHOLD_AUD", "1200"))
DATA_FILE = "state.json"

def load_state():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(DATA_FILE, "w") as f:
        json.dump(state, f, indent=2)

def fetch_price_aud(route: str) -> float:
    """
    TODO: Replace with real data source.
    For now, this is a placeholder so the pipeline runs.
    """
    # Example stub price:
    return 1500.0

def main():
    state = load_state()
    last_price = state.get("last_price_aud")

    price = fetch_price_aud(ROUTE)
    now = datetime.utcnow().isoformat() + "Z"

    state.update({"route": ROUTE, "last_checked_utc": now, "last_price_aud": price})
    save_state(state)

    print(f"[{now}] Route {ROUTE} price: AUD {price:.2f} (threshold {THRESHOLD_AUD:.2f})")

    # Simple “alert condition”
    if price <= THRESHOLD_AUD and (last_price is None or price < last_price):
        # In GitHub Actions, printing a special line lets us pass info to later steps
        print(f"ALERT: Price drop detected for {ROUTE}: AUD {price:.2f}")
        # Exit code 0 (success) — we’ll send notification via workflow step
        return 0

    return 0

if __name__ == "__main__":
    sys.exit(main())

