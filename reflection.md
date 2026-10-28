# Reflection: Static Code Analysis of parking_lot_system.py

## 1. What is static analysis, and what did it catch that running the program did not?

Static analysis examines source code without running it. When I ran `parking_lot_system.py`, it printed sensible output and looked fine. Pylint, Bandit and Flake8 still found a lot that running it never showed:

- `eval()` on a string, which would let anyone who controls that string run arbitrary code (Bandit B307).
- An `os.system` call built from a filename, which allows command injection (Bandit B605).
- MD5 used for hashing (Bandit B324) and `random` used for a PIN (Bandit B311).
- A mutable default argument, `entry_logs=[]`, shared across calls (Pylint W0102).
- A bare `except: pass` that hides every error (Bandit B110, Pylint W0702).

None of these crashed the program. They are problems that only appear under certain inputs or in the hands of an attacker, which is why a normal run never exposed them.

## 2. Which issues were the most serious, and how did you prioritise?

I used Bandit's severity ratings and fixed in order of risk. The two High findings came first: the shell command in `os.system` and the weak MD5 hash. Next was the Medium finding, `eval`, which I treated as just as important because it can run arbitrary code. I then fixed the Low findings and the Pylint bug-type warnings (mutable default, bare except). Formatting and naming came last, because they affect readability but not safety or correctness.

I committed in three rounds, one per tool, so that each commit shows one kind of fix: Bandit for security, Pylint for quality, Flake8 for formatting.

## 3. Were there any false positives, or warnings that were not worth fixing?

None of the Bandit findings were false positives. Each one pointed at real insecure code. The closest to a judgement call was the MD5 hash: if the hash were only a label, `usedforsecurity=False` would silence the warning, but I switched to SHA-256 because it is simpler to defend and has no downside here.

Some Pylint messages were low value on their own, such as the missing docstring and snake_case naming warnings. They do not change behaviour, but they were cheap to fix and make the code easier to read, and they were needed to reach a score above 9.5.

## 4. What did the tools miss?

A score of 10.00/10 does not mean the code is correct. These problems were not flagged by any tool:

- A hardcoded secret token (`BARRIER_GATE_SECRET_TOKEN_2026`) that the program also printed to the console.
- `hours_booked` was never validated, so zero or negative hours were accepted and could reduce `total_collections`.
- `"%d"` formatting truncated fractional hours (2.5 hours shown as 2).

I found these by reading the code and the program's output. Static analysis checks patterns, not whether the program's logic does what it should, so it complements testing and code review but does not replace them.

## 5. How would you use these tools in a real project?

I would run all three automatically, not just once by hand:

- Add them as a pre-commit hook, so issues are caught before code is committed.
- Run them in a CI pipeline on every pull request and fail the build on any Bandit finding or if the Pylint score drops below a set threshold.
- Agree on a shared config (`.pylintrc`, `setup.cfg` for Flake8) so the whole team follows the same rules.

Fixing issues early is much cheaper than finding them after release. The lab also showed that the score is a useful measure of progress (4.10 to 10.00), as long as it is paired with real tests and reviews.
