"""Write a point-in-time capture without letting a bad run destroy a good one.

Every collector here ends the same way: build a dict, write it over the file
committed last time. That is fine while a source answers and silently
catastrophic when one stops, because the failure does not look like a failure.
`fetch-reddit --refresh` against a subreddit that no longer serves parseable
html rebuilt its output from nothing, fetched nothing, and wrote 0 searches, 0
listings and 0 threads over a capture holding 38, 3 and 147. It exited non-zero
-- after the write, which is the wrong order and no protection at all.

`scripts/sweep --refresh` passes `--refresh` to every collector, so that is one
command away from emptying a corpus that took months of sweeps to accumulate
and that nothing else in this repo can rebuild.

So a capture may grow, and may change, and may NOT shrink without somebody
saying so. The check is deliberately crude -- one integer the caller counts --
because the alternative is a per-collector notion of what a record is, and the
cases worth catching are not subtle: a source that has gone away takes a capture
to zero, not to n-1.
"""

import json
import os


def previous_count(path, count):
    """How many records the capture on disk holds, or 0 if there is none."""
    try:
        with open(path) as f:
            return count(json.load(f))
    except (IOError, ValueError, KeyError, TypeError):
        return 0


def write(path, payload, count, allow_shrink=False, label="records"):
    """Write `payload`, unless it holds fewer `count` than the file already does.

    Returns (written, now, before). The caller reports; refusing to write is not
    an error on its own, because a collector that lost its source should still
    let the rest of the sweep run off the capture that is already there.
    """
    before = previous_count(path, count)
    now = count(payload)
    if before and now < before and not allow_shrink:
        return False, now, before
    tmp = path + ".new"
    with open(tmp, "w") as f:
        json.dump(payload, f, indent=1)
    os.replace(tmp, path)
    return True, now, before


def refused(path, now, before, label="records"):
    """The message for a write this refused, in the shape a sweep can read."""
    return ("!!! refusing to overwrite %s: it holds %d %s and this run produced "
            "%d.\n    the capture on disk is unchanged. a source that stopped "
            "answering is the\n    usual cause -- read the fetch output above. "
            "pass --allow-shrink if the\n    smaller result is the correct one."
            % (path, before, label, now))
