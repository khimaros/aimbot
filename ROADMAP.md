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
- **every model says which llama.cpp release loads it.** the fact was here
  already, as prose in four notes nothing could query, and it is upstream of
  every other number: a model that does not load has no speed, no fit and no
  score worth reading. `runtime:` carries it now for all 61 text models, derived
  by `fetch-llama-support` from llama.cpp's own history rather than typed --
  gguf header to architecture, architecture to the commit that added the string,
  commit to the first `bNNNN` tag containing it. it reproduces the hand-written
  claims exactly where they overlap (qwen4exp b10660, 2026-08-27) and dates
  gemma3 and gpt-oss to their release days.

  four models turned out not to load on a stock build at all: inkling and
  inkling-small (PR 25731), motif-3 (PR 26298) and solar-open2 (issue 26115,
  no PR -- the quantizer ships a 951-line patch in the gguf repo). those four
  need a `fork:`, `patch:` or `tracking:`, which is hand-written and which the
  deriver preserves; lint fails on a model that says `mainline: false` and names
  nowhere to get a build.

  the ladder is marked too. laguna m.1 publishes 28 rungs and 10 are
  ik_llama.cpp's, which the page offered with sizes beside them as if they were
  choices. matching tags against mainline's type names naively flagged 60 of 63
  repos, because `UD-Q4_K_XL` is not an ftype either. reducing the publisher
  prefix and recipe decoration first, then asking about LAYOUT rather than name
  -- `_R4` row-interleaving, `_G64` block size, a type family mainline defines
  nothing in -- leaves 12 rungs over 3 repos and every one is real.
- **a deriver can create a block, not just rewrite one.** `resolve-ids` could
  only replace an `ids:` block that was already there, so a model added without
  one was matched, counted as filled and silently dropped: qwen3.8 flash next
  carried AA and lmarena ids for a full capture that way and reached MODELS.md
  unscored. the splice is `scripts/registry_patch.py` now, shared with
  `resolve-runtime`; it inserts after `quants:` when a block is absent and
  leaves one that already exists where the file put it.
- **a sweep published off the card can be read.** `fetch-quant-sweeps` only
  parsed huggingface READMEs, so unsloth's ten-rung qwen3.8-flash-next ladder --
  on `unsloth.ai/docs` rather than on the card -- had to be typed into
  `quant-curves.json` by hand. a `quant_sweep:` block on the model names the url
  and the column layout, and `rsc-extract`, already here for the three next.js
  leaderboards, does the fetching. the derived curve reproduces the hand-written
  one on all ten rungs, so nothing in that file is hand-written any more.
- **two llm steps, neither of which may decide anything.** `research/propose`
  triages the discovery backlog and `research/score-sentiment` re-reads the
  captured quotes toward one named model at a time. both are off unless three
  environment variables are set, both write a file nothing downstream reads, and
  the registry stays hand-written -- the measurement/judgement split does not
  survive a script that edits the registry from a model's opinion.

  the rule that made them useful is asking only what something here can check.
  `propose` is asked which model a repo derives from, `analyze-catalog` resolves
  the same thing off the name index independently, and disagreement is what gets
  marked. where a list already knows, the model is not asked: `publishers.txt`
  now carries `[quantizer]`, `[vendor]` and `[community]` sections, and a repo
  owned by a quantizer is a re-quant by definition. asking anyway had classified
  `bartowski/Qwen2.5-Coder-32B-Instruct-GGUF` as an original release.

  `score-sentiment` turned item 6 below from an argument into a measurement: on
  the 40 comparative sentences in the committed corpus, the lexicon and a
  4b-active local model agree 48% of the time, and reading the disagreements the
  lexicon is wrong in almost all of them -- "better than GLM5.2 at a small
  fraction of the size is extremely impressive" was scored as praise FOR glm 5.2.

- **the dashboard filters by modality rather than by two toggles.** `text` and
  `vision` were chips, and chips compose wrongly for this: holding both meant
  "a text model that also takes images", and no combination of them meant audio
  in and text out, so the 26 non-text models on the roster were unreachable
  except through search. one dropdown replaces both, over the shapes
  `llama-swap-groups` already derives membership from -- text, vision, audio to
  text, text to audio, to image, to embeddings, and the diarizers.

  `text models` stays the default, which matters more than it looks: MODELS.md's
  ranking blocks are generated by booting the page with nothing set, so the
  default view IS the document's roster. `refresh-tables --check` reports all 15
  blocks current across the change, which is the check that says so.

