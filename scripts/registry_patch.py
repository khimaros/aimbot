"""Splice generated blocks into registry/models.yaml without reformatting it.

Four scripts write blocks back into the registry and three of them had grown
their own copy of this loop. They did not agree, and the disagreement was a
bug rather than a style difference: `resolve-turns` appends a block a model
does not have yet, `resolve-ids` only ever replaced one, so a model added
without an `ids:` block was matched, counted as filled, and silently dropped --
qwen3.8 flash next carried AA and lmarena matches for a full capture that way
and reached MODELS.md unscored.

So the locating and splicing live here once, and each caller still renders its
own lines. That split is deliberate: `turns:` is short scalars and `runtime:`
carries prose long enough that it has to go through a yaml dumper to be wrapped
and quoted, and a single renderer for both would either mangle the prose or
quote every enum.

Dumping the parsed document back would be shorter than any of this and would
delete every comment in the file. The quant notes and the sampler provenance
are the part of the registry a human wrote, and a script that fills in benchmark
ids has no business reformatting them.
"""

import re

# `  owner/name:` at model depth, as distinct from the `    key:` inside it
MODEL_KEY = re.compile(r"^  (\S.*?):\s*$")
BLOCK_KEY = re.compile(r"^    (\S+):\s*$")
BODY_INDENT = "    "
BLOCK_INDENT = "      "


def _skip_block_body(lines, i):
    """Past the values under a `    key:` line, which are indented deeper."""
    while i < len(lines) and lines[i].startswith(BLOCK_INDENT):
        i += 1
    return i


def _present(lines, i):
    """The block names in the model body starting at `i`."""
    names = set()
    while i < len(lines) and (not lines[i].strip() or lines[i].startswith(BODY_INDENT)):
        key = BLOCK_KEY.match(lines[i])
        if key:
            names.add(key.group(1))
        i += 1
    return names


def patch_blocks(path, blocks, after=None):
    """Insert or replace named blocks in each model's body. Returns the count.

    `blocks` is {model key: {block name: [rendered lines]}}. A block already
    present is replaced WHERE IT SITS, so a hand-ordered file keeps its order:
    the body is scanned for what it already has before anything is written,
    because otherwise `after` relocates every existing block to the anchor and
    a run that changed nothing rewrites 816 lines.

    A block that is absent is inserted after the `after:` block when that is
    given and found, and otherwise appended to the end of the model's body --
    the only other position that cannot end up between a comment and the key
    it explains.
    """
    lines = open(path).read().split("\n")
    out, i, n = [], 0, 0
    while i < len(lines):
        m = MODEL_KEY.match(lines[i])
        out.append(lines[i])
        i += 1
        if not m or m.group(1) not in blocks:
            continue
        want = blocks[m.group(1)]
        # a block the body already has is rewritten where it sits; the anchor
        # is only ever used for one this model does not have yet
        present = set(want) & _present(lines, i)
        body, done = [], set()
        while i < len(lines) and (not lines[i].strip() or lines[i].startswith(BODY_INDENT)):
            key = BLOCK_KEY.match(lines[i])
            name = key.group(1) if key else None
            if name in want:
                body.extend(want[name])
                done.add(name)
                i = _skip_block_body(lines, i + 1)
                continue
            body.append(lines[i])
            i += 1
            if name == after:
                # the anchor's own body has to be copied before anything is
                # inserted behind it, or the new block lands inside it
                while i < len(lines) and (lines[i].startswith(BLOCK_INDENT)
                                          or lines[i].startswith(BODY_INDENT + "- ")):
                    body.append(lines[i])
                    i += 1
                for nm, rendered in want.items():
                    if nm not in present and nm not in done:
                        body.extend(rendered)
                        done.add(nm)
        # a trailing blank line belongs to the next model, not to this body
        tail = []
        while body and not body[-1].strip():
            tail.insert(0, body.pop())
        for nm, rendered in want.items():
            if nm not in done:
                body.extend(rendered)
        out.extend(body + tail)
        n += 1
    open(path, "w").write("\n".join(out))
    return n
