import time

from .errors import TransientError


def with_retry(fn, attempts=3, delay=0.0):
    """Call ``fn`` and retry up to ``attempts`` times on transient failures.

    Waits ``delay`` seconds between attempts. Re-raises the last error when
    every attempt fails.
    """
    last = None
    for _ in range(attempts):
        try:
            return fn()
        except TransientError as exc:
            last = exc
            if delay:
                time.sleep(delay)
    raise last
