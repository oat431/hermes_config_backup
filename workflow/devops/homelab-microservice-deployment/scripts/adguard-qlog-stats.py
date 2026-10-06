#!/usr/bin/env python3
"""AdGuard Home query-log stats — who queried, who got blocked.

AdGuard's querylog.json entries are CONCATENATED JSON objects (not an array,
not JSONL). Take a tail sample of the log first, then run this against it:

  docker exec adguard sh -c "tail -c 3000000 /opt/adguardhome/work/data/querylog.json" > /tmp/qlog.json
  python3 adguard-qlog-stats.py [/tmp/qlog.json]
"""
import json
import sys
from collections import Counter

path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/qlog.json"
data = open(path, "rb").read().decode("utf-8", errors="replace")

# Entries start with {"T": — split on that marker and JSON-decode each chunk.
marker = "{" + '"T":'
starts = []
pos = 0
while True:
    i = data.find(marker, pos)
    if i == -1:
        break
    starts.append(i)
    pos = i + 1

entries = []
for i, s in enumerate(starts):
    e = starts[i + 1] if i + 1 < len(starts) else len(data)
    chunk = data[s:e].rstrip(",\n\r ")
    try:
        entries.append(json.loads(chunk))
    except Exception:
        pass

if not entries:
    print("no parseable entries — is this really a querylog sample?")
    sys.exit(1)

print(f"parsed {len(entries)} entries | {entries[0].get('T', '?')} -> {entries[-1].get('T', '?')}")

per = {}
blocked_domains = Counter()
queried_domains = Counter()
for en in entries:
    ip = str(en.get("IP", "?"))
    res = en.get("Result")
    blocked = isinstance(res, dict) and bool(res.get("IsFiltered"))
    t, b = per.get(ip, (0, 0))
    per[ip] = (t + 1, b + (1 if blocked else 0))
    qh = en.get("QH", "?")
    queried_domains[qh] += 1
    if blocked:
        blocked_domains[qh] += 1

print("\nCLIENT            TOTAL  BLOCKED     %")
for ip, (t, b) in sorted(per.items(), key=lambda x: -x[1][0]):
    print(f"{ip:16} {t:7} {b:8} {100.0 * b / t:6.1f}%")

print("\nTOP BLOCKED :", ", ".join(d for d, _ in blocked_domains.most_common(12)) or "(none)")
print("TOP QUERIED :", ", ".join(d for d, _ in queried_domains.most_common(12)))
