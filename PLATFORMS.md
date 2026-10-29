# VibeLock platform controls

Reference for `SKILL.md`. Read the **Cross-cutting** section always, then **only the sections that match the project's discovered stack**.

## How to read this file

- Each control has an ID and a minimum level: `API-01 [L1+]` applies when the component's risk level is 1 or higher. `[L3+]` applies at Level 3 and Level 4 only.
- Controls are starting points, not a complete standard. Select by project fit and explain why each one applies.
- **Maturity** notes mark how well-developed each section is. v0.1 has **not** been validated against real projects yet. Treat every section as guidance to verify, not authority.
- Platform details change. When a control depends on a vendor's current behaviour (especially Huawei, Apple, Google, and payment providers), check the vendor's current documentation and mark the result NEEDS REVIEW if you can't.

Contents: Cross-cutting, Web frontend, API/backend, Authentication, Database, Server/VPS and containers, Payments and webhooks, CI/CD, Cloud, Android, iOS, Huawei, Desktop, MCP servers and AI tools, SDKs and libraries.

---

## Cross-cutting (always read)

Maturity: core.

- ALL-01 [L1+] No secrets in source code, git history, logs, client bundles, or reports. Use environment variables or a secret manager. `.env` is gitignored; only `.env.example` with placeholders is committed.
- ALL-02 [L1+] A secret that was ever committed is compromised. Rotate it first; cleaning history comes second.
- ALL-03 [L1+] Least privilege for every key, token, and service account: only the permissions actually needed.
- ALL-04 [L1+] Dependencies come from official registries, with a committed lockfile. Review new dependencies before adding them.
- ALL-05 [L1+] Verify that every AI-suggested package exists, is the intended one, and is maintained, before installing (hallucinated and look-alike names are a supply-chain risk).
- ALL-06 [L1+] Search AI-generated code for leftovers: disabled auth "for testing", `TODO: add auth`, hard-coded test credentials, debug flags, permissive CORS, commented-out checks.
- ALL-07 [L1+] All traffic leaving the machine uses TLS (HTTPS).
- ALL-08 [L2+] Validate all external input on the server side. Never rely on client-side checks.
- ALL-09 [L2+] Log security-relevant events (failed logins, permission denials, admin actions). Never log passwords, tokens, secrets, or full payment data.
- ALL-10 [L2+] Run the ecosystem's dependency audit regularly and have a process for applying updates.
- ALL-11 [L2+] Backups exist and a restore has been tested at least once.
- ALL-12 [L2+] Human review (or tests) for AI-written auth, authorization, payment, crypto, and permission code.
- ALL-13 [L3+] Incident basics written down: who is alerted, how to revoke keys, how to roll back, how to contact users.
- ALL-14 [L3+] Independent review or penetration test before launch or major changes.

Verify: secret scan (if installed), dependency audit, reading `.gitignore` and config, grep for leftovers (ALL-06).

---

## Web frontend

Applies when: the project has browser-delivered UI (SPA, SSR, static site). Maturity: moderate.

- WEB-01 [L1+] Nothing in client-side code is secret. Keys shipped to the browser must be designed to be public (for example publishable keys), with server-side restrictions.
- WEB-02 [L1+] Rely on framework auto-escaping. Avoid `innerHTML`, `dangerouslySetInnerHTML`, `v-html` with untrusted data. If HTML must be rendered, sanitize with an established library.
- WEB-03 [L1+] Validate redirect targets (no open redirects).
- WEB-04 [L2+] Security headers: Content-Security-Policy, Strict-Transport-Security, `X-Content-Type-Options: nosniff`, clickjacking protection (CSP `frame-ancestors`), Referrer-Policy.
- WEB-05 [L2+] Session cookies are `HttpOnly`, `Secure`, and `SameSite`.
- WEB-06 [L2+] CSRF protection for state-changing requests authenticated by cookies.
- WEB-07 [L2+] CORS uses an explicit origin allowlist. Never combine wildcard origins with credentials.
- WEB-08 [L3+] Minimize third-party scripts. Self-host, or use Subresource Integrity where possible.

Verify: read the config and middleware, inspect response headers on a local or staging instance, test escaping with a harmless marker string.

---

## API and backend

Applies when: the project exposes HTTP/GraphQL/gRPC/etc. or runs backend logic. Maturity: moderate.

