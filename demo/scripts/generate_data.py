"""Generate the simulated ad data and competitor snapshots for the demo."""
import csv
import datetime as dt
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
random.seed(1106)

# platform, ad id, headline, daily spend, click rate, cost per click, click to signup rate, first day live
ADS = [
    ("Google", "G-01", "Bookkeeping for HVAC Contractors", 95, 0.062, 7.40, 0.055, 0),
    ("Google", "G-02", "ServiceTitan QuickBooks Reconciliation", 60, 0.071, 5.90, 0.070, 0),
    ("Google", "G-03", "Outsourced Bookkeeping Services", 70, 0.034, 8.80, 0.006, 0),
    ("LinkedIn", "L-01", "Your CPA Is a Rearview Mirror", 85, 0.009, 9.10, 0.050, 0),
    ("LinkedIn", "L-02", "Accounting Solutions for Growing Businesses", 75, 0.004, 11.20, 0.000, 0),
    ("LinkedIn", "L-03", "I Find Out I Lost Money Six Weeks Later", 80, 0.013, 8.20, 0.085, 21),
    ("Meta", "M-01", "Tax Tips Every Contractor Should Know", 45, 0.016, 1.60, 0.000, 0),
    ("Meta", "M-02", "Know Your Profit by Job", 50, 0.014, 2.10, 0.012, 0),
]
START = dt.date(2026, 10, 8)
DAYS = 28


def write_ads():
    path = ROOT / "data" / "ads" / "ads_daily.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", "platform", "ad_id", "headline", "impressions", "clicks", "spend_usd", "signups"])
        for i in range(DAYS):
            day = START + dt.timedelta(days=i)
            weekend = 0.55 if day.weekday() >= 5 else 1.0
            for platform, ad_id, headline, spend, ctr, cpc, cvr, first in ADS:
                if i < first:
                    continue
                cost = spend * weekend * random.uniform(0.85, 1.15)
                clicks = max(1, round(cost / (cpc * random.uniform(0.9, 1.1))))
                impressions = round(clicks / (ctr * random.uniform(0.9, 1.1)))
                signups = sum(random.random() < cvr for _ in range(clicks))
                w.writerow([day.isoformat(), platform, ad_id, headline, impressions, clicks, f"{cost:.2f}", signups])


BASE = {
    "tradesbooks-direct": """# Tradesbooks Direct, pricing page snapshot

Fictional competitor. Simulated page text.

Bookkeeping built for contractors.
Plans start at $1,150 per month.
Monthly close by day 15.
Works with QuickBooks Online.
Dedicated support inbox.
Trusted by 900 contractors.
""",
    "clearclose-ai": """# ClearClose AI, pricing page snapshot

Fictional competitor. Simulated page text.

Close your books in 3 days with AI.
Plans start at $899 per month.
Human review on every close.
Works with QuickBooks Online and Xero.
Cancel any time.
""",
    "ledger-and-level": """# Ledger and Level, contractor practice snapshot

Fictional competitor. Simulated page text.

Tax and advisory for contractors.
Quarterly reviews from $3,000 per month.
Tax planning included.
Serving Ohio, Indiana and Kentucky since 1998.
""",
}

CHANGES = {
    "tradesbooks-direct": [
        ("Plans start at $1,150 per month.", "Plans start at $995 per month for the first 6 months."),
        ("Dedicated support inbox.", "Dedicated support inbox.\nNew: ServiceTitan sync, now in beta."),
    ],
    "clearclose-ai": [
        ("Close your books in 3 days with AI.", "AI job costing for the trades. Close your books in 3 days."),
    ],
    "ledger-and-level": [],
}


def write_competitors():
    for stamp, changed in (("2026-10-23", False), ("2026-10-30", True)):
        folder = ROOT / "data" / "competitors" / stamp
        folder.mkdir(parents=True, exist_ok=True)
        for name, text in BASE.items():
            if changed:
                for old, new in CHANGES[name]:
                    text = text.replace(old, new)
            (folder / f"{name}.md").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    write_ads()
    write_competitors()
    print("done")
