# Secret exposure assessment

Procedure for `SKILL.md` Phase 9. Read the **Handling rules** as soon as you find environment, key, or credential files in Phase 1, and the rest when you run the assessment. The plan (Phase 6) sets the depth.

**Goal:** find credentials that may be exposed through the project, say how sure you are and how bad it is, and recommend the right response, without ever revealing a value and without changing anything until the user approves.

## Handling rules

These apply from the first file you read until the end of the conversation.

1. **Never print, quote, copy, or partly reveal a secret value.** Not in chat, in files, in commands, in logs, or in the report. Not the first or last characters, not a hash, not the line it sits on. Refer to a secret by a label ("Secret 1"), its type, and its location.
2. **Don't put a secret in a command line or a search query.** Command lines end up in process lists and shell history.
3. **Make commands print locations, not content.** Use `-l` or `-c`, or pipe through `cut -d: -f1,2` so only `file:line` remains. Never use `-o`, `-A`, `-B`, or `-C` with a secret pattern. Run scanners with their redaction option on (for example `gitleaks` has `--redact`; check `--help`). If a tool can't redact, don't paste its output anywhere.
4. **Don't verify a secret by using it.** Some scanners test a credential by calling the provider's API (TruffleHog does this unless run with `--no-verification`). That sends the secret to a third party and can trigger alerts or side effects. Don't do it without explicit approval. "Is it still live?" is a question for the owner.
5. **Detect only.** Don't modify, move, or delete a secret, an env file, or git history without approval.
6. **If the user pastes a secret into the chat, don't repeat it back.** Tell them it should be treated as exposed.
7. **Read only as much as you need.** For files that are probably full of secrets (`.env`, key files), prefer checking that they exist, whether git tracks them, and whether they are ignored, instead of opening them.

## Step 1: Where to look

Cover, in this order, whatever applies to the project:

1. **Files that git tracks.** The strongest signal needs no file content at all: is a sensitive file tracked?
2. **The working tree**: source, config, scripts, IaC, notebooks, CI files, mobile and desktop config, docs, and test fixtures.
3. **Git history**, including other branches and tags: a secret removed in a later commit is still in history.
4. **Things that ship:** client-side bundles and source maps, build artifacts, container images, logs, and backups or dumps. A secret in a client bundle is exposed by design.
5. **CI and deployment config**: workflow files, pipeline variables written inline, Dockerfiles (`ENV`, `ARG`), compose files.

File names that deserve attention: `.env`, `.env.*`, `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.jks`, `*.keystore`, `id_rsa`, `id_ed25519`, `.npmrc`, `.pypirc`, `.netrc`, `*.tfvars`, `terraform.tfstate`, cloud credential files, service-account JSON files, `*.sql` and `*.dump` backups, and Kubernetes `Secret` manifests (base64 is not encryption).

## Step 2: Recipes

These print names and locations only. Adapt them, and keep the rule: **no content in the output.**

Sensitive file names that git tracks (no content is read):

```bash
git ls-files | grep -E '(^|/)\.env($|\.)|\.(pem|key|p12|pfx|jks|keystore|tfvars)$|(^|/)id_(rsa|ed25519|ecdsa)$|(^|/)\.(npmrc|pypirc|netrc)$|terraform\.tfstate|service[-_]?account.*\.json$' | grep -vE '\.(example|sample|template)$'
```

Is a file ignored by git?

```bash
git check-ignore -v .env
```

Sensitive files that were **ever added** in history, by commit and name (no content):

```bash
git log --all --diff-filter=A --name-only --pretty=format:'commit %h' -- '*.env' '.env*' '*.pem' '*.key' '*.p12' '*.pfx' '*.jks' '*.keystore'
```

Pattern search in tracked files, printing only `file:line`:

```bash
git grep -nIE 'PATTERN' | cut -d: -f1,2
```

Pattern search in the whole working tree, including untracked files:

```bash
grep -rnIE 'PATTERN' --exclude-dir=.git --exclude-dir=node_modules . | cut -d: -f1,2
```

Which commits in history added or removed a line matching a pattern (commit subjects only, no diff):

```bash
git log --all -G'PATTERN' --oneline
```

Replace `PATTERN` with the combined shape pattern in Step 3. A pattern search is a **lead generator, not a scanner**: it misses secrets in unknown formats and splits across lines.

## Step 3: What secrets look like

Examples of well-known shapes. Providers change formats, so treat this as a starting list, not a complete or guaranteed-current one.

| Type | Shape |
|---|---|
| AWS access key ID | `AKIA` (long-term) or `ASIA` (temporary) followed by 16 upper-case letters and digits. The matching secret key is only meaningful next to one. |
| GitHub token | Prefixes `ghp_`, `gho_`, `ghu_`, `ghs_`, `ghr_`, or `github_pat_` |
| Stripe | `sk_live_` and `rk_live_` are secret. `sk_test_` is a test secret (still sensitive). `pk_live_` and `pk_test_` are publishable and meant to be public. `whsec_` is a webhook signing secret. |
| Slack | `xoxb-`, `xoxp-`, `xoxa-`, `xoxs-` tokens, and webhook URLs containing `hooks.slack.com/services/` |
| Google | API keys starting `AIza`; service-account JSON containing `"type": "service_account"` and a `private_key` field |
| Private keys | PEM blocks: a line beginning `-----BEGIN` that contains `PRIVATE KEY` |
| Package registries | `npm_` (npm), `pypi-` (PyPI) |
| Other providers | `SG.` (SendGrid), `sk-ant-` (Anthropic), `sk-` (OpenAI and others) |
| Database and queue URLs | `scheme://user:password@host` for postgres, mysql, mongodb, redis, amqp |
| JWTs | Three base64url parts, the first starting `eyJ`. A long-lived signed token is a credential. A sample or expired one in a test is not. |
| Generic | A name such as `password`, `secret`, `token`, `api_key`, `credential`, or `private_key` assigned a literal string of real length, or an `Authorization` header with a literal value |

