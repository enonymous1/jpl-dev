---
title: Choosing a Password Manager (and Keeping It Healthy)
slug: choosing-a-password-manager
date: 2026-11-24
summary: 1Password and Bitwarden are the two picks worth your money, the rest of the field in brief, what the LastPass breach actually teaches, and the monthly / quarterly / annual schedule that keeps a vault healthy.
tags: [passwords, security, 2fa]
pinned: false
---

A password manager is the single highest-leverage security habit there is. One reused password, one breach, and every account sharing that password falls with it. A manager fixes that by making every password unique and remembering them for you — you remember one strong account password, it remembers the rest.

This is practitioner advice, not a sponsored roundup. There are no affiliate links here: nothing on this page pays me if you pick one product over another. Prices and features were checked against the vendors' own pricing pages on November 24, 2026, and they will have moved by the time you read this — check before you buy. This post itself gets reviewed every six months, same as the schedule below.

## What actually matters when you pick one

Forget the feature-count tables. Judge a manager on these:

- **Zero-knowledge encryption.** Your vault is encrypted on your device before it reaches the vendor's servers, and the vendor cannot decrypt it. If a company can reset your account password for you, it can read your vault — that is the trade-off to notice.
- **Independent audits, published.** Annual third-party assessments, not a "we take security seriously" page. Look for named firms and recent dates.
- **Passkeys.** The manager should store and fill passkeys, not just passwords. Passkeys are bound to the site that issued them, so a phishing page cannot reuse one.
- **Built-in second factor.** Storing time-based one-time codes (TOTP) in the vault is convenient. Whether you should is a separate question — see the 2FA section.
- **Sharing that respects boundaries.** Family or team sharing should be vault-by-vault, not all-or-nothing, with a way to remove someone.
- **Recovery and emergency access.** A vault nobody can open when you're locked out — or worse — is a liability. There must be a recovery path you set up *before* you need it.
- **Export.** You can get your data out in an open format. A manager you cannot leave is a manager you do not own.
- **Every platform you use.** If it does not work on your phone, it does not get used, and an unused manager is worse than none.

## The two picks

### 1Password — the polished one

1Password is the manager I would set up for a family or a small office. It is the cleanest app in the category, it runs on effectively everything, and its sharing model — private vaults plus unlimited shared vaults — is the easiest to explain to a non-technical person.

What sets it apart is the Secret Key: on top of your account password, your device generates a 128-bit key that 1Password says it never sees and cannot recover. A stolen copy of their servers is far harder to crack because of it. Vaults are end-to-end encrypted (AES-256), Watchtower flags weak, reused, and breached passwords plus accounts missing two-factor authentication, passkeys are ordinary vault items you can move or share, and the built-in authenticator fills one-time codes after your password.

Individual is $47.88 a year ($3.99 a month, billed yearly; $35.88 the first year for new customers). Families is $71.88 a year ($5.99 a month; $53.88 the first year) for five people plus five guests, with account recovery for a locked-out member — the one meaningful escape hatch in a system that is otherwise deliberately unrecoverable. There is no free tier, only a 14-day trial, and both plans went up $12 a year at renewal in March 2026, which is worth knowing before you budget around the intro price.

The honest downsides: it costs more than twice Bitwarden Premium, there is no free fallback if you stop paying, and the account password plus Secret Key means losing both is genuinely unrecoverable — which is the point, until it happens to you.

### Bitwarden — the open one

Bitwarden is the manager I would set up for someone who wants to pay little or nothing, or who wants to read the code before trusting it. The server is open source, the audits are annual and named, and the free tier is a real vault: unlimited passwords on unlimited devices, passkeys included, no device cap.

Premium is $19.80 a year ($1.65 a month, billed yearly only) and adds the built-in authenticator, vault health reports, emergency access, and 5 GB of encrypted attachments. Families is $47.88 a year for six people. Self-hosting is available on the paid tiers, which is the option for anyone who wants the vault under their own roof — with the understanding that patching, backups, and uptime then become your job.

The honest downsides: the apps put function ahead of polish, health reports and the authenticator are paywalled (1Password includes Watchtower on every plan), and self-hosting is a commitment, not a weekend project you forget about.

**Either one beats the browser.** If you want the most polished experience and the easiest family sharing, take 1Password. If you want free, open, or self-hosted, take Bitwarden. The wrong choice is whichever one you will not actually use.

## The rest of the field, in brief

- **Proton Pass** — free tier with unlimited passwords, Plus at $35.88 a year, Family at $59.88 for six. Open source, audited, and the pick if you already live in Proton's world or want built-in email aliases.
- **NordPass** — Premium renews at $35.88 a year after a cheaper first year, Family at $71.88. Modern apps, XChaCha20 encryption, solid value if you catch the intro price and note the renewal.
- **Dashlane** — Premium around $65 a year, Friends & Family $97.49 for ten. The free plan ended in September 2025, and it bundles a VPN — worth it only if you would pay for the VPN anyway.
- **Keeper** — Unlimited around $42.99 a year, Family $91.99 for five. Enterprise-grade certifications; the family price is the highest here.
- **Apple Passwords / Google Password Manager** — free, and fine if you live entirely inside one company's devices or browser. The moment you mix platforms, the friction starts, and friction is what kills a manager.
- **KeePassXC** — free and open source, but the vault is a local file you sync yourself. Powerful, and exactly the wrong default for anyone who will not maintain the sync.

