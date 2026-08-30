# roadmap

what is done, and what is next. a user-visible feature goes here before it is
built and is marked done when it ships.

## done

- **the registry** (74 models, 61 of them text), keyed by huggingface base repo.
- **named sampling profiles**, with each profile's `source:` derived rather than
  asserted.
- **derived registry blocks**: `turns:` and `thinking:` executed out of the chat
  templates, `ids:` resolved against each source's own key space, `modalities`
  checked against each model's `config.json`.
- **the research corpus**: 20 point-in-time captures, every one committed so a
  refresh is a reviewable diff rather than a silent change in conclusions.
- **the `docs/` dashboard**: 1676 facets over 74 models, every weight a slider,
  the memory budget a setting, every number one hover from its source.
- **one sweep command** (`make sweep`) that collects, derives, builds and
  checks, and ends by printing what only a human can decide.
- **MODELS.md generated from the dashboard.** the ranking, the picks, the
  per-model verdicts, the role index and every size table are generated blocks;
  `make lint` fails if the document is behind the data.
- **the roster derived from the registry.** `build-tables` used to carry its own
  twenty-model literal, so a model added to `registry/models.yaml` never reached
  MODELS.md.
- **a cache window per collector, and a visible one.** every hub-facing
  collector defaulted to 6h, which is shorter than the gap between two daily
  sweeps, so a sweep re-run the next morning paid ~1900 round trips to be told
  nothing had changed; the windows now come from how fast each source moves.
  httpcache's per-request status used to go to `/dev/null` in six collectors,
  which is why a working cache read as a stalled one.
- **`name.match` overlap is checked rather than warned about.** CONTRIBUTING.md
  had said since the ling 3.0 incident that an alias must not claim another
  model, and nothing enforced it, so `\bornith\b` did it again -- 22 of the 26
  ornith sentences in the corpus were about a generation the registry did not
  carry. `make lint` fails on it now, and a text model with no alias at all,
  which sentiment silently scores zero, prints in the sweep's punch list.
- **every text model has an alias.** twelve did not, and a missing one costs
  twice: sentiment scored those models zero, and `analyze-catalog` could not
  tell that a repo was a requant of one, so it read as a model nobody had
  heard of. filling them recovered 188 forum mentions -- 65 for qwen3.5 35b
  a3b, 34 for gpt-oss-20b -- and no existing model lost a single one, which is
  what the new overlap check predicted. the requant label now takes the union
  of the alias and the exact roster names `resolve-ids --names` derives, so it
  no longer depends on an alias existing at all.
- **discovery asks the leaderboards, not just the hub.** `analyze-catalog`
  ranks by lifetime downloads, which a release from last week cannot have, so
  granite 4.2 30b sat at rank 39 of a top-25 report while trending -- scored by
  artificial analysis, with a gguf, four days old. `resolve-ids --unclaimed`
  asks the other question: what do the five leaderboards we already collect
  score that the roster does not carry? the catalog report also prints a
  trending-now table before the download one, and the candidate filter's 20b
  floor is gone from the cross-check, because a third party having scored a
  model answers the question that floor was guessing at.

## next

1. **finish deduplicating MODELS.md against the dashboard.** the headline
   ranking is generated from the page now, but `--table weights`, `--table
   arena`, `--table effective` and `--table speed` still come from
   `research/build-tables`, which computes its own composite over min-max
   normalised raw values rather than the page's percentiles. those four tables
   can therefore disagree with the ranking above them. either port them onto
   `dashboard-table`, or make the page emit them and retire the second
   implementation. the second is better: the point of running the page is that
   there is one implementation, and four tables outside it is four ways back to
   the old problem.

