#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Push files from x0.at temp-host URLs to user's PC via AlMoutmag file_upload.
- placeholder via code_write_file creates parent dirs (dl1, no confirmation)
- file_upload (dl1) downloads URL -> dest_path
- verification via file_list size check; resume via results log
"""
import json, time, sys, urllib.request, ssl, os

PLAN = "/home/z/my-project/scripts/pc_transfer_plan.json"
LOG = "/home/z/my-project/scripts/pc_transfer_results.json"
BASE = os.environ.get("PC_BASE", r"C:\")  # مسار جهاز الطالب — من متغير البيئة PC_BASE (القيمة في الخزنة)

TUNNELS = [
    "https://mom-obtained-beaver-samuel.trycloudflare.com",
    "https://vitamin-defeat-advertising-establish.trycloudflare.com",
]
CTX = ssl.create_default_context()
_state = {"t": 0}
_rid = [200]

def call(tool, args, timeout=600):
    for _ in range(2):
        t = TUNNELS[_state["t"]]
        _rid[0] += 1
        payload = json.dumps({"jsonrpc": "2.0", "id": _rid[0], "method": "tools/call",
                              "params": {"name": tool, "arguments": args}}).encode()
        req = urllib.request.Request(t + "/mcp", data=payload, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + os.environ.get("ALMOUTMAG_TOKEN", "")})  # التوكن من متغير البيئة (القيمة في الخزنة)
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
                body = json.loads(r.read().decode())
            if "result" in body:
                txt = body["result"]["content"][0]["text"]
                try:
                    return json.loads(txt)
                except Exception:
                    return {"raw": txt[:500]}
            err = body.get("error", {}).get("message", "?")
            if "confirmation" in err or "danger_level" in err or "deny" in err:
                return {"error": err[:150]}
            _state["t"] ^= 1
        except Exception as e:
            print(f"  net err ({t.split('//')[1][:24]}): {str(e)[:70]} -> switch")
            _state["t"] ^= 1
    return {"error": "both_tunnels_failed"}

def load_results():
    if os.path.exists(LOG):
        try:
            return json.load(open(LOG))
        except Exception:
            return {}
    return {}

def main():
    tasks = json.load(open(PLAN))
    done_map = load_results()
    n = len(tasks)
    bad = 0
    for i, t in enumerate(tasks):
        if done_map.get(t["pc_rel"], {}).get("actual") == t["size"]:
            print(f"[{i+1}/{n}] SKIP {t['pc_rel'][:55]}")
            continue
        dest = BASE + "\\" + t["pc_rel"]
        print(f"[{i+1}/{n}] {t['pc_rel'][:55]} ({t['size']:,} B)")
        ph = call("code_write_file", {"path": dest, "content": "ph", "create_backup": False})
        if ph.get("error"):
            print(f"  placeholder ERR: {ph['error'][:90]}")
        fu = call("file_upload", {"source_url": t["url"], "dest_path": dest,
                                  "overwrite": True, "timeout_seconds": 600})
        status = "ok" if not fu.get("error") else "ERR:" + str(fu.get("error"))[:90]
        actual = None
        parent = dest.rsplit("\\", 1)[0]
        name = dest.rsplit("\\", 1)[1]
        fl = call("file_list", {"path": parent})
        for f in (fl.get("files") or []):
            if f.get("name") == name:
                actual = f.get("size_bytes")
        ok = (actual == t["size"])
        if not ok:
            bad += 1
        print(f"  -> {status} size={actual}/{t['size']} {'OK' if ok else 'MISMATCH'}")
        done_map[t["pc_rel"]] = {"url": t["url"], "status": status,
                                 "expected": t["size"], "actual": actual}
        json.dump(done_map, open(LOG, "w"), ensure_ascii=False, indent=1)
        time.sleep(1)
    print(f"\nDONE bad={bad}")
    if bad:
        sys.exit(1)

if __name__ == "__main__":
    main()
