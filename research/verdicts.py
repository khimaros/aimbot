"""Verdict prose that cannot quote a stale number.

The written judgements carried their figures as literal text, and literal text
goes stale every time a capture moves. Muse glimmer shipped `gbench overall
p84` against a facet reading p74 -- ten percentile points, printed in MODELS.md
as the grounds for its own argument -- and nothing caught it, because only the
forum figures were ever checked.

So a verdict names the FACET and this renders the number when it is printed:

    "{aa.lcr} and {gbench.overall}"  ->  "aa.lcr p95 and gbench.overall p74"

which removes the class of error rather than detecting it. It also turns a
rename into a build failure instead of silent prose: when artificial analysis
retired its coding index, 24 evidence lines kept saying `aa coding index
(retired) p74` and pointed at nothing, which no check could see because the
text was only ever text.

What this does NOT do is keep the argument honest. The numbers stay live while
the sentence around them was written against the old ones -- muse glimmer's
`reddit leaning the other way` was written when reddit read 100% and survives
at 86%. That is what `authored_against` and the staleness check are for.
"""

import hashlib
import re

# `{facet.key}` for the percentile, `{facet.key:value}` when the measurement
# itself is part of the sentence, and `{facet.key@owner/Repo}` for the model a
# comparison is against. no other forms: a reference a reader cannot predict the
# rendering of is worse than the number it replaced.
REF = re.compile(r"\{([a-z0-9_.\-]+)(?:@([\w.\-]+/[\w.\-]+))?(?::(value))?\}", re.I)
# a citation marker in prose: a facet key or a quote id, in braces. the colon in
# `q:1a2b3c4d` is why this is not REF -- that one reads `:value` as a form
CITE_REF = re.compile(r"\{(q:[0-9a-f]+|[a-z0-9_.\-]+)\}", re.I)

# how a forum is spelled in prose, which is not how its facet is keyed
FORUM_SHORT = {"reddit-localllama": "reddit"}

# units as the verdicts already write them
UNIT_SUFFIX = {"rate": " tok/s", "share": "", "gscore": "", "score": "",
               "index": "", "elo": ""}
# and how many digits each is worth, where the default is not right. a rate and
# an elo are whole numbers to a reader; a bits-per-weight is two places. every
# other figure takes the default below, which is what the tables beside the
# prose print -- 103.7 gib, not 104, and 51.8 resolved, not 52
UNIT_DIGITS = {"rate": 0, "elo": 0, "bpw": 2}
# a measurement under ten is a fraction and needs its places; over ten it is a
# score, an index or a size, and one place is what the generated tables show
SMALL, BIG = 3, 1

# what a drafting endpoint answers in, against what this repository is written
# in. none of these is a disagreement about the sentence, so none is worth
# refusing a draft over -- they are folded before it is judged, on every surface
# that drafts. folding is also what lets the quote check SEE a quotation:
# QUOTED matches an ascii pair, so a paraphrase inside typographic quotes next
# to a real quote id would read as sourced and be checked by nothing
ASCII_FOLD = {"‘": "'", "’": "'", "“": '"', "”": '"',
              "–": "-", "—": " -- ", "‑": "-", "…": "...",
              " ": " ", "−": "-", "×": "x", "→": "->",
              "≥": ">=", "≤": "<=", "·": "-"}


def fold(text):
    """(text, [what changed]) -- the typography this repository does not hold.

    What is left non-ascii after this is not typography: a quoted Russian
    comment or an emoji in a forum post cannot be folded into meaning, and is
    refused so a human decides whether to transliterate it or not quote it.
    """
    out = "".join(ASCII_FOLD.get(c, c) for c in text or "")
    return out, ["folded to ascii"] if out != (text or "") else []


# a quoted fragment in single marks, immediately in front of a citation. the
# citation is what makes it safe to touch: an apostrophe is not a quotation
# mark, and `the model's own {q:1a2b}` must not be read as one
CITED_SINGLE = re.compile(r"'([^'\n]{4,})'(\s*\{(?:q:[0-9a-f]+|"
                          r"[a-z0-9_.\-]+(?:@[^}\s]+)?)\})")


