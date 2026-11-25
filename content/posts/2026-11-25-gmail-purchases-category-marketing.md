---
title: Gmail's Purchases Category Is Full of Marketing Mail
slug: gmail-purchases-category-marketing
date: 2026-11-25
summary: Searching category:purchases in Gmail returned 4,977 messages, with a Lucky Brand jacket promotion at the top and no receipt in sight. Why Purchases is different from a label, why you can't just remove a message from it, and what you can actually do about it.
tags: [gmail, email, google]
pinned: false
---

I went looking for a receipt in Gmail and searched `category:purchases`. It returned 4,977 messages. The first one was this, from Lucky Brand on November 24:

> Your next head-turning jacket? Found it 🔥 — Strut in style this season

That is a promotional lookbook email. It has no order number, no order total, no payment, no shipping, and no tracking information. Nothing was purchased. The same sender shows up again in Purchases on November 9 and November 6, with similar marketing subjects.

This is not a one-off misfile. It is a pattern, and it is worth understanding, because Purchases does not behave like the rest of Gmail's organisation — and that limits what you can do about it.

## The short version

- **Purchases is meant for receipts**, not marketing — order confirmations, shipping notices, delivery confirmations.
- **The Lucky Brand mail has none of the receipt signals**: no order number, no total, no payment, no tracking.
- **You cannot remove a message from Purchases**, because it is not a label. It is computed by Google at search time, and Purchases has no label ID in the Gmail API.
- **Archiving does not help**, and deleting is the only thing that takes a message out of the results.
- **What helps**: per-sender filters, training the five inbox tabs, and reporting the misclassification with a concrete example.

## Receipt or marketing? Check the signals

A receipt and a promotion can both mention a product and a price. What separates them is the transaction record:

| Signal | In a real receipt | In the Lucky Brand mail |
| --- | --- | --- |
| Order number / confirmation | Yes | No |
| Order total | Yes | No |
| Payment method | Usually | No |
| Shipping or tracking number | Usually | No |
| "Shop now", "% off", "New styles" | No | Yes |
| Sent to thousands at once | No | Yes |

If a message has the bottom two rows and none of the top four, it is marketing — however much it talks about shopping.

## Is it a purchase? A quick decision flow

<div style="max-width:560px; margin:0 auto 14px; text-align:center;">
  <div style="border:1px solid var(--border-color); border-radius:8px; padding:10px 14px; background:var(--bg-secondary);"><strong>Does it name an order?</strong><br><span style="color:var(--text-secondary);">Order number, confirmation, total, or tracking?</span></div>
  <div style="font-size:18px; color:var(--text-secondary); margin:2px 0;">↓ Yes</div>
  <div style="border:1px solid var(--border-color); border-radius:8px; padding:10px 14px; background:var(--bg-secondary);"><strong>Likely a real receipt</strong><br><span style="color:var(--text-secondary);">It belongs in Purchases.</span></div>
  <div style="font-size:18px; color:var(--text-secondary); margin:2px 0;">↓ No</div>
  <div style="border:1px solid var(--border-color); border-radius:8px; padding:10px 14px; background:var(--bg-secondary);"><strong>Does it only sell you something?</strong><br><span style="color:var(--text-secondary);">A product, a price, a discount, "shop now"?</span></div>
  <div style="font-size:18px; color:var(--text-secondary); margin:2px 0;">↓ Yes</div>
  <div style="border:1px solid var(--border-color); border-radius:8px; padding:10px 14px;"><strong>Marketing, not a purchase</strong><br><span style="color:var(--text-secondary);">It does not belong in Purchases, even if Gmail put it there.</span></div>
</div>

## What Purchases is supposed to be

Gmail's Purchases category is meant for order, shipping, and delivery confirmations: the receipts, the "your order has shipped" notices, the delivery confirmations. It is a search category, alongside Reservations for flights, hotels, and restaurant bookings.

In practice, the classifier keys on shopping signals — product names, prices, and words like "order" and "shipping" — and marketing mail from retailers is full of all of those. A jacket promotion reads, to the classifier, a lot like a jacket purchase.

## Why you can't just remove a message from it

This is the part that surprised me, and it is the reason this post exists.

A Gmail label is something stored on a message. You can add it, remove it, rename it, delete it. A category is not. `category:purchases` is computed by Google at search time; there is no label stored on the message to strip.

More precisely: Gmail search exposes seven category operators — primary, social, promotions, updates, forums, reservations, and purchases — but the Gmail API only has five `CATEGORY_*` label IDs, for the first five. Purchases and Reservations have no label ID, so search is the only way to query them, and there is no API call to move a message out of them.

| Category | Search operator | API label ID | Can you move a message out of it? |
| --- | --- | --- | --- |
| Primary | `category:primary` | `CATEGORY_PERSONAL` | Yes — add/remove the label |
| Social | `category:social` | `CATEGORY_SOCIAL` | Yes — add/remove the label |
| Promotions | `category:promotions` | `CATEGORY_PROMOTIONS` | Yes — add/remove the label |
| Updates | `category:updates` | `CATEGORY_UPDATES` | Yes — add/remove the label |
| Forums | `category:forums` | `CATEGORY_FORUMS` | Yes — add/remove the label |
| Reservations | `category:reservations` | None | No |
| Purchases | `category:purchases` | None | No |

