# Dependency security assessment

Procedure for `SKILL.md` Phase 9. Read it when the project has any dependency manifest or lockfile. The plan (Phase 6) sets the depth.

**Goal:** find which dependencies put this project at risk, how sure you are, how urgent each one is, and the smallest safe fix, without changing anything until the user approves.

## Rules

1. **Read-only by default.** Don't install, update, or remove packages. Don't run commands that execute project or dependency code (installs that run scripts, Maven or Gradle builds, test runs on unreviewed code) without approval. Lockfile-based audit commands install nothing.
2. **Never state a vulnerability ID, affected range, or fixed version from memory.** Take it from a tool's output or an advisory you fetched, and record which one and when. If you can't, it is an Unverified suspicion.
3. **Tools are optional.** Use what is installed. If nothing is, say so and report NOT TESTED for the vulnerability check. Don't install a tool without asking.
4. **Commands change between versions.** If one fails, read `--help` or the tool's documentation. Don't guess flags.
5. **Audits send package names and versions to a remote service.** For a private project, tell the user before you run one.

## Step 1: Inventory

List manifests and lockfiles, including monorepo packages and nested folders. This command is read-only:

```bash
find . \( -name node_modules -o -name .git -o -name vendor -o -name target -o -name .venv -o -name venv -o -name dist \) -prune -o -type f \( \
  -name package.json -o -name package-lock.json -o -name npm-shrinkwrap.json -o -name pnpm-lock.yaml -o -name yarn.lock \
  -o -name 'requirements*.txt' -o -name pyproject.toml -o -name Pipfile -o -name Pipfile.lock -o -name poetry.lock -o -name uv.lock -o -name setup.py -o -name setup.cfg \
  -o -name pom.xml -o -name 'build.gradle' -o -name 'build.gradle.kts' -o -name 'libs.versions.toml' -o -name gradle.lockfile \
  -o -name Cargo.toml -o -name Cargo.lock -o -name go.mod -o -name go.sum \
  -o -name composer.json -o -name composer.lock \
  -o -name '*.csproj' -o -name Directory.Packages.props -o -name packages.config -o -name packages.lock.json \
  -o -name Gemfile -o -name Gemfile.lock -o -name pubspec.yaml -o -name pubspec.lock -o -name Podfile.lock -o -name Package.resolved \
  -o -name Dockerfile -o -name 'Dockerfile.*' \) -print
```

It skips `vendor/`. If the project commits vendored dependencies, say so and inspect them separately.

For each manifest, record: ecosystem, runtime versus dev dependencies, whether a **lockfile** exists, and anything unusual: dependencies from a git URL or a tarball, unpinned versions (`*`, `latest`), a non-default registry, and install scripts. **No lockfile means the transitive versions are unknown**, so confidence is lower and you say so.

Also list container base images (`FROM` lines) and CI action references (`uses:` lines). Their pinning is covered by SRV-11 and CI-03, not here.

## Step 2: Choose checks

Use tools that are already installed. Prefer ones that read the lockfile and don't run code.

| Ecosystem | Vulnerabilities | Outdated | Why is it here? | Notes |
|---|---|---|---|---|
| npm | `npm audit` | `npm outdated` | `npm ls <pkg>` | Audit queries the registry for the lockfile's versions |
| pnpm | `pnpm audit` | `pnpm outdated` | `pnpm why <pkg>` | |
| Yarn 1 | `yarn audit` | `yarn outdated` | `yarn why <pkg>` | |
| Yarn 2+ | `yarn npm audit` | no built-in equivalent. Check the registry, or ask before adding a plugin. | `yarn why <pkg>` | `yarn upgrade-interactive` changes files. Use it only after approval. |
| Python | `pip-audit` | `pip list --outdated` | `pipdeptree`, `poetry show --tree`, `uv tree` | Resolving unpinned requirements can build packages and run their code. Prefer auditing a fully pinned lock file, and ask before anything that installs. |
| Java and Kotlin (Maven) | OWASP Dependency-Check | `mvn versions:display-dependency-updates` | `mvn dependency:tree` | Maven and Gradle run build scripts and plugins. Ask first. No standard lockfile, so resolved versions come from the build tool. |
| Java and Kotlin (Gradle) | OWASP Dependency-Check | a versions plugin, if configured | `gradle dependencyInsight --dependency <name>` (add `--configuration` if it asks) | `gradle.lockfile` exists only if dependency locking is on |
| Rust | `cargo audit` | `cargo outdated` | `cargo tree -i <crate>` | `cargo audit` and `cargo outdated` are separate installs |
| Go | `govulncheck ./...` | `go list -m -u all` | `go mod why -m <module>` | `govulncheck` separates vulnerabilities in code your project actually calls from those in modules it merely requires, which is useful reachability evidence |
| PHP | `composer audit` | `composer outdated` | `composer why <pkg>` | |
| .NET | `dotnet list package --vulnerable --include-transitive` | `dotnet list package --outdated` | `dotnet list package --include-transitive` | |
| Anything else (Ruby, Dart, Swift, CocoaPods, others) | `osv-scanner`, `trivy fs`, or `grype`, if installed | the ecosystem's own tool | the ecosystem's own tool | See each tool's `--help` for current syntax |

