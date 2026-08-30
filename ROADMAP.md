# roadmap

what is done, and what is next. a user-visible feature goes here before it is
built and is marked done when it ships.

## done

- **the registry** (65 models, 52 of them text), keyed by huggingface base repo.
- **named sampling profiles**, with each profile's `source:` derived rather than
  asserted.
- **derived registry blocks**: `turns:` and `thinking:` executed out of the chat
  templates, `ids:` resolved against each source's own key space, `modalities`
  checked against each model's `config.json`.
- **the research corpus**: 20 point-in-time captures, every one committed so a
  refresh is a reviewable diff rather than a silent change in conclusions.
- **the `docs/` dashboard**: 1544 facets over 65 models, every weight a slider,
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
   optimistic for small models, and both published sweeps held here are large
   too (127b and 250b). sweeping ONE small model at several quants would settle
   it for less compute than any of the above.

3. **a consumer-side memory budget check.** gguf sizes join by repo but nothing
   enforces a consumer's budget with them; that check belongs to the consumer,
   and llama-tools has the TODO. the dashboard answers the same question for a
   reader rather than for a config.

4. **card claims cover 25 of 51 text models.** gpt-oss, laguna, inkling, step
   and minimax m2.7 publish no parseable benchmark table.

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
