# VibeLock architecture

How the repository is organized and why. For what VibeLock does, see the [README](../README.md).

## The layers

| Layer | File(s) | Purpose | Depends on an agent? |
|---|---|---|---|
| Core workflow | `SKILL.md` | The 12-phase process, ground rules, approval gates, statuses | No. Plain Markdown. |
| Risk model | `docs/RISK_MODEL.md` | How risk is rated and how a project moves between tiers | No |
| Platform guidance | `PLATFORMS.md` | Controls per platform, tagged by tier and classified | No |
| Assessments | `assessments/DEPENDENCIES.md`, `SECRETS.md`, `CODE_REVIEW.md` | Step-by-step procedures for the dependency, secret, and code-review assessments, loaded only when in scope | No |
| Templates | `examples/REPORT_TEMPLATE.md` | Plan, finding, and report formats | No |
| Agent install and fallback | `docs/AGENT_COMPATIBILITY.md` | Install path for each agent, and the `AGENTS.md` pointer fallback. No agent-specific copy of the methodology. | Yes, by definition |

**Runtime files.** Only `SKILL.md`, `docs/RISK_MODEL.md`, `PLATFORMS.md`, `examples/REPORT_TEMPLATE.md`, and the files in `assessments/` are read while the skill runs. The rest is for visitors and maintainers.

**One canonical source for each thing.** The tier rubric lives only in `RISK_MODEL.md`. Controls live only in `PLATFORMS.md`. The statuses are defined in `SKILL.md`. Assessment procedures live only in `assessments/`: `SKILL.md` decides when they run, and `PLATFORMS.md` holds the controls they point to. Install paths per agent live only in `AGENT_COMPATIBILITY.md`. Other files link to these instead of copying them, so a fix is made once.

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
   +--Phase 8-10-> implement; run checks and the in-scope assessments (assessments/*.md); review own diff
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

**Assessments are procedures, not scanners.** Dependency security, secret exposure, and code review are written as step-by-step instructions for the agent, using whatever tools the user already has. Nothing is bundled and nothing is required. When a tool is missing, that part of the assessment says NOT TESTED instead of guessing. Each assessment is its own file so the agent loads only the ones the project needs. Findings carry a class and a confidence, so a confirmed vulnerability, an outdated package, and a hunch are never reported as the same thing.

**Reference files are linked by relative path.** The skill folder can be cloned or copied anywhere and keep working, as long as the folder structure stays intact.

## Agent compatibility

VibeLock is written in the open Agent Skills format: a folder named `vibelock` with `SKILL.md` and reference files. Agents that support the format load that one copy directly, so the methodology is never duplicated per agent. The install path for each agent, how to check that it loaded, and what has and hasn't been verified are kept in one place: [AGENT_COMPATIBILITY.md](AGENT_COMPATIBILITY.md).

The methodology is plain Markdown. It uses only frontmatter fields from the open standard, and its one agent-flavored hint (use a structured question tool if the agent has one) is optional.

Reading Markdown is not the same as supporting a skill. Each agent has its own way to discover instructions, load referenced files, ask questions, and run commands. A row is added to the compatibility guide only when its author can point to the agent's official documentation and says exactly what was and wasn't run.

**Adapter rule:** an adapter may contain installation glue and a pointer to `SKILL.md`. It must not copy the methodology. If an agent needs different wording, change `SKILL.md` for everyone or document the limitation.

## Future deterministic checks (proposed, not implemented)

There is no `vibelock` command today. If one is ever built, the commands below are the current idea:

| Proposed command | Idea |
|---|---|
| `vibelock init` | Detect the stack and write a draft fact table for the agent to confirm |
| `vibelock analyze` | Produce the discovery output (files, entry points, data, exposure) deterministically |
| `vibelock check` | Run supported checks and emit evidence records |

The skill is written so that such a tool could slot in without changing the methodology. The seam is the **evidence record**: each check yields an ID (matching a control ID in `PLATFORMS.md`), a status from the six statuses, the command that ran, and a short output summary. The agent would treat tool output exactly like any check it ran itself: cite it, and never upgrade a missing result to PASS. Until a tool exists, the agent produces these records by hand in the report. Dependency auditing and secret scanning are the most natural first candidates, because their tools already produce structured output, but neither exists as a VibeLock tool.

Rules for any future tool: stdlib or well-known dependencies only, no network calls without opt-in, no telemetry, and it never prints secret values.
