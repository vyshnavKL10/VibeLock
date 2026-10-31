# Secure code review

Procedure for `SKILL.md` Phase 9. Read it when the project has application code with entry points that accept input. The plan (Phase 6) sets the scope and depth.

**Goal:** find weaknesses that matter *in this project*. A match on a risky-looking pattern is a **lead**, never a finding. Report something only when you can explain how untrusted input reaches it, what stops it, and what an attacker would gain.

## Rules

1. **Trace, don't grep.** Search output and scanner results tell you where to read. They don't tell you what is wrong.
2. **Report only what you can support.** Say what you read, what you ran, and what you assumed.
3. **Say what you didn't review.** "No findings" is only about the code you read. Never write "reviewed the codebase" if you read part of it.
4. **Tools are optional and their output is a lead.** If installed, static analyzers (for example Semgrep, CodeQL, Bandit, gosec, Brakeman, SpotBugs with Find Security Bugs, ESLint security plugins) can point you at code. Judge every result with the steps below. Don't copy results into the report unexamined, and don't install a tool without asking.
5. **Don't run the project's code** to prove a point unless it is a local test you wrote, on a system you're authorized to test (SKILL.md Phase 9).

## Step 1: Decide the scope

Start from the threats and trust boundaries you mapped (Phases 3 and 4). Review, in this order:

1. **Entry points** that accept input: routes, handlers, GraphQL resolvers, webhook receivers, message consumers, CLI arguments, file and archive parsers, deep links, IPC, MCP tool handlers.
2. **High-risk components** from the risk assessment: authentication, authorization, session handling, payments, file uploads, admin features, cryptography, secrets handling, anything that runs commands or queries.
3. **Shared code** those paths call: data access, validation, middleware, helpers.

| Tier of the component | Depth |
|---|---|
| Basic | Entry points that touch files, commands, queries, or secrets. Quick read. |
| Standard | All entry points, authentication, authorization, and the data-access layer |
| Advanced or Critical | Every high-risk component, traced end to end, with local tests for the important findings |

For a large codebase, a sample is acceptable **if you say so**. Keep a coverage list: modules reviewed, modules skipped, and why. Anything not reviewed is NOT TESTED, not PASS.

## Step 2: Look for leads

Use the table to know what to read for. The last column lists the controls in `PLATFORMS.md` that describe the fix, so you don't restate them.

