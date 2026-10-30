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

1. Use the next free ID in its section, in the form `API-11 [L2+] ...`. The tag is the lowest tier at which the control is Mandatory (see "Control classes" in the file).
2. Start the text with "If" when the control only applies under a condition.
3. Keep it one specific, actionable sentence. Say what, not just "consider security".
4. Add how to verify it in the section's `Verify:` line if the method changes.
5. Cite the vendor or standard documentation in your pull request, not from memory.

## Adding an agent adapter

Only if you can explain that agent's conventions for discovering instructions and loading files. Include the exact install steps and how to confirm the skill loaded on that agent. An adapter may hold installation glue and a pointer to `SKILL.md`. It must not copy the methodology.

## Before you open a pull request

Check that links between files still work, that control IDs stay unique, and that file names match what the README says. In the pull request, say how you verified your change.

## Reporting a vulnerability

Please use the process in [SECURITY.md](SECURITY.md) instead of a public issue.
