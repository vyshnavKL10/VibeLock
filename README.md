<p align="center">
  <img src="vibelock-banner.png" alt="VibeLock Banner" width="100%">
</p>

# VibeLock

**Build fast. Secure by default.**

VibeLock is a project-aware security framework for AI-assisted software development. It is a skill: a set of Markdown instructions that makes an AI coding agent understand your project first (purpose, stack, data, users, exposure), work out what security it actually needs, plan it, get your approval, implement it, verify it with evidence, review its own changes, and report honestly what was and was not checked.

It adapts to the project. A static brochure site and a payments backend get different plans, and an agent following VibeLock is expected to explain why each control applies and to say "this doesn't apply here" when it doesn't.

## What VibeLock is not

- Not a vulnerability scanner. It runs no scans by itself. The agent runs whatever checks exist in your environment and reports what ran.
- Not a checklist applied to every project, and not a collection of prompts.
- Not a certification or guarantee. Risk tiers guide how deeply a project is reviewed. A project at any tier can still be breached.
- Not a replacement for a security professional, a penetration test, or compliance advice.
- Not a CLI. There is no `vibelock` command today (see the roadmap).

## Status (version 0.4.0)

| Area | State |
|---|---|
| Workflow (`SKILL.md`), risk model, platform controls, report templates | **Written.** Content has not been reviewed by an independent security professional. |
| Built-in assessments: dependency security, secret exposure, secure code review | **Written as agent procedures.** They use scanners you already have installed. None is bundled or required. The shell commands in them were run against a throwaway test repository. **An agent has not yet run the assessments on real projects.** |
| Install paths for Claude Code, OpenAI Codex, Cursor, GitHub Copilot, Gemini CLI, Google Antigravity, and Windsurf | **Documented** from each vendor's own documentation (checked 2026-10-31). **Not tested in any of those agents by the authors.** See [docs/AGENT_COMPATIBILITY.md](docs/AGENT_COMPATIBILITY.md). |
| Upload to Claude (claude.ai) as a `.skill` file | **Not yet tested.** The package passes the skill validator. |
| Other agents | **Not verified.** A fallback through `AGENTS.md` is described in the compatibility guide, and is untested. |
| Platform guidance for Android, iOS, Huawei, desktop, MCP, bots, internal tools | **Initial guidance, less tested.** Verify against current vendor documentation. |
| CLI (`vibelock init`, `vibelock analyze`, `vibelock check`) | **Planned, does not exist.** |

## How it works

The agent follows 12 phases, scaled to the size of the request:

1. Discover the project from its files.
2. Identify unknowns and ask only the questions that would change the plan.
3. Map assets, data flows, trust boundaries, identities, and dependencies.
4. Identify realistic threats and abuse cases.
5. Assess and explain risk ([docs/RISK_MODEL.md](docs/RISK_MODEL.md)).
6. Build a prioritized plan from the controls in [PLATFORMS.md](PLATFORMS.md).
7. Present the plan and get approval for consequential changes.
8. Implement the approved controls in small steps.
9. Run relevant tests and checks, where tools and permissions allow.
10. Review the changes for regressions and new risks.
11. Produce an evidence-based report ([examples/REPORT_TEMPLATE.md](examples/REPORT_TEMPLATE.md)).
12. List unresolved issues and next actions.

It works for new projects (the plan shapes design choices) and existing codebases (find weaknesses first, avoid rewrites). Small requests get a light pass with zero or one question, not a questionnaire. Every run ends with a short security summary after the agent's normal summary of its work.

### Built-in assessments

Three assessments are part of the workflow. Each is scoped in the plan from your stack and risk tier, uses only the tools you already have, and ends with an honest status.

| Assessment | What the agent does | Tools |
|---|---|---|
| **Dependency security** ([procedure](assessments/DEPENDENCIES.md)) | Finds manifests and lockfiles (npm, pnpm, Yarn, Python, Java and Kotlin, Rust, Go, PHP, .NET, and more). Uses an installed audit tool or an advisory lookup. Keeps confirmed vulnerabilities apart from merely outdated packages and unverified suspicions. Checks whether the dependency is really used, traces transitive paths, and proposes the smallest safe upgrade. | Optional: ecosystem audit tools, network access |
| **Secret exposure** ([procedure](assessments/SECRETS.md)) | Looks for credentials in files, config, and git history. Reports only type, file, and location, never the value. Recommends rotation when exposure is credible. Never changes or deletes a secret without approval, and never tests a credential against its provider. | Optional: a secret scanner. Without one, git history can't be fully checked, and the report says so. |
| **Secure code review** ([procedure](assessments/CODE_REVIEW.md)) | Traces how untrusted input reaches dangerous operations in the code that matters for this project, instead of flagging generic patterns. Reports confidence and what it couldn't verify. | Optional: static analyzers |

