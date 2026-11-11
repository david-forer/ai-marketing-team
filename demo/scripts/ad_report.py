"""Compute ad numbers for the morning report, so the agent never does the math itself."""
import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

rows = list(csv.DictReader((ROOT / "data" / "ads" / "ads_daily.csv").open(encoding="utf-8")))
days = sorted({r["date"] for r in rows})
report_day = sys.argv[1] if len(sys.argv) > 1 else days[-1]
if report_day not in days:
    sys.exit(f"No ad data for {report_day}. Latest date in the file is {days[-1]}.")
position = days.index(report_day)
last7 = set(days[max(0, position - 6): position + 1])


def add(bucket, r):
    bucket["spend"] += float(r["spend_usd"])
    bucket["signups"] += int(r["signups"])
    bucket["clicks"] += int(r["clicks"])


stats = defaultdict(lambda: {"y": defaultdict(float), "w": defaultdict(float), "all": defaultdict(float), "platform": "", "headline": ""})
for r in rows:
    if r["date"] > report_day:
        continue
    s = stats[r["ad_id"]]
    s["platform"], s["headline"] = r["platform"], r["headline"]
    add(s["all"], r)
    if r["date"] == report_day:
        add(s["y"], r)
    if r["date"] in last7:
        add(s["w"], r)

print("ad_id,platform,headline,yesterday_spend,yesterday_signups,7d_spend,7d_signups,7d_cost_per_signup,total_spend,total_signups")
for ad_id, s in sorted(stats.items(), key=lambda kv: -kv[1]["w"]["signups"]):
    w = s["w"]
    cps = f"{w['spend'] / w['signups']:.0f}" if w["signups"] else "none"
    print(f"{ad_id},{s['platform']},{s['headline']},{s['y']['spend']:.2f},{s['y']['signups']:.0f},{w['spend']:.2f},{w['signups']:.0f},{cps},{s['all']['spend']:.2f},{s['all']['signups']:.0f}")
