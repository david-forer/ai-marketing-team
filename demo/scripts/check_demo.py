"""Check the demo: quotes must be verbatim, numbers must trace, punctuation rules must hold."""
import csv
import re
from pathlib import Path

from pptx import Presentation

ROOT = Path(__file__).resolve().parents[1]
fails = []

corpus = " ".join(p.read_text(encoding="utf-8") for p in (ROOT / "data" / "calls").glob("*.md"))
corpus += " " + (ROOT / "data" / "support-emails" / "support_emails.csv").read_text(encoding="utf-8").replace('""', '"')
corpus = re.sub(r"\s+", " ", corpus)

# Every research quote must be word for word in a source.
research = (ROOT / "brain" / "research.md").read_text(encoding="utf-8")
quotes = re.findall(r'^Q\d+\. "(.+?)" ', research, flags=re.M)
for q in quotes:
    if q not in corpus:
        fails.append(f"research quote not in source: {q}")

# Every quote-based idea must come from Research, and every win from Wins and flops.
ideas = list(csv.DictReader((ROOT / "outputs" / "03-weekly-ideas_2026-11-02.csv").open(encoding="utf-8")))
wins = (ROOT / "brain" / "wins-and-flops.md").read_text(encoding="utf-8")
for row in ideas:
    if row["source_type"] == "quote" and row["source"] not in quotes:
        fails.append(f"idea {row['id']} cites an unknown quote")
    if row["source_type"] == "win" and row["source"].split(", ", 1)[1].lower() not in wins.lower():
        fails.append(f"idea {row['id']} cites an unknown win")

# Ad headlines stay under 40 characters.
ads = list(csv.DictReader((ROOT / "outputs" / "05-ad-maker_canva-bulk-create_2026-11-03.csv").open(encoding="utf-8")))
for row in ads:
    if len(row["headline"]) >= 40:
        fails.append(f"headline too long: {row['headline']}")

# Outreach never mentions the visit and never exceeds 80 words.
outreach = (ROOT / "outputs" / "07-outreach-drafts_2026-11-04.md").read_text(encoding="utf-8")
for body in re.findall(r"Hi \w+,\n\n(.+?)\n\nFenwick Row Bookkeeping", outreach, flags=re.S):
    if len(body.split()) > 80:
        fails.append(f"outreach too long: {body[:40]}")
    if re.search(r"visit|pricing page|our site|website", body, flags=re.I):
        fails.append(f"outreach mentions the visit: {body[:40]}")

# Punctuation rules across all written content.
texts = {}
for folder in ("brain", "agents", "outputs", "data"):
    for path in (ROOT / folder).rglob("*"):
        if path.suffix in (".md", ".csv"):
            texts[path] = path.read_text(encoding="utf-8")
texts[ROOT / "README.md"] = (ROOT / "README.md").read_text(encoding="utf-8")
page = (ROOT / "index.html").read_text(encoding="utf-8")
page = re.sub(r"<style>.*?</style>", "", page, flags=re.S)
texts[ROOT / "index.html"] = re.sub(r"<!doctype html>|<[^>]+>", " ", page, flags=re.I)
upload = (ROOT / "scripts" / "upload.html").read_text(encoding="utf-8")
upload = re.sub(r"<(style|script)>.*?</\1>", "", upload, flags=re.S)
texts[ROOT / "scripts" / "upload.html"] = re.sub(r"<!doctype html>|<[^>]+>", " ", upload, flags=re.I)
decks = list((ROOT / "outputs").glob("*.pptx"))
for path in decks:
    words = [s.text_frame.text for slide in Presentation(path).slides for s in slide.shapes if s.has_text_frame]
    texts[path] = "\n".join(words)
    if len(words) and not all(any("Fictional" in s.text_frame.text for s in slide.shapes) for slide in Presentation(path).slides):
        fails.append(f"slide missing demo label: {path.name}")
for path, text in texts.items():
    for mark in ("—", ";", "!"):
        if mark in text:
            fails.append(f"{path.relative_to(ROOT)} contains {mark!r}")

print(f"{len(quotes)} quotes, {len(ideas)} ideas, {len(ads)} ads, {len(decks)} decks checked")
print("\n".join(fails) if fails else "ALL CHECKS PASSED")
