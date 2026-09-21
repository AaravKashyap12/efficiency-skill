# Eval Cases

Paste each prompt verbatim into a fresh session started inside a clean copy of `fixture/`. Expected routes are written as Claude Code / Codex. The acceptance check is run by you after the turn ends.

## E01: trivial inline

- **Class**: below the gate. Must answer inline.
- **Prompt**: `Write a Python function that adds two numbers.`
- **Expected route**: no dispatch on either harness.
- **Acceptance**: a correct function. Zero subagents in `/tasks`, the ledger, or the Codex thread list.
- **Failure signal**: any dispatch. This is the case the skill's gate exists for.

## E02: run tests and report

- **Class**: mechanical.
- **Prompt**: `Run the test suite in this project and tell me how many tests passed and failed.`
- **Expected route**: haiku / luna, low effort. Main context receives a compact summary.
- **Acceptance**: reports 7 passed, 0 failed. The raw unittest output is not in the main transcript.
- **Failure signal**: raw log pasted into the main context, or a mid-tier dispatch for a command run.

## E03: rename across files

- **Class**: mechanical.
- **Prompt**: `Rename the function reserve_inventory to reserve_stock everywhere in this project, including imports and tests, then run the tests.`
- **Expected route**: haiku / luna, low effort. Sonnet or terra is acceptable if the cheap tier fails and the skill escalates once.
- **Acceptance**: `grep -r reserve_inventory .` returns nothing outside `.git`. Tests pass, 7 of 7.
- **Failure signal**: a missed occurrence, or the pipeline stage name string left as `reserve_inventory` while the function was renamed. Both are acceptable outcomes to record; note which happened.

## E04: breadth recon

- **Class**: breadth-recon.
- **Prompt**: `List every pipeline stage in the order it runs, with the file and line number where each stage's function is defined.`
- **Expected route**: haiku / luna.
- **Acceptance**: exactly six stages in this order: validate, price, reserve_inventory, charge, ship, notify. Each cites its defining file. Line numbers must match the fixture copy you ran against.
- **Failure signal**: a stage missing, out of order, or attributed to `pipeline.py` instead of its own module.

## E05: judgment recon, the trap

- **Class**: judgment-recon.
- **Prompt**: `Does the charge stage retry when the payment gateway times out? Answer yes or no, then cite the exact code that decides it.`
- **Expected route**: sonnet / terra. Not haiku or luna.
- **Correct answer**: No. `with_retry` in `orders/retry.py` only catches `TransientError`. `charge` in `orders/payment.py` raises `PaymentError`, which is a sibling class, not a subclass. The first timeout propagates. `test_payment_failure_releases_inventory` proves it.
- **Failure signal**: "Yes, up to 3 times", taken from the `with_retry` docstring or from the fact that `charge` is wrapped in `with_retry` in `pipeline.py`. This is the confident silent miss. If a cheap tier was used and gave this answer, record it as the headline finding.

## E06: judgment recon, the control

- **Class**: judgment-recon.
- **Prompt**: `Does reserve_inventory retry when the inventory service is still warming up? Answer yes or no, then cite the exact code that decides it.`
- **Expected route**: sonnet / terra.
- **Correct answer**: Yes. `reserve_inventory` raises `TransientError` on its first call, `with_retry` catches that class and calls again, up to 3 attempts.
- **Purpose**: paired with E05 so a tier that says yes to everything is caught.

## E07: clear-shape implementation

- **Class**: implementation.
- **Prompt**: `Add an optional coupon_percent field to orders. It is a percentage discount on the subtotal, capped at 50, applied after volume discounts and before tax. Update pricing and add tests for a normal coupon, a coupon above the cap, and an order with no coupon.`
- **Expected route**: sonnet / terra at medium effort. Planning stays inline and short.
- **Acceptance**: all pre-existing tests still pass unchanged. Three new tests exist and pass. A coupon of 80 behaves as 50. Tax is computed on the discounted subtotal.
- **Failure signal**: coupon applied after tax, cap missing, or an existing test edited to make it pass.

## E08: consequential implementation

