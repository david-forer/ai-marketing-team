"""Build one client's setup folder from the kit: docs, agents and a tracker workbook."""
import argparse
import datetime as dt
import json
import re
import shutil
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

KIT = Path(__file__).resolve().parents[1] / "kit"

AGENTS = {
    1: ("Customer research", 1, []),
    2: ("Competitor research", 1, []),
    3: ("Weekly ideas", 2, [1]),
    4: ("Channel writer", 2, [3]),
    5: ("Ad maker", 2, [4]),
    6: ("Sales deck", 2, []),
    7: ("Outreach", 3, []),
    8: ("Morning report", 1, []),
}
TIERS = {
    "Install: Core": ("$7,500", "3 to 4 weeks", "50 percent upfront, 50 percent on delivery."),
    "Install: Extended": ("$11,000", "6 to 8 weeks", "50 percent upfront, 50 percent on delivery."),
    "Install: Full": ("$15,000", "8 to 12 weeks", "Two payments of $7,500, one at start and one at month two."),
}
STATUS = ["Not started", "In progress", "Blocked", "Done", "Not needed"]


def tier_for(count):
    if count <= 2:
        return "Install: Core"
    return "Install: Extended" if count <= 6 else "Install: Full"


def render(text, values):
    return re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: str(values.get(m.group(1), m.group(0))), text)


def copy_tree(kit_folder, out_folder, values, names=None):
    out_folder.mkdir(parents=True)
    for path in sorted(kit_folder.glob("*.md")):
        if names is None or path.name in names:
            (out_folder / path.name).write_text(render(path.read_text(encoding="utf-8"), values), encoding="utf-8")


def add_sheet(book, title, headers, rows):
    sheet = book.create_sheet(title)
    sheet.append(headers)
    for row in rows:
        sheet.append(row)
    for cell in sheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1F2A37")
    for column in sheet.columns:
        longest = max(len(str(c.value or "")) for c in column)
        sheet.column_dimensions[column[0].column_letter].width = min(max(12, longest + 2), 60)
    for row in sheet.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    sheet.freeze_panes = "A2"
    status_col = headers.index("Status") + 1
    letter = sheet.cell(1, status_col).column_letter
    check = DataValidation(type="list", formula1='"' + ",".join(STATUS) + '"', allow_blank=True)
    sheet.add_data_validation(check)
    check.add(f"{letter}2:{letter}{sheet.max_row}")
    for row in range(2, sheet.max_row + 1):
        if not sheet.cell(row, status_col).value:
            sheet.cell(row, status_col, "Not started")


