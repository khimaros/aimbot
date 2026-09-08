"""Who owns a repo, and what that says about it, from publishers.txt.

The file groups owners under `[role]` markers, and the roles are load-bearing
rather than decorative: `quantizer` means this owner publishes other people's
models, so a repo of theirs is a quant decision and never a roster one. Its own
comment makes the case -- asking a model to infer that from a repo name got
`bartowski/Qwen2.5-Coder-32B-Instruct-GGUF` classified as an original release by
the lab that trained it. A list beats a guess.

`propose` read it first, to decide a repo without asking. `resolve-base` needs
the same fact for a different question: when a conversion's card names several
base models with the same name, the one owned by a quantizer is the mirror and
the other is the model. Two callers with one parser, because a second copy would
be free to disagree with the first.
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
PUBLISHERS = os.path.join(HERE, "publishers.txt")

# owners whose repos republish somebody else's weights. `community` is in here
# for lineage even though propose treats the two verdicts differently: a merge
# of a model is not the model either
REPUBLISHERS = ("quantizer", "community")


def roles(path=PUBLISHERS):
    """{owner: role} from the `[role]` sections, owners lowercased."""
    out, cur = {}, None
    try:
        lines = open(path).read().split("\n")
    except IOError:
        return out
    for line in lines:
        text = line.split("#")[0].strip()
        if not text:
            continue
        if text.startswith("[") and text.endswith("]"):
            cur = text[1:-1]
        elif cur:
            out[text.lower()] = cur
    return out


def role_of(repo, table):
    """The role of a repo's owner, or None where the file does not name them."""
    return table.get(repo.split("/", 1)[0].lower())


def republishes(repo, table):
    """Whether this owner is one publishers.txt says carries other people's work."""
    return role_of(repo, table) in REPUBLISHERS
