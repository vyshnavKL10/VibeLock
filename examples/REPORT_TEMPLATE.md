# VibeLock templates

Two templates for the agent: the **Plan** (Phase 7) and the **Report** (Phase 11). Copy the structure, delete what doesn't apply, and keep it short for small projects. Every value in the worked example at the bottom is **fictional**.

## Status vocabulary

| Status | Meaning |
|---|---|
| PASS | The check ran and the output shows the requirement is met (cite command and result) |
| FAIL | The check ran and the requirement is not met |
| NOT TESTED | No check was run. Not a pass. |
| BLOCKED | A check was needed but couldn't run (no access, permission, environment, or approval) |
| NEEDS REVIEW | A person or specialist must judge it |
| NOT APPLICABLE | The control doesn't apply to this project (give the reason). Not a gap. |

## Severity guide

Severity is about one finding and decides urgency. The tier (see `docs/RISK_MODEL.md`) is about the project and decides depth.

| Severity | Typical meaning |
|---|---|
| Critical | Exploitable now with severe impact: an exposed live secret, unauthenticated admin access, remote code execution |
| High | Exploitable with some effort or preconditions, serious impact: broken object-level authorization, SQL injection |
| Medium | Real weakness with limited impact or hard preconditions: missing rate limiting on login, weak headers |
| Low | Minor hardening gap: verbose errors, missing optional headers |
| Info | Observation or good practice, no direct risk |

## Plan template (Phase 7)

````markdown
# Security plan: <project>   [PROVISIONAL if unknowns remain]

Depth: Light | Standard | Full (why)
Date: ...

## Summary
One paragraph: what the project is, the overall tier, and the reasoning.
The tier guides depth of review. It is not a certification or a guarantee.

## Facts
| Item | Status (Confirmed / Assumption / Unknown / Needs approval) | Detail and source |

## Assets, data flows, trust boundaries, identities
(short list or table; a small diagram only if it helps)

## Realistic threats and abuse cases
1. <who does what to which asset, enabled by what>

## Risk
| Component | Likelihood | Impact | Tier | Evidence for the ratings |

## Proposed controls (ordered by risk reduction per effort)
| ID | Control | Class (Mandatory / Recommended / Conditional) | Why it fits here | Effort | Needs approval? |

## Not applicable, rejected, or deferred
| ID or request | Decision | Reason | Alternative |

## Decisions I need from you
1. ...
````

## Finding template (Phase 11)

````markdown
### <ID>: <Title>
- **Severity:** Critical | High | Medium | Low | Info
- **Status:** PASS | FAIL | NOT TESTED | BLOCKED | NEEDS REVIEW | NOT APPLICABLE
- **Affected:** component or file(s), with line numbers if useful
- **Evidence:** what you saw or ran. Command and result summary. Never include secret values.
- **Reproduction (only when safe):** steps against a local or authorized environment
- **Why it matters:** the realistic consequence
- **Recommended remediation:** the specific change
- **Verification method:** how to confirm the fix, and the command or test
````

## Report template (Phase 11)

````markdown
# VibeLock report: <project>   [PROVISIONAL if unknowns remain]

Date: ...   Overall tier: ...   Depth: ...

## Scope
Examined: files, folders, configs, and tools actually used.
Not examined: everything else that matters (for example "live server", "mobile build", "CI settings").

## Results
| ID | Control or check | Status | Evidence (command, file, or summary) |

## Findings
(one finding block each, highest severity first)

## What changed
Files modified and why. Behaviour changes called out.

## Review of the changes
Regression check against the baseline, diff review, new risks considered.

## Not covered and limitations
What could not be tested and why. Tools that were missing.

## Residual risk
What could still go wrong, in plain language, and what would reduce it next.

## Unresolved issues and next actions
Now / Before launch / Later. Re-run triggers. Whether professional review is advisable.

This work reduces risk. It is not a guarantee that the project is secure.
````

## Worked example (fictional)

A made-up project to show the level of detail. Nothing below was actually run.

````markdown
### API-01: Order endpoint lacks per-object authorization
- **Severity:** High
- **Status:** FAIL
- **Affected:** `src/routes/orders.js`, handler for `GET /orders/:id` (lines 18-31)
- **Evidence:** The handler loads the order by ID and returns it after checking only that a session exists.
  Local test `orders.authz.test.js` (written during this review): user B requests user A's order and receives
  200 with A's data. Command: `npm test -- orders.authz`. Result: 1 failed, 4 passed.
- **Reproduction (local only):** Log in as user B in the dev environment, request an order ID created by user A.
- **Why it matters:** Any logged-in user can read any other user's orders, including names and addresses.
- **Recommended remediation:** Query orders by both `id` and the session user's ID (or check ownership before
  returning), and return 404 when they don't match.
- **Verification method:** Re-run `npm test -- orders.authz`; the user-B request must return 404.
````