- API-01 [L1+] Authorization is checked server-side on every request, **for the specific object** (for example, user A can't read user B's record by changing an ID). "Is logged in" is not enough.
- API-02 [L1+] Parameterized queries or an ORM. No SQL or shell commands built by string concatenation with user input.
- API-03 [L1+] File uploads: validate type and size, store outside the web root or in object storage, use random names, never execute uploaded files.
- API-04 [L2+] Schema validation on inputs (for example zod, pydantic, JSON Schema). Reject unknown fields to prevent mass assignment.
- API-05 [L2+] Rate limiting on login, password reset, signup, and costly or public endpoints.
- API-06 [L2+] Request size limits, timeouts, and pagination limits.
- API-07 [L2+] Error responses don't leak stack traces, queries, or internal paths. Debug mode off in production.
- API-08 [L2+] If the server fetches user-supplied URLs, defend against SSRF: allowlist hosts, block internal and cloud-metadata addresses.
- API-09 [L3+] Audit log for sensitive actions, stored where the application can't alter it.
- API-10 [L3+] Malware scanning for uploads where users can share files with each other.

Verify: tests that a second user gets 403/404 for another user's resources, tests for invalid input, reading handlers for string-built queries.

---

## Authentication and authorization

Applies when: the project has logins, sessions, tokens, API keys, or roles. Maturity: moderate.

- AUTH-01 [L1+] Use an established auth provider or the framework's auth system. Do not build your own.
- AUTH-02 [L1+] Passwords hashed with Argon2id, bcrypt, or scrypt through a maintained library. Never plain text, encryption, or a fast hash.
- AUTH-03 [L2+] Default deny. Role model documented. Admin routes protected separately.
- AUTH-04 [L2+] Session and token expiry; logout invalidates the session; rotate session on login and privilege change.
- AUTH-05 [L2+] Account recovery and signup responses that don't reveal whether an account exists; reset tokens are single-use and expire.
- AUTH-06 [L2+] MFA available to users.
- AUTH-07 [L2+] JWTs: fixed allowed algorithms, verify signature, `exp`, `iss`, and `aud`; short lifetimes; no sensitive data in the payload.
- AUTH-08 [L3+] MFA required for admin and privileged accounts.
- AUTH-09 [L3+] Alerting on suspicious auth activity (many failures, new-device privileged logins).

Verify: tests for unauthenticated, wrong-role, and expired-token requests; read the middleware order.

---

## Database

Applies when: the project uses a database or a backend-as-a-service. Maturity: moderate.

- DB-01 [L1+] The database is not reachable from the public internet. Bind to localhost or a private network and firewall it.
- DB-02 [L1+] The app connects with a dedicated least-privilege user, not root or superuser.
- DB-03 [L1+] Default and blank credentials changed.
- DB-04 [L1+] If clients talk to the database directly (Supabase, Firebase and similar): Row Level Security or security rules are on and tested for **every** table or collection, and service-role/admin keys are never shipped to clients. This is a common high-impact mistake.
- DB-05 [L2+] TLS for database connections.
- DB-06 [L2+] Backups are encrypted and a restore has been tested.
- DB-07 [L3+] Minimize and classify sensitive fields; consider field-level encryption and a retention/deletion policy.

Verify: read connection config and firewall rules, test RLS/rules with a non-owner account, review migrations.

---

## Server, VPS, and containers

Applies when: the user runs their own server, VM, or containers. Maturity: moderate. Changes here are consequential and need approval.

- SRV-01 [L1+] SSH uses keys. Password login disabled. Root login disabled or restricted.
- SRV-02 [L1+] Firewall default-deny; only needed ports open (typically 80/443, plus restricted SSH).
- SRV-03 [L1+] Admin panels and dev tools are not publicly exposed (VPN, allowlist, or auth in front).
- SRV-04 [L2+] App runs as a non-root user. Containers run non-root, without `--privileged`, and without mounting the Docker socket.
- SRV-05 [L2+] OS and runtime security updates on a defined cadence (automatic where suitable).
- SRV-06 [L2+] TLS certificate valid with auto-renewal; HTTP redirects to HTTPS.
- SRV-07 [L2+] Brute-force protection and basic monitoring/alerts (fail2ban or equivalent).
- SRV-08 [L3+] Separate staging and production, with separate secrets per environment.
- SRV-09 [L3+] Infrastructure as code reviewed like application code.

