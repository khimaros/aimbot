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

The count is the backstop, not the rule. The rule is that no run loses what a
capture already holds, and `carry` and `fill` are how a collector keeps it: a
row its source stopped listing stays and is marked, a field a failed fetch did
not supply keeps its value, and a sample -- the threads a forum run happened to
read -- only ever accumulates. CONTRIBUTING.md has the cases.
"""

import datetime
import json
import os
import re

# the field a carried row is marked with: the date a sweep first found the
# source no longer listing it
DELISTED = "delisted"

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
    """How many records the capture on disk holds: 0 if there is none, and
    None if there is one that does not parse -- which is not an empty capture,
    and must not be written over as if it were."""
    if not os.path.exists(path):
        return 0
    try:
        with open(path) as f:
            return count(json.load(f))
    except ValueError:
        return None
    except (IOError, KeyError, TypeError):
        return 0


def previous(path):
    """The capture on disk, or {} if there is none to carry from."""
    try:
        with open(resolve(path)) as f:
            return json.load(f)
    except (IOError, ValueError):
        return {}


def carry(before, now, key=None, on=None, mark=True):
    """(rows, n): `now`, plus the n rows of `before` it no longer lists.

    A leaderboard that stops listing a model has not withdrawn the score it
    published, and artificial analysis dropping every retired model at once is
    what made that matter: refusing the smaller board lost the new models and
    the updated scores, and accepting it lost the old ones. So a fresh row
    always wins, and a row the source dropped stays, marked with the date it
    was first found missing. A row listed again comes back unmarked.

    Rows are a dict by id, or a list with `key` naming each row's id. An empty
    `now` is a source that answered nothing, which the caller refuses before
    this: carrying would mark the whole board delisted over one failed fetch.

    `mark=False` is for a SAMPLE rather than a listing -- the forum threads a
    run happened to fetch, the comments in a top-n -- where a row missing from
    this run says nothing about its source, so it is kept as it was.
    """
    on = on or datetime.date.today().isoformat()

    def dropped(row):
        if not mark or not isinstance(row, dict):
            return row
        return dict(row, **{DELISTED: row.get(DELISTED) or on})

    def fresh(row):
        return {k: v for k, v in row.items() if k != DELISTED} \
            if isinstance(row, dict) else row

    if isinstance(now, list):
        ids = {key(r) for r in now}
        old = before if isinstance(before, list) else []
        gone = [dropped(r) for r in old if key(r) not in ids]
        return [fresh(r) for r in now] + gone, len(gone)
    old = before if isinstance(before, dict) else {}
    out = {k: fresh(v) for k, v in now.items()}
    gone = [k for k in old if k not in now]
    for k in gone:
        out[k] = dropped(old[k])
    return out, len(gone)


def fill(before, now):
    """`now`, with every field `before` had that this run came back without.

    For a record assembled from several fetches, where one failing leaves its
    field absent: an absent field is a fetch that did not answer, not a fact
    that stopped being true. A field present in `now` always wins.
    """
    if not isinstance(before, dict) or not isinstance(now, dict):
        return now if now is not None else before
    return dict({k: v for k, v in before.items() if k != DELISTED}, **now)


def carry_groups(before, now, field, key=None, on=None):
    """(groups, n): `carry` over each group's `field` rows, and over the groups.

    For a capture of boards each holding its own rows -- lmarena's boards,
    epoch's benchmarks. A group the source no longer ships is kept and marked,
    and so are its rows, so a consumer reading only the rows still sees it.
    """
    old, kept = before if isinstance(before, dict) else {}, 0
    for name in set(old) | set(now):
        was = (old.get(name) or {}).get(field)
        group = now.get(name)
        # a group that is gone carries every row it had, against no fresh ones
        fresh = group[field] if group else ({} if isinstance(was, dict) else [])
        rows, n = carry(was, fresh, key=key, on=on)
        kept += n
        (group if group else old[name])[field] = rows
    groups, _ = carry(old, now, on=on)
    return groups, kept


def carried(n, label="models"):
    """The line a collector prints for the rows it kept."""
    return ("  kept %d %s the source no longer lists, at their last published "
            "scores" % (n, label))


def write(path, payload, count, allow_shrink=False, label="records", sort_keys=False):
    """Write `payload`, unless it holds fewer `count` than the file already does.

    Returns (written, now, before). The caller reports; refusing to write is not
    an error on its own, because a collector that lost its source should still
    let the rest of the sweep run off the capture that is already there.
    """
    path = resolve(path)
    before = previous_count(path, count)
    now = count(payload)
    if before is None and not allow_shrink:
        print("!!! %s does not parse; refusing to write over it" % path)
        return False, now, 0
    if before and now < before and not allow_shrink:
        return False, now, before
    # scrubbed once over the serialized form rather than by walking the payload:
    # one pass, no recursion over a capture holding 65k comments, and it reaches
    # a key as readily as a value
    body, redacted = scrub(json.dumps(payload, indent=1, sort_keys=sort_keys))
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
