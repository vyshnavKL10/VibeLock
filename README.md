# VibeLock

**Build fast. Secure by default.**

VibeLock is an agent-independent, project-aware security workflow for software built with AI coding agents. Instead of applying the same checklist to every project, it makes the agent understand the project first, work out what security it actually needs, get your approval, implement the controls, and report honestly what was and wasn't verified.

## Status

**Version 0.1, early.** Please read this before relying on it.

- It is a **skill-only** release: three Markdown files. There is **no CLI**, no scanner, and no automation bundled. The agent following the skill runs the checks, using whatever tools exist in your environment.
- It has **not yet been tested across agents**. The first target is **Claude Code**. Support for Claude (claude.ai), Cursor, Antigravity, and other agents is planned but unproven. Until tested, treat anything else as experimental.
- The platform guidance has **not been validated against real-world projects**. Mobile (Android, iOS, Huawei), desktop, and MCP sections are initial guidance.
- VibeLock reduces risk. It does **not** guarantee security, and it is not a substitute for a professional review or penetration test.

## What it does

1. **Discovers** the project from its files before asking you anything.
2. **Separates** confirmed facts, assumptions, unknowns, and decisions that need your approval.
3. **Asks** a few questions, written from what it found in your project, only where the answer could change the plan. There is no fixed questionnaire.
4. **Maps** assets, trust boundaries, and realistic threats.
5. **Rates risk** (Level 1 to 4) from impact, exposure, data sensitivity, privilege, abuse potential, and recoverability, assessing high-risk components like auth and payments separately.
6. **Selects** only the controls that fit your stack and level, and explains why each one fits.
7. **Asks for approval** before consequential changes.
8. **Implements** controls in small, reviewable steps, preserving existing behaviour.
9. **Verifies** with checks it actually ran.
10. **Reports** results, limitations, and residual risk.

If information is missing, the plan is marked **PROVISIONAL**.

## Risk levels

| Level | Name | Typical situation |
|---|---|---|
| 1 | Basic | Local or personal use, no sensitive data, easy recovery |
| 2 | Standard | Public or multi-user, accounts or personal data |
| 3 | Advanced | Payments, admin power, health or financial data, many users |
| 4 | Critical | Irreversible, safety-critical, regulated, or large-scale money movement |

These levels are provisional heuristics. The agent shows its reasoning and you can override it.

## Result statuses

Every check is reported as one of:

| Status | Meaning |
|---|---|
| PASS | The check ran and the output shows the requirement is met |
| FAIL | The check ran and the requirement is not met |
| NOT TESTED | No check was run (not a pass) |
| BLOCKED | A check was needed but could not run |
| NEEDS REVIEW | A person must judge it |

VibeLock never reports PASS for something that didn't run.

## Install

### Claude Code (primary target)

Per project:

```bash
git clone https://github.com/<your-username>/vibelock.git .claude/skills/vibelock
```

Or for all your projects:

```bash
git clone https://github.com/<your-username>/vibelock.git ~/.claude/skills/vibelock
```

Replace `<your-username>` with the account hosting the repository.

### Claude (claude.ai / desktop)

Package the folder as a `.skill` file and upload it under Settings, then Skills. Skill upload options depend on your plan and organization. This route is untested.

### Other agents (experimental, untested)

Adapters are not provided yet. In principle, you can point the agent's instruction file (for example `AGENTS.md` or its rules directory) at `SKILL.md` and `PLATFORMS.md`. Results will vary and haven't been verified. Reports of what works are welcome.

## Usage

Ask your agent in plain language, for example:

- "Use VibeLock to make a security plan for this project."
- "Is this ready to ship? Check it with VibeLock."
- "Add login and payments to this app, securely."
- "Review the security of this MCP server."

Expect questions first, a plan second, and changes only after you approve.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | The workflow: discovery rules, risk assessment, approval gates, verification, reporting |
| `PLATFORMS.md` | Controls per platform, tagged by minimum risk level and read only when relevant |
| `README.md` | This file |

## Skill format

VibeLock follows the standard skill layout: one `SKILL.md` with YAML frontmatter (`name`, `description`, `compatibility`) and a short, instruction-style body, plus a reference file (`PLATFORMS.md`) the agent reads only when relevant. The folder name must stay `vibelock` and the repository must contain exactly one `SKILL.md`.

## Safety principles

- No guessing, no silently assuming a project is private or low-risk.
- Never exposes secrets in code, reports, or logs.
- Uses established libraries and platform mechanisms, never custom cryptography.
- Only tests systems you own or are authorized to test.
- Requires explicit approval before destructive actions or production changes.

## Roadmap (proposed, not implemented)

These are ideas, not features. Nothing below exists yet.

- Testing and tightening the skill with real projects, starting with Claude Code.
- Adapters for other agents, added only after each is tested.
- A possible small CLI (`vibelock init`, `vibelock analyze`, `vibelock check`) for the deterministic parts such as stack detection and running checks. Whether it's worth building depends on what v0.1 shows.
- Deeper per-platform guidance where the current sections are thin.

## Contributing

Issues and pull requests are welcome, especially real-world test reports, corrections to platform guidance, and tested agent adapters. Please keep the core logic agent-independent and avoid claiming support that hasn't been tested.

## License

MIT. See [LICENSE](LICENSE).

## Disclaimer

VibeLock provides guidance and a workflow, provided as is, without warranty. It can't guarantee that software is secure. You remain responsible for your project's security.
