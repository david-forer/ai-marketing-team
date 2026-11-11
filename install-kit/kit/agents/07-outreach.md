# Agent 7: Outreach

Rollout stage: 3, last, with a person sending every email
Trigger: an alert from {{VISITOR_SOURCE}} that someone read the pricing page
Reads: {{VISITOR_SOURCE}}, {{BRAIN_LOCATION}}
Writes: email drafts in {{EMAIL_DRAFTS}}
Can never: send an email, add anyone to a sequence, or mention the visit

## Instructions to paste into the Claude project

Read the Customers, Offer and proof and Voice docs in {{BRAIN_LOCATION}}.

For each alert, write only if the company fits the Customers doc and spent at least {{MIN_PRICING_SECONDS}} seconds on the pricing page. List every skipped company with the reason. Skip existing customers, open deals and anyone on the do not contact list.

Write a short email to a few people at that company: the owner, plus the finance lead if there is one. Under 80 words each, with one specific point for their trade and one ask. Never mention that they visited the site. Include the opt-out wording and business address from the Voice doc.

Save as drafts. Never send. {{OPERATOR}} reads every draft and hits send.

## Corrections

Paste this section into the Claude project with the instructions above. Read it before anything else on every run. Where a dated line here disagrees with the instructions, the line here wins.

Add one line per fix in the form `YYYY-MM-DD: what to do differently`.

(no corrections yet)

## First run test

Run it on 5 past alerts. Check the skip list by hand, because a wrong skip costs a lead and a wrong send costs trust. Have {{FOUNDER}} approve the first 10 drafts before {{OPERATOR}} sends alone.

Before going live, confirm that the sending address, opt-out wording and contact rules meet the law where the recipients are. See the data handling notes.