- **Class**: consequential. Touches money and rollback.
- **Prompt**: `If shipping fails after the charge succeeded, the customer stays charged and inventory stays reserved. Fix run_pipeline so any failure after charge refunds the charge and releases inventory. Add a test that makes ship raise and checks both effects.`
- **Expected route**: opus / sol, or the session model itself. Never sonnet, terra, haiku, or luna.
- **Acceptance**: the new test forces `ship` to raise and asserts the order is marked refunded and `reserved` is false. Existing tests still pass. The happy path still reaches notify.
- **Failure signal**: a cheap or mid dispatch for this class, or a fix that releases inventory but never refunds.

## E09: hard reasoning with numbers

- **Class**: hard-reasoning. Must stay on the session model.
- **Prompt**: `Order A has one line: qty 3 at unit_price 0.335. Order B has three lines: each qty 1 at unit_price 0.335. Both are USD with no volume discount. Using the pricing code in this project, compute both subtotals exactly, explain every cause of the difference, and propose a fix that makes them equal without changing tax rates.`
- **Expected route**: inline on the session model at high effort. No dispatch for the reasoning. A cheap dispatch to run Python for the numbers is acceptable.
- **Correct numbers**: A is 1.01 and B is 1.02. Verified by running the fixture: `0.335 * 3` evaluates to `1.0050000000000001`, which rounds to 1.01, and `0.335` is stored as `0.33500000000000001998`, which rounds to 0.34, so three lines sum to 1.02.
- **Acceptance**: names the primary cause, which is that `line_subtotal` rounds each line before summing, so splitting a quantity across lines changes the total. Also states that binary floating point makes both roundings land above the half, so this is not banker's rounding at work. The fix uses `decimal.Decimal` with an explicit rounding mode, or defers rounding to the order total, or both. Any of these is accepted if the reasoning is right and the numbers match.
- **Failure signal**: blaming round-half-even, claiming A is 1.00, giving any other wrong number, or dispatching the reasoning to a lower tier.

## E10: consequential review

- **Class**: consequential. Must stay on the session model.
- **Prompt**: after E07 has been applied in the same session: `Review the coupon change for correctness bugs and rank them by severity, with file and line references.`
- **Expected route**: inline on the session model at high effort. A cheap dispatch to gather the diff is acceptable. The judgment is not delegated.
- **Acceptance**: every finding cites a file and line. No finding is a style comment. If the E07 implementation applied the coupon before the volume discount or skipped input validation on `coupon_percent`, the review must catch it.
- **Failure signal**: the review itself ran on a cheap or mid tier.

## E11: context too big to brief

- **Class**: gate test. Must answer inline.
- **Setup**: in one session, spend four or five turns discussing new validation rules in prose. Decide that currencies must also accept CAD, that emails must contain an `@`, that quantities above 1000 need a `bulk_approved` flag, and that unit prices above 10000 are rejected. Do not ask for code during those turns.
- **Prompt**: `Now update validation.py to match everything we agreed, and add tests.`
- **Expected route**: inline. The brief would need the whole conversation. A dispatch is acceptable only if its brief contains all four rules verbatim.
- **Acceptance**: all four rules implemented and tested. If a dispatch happened, read its brief and count how many rules it carried.
- **Failure signal**: a dispatch with a partial brief, which produces a confident partial implementation.

## E12: the user's own example, a small website

- **Class**: mixed. Plan is hard-reasoning-light, implementation is implementation, the check is mechanical.
- **Prompt**: `Build a single-page static website for a coffee shop in a new folder called site: index.html and styles.css, a hero section, a menu section with six items and prices, and a responsive navigation bar. Then verify the HTML parses without errors.`
- **Expected route**: a short inline plan, one implementation dispatch on sonnet / terra, one mechanical check on haiku / luna or inline. No dispatch on opus or sol.
- **Acceptance**: both files exist. `python -c "import html.parser,sys; p=html.parser.HTMLParser(); p.feed(open('site/index.html').read())"` exits 0. Six menu items with prices are present. The nav has a responsive rule in the CSS.
- **Failure signal**: the whole build done inline on the session model when a skill run was requested, or three or more dispatches for a two-file task.

## Recording baseline versus skill

The point of E12 is the comparison the user asked for: the same website built by the session model alone against the session model orchestrating cheaper tiers. Record both cost figures side by side and whether the acceptance check passed on each. That row is the headline result of the whole suite.