2. **a proxy benchmark per evidence category.** there is one retention curve,
   from one sweep of one 671b model on one code benchmark, and everything else
   is either extrapolated from it or honestly left alone -- 40 facets
   discounted, 60 not. `QUANT_EVIDENCE` in `scripts/build-viewer` already names
   the categories; what it lacks is a benchmark per category that runs in
   minutes rather than days, cheap enough to sweep in quantbench.

   the curve is also fitted on a 671b model and applied to 27b ones. damage
   scales with how little redundancy a model has, so the low rungs read
   optimistic for small models, and every published sweep held here is large
   too: 127b, 180b, 226b and 250b. the 226b is laguna m.1's, 28 points of
   perplexity from the one uploader who quantized it, and it is the richest
   ladder in the document by a factor of three -- which makes the gap sharper,
   not smaller. sweeping ONE small model at several quants would settle it for
   less compute than any of the above.

   two assumptions underneath the curve are also wrong, and thr3e's level1techs
   measurements on qwen3.6-27b are the evidence:
   https://forum.level1techs.com/t/why-your-local-llm-feels-dumber-than-it-is/253917

   - **a quant's damage is not one number.** the curve applies a scalar per
     bpw. thr3e sampled top-1 flips against a bf16 reference across 8k windows
     out to 122k and found disagreement arriving in CLUSTERS that track prompt
     content, not a smooth function of depth -- nvfp4 reached ~50% flips by 88k
     on the same weights that look fine short. a single retention multiplier
     cannot express that, and every facet here is scored at one context.
   - **kv cache quantization is a second axis, costed at zero.** the dashboard
     sizes the cache off each model's attention geometry and charges nothing
     for quantizing it. thr3e held weights and activations fixed and moved only
     the cache: bf16 fine, int8 recovered from tool-call errors, int4 never
     closed the call. a consumer trading kv precision for context is making a
     quality decision this document currently tells them is free.

   neither is directly transferable: that work is all vllm-side (fp8, int8
   w8a16, nvfp4, awq w4a16) and carries no llama.cpp rung, so none of its
   numbers can enter `quant-curves.json`. it bounds what the curve can honestly
   claim rather than filling it in.

3. **a consumer-side memory budget check.** gguf sizes join by repo but nothing
   enforces a consumer's budget with them; that check belongs to the consumer,
   and llama-tools has the TODO. the dashboard answers the same question for a
   reader rather than for a config.

4. **card claims cover 29 of 61 text models.** gpt-oss, laguna, inkling, step
   and minimax m2.7 publish no parseable benchmark table. all three laguna
   sizes and both inklings are in that half, which is why the ornith family --
   which publishes one -- reads as better evidenced than it is.

5. **`resolve-ids --write` cannot create an `ids:` block, only rewrite one.**
   `patch_ids` edits the lines it owns rather than dumping the document, which
   is right, but a model added without an `ids:` block is then matched, counted
   as filled and silently dropped -- qwen3.8 flash next carried AA and lmarena
   matches for a full capture that way, and reached MODELS.md unscored. adding
   the block by hand is the workaround; inserting it after `quants:` when it is
   absent is the fix, and it wants a test that adds a model with no `ids:` and
   asserts the block appears.

6. **`fetch-quant-sweeps` only reads huggingface READMEs**, so a quantizer who
   publishes their ladder anywhere else is invisible to it. unsloth measured
   all ten qwen3.8-flash-next rungs -- mean KLD and top-1 agreement against
   bf16, on files whose sizes match ours to the decimal -- and put it on
   `unsloth.ai/docs` as a chart rather than on the card, so the sweep found
   nothing and the registry carried a stale figure from an older capture
   instead. that curve is hand-written into `quant-curves.json` now. worth
   deciding whether the fetcher should take a per-model source URL, since a
   docs page is a stabler home for this than a card that gets rewritten.

7. **sentiment is a blunt polarity lexicon** read over forum sentences, where
   "x is better than y" scores positive for both. it is weighted at 0.05 for
   that reason, against a redundancy analysis that says it is the most
   independent signal here. a better reader of the same corpus would be worth
   more than another benchmark.
