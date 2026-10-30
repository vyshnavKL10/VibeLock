# VibeLock risk model

This is the single source for how VibeLock rates risk. `SKILL.md` (Phase 5) tells the agent when to use it.

**Tiers guide the depth of review. They are not certifications, scores, or guarantees of security.** A project at any tier can still be breached. The tier only answers "how much care does this project deserve?"

## Why not "personal, public, or commercial"?

Those labels are poor predictors. A personal script that holds a billing-enabled cloud key and can delete production data deserves more care than a public brochure site. An internal payroll tool deserves more than a public landing page. VibeLock therefore rates the specific factors below, from evidence, and treats labels as clues to look into.

## Step 1: rate the factors

Rate each factor **Low**, **Medium**, **High**, or **Unknown**, and write down the evidence (file, config, or user statement). Rate high-risk components separately: auth, payments, admin, file upload, webhooks, secrets handling, and MCP tools or bots that can write or execute.

### Likelihood side

| Factor | Low | Medium | High |
|---|---|---|---|
| **Exposure** (who can reach it) | Only the owner, local only | Authenticated users, a known group, an internal network, or an AI agent reading only trusted content | Public internet, anonymous access, widely distributed clients, or an agent that reads untrusted content |
| **Incentive and abuse potential** | Nothing worth taking or abusing | Some value: accounts, compute, a spam relay, scrapable data | Direct gain: payments, credits, valuable data, or free resources attackers target (paid APIs, LLM credits, open relays) |
| **Known weaknesses and maturity** | Framework defaults in use, no known issues | Not yet reviewed, or partial coverage | A confirmed weakness (a FAIL finding), missing basics, or security-critical code that is AI-generated and untested |

**Likelihood** is:

- **High** if Exposure is High and (Incentive is Medium or High, or Weaknesses are High).
- **Low** if Exposure is Low and Weaknesses are not High.
- **Medium** otherwise.

### Impact side

| Factor | Low | Medium | High |
|---|---|---|---|
| **Data sensitivity** | Public or no personal data | Ordinary personal data (names, emails), business data, low-value credentials | Secrets for other systems, financial data, private messages, precise location, health data, children's data |
| **Privilege and blast radius** | Reads own data only | Modifies own or shared data | Reads or modifies other users' data, runs code, deploys, administers accounts, reaches production infrastructure |
| **Financial and business consequence** | Negligible | Noticeable loss or downtime | Significant loss, contractual or legal exposure, the business stops |
| **Affected people** | Only the owner | Tens to hundreds of users | Thousands of users, or vulnerable people |
| **Recoverability and operations** | Restore within hours, no lasting harm | Days of cleanup, some manual repair | Hard to restore or to notify people; long outage |

**Impact** is the highest of these five factors. It is **Severe** instead of High when any of these is true: irreversible harm to people or physical safety; large-scale or regulated high-risk data; large financial loss that can't be recovered; critical infrastructure. Severe is rare. Use it deliberately and write down why.

## Step 2: look up the tier

| Impact \ Likelihood | Low | Medium | High |
|---|---|---|---|
| **Low** | Basic | Basic | Standard |
| **Medium** | Basic | Standard | Standard |
| **High** | Standard | Advanced | Advanced |
| **Severe** | Advanced | Critical | Critical |

The tier decides how many controls apply (see `PLATFORMS.md`, where `[L1+]` means Basic and up, `[L2+]` Standard and up, `[L3+]` Advanced and up). The severity of an individual finding decides how urgent it is. A Basic-tier project can still have a Critical finding, such as a committed live key.

## Step 3: component tiers and the project tier

Rate each high-risk component on its own. The project tier is the highest component tier, but apply controls per component: a Standard project with one Advanced component (payments) gets Advanced controls for that component only. This keeps low-risk parts from being over-engineered.

## Unknowns

- If a factor is Unknown and could change the tier, ask the user (SKILL.md Phase 2).
- If it stays unresolved, use the higher plausible rating, mark the plan **PROVISIONAL**, and list the unknown at the top.
- A provisional tier is never presented as final.

## Worked examples

These are illustrations of the method, not fixed answers.

| Project | Key ratings | Tier |
|---|---|---|
| Public brochure site, static, mailto contact | Exposure High, Incentive Low, Weaknesses Low, so Likelihood Medium. All impact factors Low. | **Basic** |
| Personal script on a laptop using a billing-enabled API key | Exposure Low, so Likelihood Low. Financial Medium. | **Basic**, with strict key handling (ALL-01, ALL-03) |
| Public app with email/password accounts, names and emails, a few hundred users, no payments | Exposure High, Incentive Medium, so Likelihood High. Data Medium, Affected Medium. | **Standard** |
| Same app with an admin panel that can read every account | Admin component: Privilege High, Likelihood High. | Admin component **Advanced**; the rest Standard |
| Internal payroll tool, intranet only, 20 staff | Exposure Medium, so Likelihood Medium. Data High. | **Advanced** |
| Local MCP server with a tool that runs arbitrary SQL against production, reading web content | Exposure Medium (untrusted content reaches the agent), Incentive Medium, so Likelihood Medium. Privilege High. | **Advanced** for that component. "Local" is not "low risk". |
| Patient records system | Data High, Affected High, Recoverability High, regulated: Impact Severe. | **Critical** |

## How a project moves between tiers

**Re-assess when any of these happen:**

- A new kind of data is collected (payments, health, children's data, precise location).
- The app becomes public, or gains a new public endpoint, webhook, or file upload.
- A component gains power: admin features, code execution, write access to production, an AI tool that can act.
- Users or money volume grow substantially.
- A new third-party integration holds credentials or data.
- A security incident or a confirmed weakness changes Likelihood.
- A compliance duty applies (for example, personal data of people in a regulated region).

**Moving down needs evidence and the user's approval.** For example, moving card handling to a provider's hosted checkout can lower a payments component, and shutting a public endpoint lowers Exposure. Record the reason in the plan. Don't lower a tier just because the work is inconvenient.

## What each tier means for the work

| Tier | Depth of review | Typical extra work |
|---|---|---|
| **Basic (L1)** | Light discovery, baseline controls (`[L1+]`), cheap static checks, short report | Secrets hygiene, HTTPS, dependency basics |
| **Standard (L2)** | All `[L2+]` controls, authorization tests for each role, dependency audit, secret scan | Written plan saved with the repo (with the privacy caveat), findings table |
| **Advanced (L3)** | All `[L3+]` controls, a written threat model in the plan, abuse cases, CI/CD and infrastructure review | Separate staging and production, incident basics, independent review recommended before launch |
| **Critical (L4)** | Everything above | Independent review or penetration test, compliance advice, staged rollout, and tested recovery as conditions for launch. VibeLock alone is not sufficient at this tier. |

## Limits of this model

The rubric is a structured way to think, not a formula that produces truth. Two careful people can rate a factor differently. That is why the plan always shows the evidence behind each rating and lets the user challenge it.
