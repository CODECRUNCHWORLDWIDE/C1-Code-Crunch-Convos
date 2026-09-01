"""The Week 6 log analyzer, refactored until it could be tested.

Four modules, one responsibility each:

``models``
    The shapes everything else passes around — a frozen ``LogRecord`` dataclass
    and a ``Summary`` ``TypedDict``.
``parsing``
    Bytes on disk to ``LogRecord`` objects. Reads; never counts, never writes.
``analysis``
    ``LogRecord`` objects to numbers. Pure functions; no file handles at all.
``reporting``
    Numbers to files on disk. The only module that knows an output directory
    exists.
``cli``
    ``sys.argv`` to an exit code. The only module that prints.

That ordering is also the dependency order: ``cli`` imports everything,
``models`` imports nothing. No module imports a module above it, which is why
you can unit-test any layer without standing up the one below it.
"""

from __future__ import annotations

from loganalyzer.models import LEVELS, ErrorSummary, LogRecord, Summary

__all__ = ["LEVELS", "ErrorSummary", "LogRecord", "Summary", "__version__"]

__version__ = "0.1.0"
