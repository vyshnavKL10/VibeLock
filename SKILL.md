---
name: vibelock
description: Project-aware security planning, implementation and verification for software built with AI coding agents. Use this whenever the user mentions security, hardening, "secure by default", vulnerabilities, API keys or secrets, login/auth, payments or webhooks, deployment, VPS or server setup, CI/CD, releasing a mobile or desktop app, MCP servers or tools, or asks "is this safe?" or "is this ready to ship?". Also use it when starting or reviewing any project that will handle users, personal data, money, or public traffic, even if the user never says "security". Do NOT use for formal compliance audits or penetration tests (it can prepare for them but cannot replace them), or for general coding tasks with no security angle.
compatibility: Designed for coding agents that can read and edit project files and run shell commands. Primary target is Claude Code. No dependencies and no bundled scripts.
---

# VibeLock

Build fast. Secure by default.

VibeLock is a workflow, not a checklist. Its job is to understand the project, work out what security it actually needs, plan that, get approval, implement it, verify it with evidence, and report honestly what is and is not covered.

**Plan before you protect.** Do not add controls until you understand the project well enough to justify each one.

Version 0.1. Skill-only. There is no CLI and no automated scanner bundled with this skill; any checks are run by you, the agent, using tools available in the user's environment.

## Ground rules

These exist because a security plan built on guesses, or a report that claims more than was checked, is worse than none: it gives false confidence.

1. **No guessing.** Never invent requirements. Never silently assume the app is private, single-user, internal-only, or free of sensitive data. If you don't know, it is Unknown, and you either ask or mark the plan provisional.
2. **Evidence before questions.** Inspect the project before asking anything the files already answer.
3. **Label everything.** Every statement in the plan is one of: **Confirmed** (seen in files or stated by the user), **Assumption** (your inference, to be validated), **Unknown** (missing), or **Needs approval** (a consequential decision).
4. **Never promise security.** Do not say "secure", "safe", or "100%". Say what was checked, what was found, and what remains.
5. **Never claim a check passed unless it ran** and you can cite the command and its output. See "Result statuses".
6. **Never expose secrets.** Not in code, plans, reports, logs, or chat. Report a secret's location and type, never its value.
7. **Preserve behaviour.** Prefer small, targeted changes over rewrites. Don't change what the app does unless that is the fix, and say so when it is.
8. **Use established mechanisms.** Use the framework's or platform's security features and well-maintained libraries. Never invent cryptography, password hashing, token formats, or session handling.
9. **Stay in authorized territory.** Only test what the user owns or is authorized to test, preferably local or staging. Never scan third-party systems.
10. **No destructive or production actions without explicit approval.** This includes deleting data, rewriting git history, changing firewall or SSH settings, rotating keys, migrating databases, and touching anything deployed.

## Workflow

Follow these phases in order. Do not skip ahead to implementation. For a small, well-understood request (for example "add security headers to this Express app"), keep the phases short, but still confirm what the project is and what level it needs.

### Phase 1: Discover

Read what exists before asking. Look for, as applicable:

- Docs and intent: README, docs, package descriptions, issue/PR notes.
- Stack: package.json, requirements.txt, pyproject.toml, go.mod, Cargo.toml, Gemfile, composer.json, pom.xml, build.gradle, pubspec.yaml, Podfile, AndroidManifest.xml, Info.plist, and the main source layout.
- Entry points and trust boundaries: routes/controllers, API handlers, webhook handlers, middleware, auth modules, file upload code, background jobs, MCP server definitions and tool lists.
- Data: DB schema, migrations, ORM models, any field that looks like personal, financial, health, or credential data.
- Deployment: Dockerfile, docker-compose, Kubernetes or Terraform files, server config, reverse proxy config, hosting config.
- Pipeline: .github/workflows, .gitlab-ci.yml, other CI files.
- Config and secrets hygiene: .gitignore, .env.example, config files. For real `.env` or key files, note that they exist and list variable **names only**. Do not print values.
- Integrations: third-party SDKs, payment providers, OAuth providers, external APIs.

If git history is available and a secret scanner is installed, scanning history is worthwhile. If no scanner is installed, say so and mark it NOT TESTED rather than skimming by eye and declaring it clean.

### Phase 2: Record what you know, and what would change the plan

Write a short fact table, one line per item, each marked Confirmed, Assumption, Unknown, or Needs approval.

```
| Item                 | Status      | Detail / source                     |
|----------------------|-------------|-------------------------------------|
| Language / framework | Confirmed   | Next.js 14, package.json            |
| Database             | Confirmed   | Postgres via Prisma, schema.prisma  |
| Public exposure      | Unknown     | No deploy config found              |
| Stores personal data | Assumption  | `users` table has email, name       |
| Payments             | Unknown     | Stripe SDK present, usage unclear   |
```

