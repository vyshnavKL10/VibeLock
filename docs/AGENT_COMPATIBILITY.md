# Agent compatibility

VibeLock is written in the open [Agent Skills](https://agentskills.io/specification) format: a folder named `vibelock` with `SKILL.md` and reference files. There is **one canonical copy** of the methodology. Agents that support the format load it natively, so no per-agent copies or adapters are needed. This file is the only place install paths are listed.

## What has and hasn't been checked

| Item | State |
|---|---|
| Install paths below, against each vendor's own documentation | **Documented.** Checked on 2026-10-31. Vendors change these, so recheck the linked page if something doesn't load. |
| `SKILL.md` frontmatter against the Agent Skills specification | **Checked.** Only fields from the open standard are used (`name`, `description`, `compatibility`). |
| Skill works from every documented path, with relative references intact | **Checked in a temporary test project**: a copy and a symlink at each path below, with every file reference in `SKILL.md` resolved from there. |
| Size of `SKILL.md` | **Above the recommendation.** Roughly 6,000 tokens (estimated from character count), while the specification recommends under 5,000 for the instructions. It is a recommendation, not a requirement. Agents with small context windows will feel it. |
| Behaviour inside any agent | **Not tested by the authors in any agent.** Nothing below should be read as "VibeLock has been shown to work in X". |

## Agents that load skills natively

The skill folder must be named exactly `vibelock`, because the specification requires the folder name to match the `name` field. Use the project path to share the skill with a repository, or the user path for all your projects.

| Agent | Project path | User path | Notes | Official documentation |
|---|---|---|---|---|
| Claude Code | `.claude/skills/vibelock/` | `~/.claude/skills/vibelock/` | Project skills need the workspace trust dialog accepted first. Ask for it, or invoke `/vibelock`. | [Claude Code skills](https://code.claude.com/docs/en/skills) |
| OpenAI Codex | `.agents/skills/vibelock/` | see the Codex docs | Codex scans `.agents/skills` from the working directory up to the repository root. | [Codex skills](https://developers.openai.com/codex/skills) |
| Cursor | `.agents/skills/vibelock/` or `.cursor/skills/vibelock/` | `~/.agents/skills/` or `~/.cursor/skills/` | Also loads `.claude/skills/` and `.codex/skills/`. Type `/` in Agent chat to invoke by name. User-level skills aren't copied to Cloud Agents. | [Cursor skills](https://cursor.com/docs/skills) |
| GitHub Copilot (VS Code agent mode, Copilot CLI, cloud agent) | `.github/skills/vibelock/` (the CLI and VS Code also read `.claude/skills/` and `.agents/skills/`) | `~/.copilot/skills/` or `~/.agents/skills/` | Paths differ slightly between Copilot surfaces. In the CLI, `/skills reload` then `/skills info vibelock`. | [Copilot CLI skills](https://docs.github.com/en/enterprise-cloud@latest/copilot/how-tos/copilot-cli/customize-copilot/add-skills) |
| Gemini CLI | `.gemini/skills/vibelock/` or `.agents/skills/vibelock/` | `~/.gemini/skills/` or `~/.agents/skills/` | Asks your permission before activating a skill. `/skills list` and `/skills reload`. One tutorial page describes skills as experimental and needing to be enabled in settings. | [Gemini CLI skills](https://geminicli.com/docs/cli/skills/) |
| Google Antigravity | `.agent/skills/vibelock/` | `~/.gemini/antigravity/skills/` | Path from Google's Antigravity codelab. Some third-party tools list `.agents/skills/` instead. That is **not verified** here. | [Antigravity skills codelab](https://codelabs.developers.google.com/getting-started-with-antigravity-skills) |
| Windsurf (Cascade) | `.windsurf/skills/vibelock/` | `~/.codeium/windsurf/skills/vibelock/` | Cascade decides when to use it, or mention it with `@`. | [Windsurf skills](https://docs.windsurf.com/windsurf/cascade/skills) |

## Install

**One agent:** clone straight into its path from the table.

```bash
git clone https://github.com/vyshnavKL10/VibeLock.git .agents/skills/vibelock
```

**Several agents:** install once at `.agents/skills/vibelock` (read by Codex, Cursor, GitHub Copilot, and Gemini CLI), then link it for the agents that don't read that path, and only for the ones you use:

```bash
mkdir -p .claude/skills   && ln -s ../../.agents/skills/vibelock .claude/skills/vibelock     # Claude Code
mkdir -p .windsurf/skills && ln -s ../../.agents/skills/vibelock .windsurf/skills/vibelock   # Windsurf
mkdir -p .agent/skills    && ln -s ../../.agents/skills/vibelock .agent/skills/vibelock      # Antigravity
```

Symlinks on Windows need Developer Mode or an administrator shell. Otherwise copy the folder instead, and keep the copies in sync. Some agents read several of these locations, so a skill linked in more than one place may be listed more than once. That is untidy but harmless.

**A clone contains its own `.git` folder.** Inside your project's repository, pick one:

1. Add the install path to `.gitignore` (personal use).
2. `git submodule add https://github.com/vyshnavKL10/VibeLock.git .agents/skills/vibelock` to share it with a team at a pinned commit.
3. Copy the files without `.git`.

Skills are instructions your agent will follow, and teammates' agents inherit whatever is in a shared copy. Install only from the official repository, pin a commit, and read `SKILL.md` changes before updating. Leave the agent's own trust prompts on.

## Agents without skills support (fallback, untested)

Many agents read an `AGENTS.md` file from the project (see [agents.md](https://agents.md)). If yours does not support skills, install the folder as above and add a pointer to that file, adjusting the path to where you installed it:

```markdown
## Security (VibeLock)
For security work (hardening, dependency or secret checks, reviewing code for vulnerabilities, or deciding whether something is ready to ship), read `.agents/skills/vibelock/SKILL.md` and follow it. Paths inside that file are relative to it.
```

Per agents.md, Aider can be pointed at the file with `read: AGENTS.md` in `.aider.conf.yml`, and Gemini CLI by adding `AGENTS.md` to `context.fileName` in `.gemini/settings.json`.

**Limits.** The pointer holds no methodology (see the adapter rule in [ARCHITECTURE.md](ARCHITECTURE.md)). The agent has to read `SKILL.md` and then the other files when the workflow tells it to. An agent that can't open files on demand gets `SKILL.md` only, and the results will be weaker. **This fallback has not been tested in any agent.**

## Other agents (not verified)

Third-party lists claim support for the skills format in many more tools, including Cline, Roo Code, Kilo Code, Continue, Zed, Amp, Goose, OpenHands, Kiro, JetBrains Junie, and OpenCode. Their documentation hasn't been checked here, so no paths are given. If you use one, find its skills directory in its own documentation, install the folder as `vibelock`, run the load check below, and contribute the result (see "Adding or updating an agent").

## Check that it loaded

In a fresh session, in any agent, ask:

> Use VibeLock. Summarize its 12 phases in one line each, and tell me which files you would read at Phase 5 and Phase 6.

A loaded skill answers with the phases from `SKILL.md` and names `docs/RISK_MODEL.md` and `PLATFORMS.md`. An agent that answers from general knowledge didn't load it. Agent-specific listing commands, where the documentation gives one: Gemini CLI `/skills list`, Copilot CLI `/skills info vibelock`, Cursor `/` and look for it, Windsurf `@vibelock`, Claude Code `/vibelock`.

## What differs between agents

- **Activation.** Agents choose a skill from its description, so it may not trigger on a vague request. Invoking it by name, as in the table, is the reliable route.
- **Questions.** `SKILL.md` uses a structured question tool if the agent has one and plain text otherwise.
- **Sandboxes.** Agents that run in restricted or cloud environments may have no shell or network. The skill reports NOT TESTED or BLOCKED instead of guessing, so expect more of those results there.
- **Approvals are instructions, not enforcement.** VibeLock tells the agent to ask before upgrades, rotations, and destructive actions. Rely on the agent's own permission prompts as the real control, and keep them on.
- **Extensions.** `SKILL.md` uses only fields from the open standard. Agent-specific extensions (for example Claude Code's invocation controls) are not used, so behaviour doesn't depend on them.

## Adding or updating an agent

1. Find the agent's **official** documentation for skills, and record the project path, the user path, how it activates, and a way to confirm it loaded.
2. Add one row to the table above with a link to that page, and update the date at the top.
3. Install the skill at that path, run the load check, and say in your pull request exactly what you ran and saw. State plainly if you didn't test it.
4. Do not copy or rewrite the methodology for an agent. If an agent needs different wording, change `SKILL.md` for everyone or document the limitation here.
