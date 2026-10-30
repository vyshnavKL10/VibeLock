# VibeLock validation plan

How to find out whether VibeLock works, and an honest record of what has and hasn't been tried. Read the [execution log](#execution-log) first if you only want the state of things.

## What "validated" means here

Validation has four levels. Each says something different, and only the first has been done.

| Level | Question it answers | How | State |
|---|---|---|---|
| 1. Structure | Are the files consistent and the skill package valid? | `python3 tests/check_structure.py` and the skill validator | **Executed.** See the log. |
| 2. Load | Does the target agent discover and load the skill? | The load check in the [README](../README.md#check-that-it-loaded) | **Not executed** |
| 3. Behaviour | Given a realistic project, does the agent follow the workflow and reach defensible results? | The ten scenarios below | **Not executed** |
| 4. Correctness of guidance | Are the controls technically right and current? | Review by qualified security people against vendor and standards documentation | **Not executed** |

Passing level 1 says nothing about levels 2 to 4.

## Structural checks (level 1)

`tests/check_structure.py` uses only the Python standard library. It verifies:

- required files exist and there is exactly one `SKILL.md`;
- frontmatter keys, name format, and description length follow the skill rules;
- every control in `PLATFORMS.md` has a well-formed tier tag and a unique ID;
- control IDs referenced in `tests/`, `docs/`, `SKILL.md`, and `README.md` exist;
- relative Markdown links resolve;
- all six statuses appear in `SKILL.md`, `README.md`, and the report template;
- each scenario has the required sections and at least four numbered pass criteria;
- the README install path matches the skill folder name, and no unreplaced username placeholder remains.

It warns, without failing, when the LICENSE still has its copyright-holder placeholder. It does **not** check that external links resolve, and it can't judge whether guidance is correct.

## Running a behaviour scenario (levels 2 and 3)

1. Install VibeLock into the agent as the README describes, and complete the load check.
2. Build the fixture described in the scenario file in an empty folder. Use only fake values. Never put a real secret in a fixture.
3. Start a **fresh** agent session in that folder. Give the exact prompt from the scenario. Don't coach the agent.
4. Answer the agent's questions truthfully for the fixture, and approve or decline its requests as the scenario describes.
5. Save the transcript locally (the `.gitignore` already excludes `/transcripts/`).
6. Score every numbered pass criterion as met or not met, using only the transcript and the resulting files.

**Scoring.** A scenario passes only if every pass criterion is met. Record unmet criteria by number. Language models vary between runs, so run each scenario **three times** and record all three results. Treat a scenario as reliable only if it passes all three.

**Recording.** Add a row to the execution log with the date, the agent and its version, the scenario, the outcome of each run, and a link to notes. Do not record a scenario as passed from memory.

## Scenario index

| # | Scenario | What it mainly tests |
|---|---|---|
| 01 | [Static website](../tests/01-static-website.md) | Proportionality, minimal questions, NOT APPLICABLE handling |
| 02 | [Web app with authentication and roles](../tests/02-web-app-auth-roles.md) | Component-level tiers, authorization tests, approval gates |
| 03 | [API with a database](../tests/03-api-with-database.md) | Finding injection and over-privilege, evidence-based statuses, secret handling |
| 04 | [Android app](../tests/04-android-app.md) | Platform selection, extractable secrets, honest build checks |
| 05 | [MCP server with external-resource tools](../tests/05-mcp-server.md) | Tool-risk analysis, prompt-injection resistance, approval before permission changes |
| 06 | [VPS-hosted application](../tests/06-vps-hosted-app.md) | No access to the live server, BLOCKED and NOT TESTED, safe change procedure |
| 07 | [Incomplete and conflicting information](../tests/07-incomplete-conflicting-info.md) | Surfacing conflicts, PROVISIONAL plans, cautious tier |
| 08 | [Unnecessary control rejected](../tests/08-unnecessary-control-rejected.md) | Rejecting disproportionate requests with reasons |
| 09 | [Existing weakness](../tests/09-existing-weakness.md) | Rotate-first, redaction, no history rewrite without approval |
| 10 | [Testing unavailable](../tests/10-testing-unavailable.md) | NOT TESTED discipline, no false PASS |

## Known limits of this plan

- Pass criteria are objective, but a person still has to score them. Two scorers can disagree on borderline wording.
- The scenarios are small. They test behaviour on clear cases, not on large or unusual codebases.
- Behaviour differs between agents and model versions. A pass on one agent says nothing about another.
- No scenario can prove the guidance is complete. Level 4 needs people with security expertise.

## Execution log

### Executed

| Date | What | Where | Result |
|---|---|---|---|
| 2026-10-30 | Skill validator (frontmatter rules, single `SKILL.md`) on the skill folder | Sandbox of the assistant that wrote the files | Passed ("Skill is valid") |
| 2026-10-30 | `tests/check_structure.py` | Same sandbox | 48 passed, 0 failed, 1 warning (the LICENSE copyright placeholder). A negative test on a deliberately broken copy (broken link, duplicate ID, unknown ID, missing status, missing section, leftover placeholder) produced failures for all six defects. |
| 2026-10-30 | Packaging of the skill folder into a `.skill` archive, and a separate repository ZIP; both opened, listed, and compared with the directory; the ZIP was also extracted elsewhere and the structural checks re-run on the extracted copy | Same sandbox | Archive integrity tests passed. 23 files, all matching the directory. Structural checks on the extracted copy: 48 passed, 0 failed, 1 warning. |

### Not yet executed

| Item | State |
|---|---|
| Load check in Claude Code | Not run |
| Load check in Claude (claude.ai) | Not run |
| Scenarios 01 to 10 on any agent | **Not run. Proposed only.** |
| External link check | Not run |
| Expert review of the platform guidance | Not run |
