# AI Marketing Team

Eight AI employees that do the recurring marketing work in a founder-led business, built on Claude.

Picture a 12-person bookkeeping firm that serves HVAC and plumbing contractors. The founder still writes the LinkedIn posts at 10 PM, nobody has listened back to a sales call in months, and the ad accounts get checked when someone remembers. That's who this is for. Each employee owns one of those jobs, runs on a schedule or when you ask, and leaves its work in a folder your company owns.

You don't hire all eight. You hire the two to four that would save the most time in your business.

## Two rules that never change

**The last click is yours.** No employee sends an email, publishes a post, launches an ad or changes a budget. It drafts and stages the work, and a person on your team reviews it and presses the button.

**No employee holds a password.** It never creates an account, types a password or accepts terms. Your people sign in to each connected tool with their own accounts, and access can be cut in one place.

## The roster

Every example below comes from a demo week for Fenwick Row Bookkeeping, a made-up company. None of it is real customer data.

### 1. Customer researcher

Reads your sales calls and support emails every week and pulls out what customers said, word for word.

- **Replaces:** listening back to call recordings you never have time for
- **Runs:** every Friday
- **You get:** the 10 most useful customer quotes of the week, each with who said it and where
- **Never:** rewords a quote, contacts a customer or changes an existing doc

### 2. Competitor watcher

Checks your competitors' public pages every week and reports what changed.

- **Replaces:** looking at competitors' pricing pages by hand, or not at all
- **Runs:** every Friday, after the customer researcher
- **You get:** a dated note of each change, with a saved copy of the page
- **Never:** fills in a form on a competitor's site

### 3. Ideas planner

Turns the week's research and your past wins into ideas for posts, emails and ads.

- **Replaces:** the blank page at the Monday marketing meeting
- **Runs:** every Monday
- **You get:** up to 20 ideas, each tied to a real customer quote or a past win ([demo output](demo/outputs/03-weekly-ideas_2026-11-02.csv))
- **Never:** writes the content itself or publishes anything

### 4. Channel writer

Writes the ideas you kept as first drafts for each channel, in your company's voice.

- **Replaces:** a freelance copywriter for first drafts
- **Runs:** when the person running it passes over the kept ideas
- **You get:** a LinkedIn post, an email, a blog outline and ad headlines, ready to edit ([demo output](demo/outputs/04-channel-writer_2026-11-02.md))
- **Never:** publishes, writes as the founder or uses a claim you haven't approved

### 5. Ad builder

Turns approved headlines into a sheet your designer loads into Canva to make every ad in one pass.

- **Replaces:** building ad versions one at a time
- **Runs:** when a batch of headlines is approved
- **You get:** one spreadsheet per batch, with a template picked for each line ([demo output](demo/outputs/05-ad-maker_canva-bulk-create_2026-11-03.csv))
- **Never:** launches an ad or touches a campaign

### 6. Sales deck builder

Builds a short deck for a named prospect before a sales meeting.

- **Replaces:** rebuilding the pitch deck the night before every meeting
- **Runs:** when a salesperson types in the company they're meeting
- **You get:** a 6 to 8 slide PowerPoint using that prospect's industry and your approved proof ([demo output](demo/outputs/06-sales-deck_redbird-electric_2026-11-05.pptx))
- **Never:** quotes another prospect or uses a number you haven't approved

### 7. Outreach drafter

Writes a short first email when a company that fits your ideal customer reads your pricing page.

- **Replaces:** the sales rep you can't justify hiring yet
- **Runs:** when a website visitor alert comes in
- **You get:** email drafts in your inbox, plus a list of every company it skipped and why ([demo output](demo/outputs/07-outreach-drafts_2026-11-04.md))
- **Never:** sends an email, adds anyone to a sequence or mentions the visit

### 8. Morning reporter

Reads yesterday's ad numbers before you start work.

- **Replaces:** logging in to every ad platform each morning
- **Runs:** every morning
- **You get:** one page with what each ad spent, what it brought in, and which ads to consider turning off ([demo output](demo/outputs/08-morning-report_2026-11-05.md))
- **Never:** pauses, starts or changes a campaign or a budget

## How hiring works

1. **The audit.** I find where your marketing time and money go, put a dollar figure on it, and pick the employees worth hiring.
2. **The build.** We write six short reference docs together (your customers, offer, proof, voice, competitors, and what has worked before). Then I connect your tools and set up each employee in your company's own Claude account.
3. **Your first week is supervision.** Each employee runs while we watch, and its work gets checked against the source by hand before it runs on its own. Then I train the person on your team who will review the drafts each day.

When an employee gets something wrong, the fix goes into a short corrections list at the foot of its instructions. It reads that list first on every run, so the same mistake doesn't come back next week.

## What's in this repo

- [`demo/`](demo) is the full Fenwick Row demo week: the six reference docs, made-up source data, and what each employee produced on its first run.
- [`install-kit/`](install-kit) is what I use to set the team up for a client: the eight employees' instructions, blank reference docs, the kickoff questions, the runbook and a script that builds a client's folder.

Everything is plain text and spreadsheets. You can read every instruction an employee follows, and nothing here runs on a server of mine.

## Want it running in your business?

The files are free to read and use. Most owners would rather not spend three weeks wiring Claude to their Google Drive, Gmail and ad accounts, and that's the part I do.

I'm David Forer. I run AI operations audits and installs for founder-led businesses with 5 to 20 people and no ops lead. [Book a 30 minute call](https://calendly.com/david-j-forer/30min) or read more at [davidjforer.com](https://davidjforer.com).

## License

MIT. See [LICENSE](LICENSE).
