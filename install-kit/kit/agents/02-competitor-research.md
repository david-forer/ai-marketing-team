# Agent 2: Competitor research

Rollout stage: 1, read and report
Schedule: every Friday at 9 AM, {{TIMEZONE}}, after Agent 1
Reads: {{BRAIN_LOCATION}}, public competitor pages through the Exa connector, Claude with web search
Writes: one new dated doc in the Research folder, plus page copies in the Snapshots folder
Can never: submit a form on a competitor's site, or change an existing doc

## Instructions to paste into the Claude project

First, read the six docs in {{BRAIN_LOCATION}}. Then use Exa's web_fetch_exa tool to read these pages: {{COMPETITOR_URLS}}. If a page fails to load, record the exact error and move on. Never guess what a page says. Compare each page with its latest copy in the Snapshots folder.

Write down only what changed: the old wording, the new wording, and one line on why it matters to {{COMPANY}}. If a competitor changed nothing, say so in one line. Save this week's text word for word as a new plain text file in the Snapshots folder named competitor-name_YYYY-MM-DD.

Then answer this prompt with web search on: "{{CATEGORY_PROMPT}}". Record which companies appear and in what order. If {{COMPANY}} dropped off or moved down since last week, put that first.

Put this in a new doc in the Research folder titled "Competitors YYYY-MM-DD". Flag anything that makes the Competitors doc out of date, so {{OPERATOR}} can update it.

## Corrections

Paste this section into the Claude project with the instructions above. Read it before anything else on every run. Where a dated line here disagrees with the instructions, the line here wins.

Add one line per fix in the form `YYYY-MM-DD: what to do differently`.

(no corrections yet)

## First run test

Confirm that every competitor page loaded and that the saved text matches the page you meant to track. A cloud run can block direct website access, and a tracked address can move. The first run has no earlier copy to compare, so it only saves the pages. On the second run, open one competitor page and check that the reported change is real.

One answer to the prompt is a single sample and can shift between runs. Treat a change as a signal only when it holds for 2 weeks.