Verify: read sshd config, firewall rules, compose/Docker files. Do not change live server settings without approval and a rollback path (keep a second SSH session open when editing SSH or firewall config).

---

## Payments and webhooks

Applies when: the project takes payments or receives webhooks from any provider. Maturity: moderate.

- PAY-01 [L1+] Use the provider's hosted checkout or elements so card data never touches your servers.
- PAY-02 [L1+] Verify webhook signatures with the provider's library. Reject unsigned or invalid requests.
- PAY-03 [L1+] Determine prices, amounts, and entitlements server-side. Never trust amounts or plan IDs from the client.
- PAY-04 [L2+] Fulfil orders from verified server-side or webhook state, not from a redirect URL or client message.
- PAY-05 [L2+] Handle webhook replay and duplicates (store event IDs; check timestamps); handlers are idempotent.
- PAY-06 [L2+] Restricted or scoped API keys; webhook secrets stored as secrets and rotated if exposed.
- PAY-07 [L3+] Reconciliation between your records and the provider's, with alerts on anomalies; abuse and fraud controls.

Verify: tests with an invalid signature and a replayed event, read the fulfilment logic.

---

## CI/CD

Applies when: the project has automated build, test, or deploy pipelines. Maturity: moderate.

- CI-01 [L1+] Secrets live in the CI secret store, never in the repo or workflow files; masked in logs.
- CI-02 [L2+] Least-privilege pipeline tokens (for example read-only `permissions` by default in GitHub Actions).
- CI-03 [L2+] Pin third-party actions and images to a commit SHA or digest.
- CI-04 [L2+] Branch protection on the main branch; review required for changes that affect deployment.
- CI-05 [L2+] Untrusted code (pull requests from forks) doesn't run with access to secrets. Be cautious with `pull_request_target`.
- CI-06 [L2+] Pipeline runs secret scanning and a dependency audit.
- CI-07 [L3+] Protected deployment environments with manual approval; signed or verified artifacts; SBOM where useful.

Verify: read workflow files, check branch-protection settings (may be BLOCKED without repository admin access).

---

## Cloud

Applies when: the project uses AWS, GCP, Azure, or similar. Maturity: basic.

- CLD-01 [L1+] Root/owner account protected with MFA and not used day to day.
- CLD-02 [L1+] Storage buckets private by default; public only on purpose.
- CLD-03 [L2+] IAM least privilege, no wildcard permissions, separate credentials per service.
- CLD-04 [L2+] Billing alerts and budgets (abuse often shows up as cost).
- CLD-05 [L3+] Audit logging enabled and retained.

Verify: read IaC and policies; live console checks are often BLOCKED, so mark NEEDS REVIEW.

---

## Android

Applies when: the project ships an Android app. Maturity: **initial guidance, less tested.**

- AND-01 [L1+] No secrets hard-coded in the APK/AAB. Anything shipped can be extracted.
- AND-02 [L1+] Cleartext traffic disabled; TLS only; use a network security config.
- AND-03 [L1+] Signing keys protected; use Play App Signing.
- AND-04 [L1+] Sensitive data stored with Android Keystore-backed mechanisms, not plain SharedPreferences or files.
- AND-05 [L2+] Components exported only when needed; `android:exported` set explicitly; protect with permissions.
- AND-06 [L2+] Request minimal permissions.
- AND-07 [L2+] Release builds not debuggable; `allowBackup` decision made deliberately; code shrinking/obfuscation treated as a deterrent only.
- AND-08 [L2+] Validate deep link and intent inputs; use verified App Links where applicable.
- AND-09 [L3+] Consider certificate pinning (with a rotation plan) and Play Integrity for sensitive backends. Treat root detection as a signal, not a guarantee.

Verify: read AndroidManifest.xml, network config, Gradle release config; check build output for embedded keys.

---

## iOS

Applies when: the project ships an iOS app. Maturity: **initial guidance, less tested.**

- IOS-01 [L1+] Sensitive data in the Keychain, not UserDefaults or plist files.
- IOS-02 [L1+] App Transport Security on; no blanket exceptions.
- IOS-03 [L2+] Appropriate Data Protection class for stored files.
- IOS-04 [L2+] Validate URL scheme and Universal Link inputs.
- IOS-05 [L2+] No sensitive data in logs, snapshots, or the pasteboard.
- IOS-06 [L2+] Biometrics via LocalAuthentication tied to Keychain access control where appropriate.
- IOS-07 [L3+] Consider certificate pinning (with a rotation plan) and App Attest/DeviceCheck for sensitive backends. Treat jailbreak detection as a signal only.

