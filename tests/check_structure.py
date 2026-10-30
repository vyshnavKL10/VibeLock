#!/usr/bin/env python3
"""Maintainer lint for the VibeLock repository. Python standard library only.

This is NOT part of the skill and NOT a security scanner. It checks that the
repository's own files are consistent: required files exist, the skill
frontmatter is valid, relative links resolve, control IDs are well formed and
unique, IDs referenced elsewhere exist, status names are present, scenario files
have the required sections, and no leftover placeholders remain.

Usage (from anywhere):  python3 tests/check_structure.py
Exit code 0 if no FAIL results, 1 otherwise. WARN does not fail the run.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
results = []  # (level, message)


def ok(msg): results.append(("PASS", msg))
def fail(msg): results.append(("FAIL", msg))
def warn(msg): results.append(("WARN", msg))


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


# 1. Required files
REQUIRED = ["SKILL.md", "PLATFORMS.md", "README.md", "LICENSE", "SECURITY.md",
            "CONTRIBUTING.md", ".gitignore", "docs/ARCHITECTURE.md",
            "docs/RISK_MODEL.md", "docs/VALIDATION_PLAN.md", "docs/THREAT_MODEL.md",
            "examples/REPORT_TEMPLATE.md"]
for rel in REQUIRED:
    (ok if (ROOT / rel).is_file() else fail)(f"required file present: {rel}")

# 2. Exactly one SKILL.md
skills = [p for p in ROOT.rglob("SKILL.md") if ".git" not in p.parts]
(ok if len(skills) == 1 else fail)(f"exactly one SKILL.md (found {len(skills)})")

# 3. Frontmatter rules
if (ROOT / "SKILL.md").is_file():
    text = read("SKILL.md")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        fail("SKILL.md has YAML frontmatter")
    else:
        keys = {}
        for line in m.group(1).splitlines():
            if re.match(r"^[A-Za-z_-]+:", line):
                k, v = line.split(":", 1)
                keys[k.strip()] = v.strip()
        allowed = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
        extra = set(keys) - allowed
        (ok if not extra else fail)(f"frontmatter keys allowed (unexpected: {sorted(extra) or 'none'})")
        name = keys.get("name", "")
        (ok if re.fullmatch(r"[a-z0-9-]{1,64}", name) else fail)(f"name is kebab-case, <=64 chars ({name!r})")
        desc = keys.get("description", "")
        (ok if 0 < len(desc) <= 1024 else fail)(f"description length 1..1024 ({len(desc)})")
        (ok if "<" not in desc and ">" not in desc else fail)("description has no angle brackets")
    n = len(text.splitlines())
    (ok if n < 500 else warn)(f"SKILL.md under 500 lines ({n})")

# 4. Control IDs in PLATFORMS.md
ctrl_re = re.compile(r"^- ([A-Z]{2,4}-\d{2}) \[L([1-4])\+\] ", re.M)
bullet_re = re.compile(r"^- ([A-Z]{2,4}-\d{2})\b", re.M)
ids = []
if (ROOT / "PLATFORMS.md").is_file():
    plat = read("PLATFORMS.md")
    ids = [m.group(1) for m in ctrl_re.finditer(plat)]
    bullets = [m.group(1) for m in bullet_re.finditer(plat)]
    (ok if len(ids) == len(bullets) else fail)(
        f"every control bullet has a well-formed [Ln+] tag ({len(ids)} of {len(bullets)})")
    dups = sorted({i for i in ids if ids.count(i) > 1})
    (ok if not dups else fail)(f"control IDs unique (duplicates: {dups or 'none'})")
    ok(f"control count: {len(ids)}")
prefixes = {i.split("-")[0] for i in ids}
idset = set(ids)

# 5. IDs referenced elsewhere exist (range shorthand like MCP-01 to MCP-09 and
#    wildcard like AUTH-* are fine; only exact IDs with a known prefix are checked)
ref_re = re.compile(r"\b([A-Z]{2,4})-(\d{2})\b")
unknown = set()
for path in list(ROOT.glob("tests/*.md")) + list(ROOT.glob("docs/*.md")) + \
        [ROOT / "SKILL.md", ROOT / "README.md", ROOT / "examples/REPORT_TEMPLATE.md"]:
    if not path.is_file():
        continue
    for m in ref_re.finditer(path.read_text(encoding="utf-8")):
        if m.group(1) in prefixes and f"{m.group(1)}-{m.group(2)}" not in idset:
            unknown.add((path.relative_to(ROOT).as_posix(), m.group(0)))
(ok if not unknown else fail)(f"referenced control IDs exist (missing: {sorted(unknown) or 'none'})")

# 6. Relative links resolve (outside fenced code blocks)
link_re = re.compile(r"\]\(([^)\s]+)\)")
bad = []
for path in ROOT.rglob("*.md"):
    if ".git" in path.parts:
        continue
    body = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
    body = re.sub(r"````.*?````", "", body, flags=re.S)
    for m in link_re.finditer(body):
        target = m.group(1)
        if re.match(r"^(https?:|mailto:|#)", target):
            continue
        target = target.split("#")[0]
        if target and not (path.parent / target).resolve().exists():
            bad.append((path.relative_to(ROOT).as_posix(), target))
(ok if not bad else fail)(f"relative links resolve (broken: {bad or 'none'})")

# 7. Six statuses present in the files that define or use them
STATUSES = ["PASS", "FAIL", "NOT TESTED", "BLOCKED", "NEEDS REVIEW", "NOT APPLICABLE"]
for rel in ["SKILL.md", "README.md", "examples/REPORT_TEMPLATE.md"]:
    if (ROOT / rel).is_file():
        t = read(rel)
        missing = [s for s in STATUSES if s not in t]
        (ok if not missing else fail)(f"{rel} mentions all six statuses (missing: {missing or 'none'})")

# 8. Scenario files have the required sections
SECTIONS = ["## Fixture", "## Prompt", "## Expected discovery", "## Expected questions",
            "## Risks and tier", "## Controls", "## Pass criteria"]
scen = sorted(ROOT.glob("tests/[0-9][0-9]-*.md"))
(ok if len(scen) == 10 else fail)(f"ten scenario files (found {len(scen)})")
for sp in scen:
    t = sp.read_text(encoding="utf-8")
    missing = [s for s in SECTIONS if s not in t]
    (ok if not missing else fail)(f"{sp.name} has all required sections (missing: {missing or 'none'})")
    crit = re.search(r"## Pass criteria\n(.*)", t, re.S)
    n = len(re.findall(r"^\d+\. ", crit.group(1), re.M)) if crit else 0
    (ok if n >= 4 else fail)(f"{sp.name} has at least 4 numbered pass criteria ({n})")

# 9. Install path in README matches the skill folder name
if (ROOT / "README.md").is_file():
    r = read("README.md")
    (ok if ".claude/skills/vibelock" in r else fail)("README install path uses the folder name 'vibelock'")

# 10. Leftover placeholders
for path in ROOT.rglob("*"):
    if path.is_file() and ".git" not in path.parts and path.suffix in {".md", ""} and path.name != "check_structure.py":
        try:
            t = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if "<your-username>" in t:
            fail(f"leftover placeholder <your-username> in {path.relative_to(ROOT).as_posix()}")
if (ROOT / "LICENSE").is_file() and "<your name or organization>" in read("LICENSE"):
    warn("LICENSE still contains the copyright-holder placeholder: replace it before publishing")

# Report
width = max(len(m) for _, m in results)
for level, msg in results:
    print(f"{level:4}  {msg}")
counts = {k: sum(1 for l, _ in results if l == k) for k in ("PASS", "FAIL", "WARN")}
print(f"\n{counts['PASS']} passed, {counts['FAIL']} failed, {counts['WARN']} warnings")
sys.exit(1 if counts["FAIL"] else 0)