## What the breaches actually teach

Two incidents, two different lessons.

**LastPass, 2022.** Attackers compromised a developer's laptop and stole source code, then used what they learned to target one of four DevOps engineers who could reach the keys for production vault backups. A keylogger planted through an unpatched media server on the engineer's home computer captured the master password after MFA, and the corporate vault held the backup decryption keys. The attackers copied encrypted customer vault backups — website addresses unencrypted, secrets protected only by each user's master password and its key-derivation setting. Some older accounts were still at 5,000 PBKDF2 iterations; the current default was 100,100. Years later, cryptocurrency thefts are still being tied to those stolen vaults, and the UK regulator fined LastPass £1.2 million in November 2025.

The lesson is not "password managers are unsafe." It is that a stolen encrypted vault is crackable offline, and its strength is exactly your master password plus the derivation work. A short master password on a weak setting is a vault with a screen door. Pick a manager whose defaults are strong, and give it a master password worth the name — see below.

**1Password, October 2023.** Attackers used data from Okta's support-system breach to reach 1Password's own employee-facing Okta instance. 1Password detected the activity on September 29, terminated it, and found no compromise of user data or other sensitive systems. No customer vault data was accessed.

The lesson is narrower: judge a vendor on architecture and response, not on whether it has ever appeared in an incident report. Every company of this size will. What matters is whether customer data was reachable, and what the company did in the first hours.

One concrete rule from both incidents: do not store cryptocurrency seed phrases in a password manager vault. The LastPass thefts targeted exactly that, and a seed phrase is not a password — it has no second factor and no reset.

## Passwords that actually hold up

- **Length beats complexity.** A four-word passphrase you can remember is stronger than an eight-character soup of symbols you will write on a sticky note. Aim for length; let the generator handle the rest.
- **Unique per site, no exceptions.** This is the entire point of the manager. Reuse is what turns one breach into all of them.
- **Let the generator do it.** Generate, save, and never type a password yourself again. The manager fills it; your job is the one account password.
- **The account password is the one that matters.** It should be a long passphrase you can type from memory — five or six random words, not a pet's name with a digit. Everything in the vault depends on it.

## Two-factor authentication that matters

Turn it on in this order:

1. **Passkeys first, where offered.** A passkey cannot be phished the way a password can, and it replaces the password entirely on that site. Watchtower (1Password) and the health reports (Bitwarden Premium) can show you which of your logins now support one.
2. **Your email, your bank, and the password manager itself.** If an attacker owns your email, they own every password reset. These three get a second factor before anything else.
3. **Authenticator app or hardware key next.** A time-based code from an authenticator app, or a hardware key for the accounts that support one, beats SMS every time. SMS codes can be intercepted or SIM-swapped; use SMS only where nothing better is offered.

One nuance worth knowing: storing one-time codes inside the same vault as the password they protect is convenient, and it weakens the second factor — if the vault is ever opened, both factors go together. For your most important accounts, keep the codes in a separate authenticator app. For the long tail of accounts, the built-in authenticator is a reasonable trade.

## The maintenance schedule

A password manager is not set-and-forget. It is a garden. The schedule:

**Monthly — five minutes.** Open Watchtower or your vault health report. Act on any breach alert the same day: change that password, and check whether you reused it anywhere. Save any new login that is not in the vault yet.

**Quarterly — half an hour.** Work the weak-and-reused list and change the worst five. Check 2FA coverage on email, bank, and the manager itself, and turn it on anywhere missing. Delete accounts you no longer use — every account is an entry point, and the ones you forgot are the ones that get breached quietly. Check shared vaults still have the right people in them.

**Annually — an hour.** Confirm emergency access still points at the right person, and that your recovery kit is printed and stored somewhere a burglar and a house fire cannot both reach. Take an encrypted export and store it with your other backups — encrypted, not in plain text in a cloud folder. Review family plan members and guests. Re-check the prices in this post, because they move.

**When something happens.** A breach notice involving a site you use means changing that password now, not at the next quarterly review. A new phone or laptop means verifying you can still sign in and that recovery works before you wipe the old device. A job change means moving work credentials out of your personal vault and offboarding the old shared vaults.

## Moving without losing anything

Import from wherever your passwords live now — the browser's saved-password export works, and both managers take the file. Then spend one evening fixing the import: the browser will have duplicates, dead accounts, and passwords saved under the wrong site. Turn off the browser's own password saving once the manager is in place, or you will end up with two sources of truth. Keep the old store for a month, then delete it.

## Picking by use

- **Solo:** either pick works. Bitwarden Free costs nothing and covers the whole job; 1Password Individual is the smoother daily experience.
- **Family:** 1Password Families for the easiest sharing and the recovery option for a locked-out member; Bitwarden Families for the same job at $47.88 a year for six. Either way, give everyone their own private vault and share only through shared vaults.
- **Small business:** shared vaults per team or function, a written offboarding step that removes someone from every vault on their last day, and emergency access for at least one other person. This is the same access hygiene as onboarding — the manager just makes it enforceable.

## The short version

Get a manager. Make the account password a long passphrase. Let it generate everything else, unique per site. Turn on passkeys where offered and a second factor on email, bank, and the manager itself. Then keep the schedule — monthly glance, quarterly sweep, annual recovery check — because the manager is the easy part and the maintenance is the work.

*Prices and features checked November 24, 2026. This post is reviewed every six months; the next review is due May 2027.*
