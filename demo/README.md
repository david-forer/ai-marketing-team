# Marketing agent team demo

Fictional demo company: Fenwick Row Bookkeeping. Every name, number and quote in this folder is invented. Nothing here is a real customer, a real result or a real competitor.

The structure is the point. To run this on a real client, replace `brain/` and `data/` and leave `agents/` alone.

## Adding your data

Double-click `Open-Upload-Page.cmd`. It opens a page on this computer with one box per data type, and shows which areas still hold demo data. Files stay on this computer. Replaced files are kept in `data/_replaced/`. Your first upload to transcripts, competitor pages or Claude answers moves that area's demo files there too, so real and fake data never mix.

To print the same setup check without the page, run `python scripts/upload_server.py --check`.

## Folders

- `brain/` the six docs every agent reads first
- `data/` stand-ins for Fathom, Gmail, competitor sites, Supermetrics and Leadfeeder
- `agents/` one instruction file per agent, ready to paste into a Claude project
- `outputs/` what each agent produced on its first run
- `scripts/` the data generator and the checks

## The demo week

| Day | Date | Agent | Output |
|---|---|---|---|
| Fri | 2026-10-30 | 1 Customer research | Quotes added to `brain/research.md` |
| Fri | 2026-10-30 | 2 Competitor research | Changes added to `brain/research.md` |
| Mon | 2026-11-02 | 3 Weekly ideas | 20 ideas |
| Mon | 2026-11-02 | 4 Channel writer | LinkedIn post, email, blog outline, ad headlines |
| Tue | 2026-11-03 | 5 Ad maker | Canva Bulk Create sheet |
| Wed | 2026-11-04 | 7 Outreach | Draft emails for operator review |
| Thu | 2026-11-05 | 6 Sales deck | PowerPoint deck |
| Thu | 2026-11-05 | 8 Morning report | Ad report for 2026-11-04 |
