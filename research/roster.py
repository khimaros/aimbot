"""The registry, as the collectors that SEARCH for models need it.

Four collectors ask a forum what people are saying about the roster, and each
one needs the same thing from `registry/models.yaml`: the name a person would
type. That was a hand-kept literal in all four, and a literal drifts -- when
this was written, 12 of the 63 text models had a query looking for them and 51
did not, including deepseek v4.1 flash the week it was added. `build-tables`
had the same defect with its own twenty-model list and the same fix.

One copy rather than four, because four are free to disagree about which models
get searched for, and the disagreement is invisible: a model nobody searched
for is not an error anywhere, it is just quieter than it should be.
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
REGISTRY = os.path.join(HERE, "..", "registry", "models.yaml")

# a name too short or too common to search for. a two-character query returns
# the whole forum, which is worse than not asking: it buries the models that
# were found on purpose under noise nobody can filter.
MIN_QUERY = 4


def model_queries(path=None):
    """One query per registry model, from the name a person would type.

    `name.short` rather than the repo: a comment says `kokoro` or `qwen3.8 27b`,
    not `hexgrad/Kokoro-82M`. Deliberately NOT `name.match` -- that is a regex
    for scoring prose already collected, and a search takes a phrase.

    Every KIND, not just text. r/LocalLLaMA argues about whisper and kokoro too,
    and they are on the roster to be scored like everything else.

    A registry that cannot be read yields nothing rather than raising: the
    topical queries beside these still have work to do, and a collector that
    dies on a missing file takes the whole sweep stage with it.
    """
    try:
        import yaml
        models = (yaml.safe_load(open(path or REGISTRY)) or {}).get("models") or {}
    except (IOError, ImportError, ValueError):
        return []
    out = []
    for m in models.values():
        short = (((m or {}).get("name") or {}).get("short") or "").strip()
        if len(short) >= MIN_QUERY and short not in out:
            out.append(short)
    return sorted(out)