Verify: read Info.plist, entitlements, and storage code.

---

## Huawei ecosystem (HMS / AppGallery)

Applies when: the project targets Huawei devices or AppGallery. Maturity: **initial guidance, least tested. Verify against current Huawei developer documentation.**

- HW-01 [L1+] Apply the Android controls (AND-xx) to the Android build.
- HW-02 [L1+] Review what the AppGallery Connect configuration file contains before committing it, and keep server-side credentials out of the app.
- HW-03 [L2+] Verify in-app purchases and tokens server-side, not only in the app.
- HW-04 [L2+] Keep HMS SDK versions current and review the permissions each HMS kit adds.

Verify: mark anything not confirmable from current Huawei documentation as NEEDS REVIEW.

---

## Desktop (Windows, macOS, Linux)

Applies when: the project ships desktop software. Maturity: **initial guidance, less tested.**

- DSK-01 [L1+] Sign releases (Authenticode on Windows; Developer ID and notarization on macOS). Distribute over HTTPS.
- DSK-02 [L1+] Secure updates: updates are signed and verified before install.
- DSK-03 [L1+] Credentials stored in the OS credential store (Windows Credential Manager/DPAPI, macOS Keychain, Linux Secret Service), not plain files.
- DSK-04 [L2+] Run with least privilege; don't require admin/root for normal use. On macOS, hardened runtime with minimal entitlements.
- DSK-05 [L2+] Electron or embedded webviews: context isolation on, Node integration off, sandbox on, validated IPC, restricted navigation and remote content, CSP.
- DSK-06 [L2+] Local servers bind to 127.0.0.1 and require an auth token (so other local software or web pages can't drive them). Validate inputs from files, custom URL handlers, and IPC.
- DSK-07 [L2+] Windows installers: quoted service paths, non-user-writable install directories.
- DSK-08 [L3+] Linux: consider sandboxed packaging (Flatpak/Snap) or confinement profiles.

Verify: read the app config, packaging and updater setup, and Electron `webPreferences`.

---

## MCP servers, tools, and AI integrations

Applies when: the project builds, uses, or exposes MCP servers or tools that an AI model can call. Maturity: **initial guidance, less tested. The ecosystem is changing quickly.**

- MCP-01 [L1+] Treat everything a tool returns, and any fetched content or file text, as untrusted data. Prompt injection can arrive through any of it.
- MCP-02 [L1+] Least-privilege tools: read-only by default, separate read and write tools, narrowly scoped tokens.
- MCP-03 [L1+] No secrets in tool descriptions, prompts, or returned content. Credentials stay server-side.
- MCP-04 [L2+] Human confirmation for destructive, irreversible, or externally visible actions (delete, send, pay, deploy).
- MCP-05 [L2+] Validate every tool argument (path traversal, command and SQL injection). Never pass model-generated strings straight to a shell.
- MCP-06 [L2+] Remote servers require authentication. Local servers restrict filesystem access to specific directories, bind to localhost, and validate the Origin header.
- MCP-07 [L2+] Review third-party MCP servers and pin versions before installing: they run with your privileges. Re-review when tool definitions change.
- MCP-08 [L2+] Log tool calls (without secrets) and rate limit them.
- MCP-09 [L3+] Avoid combining private-data access, untrusted content, and an outbound channel in one agent. Remove at least one of the three.

Verify: list the tools and their permissions, read argument handling, test path traversal and injection strings in a sandbox.

---

## SDKs and libraries

Applies when: the project publishes a package or SDK others will use. Maturity: basic.

- SDK-01 [L1+] 2FA on the registry account; scoped publish tokens.
- SDK-02 [L1+] Secure defaults (TLS verification on, no insecure options enabled by default).
- SDK-03 [L2+] Don't embed secrets; require user-supplied keys and never log them.
- SDK-04 [L2+] Minimal, pinned dependencies; trusted publishing or provenance where the registry supports it.
- SDK-05 [L2+] A `SECURITY.md` with a private vulnerability reporting channel.
- SDK-06 [L3+] Signed releases, reproducible builds, and an SBOM.

Verify: read the publish workflow and package manifest.
