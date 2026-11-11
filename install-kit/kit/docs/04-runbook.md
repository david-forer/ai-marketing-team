# Marketing agent runbook for {{COMPANY}}

Owner: {{OPERATOR}}. Keep this next to the Brain docs in {{BRAIN_LOCATION}}.

## The agents

{{AGENT_LIST}}

Each agent is a Claude project. Its instructions are in the project, and a copy sits in this folder.

## {{OPERATOR}}'s week

- Each morning, read the morning report if Agent 8 is running, and decide what to turn off.
- On Monday, pass the ideas to {{FOUNDER}}, then send the kept ones to the writer.
- Before anything goes out, read it, check every number against Offer and proof, and fix it.
- On Friday, skim what the research agents added.
- Each month, update the Brain docs, copy lasting wins from the Ad Results folder into Wins and flops, then archive old research.

## When an output is wrong

Fix the cause, because a fix made only in the draft will return next week.

- Wrong fact: correct the Brain doc.
- Wrong tone: add a rule to the Voice doc.
- Wrong steps: add one dated line to the Corrections section of the agent's instructions, in the form `YYYY-MM-DD: what to do differently`. Update the Claude project and the copy in this folder. The agent reads Corrections first, and a line there wins over the instructions above it. Once a month, fold lines that have held for a few weeks into the instructions and delete them from Corrections.

Then run the agent again once by hand.

## The first week is supervision

Each agent runs once by hand and passes its first run test before its schedule goes on. For its first week after that, {{OPERATOR}} checks every output against the source before using it. An agent runs unwatched only after a week with no new Corrections line.

## When an agent stops

1. Open the project in Claude and look for the last run.
2. Check that the connector is still signed in. A password change or a departed employee is the usual cause.
3. Run the job by hand.
4. If it fails twice, turn off the schedule and do that week's job manually until it's fixed.

## How to turn an agent off

Delete its schedule in the Claude project. Nothing else depends on the schedule, and the project stays in place. To cut all access, the Claude Owner disconnects the connector in Organization settings.

## How to add a new person

Give them a Claude seat, share the projects and Brain folder, have them sign in to each connector, and walk them through this page.

## Rules that never change

- A person reviews everything before it reaches a customer. The last click is always a person's.
- No agent creates an account, types a password or accepts terms. People sign in to each connector with their own accounts.
- Agents use only what's in the Brain docs.
- Quotes stay word for word.
- Nobody posts as {{FOUNDER}} except {{FOUNDER}}.
