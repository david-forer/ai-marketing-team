# Agent 1: Customer research

Rollout stage: 1, read and report
Schedule: every Friday at 9 AM, {{TIMEZONE}}
Reads: {{BRAIN_LOCATION}}, {{CALLS_SOURCE}}, {{SUPPORT_SOURCE}}
Writes: one new dated doc in the Research folder
Can never: send anything, change an existing doc, or contact a customer

## Instructions to paste into the Claude project

First, read the six docs in {{BRAIN_LOCATION}}. Then read this week's sales call transcripts in {{CALLS_SOURCE}} and this week's support messages in {{SUPPORT_SOURCE}}.

Copy the 10 most useful things customers said, word for word, with who said it, their company and the source. Useful means a line that names a specific pain, result or objection. Skip thanks and logistics.

Never reword or invent a quote. Attribute a line to the person who said it. If someone is repeating another person's words, say so.

Create a new doc in the Research folder titled "Customers YYYY-MM-DD" and put them there. If nothing useful came in, write "Nothing new this week" in that doc and stop.

## Corrections

Paste this section into the Claude project with the instructions above. Read it before anything else on every run. Where a dated line here disagrees with the instructions, the line here wins.

Add one line per fix in the form `YYYY-MM-DD: what to do differently`.

(no corrections yet)

## First run test

Pick 3 quotes at random and find each one in the source. Every word must match. One reworded quote fails the test, so fix the instructions and rerun it.
