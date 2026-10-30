# Security policy

## What counts as a security issue here

VibeLock is Markdown guidance plus one small lint script. Examples of issues worth reporting:

- Guidance that could lead an agent or a user to an insecure outcome, such as a control that is wrong or a "fix" that weakens something.
- A way the skill's own instructions could be abused, for example making an agent leak secrets, skip an approval gate, run destructive commands, or mark checks as PASS without evidence.
- A weakness in how the skill handles untrusted project content (prompt injection).
- Tampering or confusion in releases, such as an unofficial copy presented as the official one.

Not security issues here: vulnerabilities in a project you analyzed with VibeLock (report those to that project), general questions, and feature requests. Use normal issues for those.

## How to report

Use GitHub's private vulnerability reporting: open this repository's **Security** tab and choose **Report a vulnerability**. If that button isn't available, open a public issue that says you need a private contact, **without** including any details.

Please include:

- What you found and where (file and section).
- Why it matters, and a way to reproduce it if one exists.
- Which agent and version you used, if relevant.

Do not include real secrets, personal data, or details of systems you aren't authorized to test.

## What to expect

VibeLock is a small open-source project. Reports are handled on a best-effort basis, with no guaranteed response time. Fixes go into the latest release. Only the latest release is supported. If you'd like credit, say so and it will be given with your permission.

## Disclosure

Please allow time for a fix before sharing details publicly.
