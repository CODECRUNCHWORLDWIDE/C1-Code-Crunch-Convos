"""Make ``python -m loganalyzer`` work.

Kept to two lines on purpose: ``coverage`` cannot reach ``__main__`` from a
test that imports the package, so anything non-trivial living here would be an
untestable hole in the report. The real work is in :func:`loganalyzer.cli.main`,
which a test calls directly.
"""

from loganalyzer.cli import main

raise SystemExit(main())