def quote_marks(text):
    """(text, [what changed]) -- a quotation in the marks the checkers match.

    Both quote checks match an ascii double pair, so a quotation written in
    single marks is not seen by either -- it reads as sourced and is compared
    to nothing. An endpoint replying in JSON writes one that way now and then
    to avoid escaping: 4 of 230 across one sweep, and one draft did it eight
    times out of eight.
    """
    out, n = CITED_SINGLE.subn(r'"\1"\2', text or "")
    return out, ["%d quotation(s) put in double quotes" % n] if n else []


def words_of(text):
    """A quotation reduced to what it says, so two spellings compare equal.

    A comment is spelled however its author typed it and prose here is ascii,
    so a faithful quotation cannot match character for character. Folding both
    sides leaves the words, which is what the quote check is about.
    """
    return re.sub(r"\s+", " ", fold(text)[0]).strip().lower()


def forum_name(key):
    """`community.reddit-localllama` as a reader spells it."""
    tail = key.split(".", 1)[-1]
    return FORUM_SHORT.get(tail, tail)


def render_ref(key, facet, form=None, named=True):
    """One reference as the text that replaces it.

    `named=False` drops the facet key, which is what a comparison against
    another model wants: it is the SAME facet on the other side, so repeating
    the key gives "aa.lcr p80 against aa.lcr p90" where "aa.lcr p80 against
    p90" says it once.

    A community facet renders as the sentence the verdicts already use, because
    mentions and approval are what a reader of a forum figure wants and its
    percentile is a ranking against other models nobody quotes. Everything else
    renders as the key and its percentile, which is the claim the cohort
    supports -- `p74` means it beat 74% of the registry models carrying the same
    facet, and that is checkable where a raw score is not comparable.
    """
    if facet.get("group") == "community":
        out = "%s %s mentions" % (forum_name(key), facet.get("mentions"))
        approval = facet.get("approval")
        # a forum with no scored comment has no approval, and inventing 0 would
        # read as unanimous disapproval
        return out if approval is None else "%s at %s%% approval" % (out, approval)
    # a figure with no cohort behind it -- a rank, a composite score, a setting
    # the page was read under -- renders as itself, with neither a percentile
    # nor its key. printing `p None` would read as a percentile that came out
    # zero, and `box.reserve 12gib` names in the figure what the sentence around
    # it has already said
    pct = facet.get("pct")
    tail = "" if pct is None else " p%s" % pct
    head = "%s " % key if named and pct is not None else ""
    if form == "value" and facet.get("value") is not None:
        value = facet["value"]
        digits = UNIT_DIGITS.get(facet.get("unit"),
                                 BIG if abs(value) >= 10 else SMALL)
        shown = "%g" % round(value, digits)
        return "%s%s%s%s" % (head, shown,
                             UNIT_SUFFIX.get(facet.get("unit"), ""), tail)
    return "%s%s" % (head, tail.strip() or "p?")


def render_parts(text, facets, other=None):
    """[str | {key, repo, shown, missing}] -- the substitution, kept not flattened.

    `render` joins these into a string, which is all markdown can hold. A page
    can do better: a figure it printed out of a capture should be able to say
    WHICH capture, the way the table cell that figure came from already does.
    That is only possible if the renderer hands over what it substituted.

    Recovering the key afterwards by matching the rendered text is a second
    implementation of the substitution, and it cannot attribute a cross-model
    reference at all -- those render bare on purpose, so there is nothing in the
    words to match. The renderer is the only thing that knows, so it says.
    """
    out, at, text = [], 0, text or ""
    for m in REF.finditer(text):
        key, repo, form = m.group(1), m.group(2), m.group(3)
        facet = ((facets if not repo else (other(repo) if other else None))
                 or {}).get(key)
        if m.start() > at:
            out.append(text[at:m.start()])
        at = m.end()
        part = {"key": key, "repo": repo,
                "shown": m.group(0) if not facet
                else render_ref(key, facet, form, named=not repo)}
        if not facet:
            part["missing"] = True
        out.append(part)
    if at < len(text):
        out.append(text[at:])
    return out