Every project needs these decision-critical facts settled, because they decide the risk level and which controls apply. They are facts to establish, not questions to read out. Find what you can from the files first.

| Fact | Why it matters | Look first |
|---|---|---|
| What the app does, who uses it | Impact, abuse potential | README, UI copy, routes |
| Who can reach it (owner, team, logged-in users, public) | Exposure | Deploy config, bind addresses, auth middleware |
| Data it stores (personal, credentials, payment, health, children's, other systems' secrets) | Sensitivity, legal duties | Schema, models, forms |
| Accounts and roles | Which authorization controls apply | Auth module, role checks |
| Money flows | Payment and webhook controls | Payment SDKs, webhook routes |
| Integrations and tool power | Trust boundaries | Dependencies, env var names, MCP config |
| Where it runs and who has access | Which platform sections apply | Dockerfile, IaC, CI files, manifests |
| Worst realistic outcome and recoverability | Risk level | Usually only the user knows |
| Safe, authorized test environment | Verification scope | Usually only the user knows |
| Scale now and in 12 months, compliance duties | Level, controls | Usually only the user knows |

### Phase 3: Ask only about the gaps that matter

There is no fixed question list. Questions come from the Unknown rows in your own fact table, written for this project.

- **Ask only if the answer could change the risk level or add or drop a control.** If it wouldn't, note it and move on.
- **Write each question from what you found.** "I found a Stripe SDK in package.json but no webhook route. Are you taking payments yet?" is better than "Do you take payments?"
- **Propose and confirm when you can infer.** "This looks like a public app with email/password accounts storing names and emails. Is that right, and is anything more sensitive stored?" lets the user fix it in one reply.
- **Some facts only the user knows** (worst outcome, authorization to test, growth, compliance). Ask for these when the plan depends on them, together in one batch.
- **At most 5 questions at a time**, ranked by how much each would change the plan. Prefer multiple choice, and always allow "I don't know".
- **Use your agent's structured question tool if it has one** (for example AskUserQuestion in Claude Code). Otherwise ask in plain text.
- **Match the size of the request.** A narrow task ("add security headers to this Express app") needs zero or one question. A new product or a pre-launch review needs more.
- **Never ask what the files already answered**, and never ask just to follow a script.

If the user doesn't know or declines, record it as Unknown, mark the plan **PROVISIONAL**, list the unknowns at the top, and choose the cautious option for any decision that depends on them. Don't ask again unless new information appears.

### Phase 4: Map assets, trust boundaries, and threats

Keep this lightweight and specific to the project. Produce:

- **Assets:** what is worth protecting (user data, credentials, payment flows, admin access, API keys, availability, reputation).
- **Trust boundaries:** where data crosses from less trusted to more trusted (browser to API, API to DB, webhook to server, user input to a shell, tool output to an AI agent, CI to production).
- **Realistic threats:** the few that actually apply (for example "a logged-in user reads another user's records by changing an ID", "forged webhook marks an order as paid"). Do not paste a generic threat catalogue.

### Phase 5: Determine the risk level

Rate each factor Low, Medium, High, or Unknown.

| Factor | Question |
|---|---|
| Impact | How bad is a compromise: inconvenience, financial or reputational loss, legal harm, or harm to people? |
| Exposure | Who can reach it: only the owner, authenticated users, or the public internet? |
| Data sensitivity | Public or none, personal contact data, or credentials, financial, health, children's data, other systems' secrets? |
| Privilege | What can the component do: read own data, modify others' data, run code, move money, deploy, administer? |
| Abuse potential | How attractive and easy to abuse (spam, fraud, cost abuse, account takeover, scraping)? |
| Recoverability | Easy restore, hard restore, or irreversible? |

Provisional levels. This is a heuristic: show your reasoning, and the user may override it with sign-off.

- **Level 1, Basic:** all factors Low. Local or personal use, no sensitive data, easy recovery.
- **Level 2, Standard:** any factor Medium, or public exposure with user accounts or personal data.
- **Level 3, Advanced:** any High in Impact, Data sensitivity, or Privilege (for example payments, admin power, health or financial data, many users).
- **Level 4, Critical:** High plus irreversible harm, safety-critical or regulated context, large-scale money movement, or critical infrastructure.

Rules:

- **Assess high-risk components separately.** Auth, payments, admin, file upload, webhooks, secrets handling, and MCP tools with write or execute power each get their own level. The project level is the highest component level, but apply controls per component so low-risk parts are not over-engineered.
- **Unknowns:** if an Unknown could change the level, ask. If it cannot be resolved, use the higher candidate level and mark the plan provisional.
- **Re-assess** when the project changes materially (new payment flow, new public endpoint, new data type, new platform).

### Phase 6: Select controls

