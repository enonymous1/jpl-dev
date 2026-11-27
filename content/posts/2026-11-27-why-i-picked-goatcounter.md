---
title: Why I Put GoatCounter on My Sites
slug: why-i-picked-goatcounter
date: 2026-11-27
summary: GoatCounter is the smallest honest answer to "who visits my site?" — a free, cookie-free counter that tells you pageviews, referrers, and browsers without a consent banner or a database to babysit. I run it on two sites now, and this is why, where it falls short, and how it stacks up against the alternatives.
tags: [goatcounter, analytics, privacy]
pinned: false
---

I run two small sites, and both of them left me with the same question: is anyone actually visiting? For the WhenWhere coming-soon page, the question had a number attached to it — how many people visit versus how many sign up for the launch list, which is the conversion rate. For this portfolio, the question is softer — which pages and posts get read, and where do people come from? I did not need a marketing suite to answer either one. I needed a counter.

I picked GoatCounter, twice: first on the WhenWhere page, then here on justinlyons.dev. This is a practitioner's read of why, where it falls short, and how it compares to the alternatives I looked at. Prices below are the hosted entry prices as published in November 2026 — vendors change them, so check the pricing page before you buy anything.

## TL;DR

- **What it is:** open-source, cookie-free web analytics — pageviews, unique visitors, referrers, locations, browsers, and basic events, and not much else. On purpose.
- **What it costs:** the hosted service is free for personal sites and reasonable small-business traffic, supported by donations. Self-hosting is free under a slightly modified EUPL-1.2 license.
- **How it works:** one async script tag, about 3.5 KB gzipped. No cookies, no personal data stored, no consent banner.
- **The catch I actually hit:** GoatCounter records the path, not the domain — so each domain needs its own site under the same account. Reusing one snippet across two domains merges their stats with no way to tell them apart.
- **When to pick something else:** if you need funnels, retention cohorts, or session paths, GoatCounter cannot do that by design. Umami is the next step up; Plausible or OpenPanel after that.

## What it is, and how the privacy part actually works

GoatCounter is a single Go binary backed by SQLite (or PostgreSQL if you outgrow SQLite). The current Linux release downloads at about 14 MB. You do not need ClickHouse, Redis, or any container orchestration to self-host it — it runs alongside whatever else is already on a small VPS, and the hosted version needs no server at all.

The privacy claim is the whole point, so it is worth saying precisely what happens. When a visitor loads a tracked page, the script makes one request to the count endpoint with the URL, the referrer, the screen size, and the user-agent string. The server hashes the visitor's IP address together with the user agent, using a salt that rotates regularly, and throws the IP away. The hash exists only to count unique visits within the same day, and it is discarded after that — so a visitor cannot be followed across days even if you wanted to. No cookies are set, no localStorage is touched, no fingerprint is computed. Country is derived from the IP at request time and then the address is gone. The whole chain looks like this:

<div style="max-width:560px; margin:0 auto 14px; text-align:center;">
  <div style="border:1px solid var(--border-color); border-radius:8px; padding:10px 14px; background:var(--bg-secondary);"><strong>Page load</strong><br><span style="color:var(--text-secondary);">One request: URL, referrer, screen size, user agent</span></div>
  <div style="font-size:18px; color:var(--text-secondary); margin:2px 0;">↓</div>
  <div style="border:1px solid var(--border-color); border-radius:8px; padding:10px 14px; background:var(--bg-secondary);"><strong>Hash</strong><br><span style="color:var(--text-secondary);">Server hashes the IP address + user agent with a rotating salt</span></div>
  <div style="font-size:18px; color:var(--text-secondary); margin:2px 0;">↓</div>
  <div style="border:1px solid var(--border-color); border-radius:8px; padding:10px 14px; background:var(--bg-secondary);"><strong>IP discarded</strong><br><span style="color:var(--text-secondary);">The raw address is thrown away immediately</span></div>
  <div style="font-size:18px; color:var(--text-secondary); margin:2px 0;">↓</div>
  <div style="border:1px solid var(--border-color); border-radius:8px; padding:10px 14px; background:var(--bg-secondary);"><strong>Count</strong><br><span style="color:var(--text-secondary);">The hash counts unique visits within the same day only</span></div>
  <div style="font-size:18px; color:var(--text-secondary); margin:2px 0;">↓</div>
  <div style="border:1px solid var(--border-color); border-radius:8px; padding:10px 14px; background:var(--bg-secondary);"><strong>Hash discarded</strong><br><span style="color:var(--text-secondary);">At day's end the hash is gone — no visitor can be followed across days</span></div>
</div>