def render(text, facets, other=None):
    """(text, unresolved) with every reference replaced by its figure.

    An unresolved reference is LEFT in the text rather than dropped. A verdict
    that silently loses a clause reads as a complete argument that happens to be
    missing its evidence, which is the failure this whole file exists to stop.

    `other(repo)` resolves `{key@owner/Repo}`, which is how a comparison reaches
    the model it is against. Without it half of "II 55.8 against 52.0" was typed,
    and the typed half went stale inside a sentence that was otherwise generated.
    """
    parts = render_parts(text, facets, other)
    missing = [p["key"] if not p["repo"] else "%s@%s" % (p["key"], p["repo"])
               for p in parts if isinstance(p, dict) and p.get("missing")]
    return "".join(p if isinstance(p, str) else p["shown"] for p in parts), missing


# a percentile typed into prose rather than referenced. `p95` is the shape the
# verdicts use; a size (`8.7 gib`) or a count is not a facet and is left alone
TYPED_PCT = re.compile(r"(?<![\w.])p\d{1,3}\b")


def check_proposal(text, facets, require_reference=False):
    """(ok, why) for a drafted verdict, against what it is allowed to assert.

    The model picks the words and the evidence; it does not pick the numbers.
    A draft that types a percentile has opted out of the rendering that keeps
    figures live, and one that references a facet the model does not carry
    would render as a claim with nothing behind it. Both are refused rather
    than accepted and fixed later, because a proposal costs nothing to redo and
    the verdict on disk is untouched until a human promotes it.
    """
    bad = TYPED_PCT.findall(REF.sub("", text or ""))
    if bad:
        return False, "writes %s instead of referencing the facet" % ", ".join(sorted(set(bad)))
    _, missing = render(text, facets)
    if missing:
        return False, "references %s, which this model does not carry" % ", ".join(sorted(set(missing)))
    # writing no figures and being grounded in nothing look identical to the
    # rule above. the first drafted verdict cited nothing at all and asserted
    # "strong tool-use and coding performance" for a model whose coding facet
    # had just stopped existing -- fluent, authoritative, resting on air
    if require_reference and not REF.search(text or ""):
        return False, "cites no facet at all, so nothing in it is checkable"
    return True, ""


# `aa.lcr p70` -- a facet named beside its percentile, which is exactly what
# `{aa.lcr}` renders back to. 262 of the verdicts' figures are in this shape
TYPED_FACET = re.compile(r"(?<![\w.]){?([a-z][a-z0-9_.\-]{2,})}?\s+p(\d{1,3})\b", re.I)
# and `aa.speed 140 tok/s p78`, which is what `{aa.speed:value}` renders back
# to. tried FIRST, because the pattern above would match its tail and drop the
# measurement the sentence was written to carry
TYPED_VALUE = re.compile(r"(?<![\w.])([a-z][a-z0-9_.\-]{2,})\s+-?[\d.]+\s*"
                         r"(?:tok/s|%)?\s+p(\d{1,3})\b", re.I)
# `card swebench verified 71.4 claim p59` -- the one multi-word name matched,
# and only because the metric sits immediately before its own value. the
# general "words then a percentile" rule was tried and matched `p42` in
# "p95 on the omniscience index, p42 on gpqa" to the INDEX rather than to gpqa
CARD_CLAIM = re.compile(r"(?<![\w.])card ([a-z][a-z0-9 _-]{2,28}?)\s+"
                        r"-?[\d.]+\s+claim\s+p(\d{1,3})\b", re.I)