| Weakness | Leads (what to look for) | What makes it safe | Often a false positive when | Controls |
|---|---|---|---|---|
| **SQL and NoSQL injection** | Queries built by string concatenation, f-strings, or template literals. Raw-query APIs fed variables. JSON bodies passed straight into NoSQL filters (operators like `$ne`, `$where`). | Parameterized queries or bound ORM parameters. Allow-lists for column and table names. Schema validation that rejects objects where strings are expected. | Only constants are interpolated, or the ORM binds the values | API-02 |
| **Command injection** | `exec`, `system`, `popen`, `subprocess` with `shell=True`, `child_process.exec`, backticks, `Runtime.exec` built from strings that include input | Argument arrays with no shell. An allow-list of commands. | The command and every argument are constants | API-02 |
| **Template and code injection** | `eval`, `exec`, `Function(...)`, `vm`, server-side templates rendered from user-supplied strings, reflection on user-supplied names | Don't evaluate input. Fixed templates with data passed as variables. | `eval` of a constant in a build script | CODE-07 |
| **Broken authentication** | Hand-written login or token code. Password comparison with `==`. Reset tokens that are guessable or never expire. A login check that can be skipped by a flag. Default credentials. JWT decoded without verification, or `alg` taken from the token. | An established auth library or provider. Verified algorithm, signature, `exp`, `aud`. Expiring single-use reset tokens. Rate limiting. | Test fixtures and local-only scripts that aren't deployed | AUTH-01, AUTH-02, AUTH-05, AUTH-07, API-05 |
| **Broken authorization** | A handler that loads a record by an ID from the path, query, or body with no ownership or tenant check. Admin routes that only check "logged in". A role taken from a client-supplied field. Mass assignment of `role` or `isAdmin`. Checks done only in the UI. GraphQL resolvers with no checks. | The ownership condition in the query itself (`WHERE id=? AND owner=?`) or a central policy layer. Default deny. Tests for another user's ID. | The resource is public by design | API-01, AUTH-03, GQL-01 |
| **Session handling** | Session IDs in URLs. Cookies without `Secure`, `HttpOnly`, `SameSite`. No new session after login. No expiry. Logout that doesn't invalidate server-side. Predictable IDs. | Framework session management with secure flags, rotation on login, expiry | Token-based APIs that don't use cookies | AUTH-04, WEB-05, WEB-06 |
| **Unsafe input and output handling** | HTML built by concatenation. `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, `\|safe`, `Markup()`. Redirects to a user-supplied URL. Server-side fetch of a user-supplied URL (SSRF). User values copied into HTTP headers. | Context-aware escaping by the framework. An established sanitizer. Allow-lists for URLs and redirect targets. Schema validation. | The value is a constant, or an upstream layer sanitizes it on every path (verify) | WEB-02, WEB-03, API-04, API-08 |
| **Path traversal and unsafe file operations** | User input in a path for read, write, delete, or send. Archive extraction without a per-entry path check (zip-slip). Upload names used as given. World-writable permissions. Predictable temp files. Symlinks followed. | Resolve the real path, then check it is inside the allowed directory. Generated file names. A checked extraction routine. | The path comes from configuration or constants | CODE-01, CODE-09, API-03 |
| **Insecure deserialization** | `pickle.loads`, `yaml.load` with an unsafe loader, `marshal`, Java `ObjectInputStream`, PHP `unserialize`, .NET `BinaryFormatter`, Json.NET `TypeNameHandling` other than none, Ruby `Marshal.load` or `YAML.load` | Data-only formats (JSON) with schema validation. `yaml.safe_load`. Allow-listed types. | Data produced and consumed only inside one trusted process (verify that boundary) | CODE-02 |
| **Cryptographic misuse** | MD5 or SHA-1 for passwords or signatures. Fast or unsalted password hashes. ECB mode. Hard-coded keys. Reused nonces or IVs. `Math.random` or `random` for tokens. Home-made crypto. Encryption with no authentication. MAC comparison with `==`. | Maintained libraries and high-level APIs. Authenticated encryption. A secure random source. Argon2id, bcrypt, or scrypt for passwords. Constant-time comparison. | MD5 or SHA-1 used as a plain checksum or cache key | CODE-03, AUTH-02 |
| **Insecure network communication** | `http://` for sensitive data. `verify=False`, `rejectUnauthorized: false`, `InsecureSkipVerify`, trust-all managers, disabled hostname checks. Secrets in URLs. No timeouts. | TLS verification on. HTTPS only. Secrets in headers or bodies. Timeouts. | Local development config that isn't shipped | CODE-04, ALL-07, AND-02 |
| **Unsafe error handling and information disclosure** | Stack traces or SQL errors returned to clients. Debug mode on. Messages that reveal whether an account exists. Passwords, tokens, or personal data in logs. Catch blocks that allow access on error. | Generic client errors with detail in logs (no secrets). Fail closed. | Verbose errors only in a build that isn't deployed | API-07, ALL-09, CODE-08 |
| **Race conditions** | Check-then-act on balances, coupons, stock, rate limits, or unique names with no database constraint. Check-then-open on files. Non-atomic read-modify-write. A payment or webhook handled twice. Shared mutable state in concurrent servers. | Transactions with suitable isolation or row locks. Unique constraints. Atomic updates. Idempotency keys. | Single-threaded scripts with one trusted user | CODE-05, PAY-05 |
| **Business-logic abuse** | Trusting a client-supplied price, quantity, or role. Negative quantities. Skipping a workflow step. Unlimited free-tier use. | Server-side recalculation. Explicit state machines. Limits. | None. Read the flow. | PAY-03, API-05 |
| **Other** | XML parsers with external entities enabled, regular expressions that can backtrack catastrophically, open redirects, CSRF on cookie-authenticated state changes, permissive CORS | See the controls | | CODE-06, CODE-10, WEB-06, WEB-07 |

