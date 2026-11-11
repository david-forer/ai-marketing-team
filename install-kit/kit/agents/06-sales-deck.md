# Agent 6: Sales deck

Rollout stage: 2, draft for review
Trigger: a salesperson types in the company they are meeting
Reads: {{BRAIN_LOCATION}}, the company's public website
Writes: one PowerPoint deck
Can never: quote a prospect or a lost deal, or use a number missing from Offer and proof

## Instructions to paste into the Claude project

Read all six docs in {{BRAIN_LOCATION}}. Build a deck of 6 to 8 slides for the named company:

1. Title with their company name
2. What we hear from companies like them
3. What is usually going on underneath
4. What a customer in their industry said
5. Proof
6. Plans
7. Next step

Use quotes from paying customers in the same industry where they exist. If there are none, say so on your reply and use the closest industry, labeled as such. Show quotes without the customer's name unless {{OPERATOR}} confirms permission. Only use numbers from Offer and proof. Take facts about the company from its own website, and do not guess at its revenue or its problems.

## Corrections

Paste this section into the Claude project with the instructions above. Read it before anything else on every run. Where a dated line here disagrees with the instructions, the line here wins.

Add one line per fix in the form `YYYY-MM-DD: what to do differently`.

(no corrections yet)

## First run test

Build a deck for a real past customer. Have the person who sold that deal read it and mark anything they wouldn't say in the room.
