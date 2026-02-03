#!/usr/bin/env python3
"""
Minimal Stage-1 demo entrypoint.

Goal:
- Read a CSV exported from .ulg (or any CSV)
- Print basic column stats and check required fields exist

This is intentionally lightweight so it can run on any machine.
"""

import argparse
import csv
import os
import sys
from typing import List


REQUIRED_COLUMNS = [
    "timestamp_us",
    "acc_x", "acc_y", "acc_z",
    "gyro_x", "gyro_y", "gyro_z",
    # Example motor columns (rename later if your CSV uses different names)
    "motor_1", "motor_2", "motor_3", "motor_4", "motor_5", "motor_6",
]


def read_header(csv_path: str) -> List[str]:
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, [])
    return header


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to exported flight log CSV")
    args = parser.parse_args()

    csv_path = args.csv
    if not os.path.isfile(csv_path):
        print(f"[ERROR] CSV not found: {csv_path}")
        return 2

    header = read_header(csv_path)
    if not header:
        print("[ERROR] Empty CSV or missing header row.")
        return 3

    missing = [c for c in REQUIRED_COLUMNS if c not in header]
    print(f"[INFO] Columns: {len(header)}")
    print(f"[INFO] First 10 columns: {header[:10]}")

    if missing:
        print("[WARN] Missing required columns (OK for now; rename in REQUIRED_COLUMNS later):")
        for c in missing:
            print(f"  - {c}")
        print("[NEXT] Update REQUIRED_COLUMNS to match your actual CSV field names.")
    else:
        print("[OK] All required columns present.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