def aliases(facets, prefer=()):
    """{short name: key} for every facet whose short name is settled here.

    The prose drops the prefix -- `ifbench p96` rather than `aa.ifbench p96` --
    and that is most of what is left once the keyed form is converted. A short
    name shared by two facets needs settling first: `tau2` is both `aa.tau2` and
    `card.tau2` on several models, and choosing between a third party's
    measurement and the vendor's own claim about itself is not a substitution
    anything should make on a guess.

    `prefer` settles it where the BLOCK already does. Two verdicts wrote
    `tau2 pNN` in their notes while their own evidence list cited `{aa.tau2}` --
    one facet named two ways in one block -- so the ambiguity was in the short
    name and never in what the author meant. Where the block cites BOTH
    candidates, nothing is settled and the name stays as written.
    """
    prefer = set(prefer or ())
    out, seen = {}, {}
    for key in facets:
        head, _, tail = key.lower().partition(".")
        forms = {tail, tail.replace("_", "-"), tail.replace("_", " ")}
        # the prose also names the SOURCE rather than the metric where a model
        # carries one facet from it -- `lmarena 1440 p73` for `lmarena.rating`.
        # ambiguous by construction on `gbench`, which most models have three of
        forms |= {head, head.replace("swerebench", "swe-rebench")}
        for form in forms:
            if form:
                seen.setdefault(form, []).append(key)
    for form, keys in seen.items():
        keys = sorted(set(keys))
        if len(keys) == 1:
            out[form] = keys[0]
            continue
        cited = [k for k in keys if k in prefer]
        if len(cited) == 1:
            out[form] = cited[0]
    return out


def convert(text, facets, prefer=()):
    """(text, converted, crossed) -- typed percentiles turned into references.

    EVERY figure a facet still carries is referenced, including one that has
    drifted. That is the point rather than a compromise: the number printed for
    `{aa.lcr}` is read from the capture at print time, so referencing a stale
    literal is what MAKES it correct. Muse glimmer's `gbench overall p84`
    against a facet reading p74 is the case this file was written for, and the
    fix for it is exactly this substitution.

    What a substitution cannot fix is the SENTENCE. A figure that has crossed a
    band -- `aa.speed p77` to p28, top to bottom -- leaves prose arguing the
    opposite of its own rendered number, and no amount of referencing repairs
    that. Those come back as `crossed`, for a human to re-read the argument.

    The substitution changes no printed character where nothing has drifted:
    `{aa.lcr}` renders as `aa.lcr p70`, which is what was there.
    """
    converted, crossed = [], []
    short = aliases(facets, prefer)

    def band_note(key, pct, now):
        if band("pct", pct) != band("pct", now):
            crossed.append((key, "p%s now, %s -> %s"
                            % (now, band("pct", pct), band("pct", now))))

    def card_claim(m):
        key = "card." + re.sub(r"[\s-]+", "_", m.group(1).strip().lower())
        facet = facets.get(key)
        if not facet or facet.get("pct") is None or facet.get("value") is None:
            return m.group(0)
        band_note(m.group(0), int(m.group(2)), facet["pct"])
        converted.append((m.group(0), "{%s:value}" % key))
        return "{%s:value}" % key

    def with_value(m):
        key, pct = m.group(1), int(m.group(2))
        facet = facets.get(key) if key in facets else facets.get(short.get(key.lower()))
        if not facet or facet.get("pct") is None or facet.get("value") is None:
            return m.group(0)
        key = key if key in facets else short[key.lower()]
        band_note(m.group(0), pct, facet["pct"])
        converted.append((m.group(0), "{%s:value}" % key))
        return "{%s:value}" % key

    def one(m):
        key, pct = m.group(1), int(m.group(2))
        if key not in facets:
            # the prose writes the short name -- `ifbench p96` for `aa.ifbench`
            found = short.get(key.lower())
            if not found:
                return m.group(0)
            key = found
        facet = facets.get(key)
        if not facet or facet.get("pct") is None:
            return m.group(0)
        now = facet["pct"]
        if band("pct", pct) != band("pct", now):
            crossed.append((m.group(0), "p%s now, %s -> %s"
                            % (now, band("pct", pct), band("pct", now))))
        converted.append((m.group(0), "{%s}" % key))
        return "{%s}" % key

    # a reference already written is left alone: `{aa.lcr}` has no `pNN` after
    # it, so the pattern cannot match one, but a caller may pass rendered text.
    # the value form goes first so its measurement is not thrown away
    out = CARD_CLAIM.sub(card_claim, text or "")
    return TYPED_FACET.sub(one, TYPED_VALUE.sub(with_value, out)), converted, crossed