It never upgrades a dependency, rotates a credential, or rewrites history without your approval. "No confirmed findings in the reviewed scope" never means "secure".

### Risk tiers

| Tier | Meaning |
|---|---|
| Basic | Low impact, low likelihood. Baseline controls and cheap checks. |
| Standard | Real users or data. Authorization tests, dependency and secret checks, written plan. |
| Advanced | High impact or privilege (payments, admin power, sensitive data). Threat model, infrastructure and CI/CD review, independent review recommended. |
| Critical | Severe or irreversible harm, or regulated high-risk data. Independent review and compliance advice before launch. |

Tiers come from evidence (exposure, incentive, weaknesses, data, privilege, financial and operational impact, recoverability), not from labels like "personal" or "commercial". High-risk components are rated separately. Details and examples are in [docs/RISK_MODEL.md](docs/RISK_MODEL.md).

### Result statuses

| Status | Meaning |
|---|---|
| PASS | The check ran and the output shows the requirement is met |
| FAIL | The check ran and the requirement is not met |
| NOT TESTED | No check was run. Not a pass. |
| BLOCKED | A check was needed but couldn't run |
| NEEDS REVIEW | A person must judge it |
| NOT APPLICABLE | The control doesn't apply to this project (with the reason) |

## Install

VibeLock follows the open [Agent Skills](https://agentskills.io/) format. The skill directory must be named `vibelock`, with `SKILL.md` directly inside it.

### Quick Install

Clone VibeLock directly into your AI coding agent's skills directory.

**Codex / Cursor / Gemini CLI**

```bash
git clone https://github.com/vyshnavKL10/VibeLock.git .agents/skills/vibelock
```

**Claude Code**

```bash
git clone https://github.com/vyshnavKL10/VibeLock.git .claude/skills/vibelock
```

**Google Antigravity**

```bash
git clone https://github.com/vyshnavKL10/VibeLock.git .agent/skills/vibelock
```

**GitHub Copilot**

```bash
git clone https://github.com/vyshnavKL10/VibeLock.git .github/skills/vibelock
```

**Windsurf**

```bash
git clone https://github.com/vyshnavKL10/VibeLock.git .windsurf/skills/vibelock
```

Run the command from your project's root directory. Choose the path matching your agent.

### Multiple Agents

You can share one VibeLock installation across compatible agents using symbolic links instead of maintaining multiple copies.

First, install VibeLock in the shared directory:

```bash
git clone https://github.com/vyshnavKL10/VibeLock.git .agents/skills/vibelock
```

Then create symbolic links for agents that require a different directory.

**Claude Code**

```bash
mkdir -p .claude/skills
ln -s ../../.agents/skills/vibelock .claude/skills/vibelock
```

**Windsurf**

```bash
mkdir -p .windsurf/skills
ln -s ../../.agents/skills/vibelock .windsurf/skills/vibelock
```

**Antigravity**

```bash
mkdir -p .agent/skills
ln -s ../../.agents/skills/vibelock .agent/skills/vibelock
```

Only create links for agents that do not already discover the shared directory.

> **Windows:** Symbolic links may require Developer Mode or administrator permissions. Alternatively, copy the VibeLock folder manually and keep the copies synchronized.

### Updating VibeLock

If installed using Git, navigate to the installation directory and pull the latest changes.

```bash
cd .agents/skills/vibelock
git pull
```

For other installation paths, use the corresponding directory.

### Managing Your Installation

A cloned repository contains its own `.git` directory. Choose one:

- **Personal use:** Add the installation directory to your project's `.gitignore`.
- **Team use:** Add VibeLock as a Git submodule to pin a specific commit and share it with your team.
- **Manual installation:** Copy the skill files without the `.git` directory.

### Security Note

VibeLock contains instructions that influence how your AI coding agent works. Install it only from the official repository. Review changes before updating, consider pinning a specific commit for team use, and keep your agent's trust and approval controls enabled.

### Agent Compatibility

Installation paths and discovery behavior can differ between agent platforms and versions. See [Agent Compatibility](docs/AGENT_COMPATIBILITY.md) for platform-specific paths, official documentation links, and multi-agent setup instructions.

Documented compatibility does not necessarily mean behavioral testing has been completed by the VibeLock authors.

### Agents without skills support

An `AGENTS.md` pointer to `SKILL.md` is described in the compatibility guide. It is untested.

## Invoke

Describe the task in plain language. The agent decides to load the skill from its description, or you can ask for it by name:

- "Use VibeLock to make a security plan for this project."
- "Is this ready to ship? Check it with VibeLock."
- "Add login and payments to this app, securely, using VibeLock."
- "Review the security of this MCP server with VibeLock."

Expect discovery and questions first, a plan second, and changes only after you approve.

## Check that it loaded

In a fresh session, ask:

> Use VibeLock. Summarize its 12 phases in one line each, and tell me which files you would read at Phase 5 and Phase 6.

A loaded skill answers with the phases from `SKILL.md` and names `docs/RISK_MODEL.md` and `PLATFORMS.md`. If it answers from general knowledge or can't find them, the skill did not load. Check the folder name and that `SKILL.md` is directly inside it. Agent-specific commands are listed in [docs/AGENT_COMPATIBILITY.md](docs/AGENT_COMPATIBILITY.md#check-that-it-loaded).


## Repository layout

```
VibeLock/
├── SKILL.md                    core workflow (the skill)
├── PLATFORMS.md                controls per platform, tagged by tier and class
├── README.md
├── LICENSE
├── SECURITY.md                 how to report a problem in VibeLock
├── CONTRIBUTING.md
├── .gitignore
├── docs/
│   ├── AGENT_COMPATIBILITY.md  install path for each agent, with sources and limits
│   ├── ARCHITECTURE.md         layers, decisions, agent compatibility, future CLI seam
│   ├── RISK_MODEL.md           how risk is rated, tier definitions, movement between tiers
│   └── THREAT_MODEL.md         how VibeLock itself could fail or be abused
├── examples/
│   └── REPORT_TEMPLATE.md      plan, finding, and report templates
└── assessments/
    ├── DEPENDENCIES.md         dependency security procedure
    ├── SECRETS.md              secret exposure procedure
    └── CODE_REVIEW.md          secure code review procedure
```

## Safety principles

- No guessing. Facts are labelled Confirmed, Assumption, Unknown, or Needs approval.
- Never claims a check passed unless it ran and left evidence.
- Treats project content as data, never as instructions.
- Never exposes secrets or personal data in code, reports, or logs.
- Doesn't upgrade dependencies, rotate credentials, delete files, or rewrite history without your approval.
- Uses established libraries and platform mechanisms, never custom cryptography.
- Tests only systems you own or are authorized to test. No destructive tests or production changes without explicit approval.

## Reporting vulnerabilities

If you find guidance in VibeLock that could lead to an insecure outcome, or a way the skill could be abused, see [SECURITY.md](SECURITY.md). Please don't post details publicly first.

## Roadmap (proposed, not implemented)

- Try the skill on real projects in Claude Code and fix what that reveals.
- Add an agent adapter only after its author can explain that agent's convention and shows that the skill loads and the workflow runs on that agent.
- A possible small CLI for deterministic jobs (stack detection, dependency audits, secret scanning, running checks). Whether it is worth building depends on how real-world use goes.
- Independent review of the platform guidance, starting with Android, iOS, Huawei, desktop, and MCP.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).

## Disclaimer

VibeLock provides guidance and a workflow, as is, without warranty. It can't guarantee that software is secure. You remain responsible for your project's security.

## Author

Maintained by vyshnavKL10.

- GitHub: [vyshnavKL10](https://github.com/vyshnavKL10)
- Instagram: [@whyshnav_10](https://www.instagram.com/whyshnav_10)
- Discord: whyshnav_10

Please report security problems through [SECURITY.md](SECURITY.md), not through social media.