- **the speech roster has a loader, a diarizer and a third-party score.** it was
  8 models carried as bare facts -- a repo, a quant, a modality pair -- and
  nothing else. they named no engine, so which server to point at kokoro rather
  than whisper was knowledge kept somewhere else entirely; no source scored
  them, so the roster could not be ranked or even checked for staleness; and
  speaker diarization, the one thing a transcript of a meeting actually needs,
  was not expressible at all.

  `crispasr:` names the engine now, for 13 models. crispasr is a whisper.cpp
  fork carrying ggml runtimes for ~60 ASR architectures behind one binary, so
  `backend` is the whole difference between two entries that otherwise run
  identically -- and it is hand-written rather than derived, because no index
  maps an architecture to a backend name the way llama.cpp's history maps one
  to a release. it is asserted only for the gguf repo crispasr's own README
  names: two conversions of one checkpoint are not interchangeable.

  the diarization weights are registry entries rather than flags, under a
  `kind: diarize` of their own -- the foxnose WeSpeaker embedder, the pyannote
  segmenter, titanet. they transcribe nothing, and without a separate kind a
  24mb embedder with no chat template and no transcript sits in the speech
  roster looking like something to serve. lint fails if the kind and the role
  disagree.

  five boards score the rest, over three sources: artificial analysis'
  speech-to-text (`aaWerIndex`, where LOWER is better -- the only headline
  number here that is not a score to maximise), its streaming twin, its
  text-to-speech elo, tts arena v2's crowd-sourced elo with the vote count
  beside it, and voice arena's WER sliced by language, noise, age, gender and
  utterance length.

  **the join's load-bearing rule is that a closed-weights row is never offered
  to the matcher.** these boards are mostly hosted endpoints, and a vendor's API
  SKU shares a family name with the checkpoint it grew from while being neither
  the same weights nor the same stack: artificial analysis scores
  `qwen3-tts-vc-realtime` at 925 elo on alibaba cloud, and this registry carries
  gguf conversions of the open Qwen3-TTS at a different codec rate. those names
  match on every fuzzy test there is, so the guard cannot be a matching rule.
  `tests/collectors` holds the case, and it is red without it.

  the two transcription boards then disagree, which is why both are collected:
  qwen3-asr leads voice arena's US english at 4.698 where cohere transcribe is
  6.159, and cohere leads artificial analysis' batch board at 0.0457 where
  qwen3-asr is not on it. voice arena also says what a single index cannot --
  qwen3-asr is best in US english and the worst open model in romanian at 29.03,
  where omniasr leads at 11.60. `--speech` prints the two remaining gaps: 6
  models naming no engine (all TTS) and 10 no board scores.

- **the speech and image halves are SCORED, not just carried.** the boards were
  collected and the ids resolved, and then nothing read either: `analyze-usecase`
  loaded five sources and none of them was a speech one, so 19 speech models
  reached the page with zero facets and a dash where the score goes. they carry
  facets now, and the two error-rate boards are stored INVERTED -- `(1 - wer) *
  100` as a transcription accuracy, `100 - corpusErrorPct` per language.

  the inversion is the whole design. the percentile pass has no notion of
  direction: it ranks a cohort by value and calls the top of it best, so a word
  error rate stored verbatim ranks the worst transcriber first, silently, since
  4% and 8% both look like plausible numbers in a column. one facet per voice
  arena language rather than an average over them, for the reason the languages
  were collected at all. `tests/collectors` checks each stored value against the
  board it came from, so a second inversion fails as loudly as none.

  image generation joins on the same terms: artificial analysis' text-to-image
  arena is a fifth board on that site, and its payload ships TWENTY rows per
  model -- the overall board plus nineteen prompt categories, identically
  shaped, all marked current, each carrying an elo two hundred points below the
  headline. the collector keeps the row with the most appearances and a test
  pins it.

- **the dashboard filters by RUNTIME, and the ops section spells that runtime's
  command.** it offered every model a choice between `llama-server` and `vllm
  serve`, which is wrong for 28 of 89: a whisper gguf is not a llama.cpp file
  and no vllm serves z-image. `engine:` on the model says what loads it, two
  entries are derived rather than written (llama.cpp from the architecture
  llama.cpp merged, crispasr from the backend the registry already names), and
  lint rejects both a typo and a hand-written copy of a derived one.

  the filter is a multi-select defaulting to llama.cpp, crispasr and
  stable-diffusion.cpp, and the snippet follows the model: `crispasr --backend
  whisper`, `sd --diffusion-model ... --vae ... --llm ...`, `tts-cli
  --model-path`. the roles in the registry turned out to already BE those flags.
  a model nothing here loads prints no command rather than a wrong one.

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

