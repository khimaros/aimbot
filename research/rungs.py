"""A model's repos, and the facts about each repo and each file in them.

Which repos a model is published in is membership, and every collector's roster
is built from it; what a repo is -- the argv role its files load under, the
crispasr backend that reads that conversion, whether its build can draft, how
a decision is read out of it where that differs from the model's other repos --
never varies inside the repo; and what one file is -- a note, the fork that
loads it, a tag its name does not carry -- is keyed by that file. Which rung to
run is not a fact: the fit picks it, from every rung each repo publishes.

`repos(model)` answers with every entry in one shape, a bare repo name included.
"""

# what a repo is, the same for every file in it
REPO_FIELDS = ("role", "crispasr", "speculative", "readout")
# what one file is. `quant` is the tag, written only where the name carries none
FILE_FIELDS = ("quant", "note", "runtime")


def repos(model):
    """[{repo, role?, crispasr?, speculative?, readout?, files: {tag or file: facts}}]."""
    out = []
    for e in model.get("repos") or []:
        e = {"repo": e} if isinstance(e, str) else e
        row = {"repo": e["repo"]}
        row.update({k: e[k] for k in REPO_FIELDS if k in e})
        row["files"] = {str(k): dict(v or {}) for k, v in (e.get("files") or {}).items()}
        out.append(row)
    return out


def repo_names(model):
    """The model's repos, in priority order."""
    return [r["repo"] for r in repos(model)]


def weight_repos(model):
    """Every repo a weight of the model comes from: its repos, then its components'."""
    names = repo_names(model) + [c["repo"] for c in model.get("components") or []
                                 if c.get("repo")]
    return list(dict.fromkeys(names))


def files(model):
    """(repo row, key, facts) for every file something is written about."""
    for r in repos(model):
        for key, facts in r["files"].items():
            yield r, key, facts


def facts_for(model, quant, repo=None):
    """(repo row, key, facts) written for one rung, by tag or by filename.

    A file keyed by its name answers for its tag too, since that is what the
    `quant` beside it says.
    """
    for r, key, facts in files(model):
        if repo and r["repo"] != repo:
            continue
        if quant in (key, facts.get("quant")):
            return r, key, facts
    return None


def is_filename(key):
    """Whether a `files:` key names an object rather than a tag."""
    return "." in key or "/" in key