1. Read `PLATFORMS.md`, and **only the sections that match the discovered stack** (always the Cross-cutting section). Do not load or recommend sections that do not apply.
2. Each control there has an ID and a minimum level, like `API-01 [L1+]`. Include a control if the component's level is at or above its tag.
3. For each selected control, write one line on **why it fits this project**. If you cannot say why, drop it.
4. Note controls you skipped on purpose (not applicable, or deferred) so the user can see the decision.
5. Where the existing code already satisfies a control, mark it Confirmed with the file reference rather than re-implementing it.

### Phase 7: Present the plan and get approval

Present the plan in chat first, using this template:

```
# Security plan: <project>   [PROVISIONAL if applicable]

## Summary
One paragraph: what the project is and the overall level, with the reasoning.

## Facts
Confirmed / Assumptions / Unknowns (from Phase 2)

## Assets, boundaries, threats
(from Phase 4)

## Risk levels
Overall: Level N. Per component: ...

## Proposed controls
| ID | Control | Why it fits | Effort | Needs approval? |

## Deferred / not applicable
...

## Decisions I need from you
1. ...
```

**Needs approval** (do not do these without an explicit yes):

- Changes to the auth, session, or permission model.
- Database schema changes or data migrations.
- Firewall, SSH, server, DNS, or infrastructure changes.
- Anything that touches production or other remote systems.
- Adding or swapping third-party services or major dependencies.
- Rotating or revoking keys (explain what will break).
- Rewriting git history or deleting anything.
- Active or dynamic testing, and installing tools globally.
- Anything that affects billing.

After approval, offer to save the plan as `SECURITY_PLAN.md` in the project root. It must never contain secret values. If the repository is public, warn the user that a plan listing open weaknesses is useful to attackers, and suggest keeping detailed findings in a private place.

### Phase 8: Implement

- Work one control at a time, in small changes the user can review.
- Match the project's existing style, structure, and framework conventions.
- Add or update tests alongside each control where the project has a test setup (for example, a test that user A gets 403 when requesting user B's record).
- Keep secrets in environment variables or a secret manager. Add `.env` to `.gitignore` and commit only `.env.example` with placeholders.
- If a secret was ever committed, treat it as compromised: **rotate it first** (with approval); cleaning history comes second and does not make the old secret safe.
- Verify any package an AI suggests actually exists and is the intended, maintained one before installing it. Hallucinated and look-alike package names are a real supply-chain risk.
- If scope grows beyond the approved plan, stop and ask.

### Phase 9: Verify

Run what is available and report evidence. Defaults:

- **Static and local checks first:** project tests, linters, the ecosystem's dependency audit (`npm audit`, `pip-audit`, `cargo audit`, and similar), secret scanners or static analyzers if already installed (for example gitleaks, Semgrep, Bandit), and reading config files to confirm settings.
- **Don't install tools** without asking. If a tool is missing, the check is NOT TESTED, and you can offer an install.
- **Dynamic checks** (hitting a running app, probing headers, attempting auth bypass) only against a local or staging system the user owns, and only after the user confirms it is authorized. Never against production unless the user explicitly authorizes it, and never against third parties.
- **Tests you write count as evidence** only if you actually ran them and they ran green. Show the command and the result summary.
- Do not repeat secret values that tools print. Mask them in anything you report.

### Result statuses

Use exactly these, per control or check:

| Status | Meaning |
|---|---|
| PASS | The check ran and the output shows the requirement is met. Cite the command and a summary of the result. |
| FAIL | The check ran and the requirement is not met. |
| NOT TESTED | No check was run (tool missing, out of scope, or not requested). This is not a pass. |
| BLOCKED | A check was needed but couldn't run (no access, missing permission, no safe environment, approval not given). |
| NEEDS REVIEW | Can't be confirmed automatically. A person or specialist must judge it. |

If you are unsure whether something qualifies as PASS, it is not PASS.

### Phase 10: Report

```
# VibeLock report: <project>   [PROVISIONAL if applicable]
Date: ...   Overall level: N   Scope: what was and was not examined

## Results
| ID | Control | Status | Evidence (command / file / summary) |

## Findings to fix
Ordered by severity, each with location and suggested fix (no secret values).

## What changed
Files modified and why.

## Not covered / limitations
What was not inspected, what could not be tested, and why.

## Residual risk
What could still go wrong, in plain language, and what would reduce it next.

## Open decisions and unknowns
...
```

Close with a plain statement: this reduces risk and is not a guarantee. A professional review or penetration test is advisable at Level 3 and above, and before handling payments or regulated data at scale.

## Maintaining the plan

When the project changes (new features, integrations, platforms, exposure, or data), re-run Phases 1 to 5 for the affected components and update the plan. If the user asks for a quick check, still state the level you are assuming and what you did not look at.

## What VibeLock does not do

It does not replace a security professional, a penetration test, or compliance certification. It does not monitor a running system. It does not guarantee anything. It is only as good as the information and checks behind it, which is why the report always lists its limits.
