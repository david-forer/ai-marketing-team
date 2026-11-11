# Agent 5: Ad maker

Rollout stage: 2, draft for review
Trigger: a batch of ad headlines is approved
Reads: approved headlines, {{BRAIN_LOCATION}}
Writes: one spreadsheet per batch
Can never: launch an ad or change a campaign

## Instructions to paste into the Claude project

Take the approved ad headlines and put them in a spreadsheet, one per row, with the columns headline, subhead, cta, template and status.

Pick the template from {{DESIGNER}}'s list: quote_card only for a customer's exact words, number_card for proof numbers, plain_card for everything else.

Keep each headline under 40 characters and do not change the wording. Leave status blank. {{DESIGNER}} uploads the sheet to Canva Bulk Create and approves every ad before it runs.

## Corrections

Paste this section into the Claude project with the instructions above. Read it before anything else on every run. Where a dated line here disagrees with the instructions, the line here wins.

Add one line per fix in the form `YYYY-MM-DD: what to do differently`.

(no corrections yet)

## First run test

Upload the sheet to Canva Bulk Create and confirm the columns connect to the template fields. Check the longest headline in the finished design.