def quote_id(text):
    """A citation for one comment, stable across refreshes of the capture.

    Keyed on the words rather than on a position, because a thread gains
    comments between sweeps and `refs[2]` would silently become a different
    person's sentence. The url is not enough on its own -- several comments in
    a capture share one thread url.
    """
    return "q:" + hashlib.sha1((text or "").strip().encode()).hexdigest()[:8]


def quotes_of(facets):
    """{quote id: (ref, facet key)} for every comment this model carries."""
    out = {}
    for key, f in (facets or {}).items():
        for ref in (f.get("refs") or []):
            out[quote_id(ref.get("quote"))] = (ref, key)
    return out


def check_evidence(keys, facets):
    """(ok, why) for the citation list beside a drafted verdict.

    Citations sit here rather than inside the sentence. Asked for inline
    references a model wrote "{aa.lcr} sits at {aa.lcr}", which renders as
    "aa.lcr p53 sits at aa.lcr p53" -- it was using one citation token as both
    a noun and a value, because splicing a citation into prose invites exactly
    that. Keeping them apart also means the prose reads as prose and the
    figures stay rendered.
    """
    if not keys:
        return False, "cites no facet at all, so nothing in it is checkable"
    known = quotes_of(facets)
    missing = [k for k in keys
               if k not in facets and not (k.startswith("q:") and k in known)]
    if missing:
        return False, ("cites %s, which this model does not carry"
                       % ", ".join(sorted(set(missing))))
    return True, ""


def cite(text, facets):
    """(text with numbered markers, the citations in the order first used).

    A citation sits beside the words it supports rather than in a list at the
    end, so a reader can tell which claim rests on which evidence. It renders as
    a MARKER and never as a value: an earlier design substituted the figure
    inline, and a model handed that promptly wrote "{aa.lcr} sits at {aa.lcr}"
    -- one token doing duty as a noun and a number in the same sentence.
    """
    order, lines = {}, []
    # what the prose put in quotation marks before each citation, so a long
    # comment is excerpted around the words actually quoted rather than from
    # its first character
    said_at = {qid: said for said, qid in QUOTED.findall(text or "")}

    def one(m):
        key = m.group(1)
        if key not in order:
            rendered = evidence_line(key, facets, said=said_at.get(key))
            if rendered is None:
                return m.group(0)
            order[key] = len(order) + 1
            lines.append(rendered)
        return "[%d]" % order[key]

    return CITE_REF.sub(one, text or ""), lines


# `"the words" {q:1a2b3c4d}` -- a fragment quoted inline and attributed. this is
# the one thing in the format that can still be false while passing every other
# check, because quotation marks assert the words are somebody else's
QUOTED = re.compile(r'"([^"]{4,})"\s*\{(q:[0-9a-f]+)\}')


def check_quoted(text, facets):
    """(ok, why) -- every inline quotation really appears in the comment it cites.

    Quoting is what makes a verdict about reception worth reading: "extreme
    overthinking" beside a link is checkable where "reception is mixed" is not.
    It is also the easiest thing to get subtly wrong, because a model that
    paraphrases inside quotation marks produces something that looks sourced
    and is not.
    """
    known = quotes_of(facets)
    for said, qid in QUOTED.findall(text or ""):
        found = known.get(qid)
        if not found:
            return False, "quotes %s, which this model does not carry" % qid
        if words_of(said) not in words_of(found[0].get("quote")):
            return False, ('quotes "%s", which is not in the comment it cites' % said)
    return True, ""


QUOTE_WINDOW = 240


