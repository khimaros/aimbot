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
import re

# where this module lives, which is where the captures live. a collector's
# `--out` defaults are written relative to THIS and not to the shell's idea of
# where it is: `./research/fetch-model-cards` from the repo root used to answer
# by building a second corpus in `./data/`, well-formed, shrink-guarded against
# nothing, and never read again by anything.
HERE = os.path.dirname(os.path.abspath(__file__))


def resolve(path):
    """A relative capture path means research/, because that is the one home."""
    return path if os.path.isabs(path) else os.path.join(HERE, path)

# credentials somebody pasted into a forum. these captures are arbitrary text
# other people wrote, and one of them titled a huggingface discussion with their
# own access token -- which this repo then carried until github's push
# protection refused the commit. by that point it is in a local commit and the
# fix is a history rewrite rather than an edit, so it is caught on the way IN.
#
# the patterns are deliberately narrow. `hf_` followed by thirty characters is a
# token; `hf_hub` and `hf_transfer` are packages people name in the same
# sentence, and redacting those would quietly edit what a comment said.
SECRETS = [
    ("hf-token", re.compile(r"\bhf_[A-Za-z0-9]{30,}")),
    ("github-pat", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}"
                              r"|\bgithub_pat_[A-Za-z0-9_]{50,}")),
    ("api-key", re.compile(r"\bsk-[A-Za-z0-9]{32,}")),
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("aws-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
]


def scrub(text):
    """(text, n) with anything credential-shaped replaced by what it was.

    Named rather than blanked, because a reader of the capture should be able to
    tell a redaction from a comment that happened to say nothing.
    """
    total = 0
    for name, pat in SECRETS:
        text, n = pat.subn("<redacted:%s>" % name, text)
        total += n
    return text, total


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
    path = resolve(path)
    before = previous_count(path, count)
    now = count(payload)
    if before and now < before and not allow_shrink:
        return False, now, before
    # scrubbed once over the serialized form rather than by walking the payload:
    # one pass, no recursion over a capture holding 65k comments, and it reaches
    # a key as readily as a value
    body, redacted = scrub(json.dumps(payload, indent=1))
    if redacted:
        print("  redacted %d credential(s) somebody pasted into %s"
              % (redacted, os.path.basename(path)))
    tmp = path + ".new"
    with open(tmp, "w") as f:
        f.write(body)
    os.replace(tmp, path)
    return True, now, before


def refused(path, now, before, label="records"):
    """The message for a write this refused, in the shape a sweep can read."""
    return ("!!! refusing to overwrite %s: it holds %d %s and this run produced "
            "%d.\n    the capture on disk is unchanged. a source that stopped "
            "answering is the\n    usual cause -- read the fetch output above. "
            "pass --allow-shrink if the\n    smaller result is the correct one."
            % (path, before, label, now))