A combined pattern for the first lead search (case-sensitive, extended regex):

```
AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{20,}|sk_live_[A-Za-z0-9]{16,}|rk_live_[A-Za-z0-9]{16,}|xox[abprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{35}|-----BEGIN [A-Z ]*PRIVATE KEY-----|npm_[A-Za-z0-9]{36}|pypi-[A-Za-z0-9_-]{20,}|sk-ant-[A-Za-z0-9_-]{20,}
```

And one for credentials inside URLs: `[a-z][a-z0-9+.-]*://[^/[:space:]:@]+:[^/[:space:]@]+@`. The generic-name pattern (name assigned a quoted literal) is noisy, so use it with `-i` and expect many placeholders.

If a dedicated scanner is installed (for example `gitleaks`, `trufflehog`, `detect-secrets`, or Semgrep secret rules), use it for history and the working tree, with redaction on and verification off. Note the tool, its version, and what it covered. **If no scanner is available, the full history scan is NOT TESTED.** Say what the manual lead search covered, and don't present "no matches" as "no secrets".

## Step 4: Classify each hit

Look at the surrounding context (file type, variable name, what code reads it) without displaying the value.

| Class | Meaning | Status |
|---|---|---|
| **Exposed credential (credible)** | A real-looking value of a known format, or clearly used as a credential, in a place that exposes it: tracked by git, in history, in a client bundle, in a public repo, or in a log or artifact | FAIL |
| **Likely secret, unconfirmed** | A plausible secret name with a value of real length, but an unknown format and unclear use | NEEDS REVIEW |
| **Placeholder or example** | `changeme`, `your-api-key`, `xxxx`, `<token>`, `${VAR}`, an environment-variable reference, an empty `.env.example` value, a clearly fake fixture or documentation value | Not a finding. Count it as examined. |
| **Public by design** | Publishable keys (Stripe `pk_`), Firebase client config, browser map keys, Sentry DSNs, analytics IDs | Not a secret. If it should be restricted by domain or app, mark NEEDS REVIEW. |
| **Local only, not exposed** | A real secret in an untracked, ignored file that is not in history | Note it. Not a repository exposure. |

Don't treat ordinary examples and obvious placeholders as confirmed secrets, but do look twice at a value in a test or example file that has a real-key shape.

**Confirmed** here means "present and credible". You usually can't know if it is **live**, and you shouldn't test it. Say "liveness not verified".

Rate **severity** by what the credential could do and where it is exposed:

- Powerful (cloud admin, payment secret key, database with write access, signing key) in a public repo, a client bundle, or a shared artifact: **Critical**.
- The same in a private repo's history: **High**.
- Narrow (read-only, single service, test mode): one level lower.
- Rate **confidence** High when the format is known, the value isn't a placeholder, and code uses it; Medium when two of three hold; Low otherwise.

Ask the user if the repository is public, since it changes severity. If you can't tell, treat it as possibly public.

## Step 5: Recommend the response

Recommend, don't do. Each step that changes something needs approval.

1. **Treat a credible exposure as compromised.** This includes private repositories: forks, clones, CI logs, and backups all hold copies.
2. **Rotate or revoke it at the provider first**, before any cleanup. Issue a new credential, deploy it, then revoke the old one. Say what will break. The owner has to do this.
3. **Check the provider's access logs** for use of the credential since it was exposed. Again, the owner's task.
4. **Fix the source:** move the value to an environment variable or secret manager, add the file to `.gitignore`, and commit a `.env.example` with placeholders. You can make these edits after approval.
5. **History cleanup is optional and comes after rotation.** Tools such as `git filter-repo` or BFG rewrite history, break existing clones and forks, usually need a force-push, and can't recall copies already taken. Never do it without explicit approval, and tell the user all of that.
6. **Prevent a repeat:** secret scanning before code reaches the remote (ALL-15), least-privilege and short-lived credentials (ALL-03), and scoped CI secrets (CI-01).
7. If the credential could have exposed personal data, flag a possible breach duty as NEEDS REVIEW (PRIV-02).

## Reporting

For each finding, use the finding template in `examples/REPORT_TEMPLATE.md`, with these exact contents and **nothing else about the secret**:

- **Label:** Secret 1, Secret 2, and so on
- **Type:** for example "Stripe live secret key" or "database URL with password"
- **Location:** `path:line` in the working tree, or `abbreviated commit` plus `path` for history
- **Exposure context:** tracked, history only, client bundle, log, public or private repo, or unknown
- **Severity and confidence**, **liveness: not verified**
- **Recommended response** from Step 5

Quote nothing from the line. If the line itself is useful context, redact it (`API_KEY=[REDACTED]`).

- **Assessment status** (see SKILL.md Phase 9): FAIL if there is an Exposed credential (credible); PASS only if the planned scope, including history, was covered by a scanner that ran and nothing was confirmed; NEEDS REVIEW if only unconfirmed leads or partial coverage; NOT TESTED or BLOCKED if no scanner or no history access; NOT APPLICABLE only if there is nothing to inspect.
- **Always state:** the tool and version, or "manual pattern search"; what it covered (working tree, history, other branches, artifacts); that liveness was not verified; and what wasn't covered (forks, other clones, CI logs, deleted branches, container images).
- "No confirmed secrets" never means "no secrets".

## In Phase 10

Before you report, re-run the working-tree pattern search and check `git status` and your diff for anything new that looks like a credential, using the same print-nothing rules. Your own changes must not introduce a secret.