def build_tracker(path, values, chosen):
    book = Workbook()
    book.remove(book.active)
    founder, operator = values["FOUNDER"], values["OPERATOR"]
    owner = "Claude organization Owner at the client"

    add_sheet(book, "Access", ["Step", "Who does it", "Check", "Status", "Date", "Notes"], [
        ["Buy a Claude Team plan on the company's card", founder, "2 seats minimum. Confirm price and terms on the day", None, None, None],
        ["Give the consultant a paid seat for the build", owner, "Guest access is unconfirmed, so plan on a temporary member seat", None, None, None],
        ["Create the Brain folder", operator, f"Owned by the company at {values['BRAIN_LOCATION']}, with Research, Snapshots and Ad Results folders inside", None, None, None],
        ["Limit each agent's tools and connectors", "Consultant", "Attach only what it needs. Exclude trash, share and update tools", None, None, None],
        ["Connect Exa for reading competitor sites", "Client account holder", "Direct access failed on all 6 test pages in a cloud run. Exa loaded all 6. Client needs their own Exa account", None, None, None],
        ["Enable connectors for the organization", owner, "Organization settings, Connectors", None, None, None],
        ["Sign in to each connector", "Each person with their own account", "Nobody uses the consultant's logins", None, None, None],
        ["Approve the app in Google Workspace or Microsoft 365", "Their IT admin", "Only if sign-in gets blocked", None, None, None],
        ["Share each project with the operator", operator, "Can edit for the operator, Can view for the founder", None, None, None],
        ["Test one schedule with the laptop closed", "Consultant", "Do this before promising any schedule", None, None, None],
        ["Test whether scheduled runs stop for approval", "Consultant", "Passed for Drive on a cloud routine with an allowed tool list. Retest on the client's setup and for Gmail", None, None, None],
        ["Confirm data terms and legal questions", founder, "See 03-data-handling-notes", None, None, None],
    ])

    data_rows = [["Brain docs", values["BRAIN_LOCATION"], "All agents", "Google Workspace or Microsoft 365 connector", None, None]]
    needs = {
        1: [("Sales calls", values["CALLS_SOURCE"], "Fathom connector not confirmed. Fallback: save transcripts to a folder the agent can read"),
            ("Support messages", values["SUPPORT_SOURCE"], "Gmail or Outlook connector, or the help desk's connector")],
        2: [("Competitor pages", values["COMPETITOR_URLS"], "Claude with web search")],
        7: [("Website visitors", values["VISITOR_SOURCE"], "Alert emails read from the inbox"),
            ("Email drafts", values["EMAIL_DRAFTS"], "Check that draft creation is allowed on a schedule")],
        8: [("Ad results", values["ADS_SOURCE"], "Confirm the connector or a scheduled export to a sheet")],
    }
    for number in chosen:
        for name, source, route in needs.get(number, []):
            data_rows.append([name, source, f"Agent {number}", route, None, None])
    add_sheet(book, "Data map", ["Data", "Where it lives", "Used by", "Route into Claude", "Status", "Notes"], data_rows)

    add_sheet(book, "Brain docs", ["Doc", "Owner", "Approved by", "Status", "Date approved"], [
        ["Customers", operator, founder, None, None],
        ["Offer and proof", founder, founder, None, None],
        ["Voice", founder, founder, None, None],
        ["Competitors", operator, founder, None, None],
        ["Wins and flops", operator, founder, None, None],
        ["Research", "Agents 1 and 2", "Not needed", None, None],
    ])

    ordered = sorted(chosen, key=lambda n: (AGENTS[n][1], n))
    add_sheet(book, "Rollout", ["Agent", "Stage", "First hand run", "Test passed", "Second clean run", "Scheduled", "Approved by", "Status", "Notes"], [
        [f"{n} {AGENTS[n][0]}", AGENTS[n][1], None, None, None, None, None, None, None] for n in ordered
    ])

    add_sheet(book, "Handover", ["Item", "Who", "Status", "Date", "Notes"], [
        ["Runbook filled in and saved with the Brain docs", operator, None, None, None],
        [f"{operator} ran a full week alone", operator, None, None, None],
        ["Training session finished", "Consultant", None, None, None],
        ["Instructions saved in the company's folder", "Consultant", None, None, None],
        ["Consultant's seat and connector access removed", "Claude Owner", None, None, None],
        ["30 day support period end date agreed", founder, None, None, None],
    ])
    book.save(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    parser.add_argument("out", type=Path, help="new folder to create for this client")
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    chosen = sorted(set(config.pop("agents", [])))
    tier = config.pop("tier", None) or tier_for(len(chosen))
    if not chosen or any(n not in AGENTS for n in chosen):
        sys.exit("Set agents to a list of numbers from 1 to 8.")
    if tier not in TIERS:
        sys.exit(f"Unknown tier: {tier}")
    if args.out.exists():
        sys.exit(f"{args.out} already exists. Nothing was changed.")

    warnings = [f"Agent {n} needs Agent {d}, which is not in scope." for n in chosen for d in AGENTS[n][2] if d not in chosen]
    price, timeline, payment = TIERS[tier]
    agent_list = "\n".join(f"- Agent {n}: {AGENTS[n][0]}" for n in chosen)
    values = {**config, "TIER": tier, "PRICE": price, "TIMELINE": timeline, "PAYMENT": payment, "AGENT_LIST": agent_list}

    copy_tree(KIT / "agents", args.out / "agents", values, {p.name for p in (KIT / "agents").glob("*.md") if int(p.name[:2]) in chosen})
    copy_tree(KIT / "brain", args.out / "brain", values)
    copy_tree(KIT / "docs", args.out / "docs", values)

    unfilled = sorted({m for p in args.out.rglob("*.md") for m in re.findall(r"\{\{([A-Z_]+)\}\}", p.read_text(encoding="utf-8"))})
    if unfilled:
        shutil.rmtree(args.out)
        sys.exit("Missing from the config, so nothing was built: " + ", ".join(unfilled))

    build_tracker(args.out / "setup-tracker.xlsx", values, chosen)
    print(f"Built {args.out}")
    print(f"{len(chosen)} agents, {tier}, {price}. Set by agent count only, so check it against the audit.")
    for warning in warnings:
        print("WARNING:", warning)


if __name__ == "__main__":
    main()
