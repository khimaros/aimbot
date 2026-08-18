# aimbot

model facts, the research behind them, and the comparison that falls out.

the model registry: one home for facts about models, shared by
[llama-tools](../llama-tools) and quantbench.

extracted from llama-tools so that those facts have exactly one home.
before the split, the same fact lived in up to six places across two repos, and
the copies had already drifted: quantbench's `models.yaml` carried
`weights_gb: 28.6` for qwen3.6-27b, which is the *plain* gguf repo rather than
the `-MTP-` one the roster actually runs -- the same 0.42gib error
[MODELS.md](MODELS.md) documents having made once already. its header also said
llama-swap "never forwards `--temp`", which stopped being true at some point
nobody noticed.

## the split

**facts** are objective, discoverable and identical for every consumer:
parameter counts, gguf sizes, native context, which thinking knob a chat
template accepts, the id each benchmark source invented. they live here.

**policy** is which of them to run, at what context, on which host, under which
sampling profile. it is legitimately different per consumer -- quantbench wants
a tool-use profile and per-slot context, llama-tools wants a chat profile and a
whole-host budget -- so it stays with the consumer.

the test for which side something belongs on: **if two consumers could
reasonably disagree about it, it is policy.**

this repo has no opinion about the shape of a consumer's config, and knows
nothing about any particular server. it publishes facts and the keys to address
them by; a consumer defines its own format and checks it against these files
itself.

## layout

```
registry/models.yaml      per-model facts, keyed by huggingface base repo
registry/sampling.yaml    the named sampling profiles, and what each one means
scripts/models-validate   check that the registry is internally consistent
scripts/resolve-ids       match registry models to each source's own ids
scripts/resolve-turns     fill turns/thinking from the executed chat template
scripts/build-viewer      build docs/ from the registry and the captures
scripts/viewer.html       the page it fills in
docs/                     the github pages site: index.html and data.json
research/                 the collectors and analysis (see research/README.md)
research/data/            committed point-in-time captures
research/data/usecase.json       every measurement per model, with a ref each
research/usecase-assessed.json   the written judgement, kept machine-readable
MODELS.md                 the comparison, generated from research/data
```

the repo IS the model's name. an invented short name is a second thing to keep
in sync, and llama-tools grew four separate short-name tables before this file
existed.

## named sampling profiles

a profile is **samplers plus the capability claim that holds at those
samplers**. that coupling is not decoration: qwen3.6-27b at temp 0.6 is a
tool-use model and at temp 1.0 it is a chat model, and consumers had been
carrying that distinction as a commented-out alternate line in their own
configs. a commented line cannot be validated, cannot be selected by name, and
gives two consumers no way to agree on which half they took.

`registry/sampling.yaml` owns the *names* and their meaning, so `sampling:
tool-use` means the same thing everywhere. each model owns the *values*,
because vendors recommend different numbers for the same idea. it also owns the
vocabularies those values are drawn from -- the `tuned` tags and the thinking
levels -- so a level no chat template accepts fails validation here.

a model may also carry `thinking.accepts` and `thinking.knob`, and most of it
is derived now: `analyze-chat-templates` sets each candidate level and compares
the render against a deliberately invalid control, which separates a level the
template ENFORCES from one it recognises from one it accepts and ignores. that
turned up a real error -- upstage's card documents `reasoning_effort="none"`
for a direct response and the template branches on `medium|high|xhigh`, so
`none` changed nothing and the registry had recorded it. `knob` is derived the
same way and is not always the name everyone assumes: kimi k3's is
`thinking_effort`, whose guard rejects the `medium` its own injected prose
tells the model is supported.

levels that render byte-identically are ONE level under two names, and listing
both would invent a gradation, so they collapse into `aliases`:

```yaml
    thinking:
      knob: reasoning_effort
      accepts: [low, medium, xhigh]
      default: xhigh
      aliases: {high: xhigh}
```

