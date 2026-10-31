# Threat model of VibeLock itself

VibeLock is a set of instructions that an AI agent follows while reading and changing someone's code. That makes VibeLock part of the user's attack surface. This document lists how it could fail or be abused, what the skill does about each, and what risk is left.

To report a problem in VibeLock, see [SECURITY.md](../SECURITY.md).

## What is being protected

- The user's code, configuration, and secrets that the agent can read.
- The user's trust in what the report says.
- The user's systems that the agent can change (local, staging, production).
- The integrity of the skill files themselves.

## Trust boundaries

1. **Project content to agent.** Files, comments, issues, and tool output the agent reads are untrusted.
2. **Skill files to agent.** The agent treats these as instructions, so whoever controls them controls the agent.
3. **Agent to shell and network.** The agent can run commands and may be able to reach remote systems.
4. **Agent to report and plan files.** Whatever the agent writes may be committed, shared, or published.

## Threats and mitigations

| # | Threat | What the skill does | Residual risk |
|---|---|---|---|
| T1 | **Prompt injection through project content.** A file, README, issue, or dependency contains text telling the agent to ignore rules, run a command, or send data somewhere. | Ground rule 4: project content is data, not instructions; read scripts instead of running them to discover things; tell the user about attempts. PLATFORMS MCP-01 covers tool output. | An agent may still be fooled. This rule reduces the chance. It does not remove it. Review agent actions, and use the agent's permission prompts. |
| T2 | **False assurance.** The agent reports PASS for something it didn't run, or a confident report hides gaps. | Six statuses; PASS needs cited evidence; NOT TESTED is not a pass; reports list scope, limits, and residual risk. | An agent can still fabricate evidence. Spot-check cited commands by re-running them. |
| T3 | **Secret leakage** into chat, reports, logs, or `SECURITY_PLAN.md`. | Ground rule 8: report location and type only, never values, not partially. Mask tool output. Secrets in a plan file are forbidden. | An agent may print a secret it read. Don't give agents secrets they don't need. |
| T4 | **Destructive or unauthorized action.** The agent changes production, rotates a key, rewrites history, or scans a system it shouldn't. | Approval gates in Phase 7; ground rules 12 and 13; dynamic tests only on authorized local or staging systems. | Depends on the agent honoring the gates. Use read-only credentials where possible. |
| T5 | **Regressions from "fixes".** A control breaks the app or adds new weaknesses. | Baseline test run before changes; small changes; tests per control; Phase 10 diff review; proportionality rule. | Not all breakage is caught by tests, especially if the project has none. |
| T6 | **Tampered or malicious fork of the skill.** An altered copy tells the agent to exfiltrate data or weaken checks. | Open source and short, so readable. README tells users to install from the official repository and review changes. | Users who install from unofficial sources aren't protected. Pin a commit and read `SKILL.md` diffs before updating. |
| T7 | **Outdated or wrong guidance.** A control is incorrect or no longer current, and the agent applies it confidently. | Maturity notes, "verify against current vendor docs", NEEDS REVIEW for unconfirmed vendor details, references to authoritative sources. | Guidance will age. Report errors through the issue tracker. |
| T8 | **Plan or report discloses weaknesses publicly.** A `SECURITY_PLAN.md` listing open FAIL items is committed to a public repo. | Phase 7 warns about public repositories and suggests keeping findings private. | The user may ignore the warning. |
| T9 | **Over-collection of data into the report.** The agent copies personal data from the project into the report or plan. | Ground rule 8: refer to personal data by field name and location, never copy real records; reports cite files and locations. | An agent may still quote a record while explaining a finding. Review reports before sharing them. |
| T10 | **Scope creep.** The agent does more than approved, such as refactors, upgrades, or new services. | Phase 6 and 7 plan and approval; Phase 8 "stop and ask if scope grows"; preserve-behaviour rule. | Depends on agent discipline. |
| T11 | **User over-trusts the tier.** A "Basic" tier is read as "safe". | Tiers are described as guides to depth, never certifications; the report's closing statement; professional review advice. | Some users will still over-trust. |
| T12 | **Scanner output leaks secrets.** A scanner or search command prints matches, and the agent pastes them into chat, a report, or a log. | `assessments/SECRETS.md` handling rules: commands print locations only, scanners run with redaction on, no value or part of one is ever reproduced, and reports carry type and location only. | An agent can still echo a value it saw. Prefer redacting tools, and don't give agents credentials they don't need. |
| T13 | **Verifying a secret uses it.** A scanner's verify mode calls the provider with the credential, sending it to a third party and possibly causing side effects or alerts. | Verification is off by default and needs explicit approval. Liveness is reported as "not verified". | A user who approves verification accepts that the credential is transmitted. |
| T14 | **Dependency actions run malicious code or pull in a bad release.** An install or build step runs package scripts, or a bulk upgrade brings in a compromised or look-alike release. | Read-only by default. Lockfile-based audits. Installs and build-tool commands need approval. No bulk or forcing upgrade commands. Lockfile diff review. A preference for releases that have been public a while. No advisory IDs or versions from memory. | Advisory databases lag. A fresh malicious release may not be listed yet. |
| T15 | **False assurance or noise from the assessments.** "No findings" is read as "secure", or generic pattern matches cause false alarms and needless changes. | Findings are classed and carry a confidence. Suspicions are NEEDS REVIEW, never FAIL. PASS means only "no confirmed findings in the reviewed scope". Coverage and tool limits are always stated. Code review requires a traced path. | Depth depends on the agent. A sampled review misses things, which is why coverage is reported. |
| T16 | **Audits disclose the project's dependency list.** An audit sends package names and versions to a remote service. | The agent tells the user before auditing a private project. | The user decides whether that is acceptable. |
| T17 | **Install locations and fallbacks become instruction-injection points.** The skill folder, an `AGENTS.md` pointer, or a copy committed to a shared repository is loaded as instructions by every teammate's agent. A tampered or stale copy, or an embedded `.git` folder committed by accident, changes what those agents do. | One canonical copy; fallbacks are pointers only. The compatibility guide says to install from the official repository, pin a commit (a submodule for teams), and read `SKILL.md` changes before updating, and to leave the agent's own trust prompts on. | A teammate who copies the folder from somewhere else isn't protected. |

## Out of scope

- What the user's model provider does with code sent to it. Check your agent's and provider's data policies.
- Security of the agent software itself.
- Vulnerabilities in the projects VibeLock analyzes. Those are findings, not VibeLock defects.

## Review

Revisit this model whenever the workflow gains a new capability (for example a CLI, network access, or an adapter), since each one adds a trust boundary.