def excerpt(quote, said=None, window=QUOTE_WINDOW):
    """A comment trimmed for printing, around the words that were quoted.

    Trimming from the front hides the evidence: a verdict cited "great speed"
    from the tail of a long comment and the rendered line showed its first 220
    characters, so a correct citation read as a fabricated one. The excerpt
    follows the quotation instead.
    """
    text = re.sub(r"\s+", " ", (quote or "")).strip()
    if len(text) <= window:
        return text
    at = text.lower().find(re.sub(r"\s+", " ", said).strip().lower()) if said else -1
    if at < 0:
        return text[:window] + ".."
    start = max(0, at - window // 3)
    end = min(len(text), start + window)
    return ("" if start == 0 else "..") + text[start:end] + ("" if end == len(text) else "..")


def evidence_line(key, facets, said=None):
    """An evidence entry, which is a bare reference rather than a sentence.

    A quote id renders as the words somebody wrote and somewhere to check them,
    so a verdict resting on what people said points at the saying rather than
    paraphrasing it.
    """
    if key.startswith("q:"):
        found = quotes_of(facets).get(key)
        if not found:
            return None
        ref, _ = found
        return '"%s" -- %s' % (excerpt(ref.get("quote"), said),
                               ref.get("url") or "no url")
    facet = facets.get(key)
    return render_ref(key, facet) if facet else None


# how many facets from each end of the range a sheet carries. a model holds up
# to 34 and listing all of them buries the shape; what a sentence gets built
# from is the strongest, the weakest, and every forum.
SHEET_TOP = 6
# and how many comments per forum. the quotes are the part that matters most:
# muse glimmer reads 86% approval on reddit and the comments behind it are
# sceptical questions the polarity lexicon scored positive, so a verdict written
# from the number argues something a verdict written from the text would not
SHEET_QUOTES = 3


def fact_sheet(repo, model, top=SHEET_TOP, quotes=SHEET_QUOTES):
    """Everything a reviewer -- or a model -- should reason from, and no more.

    Deliberately not free rein: this is handed over INSTEAD of the captures, so
    that whatever writes the prose picks which evidence matters rather than
    which numbers to believe. Every figure here is rendered by the same code
    that renders a reference, so what the author reads is what a reader will.
    """
    facets = (model or {}).get("facets") or {}
    lines = ["%s (%s), kind %s" % (model.get("name") or repo, repo,
                                   model.get("kind") or "?")]

    forums = sorted(k for k, f in facets.items() if f.get("group") == "community")

    # the quotes lead, before any figure. the record carried them in 2026-08-17
    # and the verdict written from it argued from the percentage anyway: muse
    # glimmer reads 86% approval on reddit and the comments behind it are
    # sceptical questions the polarity lexicon scored positive. reading the
    # number first is how that happens, so it is not offered first.
    said = [(k, r) for k in forums for r in (facets[k].get("refs") or [])[:quotes]]
    if said:
        lines.append("  what people actually said:")
        for key, ref in said:
            # the id is what a verdict cites, so the comment is printed from the
            # capture rather than paraphrased into the prose
            lines.append("    %s [%s] %s"
                         % (quote_id(ref.get("quote")), ref.get("polarity") or "0",
                            (ref.get("quote") or "").strip()[:220]))
            if ref.get("url"):
                lines.append("       %s" % ref["url"])

    if forums:
        lines.append("  forums, as the lexicon scored them:")
        for key in forums:
            lines.append("    " + render_ref(key, facets[key]))

    # `tasks` carries a bare count in the older captures and {n, pos, neg} in the
    # newer ones. both are read, because a verdict may have been written against
    # either and the sheet has to be reconstructable at the date it was written
    tasks = []
    for name, v in ((model or {}).get("tasks") or {}).items():
        if isinstance(v, dict):
            tasks.append((v.get("n") or 0, name, v.get("pos") or 0, v.get("neg") or 0))
        else:
            tasks.append((v or 0, name, None, None))
    if tasks:
        tasks.sort(reverse=True)
        shown = []
        for n, name, pos, neg in tasks[:8]:
            mood = "" if pos is None else " (+%d/-%d)" % (pos, neg)
            shown.append("%s %s%s" % (name, n, mood))
        lines.append("  what people bring it, counted: " + ", ".join(shown))

    scored = sorted(((f.get("pct"), k) for k, f in facets.items()
                     if f.get("group") != "community" and f.get("pct") is not None),
                    reverse=True)
    if scored:
        shown = scored[:top] + ([(None, None)] if len(scored) > 2 * top else [])
        shown += scored[-top:] if len(scored) > top else []
        lines.append("  facets, strongest first:")
        for pct, key in shown:
            if key is None:
                lines.append("    ...")
                continue
            f = facets[key]
            flag = "  LOW CONFIDENCE" if f.get("low_confidence") else ""
            # the band beside the percentile, because a bare p55 does not say
            # whether it is good: handed one, a model wrote "decodes fast",
            # which is the middle of the pack rather than fast
            lines.append("    %-26s p%-4s %-8s %-10s of %-4s %s%s"
                         % (key, pct, band("pct", pct),
                            ("%g" % round(f["value"], 3)) if f.get("value") is not None else "-",
                            f.get("cohort") or "?", f.get("label") or "", flag))

    # what the bands already conclude. offered so a written use_for that departs
    # from it is a choice somebody made rather than something nobody noticed --
    # across the blocks carrying both, the written list agreed with this one
    # less often than it disagreed
    d = (model or {}).get("derived") or {}
    for field, label in (("best_for", "bands say good for"),
                         ("weak_for", "bands say weak for")):
        if d.get(field):
            lines.append("  %s: %s" % (label, ", ".join(d[field])))
    return "\n".join(lines)


# the bands prose actually speaks in. a sentence says "well received" or "split"
# and "strong" or "middling"; it does not say "p74". so a figure moving WITHIN a
# band leaves its sentence true and a figure crossing one does not, which is a
# better trigger than any delta -- bonsai fell 75% to 50% approval, `positive`
# to `mixed`, while its note still said the two forums point opposite ways.
BANDS = {
    "approval": [(40, "negative"), (70, "mixed"), (101, "positive")],
    "pct": [(33, "bottom"), (67, "middle"), (101, "top")],
}
# the backstop for a figure that stays in its band while the weight of the
# evidence under it changes: qwen3.8 27b went 175 to 304 mentions, still
# `heavily discussed`, but the claim now rests on nearly twice the sample
MOVED_FRACTION = 0.5
# and the floor that stops it firing on noise. ling 3.0 tiny went 2 to 6
# mentions, a 200% swing that means nothing -- a verdict resting on two
# comments is thin whichever way they went
MENTIONS_FLOOR = 10


def band(kind, value):
    for edge, name in BANDS[kind]:
        if value < edge:
            return name
    return BANDS[kind][-1][1]


def snapshot(keys, facets):
    """What the author was looking at, to be stored beside the prose.

    Only the figures a verdict can quote: a percentile for a scored facet, and
    both numbers for a forum. Snapshotting the whole facet would flag on fields
    no sentence ever mentions.
    """
    out = {}
    for key in keys:
        facet = facets.get(key)
        if not facet:
            continue
        if facet.get("group") == "community":
            out[key] = {"mentions": facet.get("mentions"),
                        "approval": facet.get("approval")}
        elif facet.get("pct") is not None:
            out[key] = facet["pct"]
    return out


def _moved_one(kind, was, now):
    """Why this figure is worth re-reading the sentence for, or ""."""
    if was is None or now is None:
        return "" if was == now else "%s %s -> %s" % (kind, was, now)
    b0, b1 = band(kind, was), band(kind, now)
    if b0 != b1:
        return "%s %s -> %s (%s -> %s)" % (kind, was, now, b0, b1)
    return ""


def moved(snap, facets):
    """[(key, why)] for every snapshotted figure that changed enough to matter."""
    out = []
    for key, was in sorted((snap or {}).items()):
        facet = facets.get(key)
        if not facet:
            out.append((key, "no longer carried by any source"))
            continue
        if isinstance(was, dict):
            why = []
            # only what the verdict actually stated. a block citing a mention
            # count with no approval beside it did not rest on an approval, so
            # one appearing later is new information rather than a contradiction
            if "approval" in was:
                why.append(_moved_one("approval", was["approval"],
                                      facet.get("approval")))
            if "mentions" in was:
                m0, m1 = was.get("mentions") or 0, facet.get("mentions") or 0
                if max(m0, m1) >= MENTIONS_FLOOR and abs(m1 - m0) >= MOVED_FRACTION * max(m0, 1):
                    why.append("mentions %s -> %s" % (m0, m1))
            why = [w for w in why if w]
            if why:
                out.append((key, "; ".join(why)))
        else:
            why = _moved_one("pct", was, facet.get("pct"))
            if why:
                out.append((key, why))
    return out