`default` is the level a client gets by NOT setting the knob, derived the same
way: render the template with the knob absent and match that against each
accepted level. it is worth having as a field rather than as prose because it
is rarely the cheap one -- kimi k3 defaults to `max`, qwen3.8-27b to `xhigh`
(15k-52k thinking tokens in reported traces against qwen3.6's 3k), and hy3 to
`no_think`, so on that model thinking is off until you ask for it. 9 of the 11
models with a graded knob carry one; on the other two, omitting the knob
matches no accepted level, which is a different fact and is not stated. it is
reported in the same spelling as `accepts`, so unsloth's qwen3.8 build -- which
answers `high` where upstream answers `xhigh`, for a byte-identical prompt --
reads `xhigh` here like everything else. `models-validate` fails if a default
is not one of the levels beside it.

a template whose only thinking control is a SWITCH now gets a block too, which
is the larger half of the roster: 25 of the 41 text models read
`enable_thinking` and no graded knob, and the registry had been silent about
every one of them. the same probe answers the same question -- 19 of them think
unless told not to, and 6 do not think until asked (all five gemma 4 builds,
and qwen3.5-0.8b):

```yaml
    thinking:
      knob: enable_thinking
      kind: boolean
      default: false
```

`accepts` is deliberately absent there, and `models-validate` rejects it if
somebody adds one. the values of a switch are the booleans themselves, and a
consumer reading `accepts: [off, on]` would send the STRING `"off"` -- which
jinja evaluates as truthy, turning thinking on by asking for it off.

three templates read BOTH, and that is what `gate:` records:

```yaml
    thinking:
      knob: reasoning_effort
      gate: enable_thinking
      accepts: [low, medium, xhigh]
      default: xhigh
```

qwen3.8-27b, deepseek v4 flash and kimi k3 have a graded knob whose vocabulary
contains no `off`, because turning thinking off is the switch's job. a
consumer that only knows the graded name cannot express `off` at all -- and
sending `reasoning_effort: "off"` to qwen3.8 does not quietly do nothing, it
hits a validated guard and raises. the registry recorded only the graded knob
until now, so the viewer was generating exactly that broken request body for
the `instruct` profile, whose declared level is `off`.

this is what a widened guard usually turns out to be. unsloth's qwen3.8 build
accepts a `high` that upstream rejects, which looks like a fourth level the
model was never trained for -- and is not: the template maps `high` onto
`xhigh` before the same guard runs, so both spellings produce the identical
prompt and the model still only ever sees three. inkling-small's added `xhigh`
is `max` the same way. once the aliases collapse, the base repo and the gguf
agree about the vocabulary in both cases, which is the useful way to say it.

upstage collapses `medium|high|xhigh` into a single branch in its OWN template,
so that knob has one effective setting under three names rather than a
gradation, and `none` -- which its card documents for a direct response --
changes nothing at all.

what stays typed is the templates that interpolate the value verbatim, which
genuinely accept any string and state only a default -- gpt-oss
`low/medium/high`, step 3.7 flash the same, muse glimmer
`low/medium/high/xhigh` on `reasoning_strength`. those keep a note saying where
the vocabulary came from. `models-validate --thinking` lists the models still
missing one; `--cards` checks the sampling profiles against the sets the cards
document, base repo and quant repo alike.

## turns

`turns:` is what the chat template does with the roles a client sends, derived
by executing it rather than by reading it:

```yaml
    turns:
      source: unsloth/Qwen3.6-27B-GGUF
      developer: as-system          # own | as-system | dropped | rejected
      leading_system_max: 2
      mid_system: dropped           # ok | dropped | rejected | reordered
      mid_developer: dropped
      upstream_differs: [developer, leading_system_max, mid_developer, mid_system]
```

`upstream_differs` names the fields where the base repo's own template answers
differently, which is a fact about the QUANT rather than the model: on this
entry every one of them, because the vendor's template rejects a developer
message outright and unsloth's accepts it. a consumer that cares whether a
behaviour was designed or patched in has the list; one that does not can
ignore it.

`source` is not decoration. the base repo and the gguf disagree for 11 of the
39 models carrying both, because unsloth patches developer-role handling into
the conversion that upstream does not have, so the facts are taken from the
gguf a consumer actually serves and the repo they came from is recorded beside
them. `resolve-turns --check-quants` lists the models whose OTHER quant repos
contradict the recorded one -- `unsloth/Qwen3.5-27B-GGUF` and
`unsloth/Qwen3.5-27B-MTP-GGUF` are the same model from the same publisher and
only the MTP build accepts a developer message.

`dropped` is the value to design around. the template renders, the server
returns 200, and the message is not in the prompt; 9 of the 41 unsloth gguf
templates do this to a developer message and 9 more silently discard a THIRD
leading system message after merging the first two. `make turns` regenerates
the blocks and `make lint` fails if the registry is behind the probe data.

## using it from a consumer

one entry, trimmed:

```yaml
Qwen/Qwen3.8-27B:
  kind: text
  name: {short: qwen3.8 27b, match: 'qwen\s*-?3\.8[\s-]*27b|qwen3\.8-27b'}
  quants:
    - repo: unsloth/Qwen3.8-27B-GGUF
      quant: Q8_0
      note: measured +0.02% perplexity against bf16 over 580 chunks ...
  speculative: {type: draft-mtp, n_max: 3}
  sampling:
    thinking: {temp: 1.0, top_p: 0.95, top_k: 20, min_p: 0.0,
               tuned: [instruct, chat, reason, code, tools], thinking: xhigh}
    instruct: {temp: 0.7, top_p: 0.8, top_k: 20, min_p: 0.0,
               tuned: [instruct, chat, code, tools], thinking: 'off'}
  modalities: {input: [text, image], output: [text]}
  ids: {aa: '', gbench: '', lmarena: '', swerebench: '', epoch: ''}
```

a consumer addresses this by four keys: the repo, a `quants[]` repo/quant pair,
a `sampling` profile name, and a `speculative` block it may decline -- and which
a quant may decline on its behalf, since `draft-mtp` needs a nextn head that only
the `-MTP-GGUF` build of the same model carries.

where a profile deliberately departs from what the vendor documents, the
vendor's own set is recorded beside it as `upstream-<profile>` rather than
described in prose, so a consumer can select either and the card check can
confirm it still matches. what it
does with them -- what to call the model, what context to serve it at, which
server binary, how to group it -- is its own business, in its own file.

llama-tools keeps its hosts in `etc/aimbot/<host>.yaml` and checks them with
its own `scripts/llama-swap-validate`, which reads `registry/` for exactly
those four keys and knows llama-swap for everything else.

## the viewer

`docs/` is a single page that reads this registry: rank the models, decide what
"good" means, open one, then read how to run it. `make site` regenerates it and
`make lint` fails if the committed copy is behind the data. github pages serves
it straight from the `docs/` folder on `master`.

`make test-e2e` runs it: `tests/e2e` boots the shipped `docs/index.html` under
node against the real `docs/data.json`, behind a dom stub thin enough that it is
the page's own arithmetic being checked rather than a mock of it. `node --check`
was tried first and is not enough -- it passes a stray backtick that turns half
the file into a template literal, which reaches a reader as a blank page.

it fetches ONE file, `docs/data.json`, by relative path. the raw captures are
19mb across twenty files and half of them are yaml, so joining them in the
browser would mean shipping a yaml parser and most of the corpus to read one
table; `scripts/build-viewer` does that join once.

the factors run deep: 23 artificial analysis benchmarks (including
`omniscience non-hallucination`, the one axis where a model is rewarded for
declining to answer), the four gbench modes, epoch's runs, card claims,
community per forum, and a slider per gbench LANGUAGE -- so somebody who writes
rust can weight rust rather than trusting a coding index that averaged it away.
1210 facets over 54 models, grouped and collapsible, each group saying how many
of its weights are live.

the ranking is the part worth explaining. **quality is a weighted mean of
percentiles, and the weights are yours.** the page opens on build-tables'
composite weights -- 0.30 coding, 0.30 agentic, 0.15 gbench, 0.10 arena,
0.10 swe-rebench, 0.05 community, 0.05 card claims, set by a redundancy
analysis rather than by taste -- and every one of them is a slider. weight gbench to
zero if games do not persuade you. weight the forums to 1.0 if they do. the
table re-ranks as you drag.

the sliders are behind `custom weights`, because most readers want a stance
rather than sixty decisions. the stances are a dropdown in the ranking row:
`balanced` is the composite above, and the others answer one question each --
writing code, agentic and tool use, third-party measurement only, what people
report. picking one replaces the weights outright, and moving any slider off a
stance turns the dropdown to `custom weights`.

**how much memory you have.** pick a vram size and a reserve, and the quant
column, the sizes and the retention behind `effective` all switch to the
largest quant that fits in what is left. the reserve is not decoration: the kv
cache grows with the context you serve at and the compute buffers are not free
either, which is why build-tables budgets 105 gib of a 128gb box rather than
128. a repo publishing no file sizes reads as unknown rather than as too big,
because that is a measurement this corpus does not have.

the fit stops at q8 by default and the ceiling is a dropdown, with a floor
beside it. a box with room to spare should not be handed bf16 because it
happened to fit -- past q8 the extra bytes buy nothing measurable and cost
decode speed, which is why build-tables pins the dense models there too -- and
`min q4` says the other end: below it the answer is "not with this much
memory" rather than a two-bit version of the model.

`best fit` in the filter row is on by default and behaves like the filter it
is. releasing it swaps one row per model for one row per rung, using the same
test the fit uses so the two can never disagree about what fits -- 38 models
become 753 rows on a 128gb box at q8. clicking any row opens the modal on the
quant that row was showing, out of that row's repo, rather than on whatever the
modal would have chosen for itself.

that last part needed the table and the modal to agree on which repo a model is
read from, and they did not. where a model ships two builds the registry says
which one can speculate -- qwen3.6-27b's plain repo is marked
`speculative: false`, and only the `-MTP-` build carries the nextn head the
declared drafter needs -- but the table was taking whichever repo happened to be
listed first. both sides now share one rule, so qwen3.6-27b and qwen3.6-35b-a3b
read from their MTP builds everywhere. a test asserts the two never disagree
again, for every model. with `quant adjusted` on, each row
scores at its own bits per weight, which turns the sorted table into one merged
list of what you could actually run. it is worth reading for where it is FLAT:
qwen3.8 27b holds the same quality from UD-Q8_K_XL at 29.3 gib down to
UD-IQ3_XXS at 11.1, because the composite is a mean of percentiles and a 20%
discount does not move it past anything. that is the actionable part -- do not
pay for q8 -- and it only shows up when the ladder is on screen.

**the context costs memory too, and how much is a fact about the model.** set a
`min context` and its kv cache is computed from each model's own attention
geometry and subtracted before anything is asked to fit. the naive
`2 * layers * kv_heads * head_dim` is wrong for most of this roster and wrong
in the expensive direction: gemma 4 runs a 1024-token sliding window on all but
every Nth layer, qwen3.6 makes one layer in four global, and kimi k3 is linear
attention on 69 of its 93 layers with only 24 holding a cache that grows at
all. `fetch-model-facts` counts the full and windowed layers separately from
whatever the config states -- an itemised `layer_types`, a linear-attention
block listing its full layers, an interval -- so the number is the model's
rather than a family guess. a model whose native window is shorter than the
context asked for is not a fit at it: getting there means rope scaling, which
is the consumer's call.

**how fast it will be.** set your box's bandwidth and its compute and two more
columns appear: `tg t/s` for generation and `pp t/s` for prefill. they are two
settings because they are two limits -- generating a token reads every active
weight, prefilling multiplies through them -- and the spec sheet figures are
discounted to what a box does rather than what it claims. the numbers are
arithmetic on facts the registry already holds and nothing here has timed these
models, so they are worth a comparison between rows and an order of magnitude,
not a promise. generation is printed twice where the kv cache costs more than
15% of it, which is how ling 3.0 flash's 84 gib of cache at 128k shows up as
89 t/s empty and 1.8 full.

**raw or effective.** a benchmark measures the model; this roster runs a QUANT
of it. `quant adjusted` in the ranking row is on by default, since that is the
number a local roster is actually asking about; release it and the scores are
exactly what the source published. on, it
discounts by the retention `research/build-tables` fits for the pinned quant's
bits per weight. that curve is imported rather than restated, so the page and
MODELS.md cannot disagree about what effective means. it changes the answer:
kimi k3 runs at UD-IQ1_S, 1.71 bpw, 0.778 retention, and falls from second to
fourth the moment you ask what you would actually get.

three facets sit outside it. sentiment is people talking rather than a score
and decode speed goes UP when you quantize, so the penalty does not describe
either. the arena elo is out for a different reason worth stating: a retention
multiplier means "keep this fraction of the measured quality" only where zero
means no quality -- a pass rate, an index. an elo's zero is arbitrary, so x0.93
on a 1435 rating subtracts 101 points, wider than the spread of this whole
registry, while the same multiplier on 1408 subtracts 10. it was scaled here
until it was caught reordering all 15 rated models, several by 40 to 90
percentile points and hy3 from p93 to p0 -- sending deepseek v4 flash below
qwen3.6 27b and qwen3.5-27b above muse glimmer, none of which was a statement
about quantization. `tests/e2e` now asserts arena percentiles do not move with
the quant.

only the three artificial analysis indices are scaled, which is what
build-tables scales. the other sources measured a served endpoint whose
precision this repo does not know, so discounting them would invent a number
rather than adjust one. a discounted cell is dotted-underlined, its header
gains an `eff`, and hovering gives the raw value and the multiplier.

every column header explains itself on hover -- through the page's own panel
rather than a native tooltip, because half the columns are numbers nobody can
name on sight and a one-second delay is a description nobody reads.

two properties hold whatever you set:

**a percentile is against this registry, not against the world.** p79 on coding
means it beat 79% of the registry models that also carry a coding index. the
question a local roster asks is "best of what i can run", and ranking a 27b
against gpt-5.6 answers a different one.

**an absence is never a zero.** a model gbench has not played simply has no
gbench facet, its composite renormalizes over the facets it does carry, and the
`evidence` column says how many of the weighted factors it was actually
measured on. 3/7 in that column is a warning about the evidence, not a verdict
on the model. 22 of the 41 text models are not on the gbench board at all --
that is upstream, the api publishes 98 models and no more.

every number carries a reference: hover a `[src]` for the source, the file it
came from, and -- for a community claim -- the sentence somebody actually wrote
and a link to the thread. a model's detail opens as a modal deep-linked in the
url (`#model=Qwen/Qwen3.6-27B&tab=operate`) with six tabs, one per kind of
claim: `overview` what it is, `quality` what third parties measured, `analysis`
what we concluded and why, `community` what each forum said, `vendor` what the
people selling it say, and `operate` how to run it. keeping the vendor's own
paragraph on its own tab is the point rather than tidiness -- it used to open
the overview, which gave marketing copy the position the measurements earned.

the `operate` tab emits a `llama-server` argv, a pi `models.json` provider
block, the request body carrying the thinking knob, and a vllm line -- built
from a quant and a sampling profile you pick, since some repos publish twenty
quants and a snippet for the one the registry pinned is no use to somebody who
cannot fit it. every flag in them is a pure function of registry facts -- the
quant repo, the profile's samplers, the native context, the derived knob. what
context to serve it at, on which host, under which server binary is still
policy and still absent.

where a thinking level appears, **the template's default is in bold**: it is
the level a client gets by sending nothing, and it is rarely the cheap one. a
profile asking for `off` on a model with a `gate` is annotated `via
enable_thinking` rather than flagged, because that is how it is said.

sampler recommendations come from three places and the page keeps them apart.
the registry's own profiles are on `operate` and are what the snippets are
built from; `upstream-<profile>` is the vendor's set where this registry
deliberately departs from it. what the cards document is on `vendor`, split
between the model's own card and the quantizer's -- unsloth republishes the
vendor's numbers sometimes and its own the rest of the time, which is why
`fetch-model-cards` reads both repos and why merging them lost which was which.

`modalities.input` is the one typed field with a derived counterpart, and
`models-validate` now checks it against each model's own `config.json` as an
ERROR rather than a report -- the two had drifted on 21 of 54 entries. most
were missing `video` where the config carries a video token; one, deepseek v4
flash, claimed image and audio for a text-only model whose config has neither
encoder. `models-validate --modalities` prints the comparison. `output` stays
typed and unchecked, because nothing here derives what a model emits.

## where a sampling profile's numbers came from

every other fact here says where it came from -- `turns` names the template it
was executed from, a usecase facet carries a `ref`, a capture carries its sha
-- and a sampling profile said nothing at all, so a deliberate departure and a
typo looked identical. each profile now carries a `source`:

```yaml
      tool-use:
        source: tuned-here
        note: "the card says temp 1.0 across all tasks, tool calling included,
          and this roster runs it colder for deterministic tool-call rendering"
        temp: 0.6
```

it is DERIVED, by `scripts/resolve-samplers`, because "where did these numbers
come from" is unknowable after the fact while "what do they still agree with"
is not: `quant-card`, `vendor-card`, `generation-config`, or `tuned-here` when
they match nothing published. the quant repo wins where both cards agree, since
that card describes the weights a consumer actually serves. comparison is on
the fields BOTH sides name -- a card documenting temp and top_p cannot speak to
a min_p, and demanding it did would file every profile under `tuned-here`.

across the registry: 36 profiles agree with the quant repo's card, 4 with the
model's own, 2 with the shipped `generation_config.json`, and 14 with nothing
published. those 14 are the ones worth having: `models-validate` fails unless
each carries a `note` saying why, and `make lint` runs `resolve-samplers
--check`, so a profile claiming `vendor-card` after the card moves under it is
a build failure rather than a stale assertion.

## status

done: the registry (54 models), named sampling profiles, the research corpus,
llama-tools generating its whole llama-swap config from registry facts plus
a host file that lists only choices, and the `docs/` viewer above.

`research/data/usecase.json` is the one place a consumer reads to answer "what
is this model for". it holds 850 facets across the 54 models -- one number per
(source, benchmark) with the model's percentile among the registry models that
carry the same one, the gbench per-language breakdown, what each forum said
with quoted references, and the written judgement carried in from
`research/usecase-assessed.json`. that split is deliberate: measurement is
recomputed by `make usecase`, judgement is source, and a diff shows them moving
separately. the judgement is machine-readable so a generated MODELS.md can read
it rather than parse a document.

sentiment is now per forum rather than pooled -- reddit, hacker news,
level1techs and the huggingface discussion tabs each keep their own counts,
approval and quotes. they do not measure the same thing: reddit argues about
which model is best and the discussion tab reports whether a quant loads at
all, which is why muse glimmer reads 73% approval on one and 0% on the other.
the TOP-LEVEL aggregate stays reddit-only, because build-tables weights
sentiment on a redundancy analysis measured against reddit alone and widening
it would silently re-rank MODELS.md.

that weight is 0.05, down from 0.15, with the 0.10 moved to AA. the redundancy
table argues the other way -- sentiment is 91% new information at 18/20
coverage, the most independent signal here -- but independence is not accuracy.
it is a blunt polarity lexicon read over forum sentences, where "x is better
than y" scores positive for both, and that is not a measurement worth a sixth
of a rank. AA is the opposite trade: one axis of evidence, run as a fixed
harness across every model it scores.

derived rather than typed: `research/fetch-model-facts` covers all 41 text
models with arch, params, native context, mtp presence, the thinking knob and
the samplers the vendor ships; `fetch-chat-templates` commits the 84 templates
themselves and `analyze-chat-templates` executes them, which filled `turns:`
for 41 models and `thinking.accepts` for 11;
`scripts/resolve-ids` filled 99 source ids with zero ambiguous matches;
`research/fetch-model-cards` extracts what models claim about themselves and
`analyze-self-report` measures the discount (median +0.9 over third-party
measurement across 70 matched claims).

not done yet, in the order it should happen:

1. [done] quantbench generates `etc/models.yaml` from this registry plus its own
   `etc/selection.yaml`, checked by its `make lint`. it had been sizing the
   preview DeepSeek repo rather than the 0731 release the sweep means.
2. [done] the tables the registry now owns are retired. `SHORT`, `MODELS`,
   `SOURCES`, `NATIVE_LOW_BPW` and analyze-contamination's `ROSTER` all read
   `registry/models.yaml` now: display names and free-text aliases from
   `name.short`/`name.match`, benchmark ids from `ids`, and the
   quantization-aware exemption from `native_low_bpw`.

   the drift this removes was not hypothetical. `SOURCES` and the registry had
   disagreed, and the copy the tables read was the wrong one -- crediting
   inkling-small with the flagship inkling's gbench score and mimo v2.5 with
   mimo v2.5 Pro's swe-rebench score. analyze-contamination's `ROSTER` still
   carried that same MiMo mismapping when it was retired.

   `match-models` keeps a five-entry `DISCUSSED_ONLY` for models the community
   talks about that this registry holds no facts for -- minimax m3, glm-4.5-air,
   glm-5.2, motif 3 and a qwen3.6 finetune. that is a residue, not a copy:
   nothing appears in both.
3. gguf sizes join by repo but nothing enforces a consumer's memory budget with
   them yet; that check belongs to the consumer, and llama-tools has the TODO.
   the viewer answers the same question for a reader rather than for a config.

4. [done] memory bandwidth and compute are hardware settings, and the `tg t/s`
   and `pp t/s` columns estimate generation and prefill from them. decode is
   bandwidth bound and prefill is compute bound, so they read two settings
   rather than one, and each column appears when its setting is chosen. 36 of
   41 text models get an estimate; the rest publish no active parameter count
   or nothing that fits the budget, and get no number rather than a guess.

   the two are arithmetic, not measurement, and the discounts turning a spec
   sheet into what a box does -- 0.65 of peak bandwidth, 0.35 of peak flops --
   are rules of thumb. 256gb/s of strix halo through the first arrives at the
   fixed 160gb/s `research/build-tables --table speed` uses.

   generation is reported twice where it matters: decode re-reads the whole kv
   cache every step, so the column leads with the empty-cache figure everyone
   quotes and prints the full-cache one beside it past a 15% gap. ling 3.0
   flash is why -- 42 full-attention layers at 32 kv heads is 84 gib of cache
   at 128k against 5 gib of active weights, so it runs at 89 t/s empty and 1.8
   full.
5. card claims cover 22 of 41 text models; gpt-oss, laguna, inkling, step and
   minimax m2.7 publish no parseable benchmark table.
6. one small proxy benchmark per evidence category, cheap enough to sweep in
   quantbench, so each category earns its own curve instead of borrowing the
   code one or getting nothing. `QUANT_EVIDENCE` in `scripts/build-viewer`
   already names the categories and what each is; what it does not have is a
   benchmark per category that runs in minutes rather than days.

   this is the only way out of the current position. there is one curve, from
   one sweep of one 671b model on one code benchmark, and everything else is
   either extrapolated from it or honestly left alone -- 36 facets discounted,
   57 not. a sweep per category turns that into a measurement, and it is a
   sweep this repo can run rather than one it has to wait for somebody to
   publish.

   the curve is also fitted on a 671b model and applied to 27b ones. damage
   scales with how little redundancy a model has, so the low rungs read
   optimistic for small models, and both published sweeps held here are large
   too (127b and 250b). sweeping ONE small model at several quants would settle
   it for less compute than any of the above.
