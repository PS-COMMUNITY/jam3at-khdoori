#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Download all x0.at files into repo structure as permanent backup."""
import json, subprocess, os, hashlib, sys

REPO = "/home/z/my-project/jam3at-khdoori"
PLAN = "/home/z/my-project/scripts/pc_transfer_plan.json"
DEST_ROOT = os.path.join(REPO, "السنة الاولى", "الفصل الاول")

tasks = json.load(open(PLAN))
bad = 0
for i, t in enumerate(tasks):
    dest = os.path.join(DEST_ROOT, t["pc_rel"].replace("\\", os.sep))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(dest) and os.path.getsize(dest) == t["size"]:
        print(f"[{i+1}/{len(tasks)}] SKIP {t['pc_rel'][:50]}")
        continue
    r = subprocess.run(["curl", "-s", "--max-time", "240", "-A", "curl/8.5.0",
                        "-o", dest, t["url"]], capture_output=True, text=True)
    size = os.path.getsize(dest) if os.path.exists(dest) else 0
    ok = size == t["size"]
    if not ok:
        bad += 1
    print(f"[{i+1}/{len(tasks)}] {'OK ' if ok else 'FAIL'} {size:>10,} {t['pc_rel'][:50]}")
    sys.stdout.flush()
print(f"\nDONE bad={bad}")
sys.exit(1 if bad else 0)