5. **r/LocalLLaMA can no longer be scraped, and sentiment does not know it.**
   old.reddit.com served server-rendered html until it did not: as of the
   2026-09-02 sweep it answers with the new client, 352kb titled `Welcome to
   Reddit` with no `<div class="md">` in it, and the `.json` paths are shut too
   (302 without a user-agent, 403 with one). 135 of 135 thread fetches parsed to
   nothing.

   `fetch-reddit` exits non-zero on a total miss now, and the sweep reports it
   without letting it stop the run, so the breakage is at least loud. the
   capture is also protected: `--refresh` rebuilds the output from nothing, so
   one `scripts/sweep --refresh` would have written 0 searches, 0 listings and 0
   threads over 38, 3 and 147, and six collectors now write through
   `research/capture.py`, which refuses to shrink a capture. what is
   not fixed is the corpus: reddit is one of the four forums behind
   `community.*`, its capture is frozen at whatever the last working sweep got,
   and every model's sentiment score still quietly includes it. the options are
   an authenticated api client, a mirror, or dropping the source and reweighting
   -- and the third is the only one that does not add a credential to a repo
   whose whole point is that a reader can re-run it.

6. **sentiment is a blunt polarity lexicon** read over forum sentences, where
   "x is better than y" scores positive for both. it is weighted at 0.05 for
   that reason, against a redundancy analysis that says it is the most
   independent signal here. a better reader of the same corpus would be worth
   more than another benchmark.

   the fix is not a bigger lexicon, which `analyze-task-mentions` says in a
   comment already: the failure is TARGET ATTRIBUTION, not vocabulary. the task
   with a name is aspect-based sentiment -- score a sentence toward a named
   aspect -- and `match-models` already produces the aspect, because it knows
   which models a sentence mentions and where.

   what the hub has: `yangheng/deberta-v3-base-absa-v1.1` is the one real
   candidate by adoption (184m params, 62k downloads, 74 likes), and it takes
   exactly the `(sentence, aspect)` pair this needs. the problem is the runtime.
   mainline llama.cpp carries `bert`, `modern-bert`, `neo-bert`, `jina-bert-v2`,
   `jina-bert-v3`, `nomic-bert` and `eurobert` and has NO deberta, roberta or
   xlm-r architecture, so that checkpoint cannot be served by the stack this
   repo already runs. its classifier support is real but reaches the server only
   as `/reranking`; there is no `/classify` endpoint. so the choice is:

   - a new python dependency (torch or onnxruntime) for the good checkpoint, in
     a repo whose collectors are stdlib, curl and pyyaml
   - a BERT-family ABSA checkpoint that llama.cpp can load, which by the numbers
     above does not exist at any adoption worth the name
   - ask a generative model already on the roster, over llama-server, which adds
     no dependency at all and is the same lever item 7 wants

   the third is built and the measurement exists: `./score-sentiment --report`.
   the remaining work is the decision it was built to inform -- 48% agreement on
   the comparative sentences is enough to replace the lexicon, but only 40 of
   552 quotes are scored so far, and `analyze-task-mentions` still computes
   `approval` from the lexicon. what is missing is a full pass, a rule for
   turning per-sentence stance into the same `approval` number the dashboard
   already weights, and a decision about whether a score that needs a local
   model to reproduce belongs in a repo whose other numbers do not.

7. **the triage pass covers one punch-list entry of several.** `propose` reads
   the discovery backlog and nothing else. the other entries are the same shape
   and were all done by hand this sweep: find the PR for an architecture
   mainline does not carry, propose a `name.match` for a model with none, draft
   the `usecase-assessed.json` block for an unassessed model.

   the alias case is the one to do next, because it is the best-checked: `make
   lint` already fails a pattern that claims another model, so a generator
   cannot quietly poison the corpus however wrong it is. the judgement case is
   the one to leave longest -- nothing can check it, and a drafted opinion that
   reads like a measured one is exactly what the assessed/measured split exists
   to prevent.

   the backlog is also only sampled: `--limit` defaults to 25 of 236 untriaged
   rows, and a full pass at ~4s a call is half an hour. worth batching several
   repos per request before pushing the limit up.

8. **the open-weights Qwen3-TTS is scored by nobody, and neither is half the
   speech roster.** artificial analysis, tts arena v2 and TTSDS2 all miss it --
   the first two rate alibaba cloud's hosted SKU instead, and TTSDS2's published
   results are a 2024-era field (bark, xttsv2, tortoise). the same holds for
   sensevoice, moss-transcribe-diarize, canary-1b-v2 and parakeet v3, and for
   every diarizer here: there is no third-party DER board at all, so crispasr's
   own 7.3% on voxconverse dev is the only figure this repo has for foxnose, and
   it is quoted rather than collected.

   the honest options are to find a board that rates them or to measure them
   here, and the second is a different kind of repo than this has been, because
   every number in it so far is somebody else's. the diarizers are the tempting
   case -- `tools/der_score.py` and voxconverse dev are both public -- and the
   tempting case is exactly the one to be careful about: a DER this box computed
   would sit in a document whose whole claim is that its numbers are third
   party. the measurement/judgement split has a third column now and nothing
   names it.