If you have web access and no tool is installed, look up specific package and version pairs in an advisory database (see PLATFORMS.md, References: OSV, GitHub Advisory Database, NVD, and the ecosystem's own database). Record the ID, source, and date you queried. This is a manual lookup, not a scan, so label it that way.

## Step 3: Classify each finding

Every item gets exactly one class. This is what keeps confirmed vulnerabilities apart from mere age and from hunches.

| Class | Meaning | Evidence needed | Status |
|---|---|---|---|
| **Confirmed vulnerability** | An advisory matches the resolved version of a package in this project | Advisory ID, source and date queried, resolved version, affected range, fixed version (all taken from the tool or advisory, not from memory) | FAIL (if Medium confidence or better) |
| **Outdated only** | A newer version exists and no advisory applies | The tool's output | Not a finding. List as Info at most. |
| **Unmaintained or deprecated** | The registry or repository marks it deprecated, archived, or end-of-life | The registry or repository page | NEEDS REVIEW, usually Low or Medium |
| **Unverified suspicion** | Something looks wrong but you couldn't verify it. Examples: a name one character off a popular package, an unexpected source, a surprising install script, an unpinned git dependency | What you saw, and what you couldn't check | NEEDS REVIEW |

Do not present an outdated package as vulnerable, and do not present a suspicion as confirmed.

## Step 4: Check whether it is actually used

Do this for every Confirmed vulnerability, in order of advisory severity:

1. **Runtime or not?** Dev, test, and build-only dependencies don't ship to users. They still matter for the build machine and CI, but the exposure differs.
2. **Is the package imported?** Search the source for imports of it. A direct dependency that nothing imports is a removal candidate (ALL-17).
3. **Is the vulnerable feature used?** Advisories usually name the affected function, option, or configuration. Search for it.
4. **Can untrusted input reach it?** Trace from the entry points (Phase 3) to the call. If the tool reports reachability (for example `govulncheck`), cite it.

Record the result as **Reachable** (you traced a path), **Possibly reachable** (imported, but the path is unclear), **Not reachable or not shipped**, or **Unknown**. Say how you decided.

## Step 5: Transitive dependencies

For a vulnerable package you didn't add yourself, use the "why is it here" command to find which direct dependency pulls it in. Then the options are, in order of preference:

1. Upgrade the **direct parent** to a release that depends on a fixed version.
2. Force the fixed version with the ecosystem's override mechanism (`overrides` in npm and pnpm, `resolutions` in Yarn, `dependencyManagement` in Maven, constraints in Gradle, `replace` in Go). This can break the parent, so it needs approval and a test run.
3. Replace the parent library.
4. If no fix exists, record it as an accepted risk with a mitigation (disable the affected feature, restrict who can reach it) and mark NEEDS REVIEW.

Without a lockfile, say that transitive coverage is incomplete.

## Step 6: Prioritize

Report two severities: the **advisory's** rating and the **project's** rating after context.

- **Lower it one level** if the dependency is dev, test, or build-only; the vulnerable feature isn't used; or the attacker would need privileges they don't have.
- **Raise it one level** (never above Critical) if the vulnerability is known to be exploited (check the CISA Known Exploited Vulnerabilities catalog or the advisory text) or it is reachable by unauthenticated users on a public component, or the component is rated Advanced or Critical.
- Say why, in a sentence.

| Priority | Typical case |
|---|---|
| **P1: act now** | Confirmed, High or Critical for this project, reachable or known to be exploited, on an exposed component |
| **P2: plan soon** | Confirmed High or Critical but not shown reachable, or Medium and reachable |
| **P3: routine** | Everything else: dev-only, unused feature, Low, or unmaintained with no known issue |

## Step 7: Recommend a safe upgrade path

Don't upgrade anything yet. For each P1 and P2 item, prepare:

| Package | Current | Fixed in | Smallest safe target | Change type | Breaking-change risk | Code that uses it | Test plan |
|---|---|---|---|---|---|---|---|

How to choose the target:

- Take the **fixed version from the advisory**, then the **smallest change** that reaches it: patch before minor before major.
- Read the release notes or changelog between the current and target versions for breaking changes, and check the runtime or engine requirements and peer dependencies.
- Prefer a release that has been public for a while over one published hours ago, unless the vulnerability is being exploited. Brand-new releases are where compromised-maintainer releases appear. This is a heuristic, not a guarantee.
- Group only upgrades that are related. Otherwise do one at a time.
- If the only fix is a major version, show the options and effort and let the user decide.
- If there is no fix, see Step 5, item 4.

**Don't run bulk or forcing commands** such as `npm audit fix --force`, `npm update`, `pip install -U -r requirements.txt`, `go get -u ./...`, `cargo update` with no package named, or `composer update` with no package named. Propose the specific change instead.

## Step 8: After the user approves a change

1. Run the baseline tests first (Phase 8), or note that none exist.
2. Apply one upgrade, or one related group.
3. Read the **lockfile diff**: only the intended packages should change, with no new packages, source registries, or install scripts you didn't expect.
4. Re-run the tests and the same audit command.
5. Say "fixed" only if the advisory no longer appears **and** the tests ran. Otherwise say "applied, verification pending" or "applied, tests unavailable".

## Reporting

- Use the finding template in `examples/REPORT_TEMPLATE.md`. Include the class, advisory ID and source, resolved and fixed versions, both severities, reachability, and confidence.
- **Assessment status** (see SKILL.md Phase 9): FAIL if there is a Confirmed vulnerability; PASS only if the planned scope was fully covered by a tool that ran and nothing was confirmed; NEEDS REVIEW if only suspicions or partial coverage; NOT TESTED or BLOCKED if no tool or database was available; NOT APPLICABLE if there are no dependencies.
- **Always state:** the tool and version (or the advisory source) used and when, whether the check needed network access, whether a lockfile existed, what was not covered (private registries, vendored code, unresolved transitive depth), and that advisory databases lag behind discoveries.
- "No confirmed vulnerabilities" means none were found by this check in this scope. It never means the dependencies are safe.