If the project was built largely with AI assistance, read extra carefully for: new endpoints with no authorization check, trusting client values, permissive CORS, leftover debug or test credentials, string-built queries, and packages that don't exist (hand those to the dependency assessment).

## Step 3: Trace each lead

For every candidate, write down the chain. If you can't complete it, you don't have a finding yet.

1. **Source:** where does untrusted data enter? (request, file, message, tool output, environment)
2. **Path:** what transforms it? Is there validation, escaping, or normalization? Read it, don't assume it.
3. **Sink:** what dangerous operation does it reach?
4. **Control:** what stops it (framework protection, a check, a constraint)? Does it apply on **every** path to the sink?
5. **Reachability:** who can trigger it: anonymous, authenticated, admin, an internal job? Is it behind a flag or in dead code?
6. **Preconditions:** specific configuration, input format, timing window?
7. **Impact:** what does an attacker gain given the privileges and the data this code touches?

## Step 4: Judge, don't flag

**Don't report:**

- Code that only handles constants.
- Test, fixture, or local-only scripts that aren't deployed (unless they hold real credentials, which goes to the secret assessment).
- Vendored or third-party code (that belongs to the dependency assessment).
- A pattern whose risk is removed by a control you verified on all paths.

**If a control exists but you can't verify it covers every path,** report it as NEEDS REVIEW with Medium or Low confidence and name the exact question a person must answer ("Is `sanitize()` applied on the import path as well?").

**Severity** comes from impact and ease, in this project (see the severity guide in `examples/REPORT_TEMPLATE.md`). Lower it when the code is reachable only by admins or needs unlikely preconditions. Raise it for unauthenticated access, sensitive data, money, or a component rated Advanced or Critical. State why.

**Confidence** (see the confidence guide in `examples/REPORT_TEMPLATE.md`): High needs either a local test you ran that demonstrates it, or a complete traced path with no control on any route to the sink. Static reading with one unverified step is Medium at most. A plausible suspicion is Low and is NEEDS REVIEW.

## Step 5: Confirm safely

- Prefer proof by reading: the full source-to-sink path with file and line.
- Where the project has a test setup and you're authorized, write a **small local test** that shows the weakness with a harmless input (for example a marker string, or a request for another user's record) and run it. Show the command and the result.
- Never attack production or a third party. No exploit payloads that change data, and no load or race testing against shared systems.
- If you can't run anything, say the finding is static-only, and cap confidence at Medium.

## Step 6: Fix and re-verify

Fixes need the plan's approval (SKILL.md Phase 7). Then:

1. Make the **smallest change** that removes the weakness, using the framework's or platform's mechanism. Don't invent security primitives. Don't refactor unrelated code.
2. Preserve behavior. If the fix changes behavior (for example it rejects input that used to work), say so.
3. Add a regression test where the project has a test setup.
4. In Phase 10, re-read your diff.
5. Say "fixed" only after the test or check that showed the problem now passes. Otherwise say "changed, not yet verified".

Changes to the authentication, session, or permission model, or to the data model, are approval items in SKILL.md.

## Reporting

- Use the finding template in `examples/REPORT_TEMPLATE.md`. Include the source-to-sink path in a few lines, reachability, what attacker is required, impact, confidence, and **what you couldn't verify**.
- **Coverage:** list the modules reviewed and skipped.
- **Assessment status** (see SKILL.md Phase 9): FAIL if there are confirmed findings; PASS only if the planned scope was fully reviewed and nothing was confirmed; NEEDS REVIEW if only unverified suspicions or partial coverage; NOT TESTED or BLOCKED if you couldn't read the code or run what you needed; NOT APPLICABLE if there is no application code.
- "No confirmed findings in the reviewed scope" never means "the code is secure".
