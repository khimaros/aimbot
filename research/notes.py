"""References for registry notes, so a note cannot quote a stale size.

`verdicts.py` did this for the written judgements: a verdict names the FACET and
the number is rendered when it is printed, which removes the class of error
rather than detecting it. The registry's `note:` fields have the same problem and
worse odds -- a note on a quant is ABOUT A FILE, so most of its numbers are a
size or a bits-per-weight that `data/gguf-sizes.json` and `data/gguf-tensors.json`
already hold, exactly and currently.

vcruz305's deepseek v4.1 pack is what that costs. The note read `it is 3 of 7
shards` and `95.75 gib`, with `DISTRUST THE SIZE` beside it because 95.75 looked
like a rung that fits a 128gb box. The publisher finished the upload; the sizes
capture read 246.35 gib over seven shards on the next sweep and the sentence went
on saying 95.75, because it was only ever text.

    "the pack is {gib}"  ->  "the pack is 246.35 gib"

THE SUBJECT IS IMPLICIT. A note hanging off a quant means that rung, and one
hanging off the model means the model, so the common case writes `{gib}` with no
locator at all. `@` names something else when a comparison needs it:

    {gib}                                    this rung
    {gib@UD-Q8_K_XL}                         another rung in the same repo
    {gib@ISTA-DASLab/Qwen3.8-27B-GGUF:IQ3_S} a rung anywhere
    {params_b}                               the model, which has no rung

`@` rather than a dotted path because a rung can be keyed by FILENAME where the
publisher does not name its types, and `Kokoro_espeak_Q8.gguf.gib` has no reading
that separates the object from the field.
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
CARDS = "cards"
GIB = 2 ** 30
HF = "https://huggingface.co/"

# `{field}` or `{field@locator}`. the field is a bare word so that a reference
# is never mistaken for the braces the notes already use around code -- those
# hold `split.count` and `base_model:quantized`, neither of which matches
REF = re.compile(r"\{([a-z_]+)(?:@([^}]+))?\}")

# a figure typed into a note that one of these could have rendered. sizes are
# the whole problem -- 69 of them across the notes -- and a bits-per-weight is
# the same fact read another way.
#
# `gb` is deliberately NOT in here. In these notes it is one of two things and
# neither goes stale: the box, which is hardware, and a card's decimal figure
# being contrasted with the gib beside it, which is the contrast the sentence
# is about. `gib` is what this repository measures in and what a requant moves.
TYPED = re.compile(r"(?<![\w.])\d+(?:\.\d+)?\s*(?:gib|bpw|bits per weight)\b", re.I)

# WHETHER A RUNG FITS IS NOT A FACT ABOUT THE RUNG. it is a fact about the
# reader's box, and the reader sets it: `#ram`, `#reserve` and `#ctx` are three
# controls on the page and every size, quant pick and retention figure
# recomputes from them. a note saying `the largest that fits 105` is frozen
# prose contradicting a live computation for anybody who moved the slider, and
# it cannot be fixed by referencing the budget -- there is no one budget to
# reference. the note says what the file IS; the page says whether you can run
# it.
#
# `size budget` is NOT one of these: that is what ISTA's search optimises
# against when it builds the file, which is a fact about the quantization and
# has nothing to do with anybody's machine.
# `a fit` and `the fit` are the retention CURVE, which two ternary notes talk
# about for a good reason, so the article rules them out
FITS = re.compile(r"(?<!a )(?<!the )\bfits?\b|\bhost budget\b|"
                  r"(?<!size )\bbudget\b", re.I)


def load(data=DATA):
    """The captures a note can name, read once and passed around."""
    out = {"cards_dir": os.path.join(data, CARDS)}
    for key, name in (("sizes", "gguf-sizes.json"), ("tensors", "gguf-tensors.json"),
                      ("facts", "model-facts.json")):
        try:
            with open(os.path.join(data, name)) as f:
                out[key] = json.load(f)
        except (IOError, ValueError):
            out[key] = {}
    return out


def card_path(repo, cards_dir):
    return os.path.join(cards_dir or "", "%s.md" % repo.replace("/", "_"))


def card_text(repo, data):
    """The publisher's own words, as captured.

    Read off disk per call rather than held in memory: 173 cards is six
    megabytes and a build touches a handful of them, so the loader would spend
    more than the lookups save.
    """
    try:
        with open(card_path(repo, data.get("cards_dir"))) as f:
            return f.read()
    except IOError:
        return None


def _subject(locator, repo, quant):
    """(repo, quant) for a reference, from its locator or from the note's own.

    A locator naming another repo is `owner/name:tag`, and the split is at the
    FIRST colon after the slash rather than the last: a tag can itself carry one
    -- the sizes capture keys a projector `mmproj:F16` -- and splitting at the
    last made the repo `unsloth/X-GGUF:mmproj` and resolved nothing.
    """
    if not locator:
        return repo, quant
    if "/" in locator:
        head, sep, tag = locator.partition("/")
        name, sep, tag = tag.partition(":")
        return "%s/%s" % (head, name), (tag or None)
    return repo, locator


def _keys(quant):
    """The capture keys one pin could be under, in the order to try them.

    A registry rung names a TYPE and may also name a FILE, and the size table
    is keyed by whichever the publisher's filenames support -- the tag where
    they carry one, the filename where they do not. build-viewer has always
    tried both in this order; a caller passing a list gets the same rule here.
    `cstr/wespeaker-resnet34-lm-GGUF` is the case: pinned by filename, captured
    under `F32`, and looked up by the filename alone it resolved to nothing.
    """
    if quant is None:
        return []
    return list(quant) if isinstance(quant, (list, tuple)) else [quant]


def _gib(repo, quant, data):
    sizes = (data.get("sizes") or {}).get(repo) or {}
    for key in _keys(quant):
        if sizes.get(key) is not None:
            return sizes[key] / GIB
    return None


def _bpw(repo, quant, data):
    for key in _keys(quant):
        row = (data.get("tensors") or {}).get("%s:%s" % (repo, key))
        if (row or {}).get("bpw") is not None:
            return row["bpw"]
    return None


def _params_b(repo, quant, data, model=None):
    return ((data.get("facts") or {}).get(model or repo) or {}).get("params_total_b")


def _context(repo, quant, data, model=None):
    return ((data.get("facts") or {}).get(model or repo) or {}).get("context_native")


# field -> (lookup, how it prints). the unit is part of the rendering because a
# bare 246.35 in a sentence about a file is ambiguous between gib and gb, and
# the notes already disagree about which they mean
FIELDS = {
    "gib": (_gib, lambda v: "%.2f gib" % v),
    "bpw": (_bpw, lambda v: "%.2f bpw" % v),
    "params_b": (_params_b, lambda v: "%gb" % v),
    "context": (_context, lambda v: "%dk" % round(v / 1024)),
}
# the fields that describe a MODEL rather than a file, and so ignore any rung
# the note happens to hang off
MODEL_FIELDS = ("params_b", "context")

# which capture each field is read out of, so a figure standing in a note can
# say where it came from the way a figure standing in a verdict does. the
# reader's question is the same one -- 29.30 gib of WHAT, measured by whom
FIELD_SOURCE = {
    "gib": ("gguf sizes", "research/data/gguf-sizes.json"),
    "bpw": ("gguf tensors", "research/data/gguf-tensors.json"),
    "params_b": ("model facts", "research/data/model-facts.json"),
    "context": ("model facts", "research/data/model-facts.json"),
}


# a reference that names WHERE a claim came from rather than what it is. these
# render as somewhere a reader can go, and the words quoted in front of one are
# checked against it -- see check_quoted, and verdicts.check_quoted, which does
# the same job for a forum comment
SOURCES = ("card", "url")


def source_of(field, locator, repo, quant, data, model=None):
    """(url, text) for a source reference, or None if it is not one.

    `text` is what a quote in front of the reference is checked against, and is
    None for a source this repo does not capture the body of -- an explicit url
    is somewhere to go rather than something to quote.
    """
    if field == "url":
        return (locator, None) if locator else None
    if field != "card":
        return None
    at = locator or (repo if quant is None else repo)
    return HF + at, card_text(at, data)


def resolve(field, locator, repo, quant, data, model=None):
    """The text one reference renders as, or None if nothing carries it."""
    if field in SOURCES:
        found = source_of(field, locator, repo, quant, data, model)
        if not found:
            return None
        url, _text = found
        # a card with no captured body STILL RESOLVES. the hub gates eleven of
        # this roster's repos behind auth, so `fetch-model-cards` gets a 401 and
        # keeps nothing -- and refusing the reference left those notes pointing
        # at nothing when the thing they point at plainly exists. what the
        # missing body costs is the ability to QUOTE it, which check_quoted
        # enforces separately and by name.
        return url
    found = FIELDS.get(field)
    if not found:
        return None
    lookup, show = found
    if field in MODEL_FIELDS:
        value = lookup(repo, quant, data, model)
    else:
        at, tag = _subject(locator, repo, quant)
        value = lookup(at, tag, data)
    return None if value is None else show(value)


def render_parts(text, repo, quant, data, model=None):
    """[str | {field, locator, shown, url, missing}] -- what was substituted.

    Same reason verdicts.render_parts exists: the page can hang a source panel
    off a figure it printed, but only if the renderer says which reference each
    figure was. A `{card}` already knows the url it resolves to, and a `{gib}`
    knows which rung it read, so both travel with the words instead of being
    guessed at from them afterwards.
    """
    out, at, text = [], 0, text or ""
    for m in REF.finditer(text):
        field, locator = m.group(1), m.group(2)
        got = resolve(field, locator, repo, quant, data, model)
        if m.start() > at:
            out.append(text[at:m.start()])
        at = m.end()
        part = {"field": field, "locator": locator,
                "shown": m.group(0) if got is None else got}
        if got is None:
            part["missing"] = True
        elif field in SOURCES:
            source = source_of(field, locator, repo, quant, data, model)
            if source:
                part["url"] = source[0]
        elif field in FIELD_SOURCE:
            name, path = FIELD_SOURCE[field]
            keys = _keys(quant)
            read = locator or (repo if field in MODEL_FIELDS
                               else "%s:%s" % (repo, keys[0] if keys else "?"))
            part["ref"] = {"source": name, "file": path, "id": read}
        out.append(part)
    if at < len(text):
        out.append(text[at:])
    return out


def render(text, repo, quant, data, model=None):
    """(text, unresolved) with every reference replaced by its figure.

    An unresolved reference is LEFT in place rather than dropped, for the reason
    verdicts.render gives: a note that silently loses a clause reads as a
    complete sentence that happens to be missing its evidence.
    """
    parts = render_parts(text, repo, quant, data, model)
    missing = [p["field"] + ("@" + p["locator"] if p["locator"] else "")
               for p in parts if isinstance(p, dict) and p.get("missing")]
    return "".join(p if isinstance(p, str) else p["shown"] for p in parts), missing


# `"the words" {card@owner/Repo}` -- a fragment quoted and attributed. this is
# the one thing in the format that can pass every other check and still be
# false, because quotation marks assert the words are somebody else's
QUOTED = re.compile(r'"([^"]{4,})"\s*\{([a-z_]+)(?:@([^}]+))?\}')


def check_quoted(text, repo, quant, data, model=None):
    """(ok, why) -- every quotation really appears in the source it cites."""
    for said, field, locator in QUOTED.findall(text or ""):
        found = source_of(field, locator, repo, quant, data, model)
        if not found:
            continue
        _, body = found
        if body is None:
            return False, ('quotes "%s" against %s, which is a link rather than '
                           'a captured body' % (said, locator or repo))
        whole = re.sub(r"\s+", " ", body).lower()
        if re.sub(r"\s+", " ", said).lower().strip() not in whole:
            return False, ('quotes "%s", which is not in the source it cites' % said)
    return True, ""


# how much of a card a sheet carries. a card runs to 200 lines of badges,
# install snippets and bibtex, and what a note is written from is the prose and
# the tables -- so the sheet is the lines that say something, capped
SHEET_CARD_LINES = 60
SHEET_LINE = 200
# markup a card opens with and a note has no use for
BOILERPLATE = re.compile(r"^\s*(?:!\[|<div|</div|<a href|\[!\[|<br|<sub|<!--|---\s*$|"
                         r"@article|\s*[a-z_]+\s*=\s*\{)", re.I)


def card_lines(repo, data):
    """The lines of a card a note could be written from, in order.

    Badges, banners, install snippets, bibtex and the yaml frontmatter are
    dropped: they are most of the file and none of them is a claim a note would
    make. What is left is what the publisher asserts, which is the only part
    worth quoting.
    """
    text = card_text(repo, data)
    if not text:
        return []
    out, in_front, in_comment = [], False, False
    for i, line in enumerate(text.split("\n")):
        line = line.rstrip()
        if not i and line.strip() == "---":
            in_front = True
            continue
        if in_front:
            in_front = line.strip() != "---"
            continue
        if "<!--" in line:
            in_comment = "-->" not in line
            continue
        if in_comment:
            in_comment = "-->" not in line
            continue
        line = line.strip()
        if not line or BOILERPLATE.match(line):
            continue
        out.append(line[:SHEET_LINE])
        if len(out) >= SHEET_CARD_LINES:
            break
    return out


# what a repo holds beside its rungs. the projector, the draft head and the
# importance matrix are files in the same directory and none of them is a rung
# of the ladder -- offering `imatrix-qwen3.8-27b.gguf` as an alternative to
# compare against is offering a 0.01 gib side file
SIDECAR = re.compile(r"^(mmproj|mtp|imatrix|dspark|dflash|eagle3)", re.I)


def rungs_of(repo, data):
    """[(tag, gib, bpw)] for every rung the captures hold in one repo."""
    out = []
    for tag, size in sorted(((data.get("sizes") or {}).get(repo) or {}).items()):
        if SIDECAR.match(tag):
            continue
        out.append((tag, size / GIB, _bpw(repo, tag, data)))
    return out


# what this registry sizes against, from research/build-tables BUDGET_GIB. a
# note's most common judgement is "does this fit", and a sheet that does not say
# what it has to fit gets a description instead of a decision
BUDGET_GIB = 105.0
BOX = "128gb"


def _ladders(entry, repo, data):
    """[(other repo, [(tag, gib)])] for every OTHER repo publishing this model.

    A note's second most common judgement is a comparison -- "no unsloth repo
    exists, so these five hand-rolled rungs are what there is", "0.42gib smaller
    than the -MTP- build of the same tag" -- and none of it is derivable from
    the rung's own size. Handing over one repo got card summaries back.
    """
    out = []
    for q in ((entry or {}).get("quants") or []) + ((entry or {}).get("components") or []):
        at = q.get("repo")
        if not at or at == repo or any(at == seen for seen, _ in out):
            continue
        out.append((at, [(t, g) for t, g, _ in rungs_of(at, data)]))
    return out


def fact_sheet(repo, quant, data, model=None, entry=None, pin=None):
    """Everything a note about this rung should be written from, and no more.

    Handed over INSTEAD of the captures, the same way verdicts.fact_sheet is:
    whatever writes the note picks which evidence matters rather than which
    numbers to believe. The figures are shown as the REFERENCE that renders
    them, so what the writer reads is the token it is supposed to write.

    The registry's own decisions are here too -- what fits, which other repos
    publish this model, what the entry already says about drafting and runtime
    -- because a note is a DECISION about a file and a sheet of card text and
    sizes can only produce a description of one.
    """
    lines = ["%s, rung %s" % (repo, quant or "(the model, not a rung)")]
    # ONLY references that resolve are offered. a sheet that shows `{gib} = -`
    # invites a reference the check then refuses, which is the tool arguing
    # with itself: unsloth's Qwen3.5-397B ladder has no UD-Q2_K_XL in the size
    # capture and the first draft of that note was rejected for using it
    if quant:
        have = [(f, resolve(f, None, repo, quant, data))
                for f in ("gib", "bpw")]
        shown = ["{%s} = %s" % (f, v) for f, v in have if v]
        if shown:
            lines.append("  this rung:   " + "   ".join(shown))
        gone = [f for f, v in have if not v]
        if gone:
            lines.append("  NO CAPTURE HOLDS %s for this rung, so do not write it"
                         % " or ".join("{%s}" % f for f in gone))
    for field in MODEL_FIELDS:
        got = resolve(field, None, repo, quant, data, model)
        if got:
            lines.append("  the model:   {%s} = %s" % (field, got))
    others = [(t, g, b) for t, g, b in rungs_of(repo, data) if t != quant]
    if others:
        lines.append("  other rungs in this repo, cite as {gib@TAG}:")
        for tag, gib, bpw in others:
            lines.append("    %-34s %8.2f gib  %s"
                         % (tag[:34], gib, ("%.2f bpw" % bpw) if bpw else "-"))
    gib = _gib(repo, quant, data) if quant else None
    if gib is not None:
        lines.append("  the box:     %.1f gib usable on a %s host, so this rung %s"
                     % (BUDGET_GIB, BOX, "FITS with %.1f gib left for context"
                        % (BUDGET_GIB - gib) if gib <= BUDGET_GIB
                        else "DOES NOT FIT, by %.1f gib" % (gib - BUDGET_GIB)))
    for at, rungs in _ladders(entry, repo, data):
        if not rungs:
            lines.append("  the registry also carries %s, which the size capture "
                         "has not read" % at)
            continue
        lines.append("  the same model is also published by %s, cite as "
                     "{gib@%s:TAG}:" % (at, at))
        for tag, other in rungs:
            lines.append("    %-34s %8.2f gib" % (tag[:34], other))
    for field, label in (("speculative", "this entry drafts with"),
                         ("runtime", "llama.cpp support")):
        got = (entry or {}).get(field)
        if isinstance(got, dict) and got:
            lines.append("  %s: %s" % (label, ", ".join(
                "%s %s" % (k, v) for k, v in sorted(got.items()) if k != "note")))
    if pin and pin.get("role"):
        lines.append("  this file's role in the pipeline: %s" % pin["role"])

    mix = {}
    for key in _keys(quant):
        mix = (data.get("tensors") or {}).get("%s:%s" % (repo, key)) or mix
    if mix.get("types"):
        # by share, because the capture is written sorted by key and a note
        # cares which type most of the weights are in
        top = sorted(mix["types"].items(), key=lambda kv: -kv[1])[:6]
        lines.append("  what the tensor table says it actually is: "
                     + ", ".join("%s %d%%" % (k, round(100 * v)) for k, v in top))
    card = card_lines(repo, data)
    if card:
        lines.append("  the publisher's own card, cite as {card} and QUOTE EXACTLY:")
        lines += ["    " + line for line in card]
    return "\n".join(lines)


# how close a typed figure has to be to the captured one to BE it. the notes
# round to two places and some of them to one, so `246.3` and `246.35` are the
# same claim while `95.75` against `246.35` is not anything like it
MATCH_GIB = 0.06


def _same_figure(literal, value, captured):
    """Whether a typed figure and a captured one are the same claim.

    To the precision the SENTENCE chose, and no looser. `120` for a rung
    weighing 119.60 is that rung written to the nearest gib, which is the
    commonest shape in these notes. `105` beside one weighing 106.32 is the box
    budget, and rounding it in would put a file's size where a threshold
    belongs -- so this rounds rather than truncates, which is what separates the
    two: 119.60 rounds to 120 and 106.32 does not round to 105.
    """
    if abs(captured - value) <= MATCH_GIB:
        return True
    places = len(literal.partition(".")[2].strip(" gib"))
    return round(captured, places) == value


def _candidates(repo, quant, data, entry=None):
    """[(reference, gib)] for every size a note here could be naming."""
    out = []
    own = _gib(repo, quant, data)
    if own is not None:
        out.append(("{gib}", own))
    # the sidecars too, which `rungs_of` drops. a projector is not a rung of the
    # ladder and does not belong in the sheet's list of alternatives, but a note
    # naming its size -- `plus a 1.1 gib mmproj for the vision half` -- is naming
    # a file the capture holds, and that figure goes stale like any other
    sizes = (data.get("sizes") or {}).get(repo) or {}
    for tag in sorted(sizes):
        if quant is not None and tag in _keys(quant):
            continue
        out.append(("{gib@%s}" % tag, sizes[tag] / GIB))
    for at, rungs in _ladders(entry, repo, data):
        for tag, gib in rungs:
            out.append(("{gib@%s:%s}" % (at, tag), gib))
    return out


def convert(text, repo, quant, data, model=None, entry=None):
    """(text, converted, stale) -- typed sizes turned into references.

    Mechanical on purpose, and that is what makes it safe to run over 69 of
    them: a literal is replaced only where a capture agrees it is that figure
    RIGHT NOW. Where nothing agrees, the literal is LEFT ALONE and reported --
    because a stale figure is not a reference waiting to happen, it is the thing
    this whole mechanism exists to find, and converting it would silently repair
    the sentence and destroy the evidence that it was wrong.

    Bare numbers with no unit are never touched. A note saying `3 of 7 shards`
    or `top 5` is not naming a size and guessing that it might be is how a
    conversion pass starts inventing claims.
    """
    cands = _candidates(repo, quant, data, entry)
    converted, stale = [], []

    def one(m):
        literal = m.group()
        value = float(re.match(r"[\d.]+", literal.strip()).group())
        if not literal.lower().rstrip().endswith("gib"):
            return literal
        hit = [(ref, gib) for ref, gib in cands
               if _same_figure(literal, value, gib)]
        if not hit:
            # THIS rung's size leads the report whatever the arithmetic says.
            # ranking by distance alone answers "what else is near 95.75" when
            # the question a reader has is "what does the file in front of me
            # weigh", and on the pack that motivated this the two are 70 apart
            own = [c for c in cands if c[0] == "{gib}"]
            near = own + [c for c in sorted(cands, key=lambda c: abs(c[1] - value))
                          if c[0] != "{gib}"][:2]
            stale.append((literal.strip(),
                          "nothing here weighs that; this rung is %s"
                          % ", ".join("%s at %.2f" % (r, g) for r, g in near)))
            return literal
        # the bare `{gib}` wins a tie: a note about a rung that happens to
        # match a sibling of the same size means its own
        ref = sorted(hit, key=lambda c: (c[0] != "{gib}", len(c[0])))[0][0]
        converted.append((literal.strip(), ref))
        return ref

    return TYPED.sub(one, text or ""), converted, stale


# claims a note makes about the REGISTRY'S OWN STRUCTURE rather than about the
# world. these are the easiest thing here to check and were the only kind
# unchecked: `FireRedTeam/FireRedPunc` said "the pin names its file" beside a
# pin that is `quant: Q8_0` and nothing else, and the sentence had presumably
# been true of some earlier shape of the entry.
# THERE IS NO RUNG-COUNT RULE and that is a decision, not an omission. "N rungs"
# was tried and matched fifteen notes, eleven of them wrongly: a model-level
# note counts the ladder of a gguf repo that is not its own subject, "ten rungs
# of mean kl divergence" counts a published SWEEP rather than a ladder, and
# "three models rather than three rungs" is a negation. A check that is wrong
# three times in four teaches a reader to skip it, which costs more than the
# count was worth.
NAMES_FILE = re.compile(r"the pin names (?:its|the) file|pin names its file", re.I)
NO_RUNG = re.compile(r"there is no ([A-Z][\w_]*)\b(?: rung)? here|"
                     r"\bno ([A-Z][\w_]*) rung here", re.I)
# what a drafting endpoint answers in, against what the vocabulary is written
# in. none of these is a disagreement about the sentence, so none is worth
# refusing a draft over -- they are folded before it is judged
ASCII_FOLD = {"‘": "'", "’": "'", "“": '"', "”": '"',
              "–": "-", "—": " -- ", "…": "...", " ": " ",
              "−": "-", "×": "x", "→": "->", "≥": ">=",
              "≤": "<=", "·": "-"}
PASTED_CARD = re.compile(r"(?:the card |see )?https?://huggingface\.co/"
                         r"([\w.\-]+/[\w.\-]+)/?(?![\w/])", re.I)


def normalize(text, repo, quant, data, model=None, entry=None):
    """(text, [what changed]) -- a draft put into the vocabulary it is judged in.

    A draft comes back grounded in substance and wrong in form: across 75 of
    them the endpoint quoted the card 72 times, named its url 73 times and wrote
    a reference once. It pastes the url where the vocabulary says `{card}`,
    types a size where it says `{gib}`, and answers in typographic quotes.

    Every fold here is mechanical and reversible in meaning. Turning a typed
    figure into a reference is not a repair of a drifting number -- `convert`
    leaves a literal alone wherever no capture agrees with it, which is exactly
    how a stale claim stays visible.
    """
    why = []
    folded = "".join(ASCII_FOLD.get(c, c) for c in text or "")
    if folded != (text or ""):
        why.append("folded to ascii")

    def card(m):
        # only the repo this note is ABOUT: a url pointing somewhere else is a
        # citation of another model and `{card}` would silently re-aim it
        if m.group(1).lower() not in (repo or "").lower():
            return m.group()
        why.append("%s -> {card}" % m.group(1))
        return "the card {card}" if m.group().lower().startswith("the card") \
            else "{card}"

    folded = PASTED_CARD.sub(card, folded)
    folded, converted, stale = convert(folded, repo, quant, data, model, entry)
    why += ["%s -> %s" % (was, now) for was, now in converted]
    why += ["%s matches no capture and was left alone" % s for s in stale]
    return re.sub(r"[ \t]{2,}", " ", folded).strip(), why


def check_structure(text, repo, quant, data, pin=None, model=None, entry=None):
    """[why] -- claims about the pin, against the pin.

    Deliberately narrow. Both shapes matched are statements with exactly one
    right answer sitting in the registry or in `data/gguf-sizes.json`. A note is
    free to say anything else.

    A MODEL-level note gets the whole entry rather than one rung, because that
    is where the claim was found: FireRedPunc says "the pin names its file" in
    its `notes:`, and the pin it means is a `quants:` entry two fields down.
    """
    out = []
    text = text or ""
    if NAMES_FILE.search(text):
        pins = [pin] if pin else ((entry or {}).get("quants") or [])
        if pins and not any((p or {}).get("file") for p in pins):
            out.append("says the pin names its file, and no pin here has a "
                       "`file:` -- %s" % ", ".join(
                           "`quant: %s`" % (p.get("quant") or "?") for p in pins))
    rungs = rungs_of(repo, data)
    for m in NO_RUNG.finditer(text):
        tag = m.group(1) or m.group(2)
        if any(t.lower() == tag.lower() for t, _, _ in rungs):
            out.append("says there is no %s here, and the capture holds one" % tag)
    return out


def check(text, repo, quant, data, model=None, beside=(), pin=None, entry=None):
    """[why] -- what is wrong with one note, whoever wrote it.

    `beside` is any url the note's own block already carries; a note sitting
    next to the pull request it describes is grounded by that and is not asked
    to repeat it. `pin` is the registry entry the note hangs off, for the
    claims it makes about that entry's own shape.
    """
    out = []
    typed = sorted({m.group().strip() for m in TYPED.finditer(REF.sub("", text or ""))})
    if typed:
        out.append("types %s instead of referencing it" % ", ".join(typed))
    _, missing = render(text, repo, quant, data, model)
    if missing:
        out.append("references %s, which no capture carries"
                   % ", ".join(sorted(set(missing))))
    fits = FITS.search(REF.sub("", text or ""))
    if fits:
        out.append("asserts %r, which is the reader's box rather than this file "
                   "-- the page recomputes it from their own settings"
                   % fits.group().strip())
    out += check_structure(text, repo, quant, data, pin, model, entry)
    ok, why = check_quoted(text, repo, quant, data, model)
    if not ok:
        out.append(why)
    # a reference IS a source: `{gib}` names the capture it renders out of, and
    # a note built from them is as checkable as one pointing at a card. what is
    # left over is prose resting on neither -- a sentence a reader cannot follow
    # to anything at all, which is the case worth reporting
    if not REF.findall(text or "") and not beside:
        out.append("points at nothing -- no reference and no source, so there is "
                   "nowhere to check it")
    return out
