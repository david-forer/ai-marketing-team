"""Build the sales deck the Agent 6 instructions call for."""
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
company = sys.argv[1] if len(sys.argv) > 1 else "Redbird Electric"

INK = RGBColor(0x1F, 0x2A, 0x37)
ACCENT = RGBColor(0xB4, 0x53, 0x09)
MUTED = RGBColor(0x6B, 0x72, 0x80)

SLIDES = [
    ("What we hear from electrical contractors", [
        "You can see what you billed. It is harder to see what you kept.",
        "Service work and new construction get blended into one number.",
        "Job numbers take weeks to pull when a bank asks for them.",
    ]),
    ("What is usually going on underneath", [
        "Field software and QuickBooks disagree.",
        "Materials get booked to the wrong job.",
        "Callbacks vanish into payroll.",
    ]),
    ("From a customer in your trade", [
        "“So my margin was fine and my process was not.”",
        "Electrical contractor client, after a job showed a loss because materials were booked to the wrong job",
    ]),
    ("Proof", [
        "Median close moved from day 31 to day 8 across 61 clients.",
        "96 percent of clients stayed through the last 12 months.",
        "One HVAC client found $84,000 a year in underpriced maintenance agreements in the first quarter.",
    ]),
    ("Plans", [
        "Core Books, $1,400 per month: close by day 10 and reconciliation",
        "Job Cost, $2,600 per month: adds profit by job, technician and service line",
        "Fractional Controller, $5,200 per month: adds monthly review, cash forecast and pricing support",
    ]),
    ("Next step", [
        "A free 30 minute Job Cost Check.",
        "You bring one month of numbers. We show you where the two systems split.",
    ]),
]


def add_text(slide, text, left, top, width, height, size, color, bold=False):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    frame = box.text_frame
    frame.word_wrap = True
    frame.text = text
    run = frame.paragraphs[0].runs[0]
    run.font.size, run.font.color.rgb, run.font.bold = Pt(size), color, bold
    return frame


def footer(slide):
    add_text(slide, "Demo. Fictional company and data.", 0.6, 6.85, 8, 0.4, 11, MUTED)


deck = Presentation()
deck.slide_width, deck.slide_height = Inches(13.333), Inches(7.5)
blank = deck.slide_layouts[6]

first = deck.slides.add_slide(blank)
add_text(first, f"Knowing what {company} keeps", 0.6, 2.4, 12, 1.2, 44, INK, True)
add_text(first, "Fenwick Row Bookkeeping", 0.6, 3.8, 12, 0.6, 22, ACCENT)
footer(first)

for title, lines in SLIDES:
    slide = deck.slides.add_slide(blank)
    add_text(slide, title, 0.6, 0.6, 12, 1, 34, INK, True)
    top = 2.0
    for line in lines:
        frame = add_text(slide, line, 0.6, top, 12, 1.1, 24, INK)
        top += 1.3
    footer(slide)

out = ROOT / "outputs" / f"06-sales-deck_{company.lower().replace(' ', '-')}_2026-11-05.pptx"
deck.save(out)
print(out)