The last two rows are the whole problem. They exist only as search results, not as labels on a message — so there is nothing to add, remove, or strip.

That has three practical consequences:

- **There is no "remove from Purchases" operation** — not in Gmail settings, not in the API, and not in any third-party tool. My own Gmail toolkit could not touch it for the same reason.
- **Archiving does not help.** Search covers All Mail, so an archived message still shows up in `category:purchases`. Deleting a message is the only thing that takes it out of the results.
- **There is no toggle to stop Google classifying future mail the same way.** You can influence the five inbox tabs, but Purchases is not one of them.

Google's own help page confirms the tab side of this: you can only choose from the current categories, you cannot create your own, and moving an email to the wrong category helps Gmail learn your preferences over time. That training applies to the five tabs — Primary, Social, Promotions, Updates, Forums — not directly to the Purchases search bucket.

## What I did

I reported it through Gmail's own feedback channel, since that is the only channel Google offers for the classifier:

1. In Gmail on a computer, click **Help (?)** at the top right, then **Send feedback to Google**.
2. Choose **Report an issue**.
3. For "When you noticed this issue, what were you trying to do?", pick **Find messages or attachments** — the closest option to searching for a receipt.
4. Paste a description, attach a screenshot, and send.

The description I sent:

> When I search category:purchases, Gmail returns 4,977 messages, but many are marketing, not receipts.
>
> Top result: Lucky Brand, Nov 24 — "Your next head-turning jacket? Found it" — a promotional lookbook email with no order number, order total, payment, shipping, or tracking info. The same sender appears again in Purchases on Nov 9 and Nov 6 with similar marketing subjects.
>
> Please exclude promotional mail with no receipt, order, or tracking signals from category:purchases, and reserve it for actual order confirmations, shipping notices, and receipts.

Do not expect a reply. This goes to the product team as feedback, not to support. I sent it anyway, because a classifier problem that nobody reports is a classifier problem Google has no signal on at all.

## What you can do

If you are seeing the same thing, here is what actually helps, in order of usefulness:

| Lever | What it does | Fixes the Purchases search? |
| --- | --- | --- |
| Send feedback with an example | Gives Google a concrete misclassification to learn from | Not directly — but it is the only channel to the classifier |
| Per-sender filter: Categorize as Promotions | Hard rule for that sender, going forward | For future mail, partly — old messages may stay in the search |
| Drag mail to the correct tab | Trains the five inbox tabs for that sender | No — but it fixes Primary / Promotions / Updates |
| Archive the message | Removes it from the inbox | No — search covers All Mail |
| Delete the message | Removes it from Gmail entirely | Yes — the only sure way, and the most drastic |

The detail on each one follows.

**1. Send the same feedback.** Use the steps above, with your own example — the sender, the date, and the subject line of a marketing email that landed in Purchases, and what was missing from it (no order number, no total, no tracking). One report is a data point; a pattern of reports with concrete examples is harder to ignore. Attach a screenshot, cropped to the offending row — there is no need to share your whole inbox or label list.

**2. Force the sender into Promotions with a filter.** This is the most deterministic lever you have. Create a filter for the sender — for example, from Lucky Brand — and set **Categorize as: Promotions**. You can apply it retroactively to matching conversations. It is a hard rule going forward, unlike training, which is a suggestion. Be aware of the limit: a filter can categorise mail into the five tabs, and it may not remove old messages from a `category:purchases` search, since that bucket is computed separately.

**3. Train the tabs by moving mail.** If a message is in the wrong inbox tab, drag it to the correct one. Gmail will ask whether to do the same for future messages from that sender — say yes. This trains the Primary / Promotions / Updates classification, which is genuinely useful, even though it does not directly fix Purchases.

**4. Do not mark legitimate marketing as spam to fix this.** Unsubscribing from a sender you no longer want is fine, and reporting genuinely deceptive mail as spam is fine. But marking a retailer's marketing as spam because it is in the wrong category can damage that sender's classification for the messages you do still want from them — including their order confirmations.

## The honest summary

`category:purchases` is a useful idea with a noisy implementation: it catches receipts, and it also catches anything that looks like shopping. Because it is a computed search category with no label behind it, you cannot fix it yourself, message by message. The levers you do have are per-sender filters, tab training, and feedback with concrete examples.

If you have run into the same thing, the most useful thing you can do is report it the same way, with your own example. And if you want a clean list of actual purchases in the meantime, do not trust the category — filter on receipt signals instead: order confirmation, order number, total, and tracking.

*Checked November 25, 2026. Links: [Organize your emails into categories](https://support.google.com/mail/answer/3094499) and [Send feedback in Gmail](https://support.google.com/mail/answer/9212652).*
