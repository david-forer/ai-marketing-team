# Client agent team kit

Use this after an audit, when a client wants the marketing agent team in their own accounts.

## Start a client

1. Copy `client.example.json`, fill it in, and list the agents in scope.
2. Run the command below. It stops if the client folder already exists.

```powershell
python scripts\new_client.py client.json D:\path\to\new-client-folder
```

The client folder gets `agents/`, `brain/`, `docs/` and `setup-tracker.xlsx`, with only the agents in scope.

## Order of work

1. Send `docs/01-kickoff-questions.md` and hold the call.
2. Add `docs/02-scope-of-work-insert.md` to the statement of work. The tier comes from the agent count, so check it against the audit.
3. Work through the Access tab, then confirm each route on the Data map tab.
4. Answer the legal questions in `docs/03-data-handling-notes.md`.
5. Write the Brain docs from real customer sources and get the founder's approval.
6. Roll out by stage. Run each agent by hand, pass its first run test, then schedule it.
7. Fill in `docs/04-runbook.md`, train the operator, and work through the Handover tab.

## Facts to recheck per client

Checked 2026-11-05 against Anthropic's pages, some through secondary sources. Plans and connectors change, so recheck them before quoting.

- Team plan: 2 to 150 seats.
- Guest or consultant access: not confirmed. The kit assumes a temporary paid seat.
- Connectors: an Owner enables them, then each member signs in with their own account.
- Fathom connector: not found. The kit routes transcripts through a folder instead.
- Microsoft 365 connector: plan availability was unclear.
- Scheduled tasks: Anthropic's help page says they run in the cloud without the computer. Older posts disagree, so test one.

## Results from the live test on 2026-11-05

Agent 2 ran as a Claude Code cloud routine on David's account, with Drive as its only connector. Cowork scheduled tasks and Team plans were not tested.

- Drive reads and new docs worked with no approval stop.
- The Drive connector can't edit an existing doc, so agents create a new dated doc each run.
- All 6 competitor sites failed to load directly from the cloud environment, which has a network allowlist.
- With the Exa connector added, all 6 loaded and the run saved a snapshot of each. Exa lists page text at about $1 per 1,000 pages, so 26 pages a month costs about 3 cents. Recheck the price and free credit per client.
- One page came back cut at the 30,000 character limit, so raise the limit for long pages.
- Snapshots are copied by the model. Check for false changes on the first comparison run.
