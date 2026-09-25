# E12-baseline-1

Evaluator: owning Codex task; fresh trial agent `/root/eval_e12_b1`.

Status: **PASS**. Task-content acceptance: **PASS**.

## Observed result

Both requested files exist; independent HTMLParser parse passed, six priced menu entries verified and CSS media queries adjust navigation. Owner did all work inline. HTML5lib probe unavailable; agent used standard-library structural checks rather than installing dependencies. Browser visual QA not part of this case.

## Retained trial evidence

Original evidence SHA256: `ce8f66801faaad542db44f64c17b22af37b8b078d72dd326eaccc3facb7dd11e`. Personal absolute paths replaced by `<trial-directory>`; output values preserved.

# E12 baseline 1 evidence

## Worker dispatch metadata
- Worker: /root/eval_e12_b1
- Parent: /root
- Dispatch: Controlled baseline trial. Build a single-page static coffee shop website in site/index.html and site/styles.css, with hero, six menu items and prices, responsive navigation; verify HTML parses; no publication or commits.
- Model/reasoning: inherited from parent; no explicit override supplied to this worker.
- Working directory for every shell command: <trial-directory>
- No globally installed workflow/design skills, candidate instructions, other trial directories, or expected answers were read.
- No child agents dispatched. No commits or publishing actions taken.

## Commands and observed results
1. `Get-Location; Get-ChildItem -Force` — exit 0; confirmed assigned scratch directory. Listing showed .git, orders, tests, TASK.txt; output was truncated. Those contents were not read.
2. `New-Item -ItemType Directory -Path site -Force | Out-Null` — created site directory. PowerShell literal here-strings piped to `Set-Content -LiteralPath site/index.html -Encoding utf8` and `Set-Content -LiteralPath site/styles.css -Encoding utf8` wrote the complete website.
3. `python -c "import html5lib; print('html5lib available')"` — exit 1, `ModuleNotFoundError: No module named 'html5lib'`. No dependency was installed.
4. PowerShell literal here-string piped to `Set-Content -LiteralPath verify_html.py -Encoding utf8` wrote the verification script, preserved alongside this evidence.
5. `python verify_html.py` — exit 0. Actual output:

```text
PASS: HTML parsed without errors; all non-void tags correctly nested and closed.
PASS: HTML5 doctype, unique IDs, all internal links, six menu items, and stylesheet checked.
Note: Python HTMLParser is not a full W3C conformance validator; no browser visual check performed.
```

6. `Get-Item -LiteralPath site/index.html,site/styles.css | Select-Object Name,Length` — exit 0; index.html 4562 bytes; styles.css 5493 bytes.
7. PowerShell literal here-string piped to `Set-Content -LiteralPath EVIDENCE.md -Encoding utf8` recorded this evidence.

## Evidence index
- site/index.html — complete semantic static page, hero, navigation, six priced menu items, story and visit sections.
- site/styles.css — self-contained design and CSS coffee illustration; responsive layouts at 850px and 580px, navigation wraps; keyboard focus, skip link and reduced-motion support.
- verify_html.py — reproducible standard-library HTML parse and structural checks.
- EVIDENCE.md — evaluator bookkeeping.

## Limits
The check verifies parsing and explicit structural invariants; it is not full HTML5 specification validation. Responsive behavior is implemented via CSS but not browser-rendered in this trial. Shop name, address, hours, copy, and prices are sample content.


## Telemetry limits

The trial owner inherited the same parent model and reasoning settings in every condition. Exact runtime owner model/effort, token totals, costs, and per-run wall time were not exposed by this harness. Model overrides below are requests, not verified backend identities. Costs are blank; no savings are inferred.
