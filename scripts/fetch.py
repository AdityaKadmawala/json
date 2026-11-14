#!/usr/bin/env python3
"""Polite fetch helper: saves raw responses under raw/<subdir>/ with 1s+ delay.
usage: fetch.py SUBDIR NAME URL"""
import sys, time, os, hashlib, requests
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
S = requests.Session(); S.headers.update({"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "raw")
_last = [0.0]
def get(url, subdir=None, name=None, delay=1.2, **kw):
    w = _last[0] + delay - time.time()
    if w > 0: time.sleep(w)
    try:
        r = S.get(url, timeout=kw.pop("timeout", 40), **kw)
    except Exception as e:
        _last[0] = time.time(); return None, str(e)
    _last[0] = time.time()
    if subdir and name and r.status_code == 200 and len(r.content) < 50_000_000:
        d = os.path.join(ROOT, subdir); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, name), "wb").write(r.content)
    return r, r.status_code
if __name__ == "__main__":
    r, st = get(sys.argv[3], sys.argv[1], sys.argv[2]); print(st, len(r.content) if r is not None else 0)
