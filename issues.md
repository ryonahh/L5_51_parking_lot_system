# Issues Found: parking_lot_system.py

| Issue | Type | Line(s) | Description | Fix Approach |
| ----- | ---- | ------- | ----------- | ------------ |
| Shell command from string (Bandit B605, High) | Security | 64 | `os.system("echo ..." + filename)` starts a shell, so a crafted filename could inject commands. | Replaced with `print()`. |
| Weak MD5 hash (Bandit B324, High) | Security | 53 | MD5 is broken for security use. | Switched to SHA-256. |
| `eval` on a string (Bandit B307, Medium) | Security | 48 | `eval(surge_expr)` runs arbitrary code. | Removed it. The function now takes a numeric multiplier and returns `base_rate * surge_multiplier`. |
| Mutable default argument (Pylint W0102) | Bug | 15 | `entry_logs=[]` is created once and shared across calls. | Default changed to `None`; the list is created inside the function. |
| Bare `except: pass` (Bandit B110, Pylint W0702) | Bug / Security | 32 | Silently hides every error, including a missing slot. | Catch `KeyError`, report it, and return `False`. |
| Insecure random PIN (Bandit B311, Low) | Security | 57 | `random.randint` is predictable. | Used `secrets.randbelow(9000) + 1000`. |
| Hardcoded and printed secret (not flagged by tools) | Security | `main()` | Secret token in the source and printed to the console. | Read from an environment variable and print only whether it is set. |
| No validation of booked hours (not flagged by tools) | Bug | 15-24 | Zero or negative hours reduce the total collected. | Reject `hours_booked <= 0`. |
| `global` statement (Pylint W0603) | Code quality | 16 | Hard to test and reason about. | Replaced with a `COLLECTIONS` dict. |
| `open()` without `with` or encoding (Pylint W1514, R1732) | Code quality | 61 | File may not be closed if an error occurs. | Used `with open(..., encoding="utf-8")`. |
| camelCase names, missing docstrings (Pylint C0103, C0116) | Style | many | Names not snake_case and no docstrings. | Renamed everything to snake_case and added docstrings. |
| Line too long (Flake8 E501) | Style | 7-9 | Lines of 82-83 characters, over the 79 limit. | Split the dictionaries across lines. |
| Trailing whitespace (Flake8 W291) | Style | 99 | Whitespace at the end of the last line. | Removed with `autopep8`. |
