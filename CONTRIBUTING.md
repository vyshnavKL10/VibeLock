# Contributing to VibeLock

Thanks for helping. VibeLock's value is accuracy and honesty, so the bar for changes is "is it correct, relevant, and not overclaiming?"

## Principles

- **One canonical source.** The risk rubric lives in `docs/RISK_MODEL.md`, controls in `PLATFORMS.md`, statuses in `SKILL.md`. Link to them, don't copy them.
- **Project-aware, not generic.** Don't add advice that applies to every project. Controls need a tier and an "applies when" condition.
- **No invented facts.** Don't fabricate citations, standard requirements, or version-specific behaviour. If you aren't sure, say NEEDS REVIEW and point to the vendor's documentation.
- **Label state honestly.** Mark features as implemented, planned, or unverified. Don't claim an agent is supported without testing it.
- **No complexity for show.** No CLI, scanner, or dependency unless it clearly earns its place.
- **Keep `SKILL.md` short** (under 500 lines). Put detail in a reference file that is read at the phase that needs it.

## Adding or changing a control in `PLATFORMS.md`

1. Use the next free ID in its section, in the form `API-NN [L2+] ...`, using the next unused number. The tag is the lowest tier at which the control is Mandatory (see "Control classes" in the file).
2. Start the text with "If" when the control only applies under a condition.
3. Keep it one specific, actionable sentence. Say what, not just "consider security".
4. Add how to verify it in the section's `Verify:` line if the method changes.
5. Cite the vendor or standard documentation in your pull request, not from memory.

## Changing an assessment (`assessments/`)

- Use only commands and flags you have run, or that the tool's documentation shows, and say which tool they apply to. Tools change between versions.
- Never include a real or real-looking secret, advisory ID, or scan result. Describe shapes and use placeholders.
- A new ecosystem is a new row in the table in `DEPENDENCIES.md`: manifest and lockfile names, the audit command, and the "why is this here" command.
- A new secret shape is a new row in the table in `SECRETS.md`, limited to formats you can confirm in the provider's documentation.
- A new weakness class is a new row in the table in `CODE_REVIEW.md`, with the safe pattern, the usual false positives, and the matching `PLATFORMS.md` control. Add the control there if it doesn't exist.

## Adding or updating an agent

Follow the steps at the end of [docs/AGENT_COMPATIBILITY.md](docs/AGENT_COMPATIBILITY.md#adding-or-updating-an-agent): link the agent's official documentation, add one row, and say exactly what you ran. Don't copy or rewrite the methodology for an agent.

## Before you open a pull request

Check that links between files still work, that control IDs stay unique, and that file names match what the README says. In the pull request, say how you verified your change.

## Reporting a vulnerability

Please use the process in [SECURITY.md](SECURITY.md) instead of a public issue.