That is why there is no consent banner: there is nothing to consent to. That is GoatCounter's own position, and it matches how I run it — no banner on either site. I am not a lawyer, and if your site does something else with visitor data, that is a different conversation. For a static site with one analytics script, the banner question simply does not arise.

Beyond the script tag, there are three more ways to get pageviews in, and they matter more than they first look. There is a JavaScript-free 1x1 tracking pixel for pages where scripts are not allowed, a REST API for recording events from backend middleware, and a logfile importer that parses nginx, Apache, Caddy, and CloudFront logs — which also works against the hosted service, so you can backfill history from logs you already have. Log import has its own trade-offs (more bot traffic in the numbers, no screen sizes or page titles), but it means the tool is not only a script tag.

You can also flip your stats page public with one click, which suits an open-source project page or a personal site that has nothing to hide.

## Putting it on a site

The integration is one script tag:

```html
<script data-goatcounter="https://YOURCODE.goatcounter.com/count"
        async src="https://gc.zgo.at/count.js"></script>
```

`YOURCODE` is the site you create in the dashboard. I use the explicit `https` source rather than a protocol-relative one, so the script loads over HTTPS even if the page is ever served over plain HTTP.

Two things I learned doing this twice:

**One site per domain.** GoatCounter does not store which domain a pageview belongs to. If you put the same snippet on two domains, both sites' visits land in one dashboard as the same paths, with no way to separate them. The fix is what the documentation prescribes: create a new site for every domain. It is the same account and the same login — a new site is a separate dashboard with its own snippet. That is what I did: `whenwherebiz.goatcounter.com` for the WhenWhere page, `jpl-dev.goatcounter.com` for this site.

**Local visits do not count, by design.** When I verified the setup from my own machine, the script loaded and initialized fine, but no count fired — and the console said why: `goatcounter: not counting because of: localhost`. Local development traffic never pollutes the stats. Real visits on the live domain count normally. Your own visits to the live site do count, though, unless you set "ignore your IP" in the dashboard — worth doing once, on day one.

## Where it falls short

The same design that makes GoatCounter light is what limits it:

- **No funnels or user journeys.** Because there is no persistent identifier, you cannot build multi-step conversion funnels, track retention cohorts, or inspect individual session paths. If your question is "where do people drop off between the landing page and checkout," this is the wrong tool.
- **A plain dashboard.** It is fast, clean, and functional, but noticeably more barebones than the modern React dashboards its competitors ship. It shows you the numbers and gets out of the way; it does not try to look impressive doing it.
- **Not built for massive scale.** SQLite handles hundreds of hits a second without trouble, but a site pushing millions of daily pageviews, or asking complex multi-dimensional questions of its data, will outgrow the hosted service — at which point the documented path is self-hosting with PostgreSQL.

None of those mattered for my two sites. Both questions I needed answered — visits versus signups, and which pages get read — are exactly the questions GoatCounter answers.

## The alternatives

| Tool | License & self-hosting | Typical stack | Hosted pricing | Best for |
| --- | --- | --- | --- | --- |
| **GoatCounter** | Slightly modified EUPL-1.2 (Yes) | Single Go binary + SQLite/Postgres | Free (reasonable use) | Minimalist traffic stats, static sites, zero-maintenance self-hosting |
| **Umami** | MIT (Yes) | Node.js + PostgreSQL | Free tier (up to 100k events/mo), then $20/mo | Modern UI, custom events, basic funnels, and UTM tracking without heavy infra |
| **Plausible (CE)** | AGPL-3.0 (Yes) | Docker + PostgreSQL + ClickHouse | From $9/mo | Polished marketing/blog dashboards and goal conversions (heavier self-hosted stack) |
| **OpenPanel** | AGPL-3.0 (Yes) | Docker + Postgres + ClickHouse + Redis | From $2.50/mo | Bridging web analytics with SaaS product analytics (funnels, cohorts, user IDs) |
| **Matomo** | GPL-3.0 (Yes) | PHP + MySQL/MariaDB | Cloud from €29/mo | Full Google Analytics replacement with heatmaps, SEO tools, and e-commerce tracking |
| **Fathom** | Proprietary (No) | Managed cloud only | From $15/mo | Teams wanting a completely hands-off, EU-compliant managed service |

Hosted entry price, per month:

<div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;"><span style="width:110px; text-align:right; font-size:14px; color:var(--text-secondary);">GoatCounter</span><span style="flex:1; background:var(--bg-secondary); border:1px solid var(--border-color); border-radius:4px; height:18px;"><span style="display:block; height:100%; width:0%; background:var(--primary-color); border-radius:4px;"></span></span><span style="width:52px; font-size:14px;">$0</span></div>
<div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;"><span style="width:110px; text-align:right; font-size:14px; color:var(--text-secondary);">Umami</span><span style="flex:1; background:var(--bg-secondary); border:1px solid var(--border-color); border-radius:4px; height:18px;"><span style="display:block; height:100%; width:0%; background:var(--primary-color); border-radius:4px;"></span></span><span style="width:52px; font-size:14px;">$0</span></div>
<div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;"><span style="width:110px; text-align:right; font-size:14px; color:var(--text-secondary);">OpenPanel</span><span style="flex:1; background:var(--bg-secondary); border:1px solid var(--border-color); border-radius:4px; height:18px;"><span style="display:block; height:100%; width:17%; background:var(--primary-color); border-radius:4px;"></span></span><span style="width:52px; font-size:14px;">$2.50</span></div>
<div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;"><span style="width:110px; text-align:right; font-size:14px; color:var(--text-secondary);">Plausible</span><span style="flex:1; background:var(--bg-secondary); border:1px solid var(--border-color); border-radius:4px; height:18px;"><span style="display:block; height:100%; width:60%; background:var(--primary-color); border-radius:4px;"></span></span><span style="width:52px; font-size:14px;">$9</span></div>
<div style="display:flex; align-items:center; gap:8px; margin-bottom:14px;"><span style="width:110px; text-align:right; font-size:14px; color:var(--text-secondary);">Fathom</span><span style="flex:1; background:var(--bg-secondary); border:1px solid var(--border-color); border-radius:4px; height:18px;"><span style="display:block; height:100%; width:100%; background:var(--primary-color); border-radius:4px;"></span></span><span style="width:52px; font-size:14px;">$15</span></div>

<p style="font-size:14px; color:var(--text-secondary);">Entry price only — the allowances behind each price are different units (events vs pageviews): GoatCounter is free for reasonable use, Umami Hobby covers 100k events a month, OpenPanel $2.50 covers 5k events, Plausible $9 covers 10k pageviews, Fathom $15 covers 100k pageviews. Matomo Cloud starts at €29/mo (50k hits), priced in euros, so it sits off this dollar scale.</p>

A few footnotes the table does not show. Umami's free tier counts *events*, not pageviews — every pageview, custom event, and event property counts toward the 100k, on one website, with six months of retention. Plausible's $9 tier covers 10k pageviews on one site, with a 30-day trial and no free tier; its Community Edition is free to self-host. OpenPanel's $2.50 tier covers 5,000 events a month, and it has no free tier either — a 30-day trial, then usage-based tiers. Matomo's cloud starts at €29 a month for 50,000 hits, and its funnels, heatmaps, and session recording are premium plugins that cost extra even when you self-host; note also that Matomo sets cookies by default, with a cookieless mode available. Fathom's $15 tier covers 100,000 pageviews and includes 50 sites on every plan, which is why agencies like it — but there is no self-hosted option at any price.

## Which one should you pick?

- **Stick with GoatCounter** if you want to drop a 3.5 KB script (or parse server logs) on a static site, portfolio, or small business page and never think about database maintenance or cookie banners again.
- **Step up to Umami** if you want a sleeker, modern dashboard with custom event tracking, retention metrics, and simple conversion goals while keeping your self-hosted stack lightweight — just Node and Postgres.
- **Move to Plausible or OpenPanel** if you are running a commercial SaaS or high-traffic storefront where ClickHouse-backed query speed, multi-step conversion funnels, and campaign attribution justify the extra server overhead.
- **Pick Matomo** if you want the closest thing to a full Google Analytics replacement and are willing to run PHP and MySQL — and to pay for the plugins — to get it.
- **Pick Fathom** if you want someone else to run everything, you have many small sites to cover under one bill, and you will never need to self-host.

I picked GoatCounter because my question was small and my sites are small. The day either of those stops being true, Umami is where I would look first.

## Sources

- GoatCounter documentation — server logfiles: <https://www.GoatCounter.com/help/logfile>
- GoatCounter README (features, ingestion methods, license): <https://raw.githubusercontent.com/arp242/goatcounter/master/README.md>
- Umami Cloud pricing (Hobby free tier, Pro at $20/mo): <https://tailkits.com/tools/umami/>
- Plausible vs Fathom vs Umami price comparison, checked November 2026: <https://dev.to/octave_nkurunziza_afb0512/plausible-vs-fathom-vs-umami-which-one-costs-less-in-2026-d1c>
- OpenPanel vs Matomo pricing (OpenPanel from $2.50/mo, Matomo Cloud from €29/mo): <https://openpanel.dev/compare/matomo-alternative>
