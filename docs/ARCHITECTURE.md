# VibeLock architecture

How the repository is organized and why. For what VibeLock does, see the [README](../README.md).

## The layers

| Layer | File(s) | Purpose | Depends on an agent? |
|---|---|---|---|
| Core workflow | `SKILL.md` | The 12-phase process, ground rules, approval gates, statuses | No. Plain Markdown. |
| Risk model | `docs/RISK_MODEL.md` | How risk is rated and how a project moves between tiers | No |
| Platform guidance | `PLATFORMS.md` | Controls per platform, tagged by tier and classified | No |
| Templates | `examples/REPORT_TEMPLATE.md` | Plan, finding, and report formats | No |
| Agent adapters | none yet | Agent-specific install or loading glue | Yes, by definition |

**Runtime files.** Only `SKILL.md`, `docs/RISK_MODEL.md`, `PLATFORMS.md`, and `examples/REPORT_TEMPLATE.md` are read while the skill runs. The rest is for visitors and maintainers.

**One canonical source for each thing.** The tier rubric lives only in `RISK_MODEL.md`. Controls live only in `PLATFORMS.md`. The statuses are defined in `SKILL.md`. Other files link to them instead of copying them, so a fix is made once.

## How a run flows

```
user request
   |
   v
SKILL.md  --Phase 1-4-->  discover, ask about gaps, map, threats
   |
   +--Phase 5-->  docs/RISK_MODEL.md  -> tier per component
   |
   +--Phase 6-->  PLATFORMS.md (Cross-cutting + matching sections) -> classified controls
   |
   +--Phase 7-->  examples/REPORT_TEMPLATE.md (Plan)  -> user approval
   |
   +--Phase 8-10-> implement, run checks, review own diff
   |
   +--Phase 11-12-> examples/REPORT_TEMPLATE.md (Report) -> unresolved issues, next actions
```

The agent loads the reference files only at the phase that needs them. This keeps the always-loaded part (`SKILL.md`) short and the rest on demand.

## Key decisions, in plain English

**Skill first, no CLI yet.** The hard part of VibeLock is judgment: understanding a project, deciding what matters, and being honest about what was checked. A CLI can't do that. A CLI can do deterministic jobs (detect the stack, scan for secrets, run known checks) and that may be worth building later. Building it now would freeze guesses about what is useful, and would risk implying automated scanning exists when it doesn't.

**Questions come from gaps, not a script.** A fixed questionnaire either asks things the repository already answers or misses things this project needs. `SKILL.md` instead lists the facts that matter and has the agent ask only about the ones it can't find and that would change the plan.

**Tiers guide depth, they don't certify.** A tier says how much care a project deserves. It is built from evidence (exposure, data, privilege, impact, recoverability) instead of labels like "personal" or "commercial".

**Controls are classified, not just listed.** Mandatory, Recommended, Conditional, and Not applicable make the agent explain why a control fits, and let it say "this doesn't apply here" without that being a gap. This is also how an over-the-top request (say, a WAF for a static page) gets rejected.

**Six statuses, with no "pass by default".** PASS needs evidence. NOT TESTED is never counted as PASS. NOT APPLICABLE is not a gap. This is the main defence against a security report that sounds more confident than the work behind it.

**Reference files are linked by relative path.** The skill folder can be cloned or copied anywhere and keep working, as long as the folder structure stays intact.

## Agent compatibility

The methodology is plain Markdown and does not mention an agent-specific mechanism, except one optional hint to use a structured question tool if the agent has one.

| Target | How it is meant to load | Status |
|---|---|---|
| Claude Code | Folder at `.claude/skills/vibelock/` (project) or `~/.claude/skills/vibelock/` (user) with `SKILL.md` at its root | Documented skill convention. **Not yet tested end to end by the authors.** |
| Claude (claude.ai) | Upload of a packaged `.skill` file | The package passes the skill validator. **Upload and behaviour not tested by the authors.** |
| Other agents (Cursor, Antigravity, Codex, and others) | No adapter provided | **Unsupported until an adapter is explained and validated.** You can point an agent's instruction file at `SKILL.md`, but results are unknown. |

Reading Markdown is not the same as supporting a skill. Each agent has its own way to discover instructions, load referenced files, ask questions, and run commands. An adapter should be added only when its author can explain that agent's convention and show that the skill loads and the workflow runs on that agent.

**Adapter rule:** an adapter may contain installation glue and a pointer to `SKILL.md`. It must not copy the methodology. If an agent needs different wording, change `SKILL.md` for everyone or document the limitation.

## Future deterministic checks (proposed, not implemented)

There is no `vibelock` command today. If one is ever built, the commands below are the current idea:

| Proposed command | Idea |
|---|---|
| `vibelock init` | Detect the stack and write a draft fact table for the agent to confirm |
| `vibelock analyze` | Produce the discovery output (files, entry points, data, exposure) deterministically |
| `vibelock check` | Run supported checks and emit evidence records |

The skill is written so that such a tool could slot in without changing the methodology. The seam is the **evidence record**: each check yields an ID (matching a control ID in `PLATFORMS.md`), a status from the six statuses, the command that ran, and a short output summary. The agent would treat tool output exactly like any check it ran itself: cite it, and never upgrade a missing result to PASS. Until a tool exists, the agent produces these records by hand in the report.

Rules for any future tool: stdlib or well-known dependencies only, no network calls without opt-in, no telemetry, and it never prints secret values.
