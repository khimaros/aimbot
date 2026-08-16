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
research/                 the collectors and analysis (see research/README.md)
research/data/            committed point-in-time captures
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

a model may also carry `thinking.accepts`, which is the one thinking fact that
is NOT derivable. a template that validates its levels enumerates them and
`fetch-model-facts` reads them off, whether the guard is a membership test or a
jinja map; one that interpolates the value verbatim states only a default, so
the vendor's documented vocabulary has to be declared with a note saying where
it came from -- gpt-oss `low/medium/high`, hy3 `no_think/low/high`, muse glimmer
`low/medium/high/xhigh` on `reasoning_strength`. `models-validate --thinking`
lists the models still missing one; `--cards` checks the sampling profiles
against the sets the cards document, base repo and quant repo alike.

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

## status

done: the registry (54 models), named sampling profiles, the research corpus,
and llama-tools generating its whole llama-swap config from registry facts plus
a host file that lists only choices.

derived rather than typed: `research/fetch-model-facts` covers all 41 text
models with arch, params, native context, mtp presence, the thinking knob and
the samplers the vendor ships;
`scripts/resolve-ids` filled 97 source ids with zero ambiguous matches;
`research/fetch-model-cards` extracts what models claim about themselves and
`analyze-self-report` measures the discount (median +0.9 over third-party
measurement across 64 matched claims).

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
4. card claims cover 21 of 41 text models; gpt-oss, laguna, inkling, step and
   minimax m2.7 publish no parseable benchmark table.
