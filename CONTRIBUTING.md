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

## Adding a scenario

Copy the structure of an existing file in `tests/`. Every scenario needs a fixture, a prompt, expected discovery, expected questions (including ones that must **not** be asked), risks and tier, controls, and at least four objective, numbered pass criteria. Never put real or real-looking secrets in a fixture. Tell the tester to generate their own fake value.

## Adding an agent adapter

Only if you can explain that agent's conventions for discovering instructions and loading files. Include the exact install steps, a load check, and a record of scenarios 01 and 08 run on that agent. An adapter may hold installation glue and a pointer to `SKILL.md`. It must not copy the methodology.

## Before you open a pull request

```bash
python3 tests/check_structure.py
```

It must report no FAIL results. It checks structure and consistency only. It can't tell you whether your guidance is correct, so say in the pull request how you verified it.

## Reporting a vulnerability

Please use the process in [SECURITY.md](SECURITY.md) instead of a public issue.
