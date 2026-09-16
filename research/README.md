# research

source data behind [MODELS.md](../MODELS.md), plus the scripts that collect it.

the data is committed so the comparison can be audited and re-derived without
refetching, and so a later refresh shows up as a reviewable diff rather than a
silent change in conclusions. everything here is a point-in-time capture; the
date is in each file's provenance below.

## data

| file | captured | source |
|---|---|---|
| `data/artificial-analysis.json` | 2026-08-17 | artificialanalysis.ai leaderboard |
| `data/artificial-analysis-speech.json` | 2026-09-04 | artificialanalysis.ai speech-to-text (non-streaming and streaming) and text-to-speech |
| `data/artificial-analysis-image.json` | 2026-09-04 | artificialanalysis.ai text-to-image arena, one elo per model |
| `data/tts-arena.json` | 2026-09-04 | tts-agi TTS Arena v2, crowd-sourced blind-vote elo |
| `data/voicearena.json` | 2026-09-04 | voicearena.com speech-to-text, WER sliced by language and noise |
| `data/gguf-voices.json` | 2026-09-04 | the speaker names each TTS gguf ships, read from its own header |
| `data/sdcpp-support.json` | 2026-09-04 | stable-diffusion.cpp's tensor-name detector, and which registry image models it fires on |
| `data/crispasr.json` | 2026-09-04 | crispasr's own catalog: 83 backends with the repos each was published against, plus the capability bits it generates from `--list-backends-json` |
| `data/gbench.json` | 2026-08-17 | gertlabs.com/rankings |
| `data/gguf-sizes.json` | 2026-08-17 | huggingface hub tree api |
| `data/gguf-tensors.json` | 2026-09-09 | the ggml type of every tensor in each published rung, read from its own tensor table: 1805 rungs over 177 repos |
| `data/gbench-compare-observed.json` | 2026-08-10 | gertlabs compare view |
| `data/reddit-localllama.json` | 2026-08-17 | r/LocalLLaMA, via the reddit api: one search per registry model plus four themes |
| `data/sentiment.json` | derived | analyze-task-mentions --json |
| `data/hackernews.json` | 2026-09-04 | hn.algolia.com: one query per registry model plus nine themes, stories deduped across queries |
| `data/lmarena.json` | 2026-08-17 | lmarena.ai/leaderboard |
| `data/swe-rebench.json` | 2026-08-17 | swe-rebench.com |
| `data/tbench.json` | 2026-08-17 | hf datasets, harborframework/terminal-bench-2-leaderboard |
| `data/epoch.json` | 2026-08-17 | epoch.ai benchmarking hub (csv bundle) |
| `data/model-facts.json` | 2026-08-17 | derived: hf config.json, safetensors index, chat template |
| `data/chat-templates/` | 2026-08-17 | the chat templates themselves, verbatim, base repo and gguf header |
| `data/chat-templates.json` | 2026-08-17 | the index over them: source, size, hash, base/gguf pairing |
| `data/template-probes.json` | derived | analyze-chat-templates --json |
| `data/model-cards.json` | 2026-08-17 | huggingface model cards: benchmark tables (self-reported), opening prose, hub metadata |
| `data/usecase.json` | derived | analyze-usecase: every facet per model, with a ref each |
| `usecase-assessed.json` | written | the judgement analyze-usecase carries into it |
| `data/hf-discussions.json` | 2026-09-07 | huggingface per-repo discussion tabs, for every repo the registry names -- base, quants and components -- with each box naming the model it belongs to |
| `data/github-issues.json` | 2026-08-17 | api.github.com, ggml-org/llama.cpp: hardware terms plus one query per registry model |
| `data/sentiment-llm.json` and `data/proposals.json` are written by `make llm`; see CONTRIBUTING.md. six collectors write through `capture.py`, which refuses to replace a capture with a smaller one -- `fetch-reddit --refresh` against the dead scrape would otherwise have emptied a corpus nothing here can rebuild. |
| `data/proposals.json` | derived | a model's triage of the discovery backlog. PROPOSALS, not facts: nothing downstream reads it |
| `data/sentiment-llm.json` | derived | a second reading of the captured quotes, toward one named model at a time. nothing downstream reads it either |
| `data/llama-support.json` | derived | which llama.cpp release carries each architecture, from a local clone's history plus the gguf headers the hub parses |
| `data/level1techs.json` | 2026-08-17 | forum.level1techs.com discourse api: box terms plus one query per registry model |
| `data/hf-catalog.json` | 2026-08-17 | huggingface hub model listing (trending) |
| `data/hf-catalog-new.json` | 2026-08-17 | huggingface hub model listing (newest) |

`artificial-analysis.json` is keyed by model slug. it carries 650 models, 368
of them open weights, trimmed to the fields MODELS.md cites and assembled from
two pages -- the leaderboard row and a model page, which carry different halves
of one record. scores are third party and run on one harness across every
model, which is why MODELS.md prefers them to self-reported model card numbers.

## the speech sources

three sources score the speech half of the roster, and they measure three
different things. none of them is a version of the text leaderboard with audio
in it, which is why they are kept apart rather than folded into one number.

`artificial-analysis-speech.json` has one section per board:

- **`speech-to-text`** (non-streaming) is keyed by `aaWerIndex`, a WORD ERROR
  RATE. **lower is better** -- the only headline number in this repo that is not
  a score to maximise. the component WERs (`aaSttDatasetWer`,
  `earnings22CleanedWer`, `voxpopuliCleanedWer`) are kept beside it because the
  index is their roll-up and a model can be strong on read speech and weak on
  earnings calls.
- **`speech-to-text-streaming`** re-measures the same models live, where the
  number that decides an interactive use is not the WER but
  `timeToFinalTranscriptSeconds` -- how long after speech ends a final
  transcript exists. a model can be on both boards with different numbers, and
  the registry gives them separate ids for that reason.
- **`text-to-speech`** is `qualityElo`, a human-preference arena rating, so
  **higher is better** and its units are comparable with neither WER index.

`tts-arena.json` is the second opinion on synthesis and the one artificial
analysis cannot give: crowd-sourced blind A/B votes, published with the VOTE
COUNT and the uncertainty band. an elo of 1393 at +-49 over 210 votes is not the
same claim as 1482 at +-18 over 1806, and a board that prints only the rating
hides which it is.

`voicearena.json` is the one source that does not collapse transcription to a
single number. it scores every model on the same corpus sliced by language, by
how noisy the recording is, by the speaker's age range and gender, and by
utterance length. the slices disagree loudly: qwen3-asr leads US english at 4.70
and is the worst open model in romanian at 29.03, where omniasr leads at 11.60.
artificial analysis, measuring on english corpora, cannot say that. only the
fully aggregated demographic slices are kept, and they are READ rather than
averaged -- voice arena publishes an explicit `All` level in each dimension, so
computing our own mean over 27730 rows would invent a number the site does not
publish and nothing could check it against.

the site is a client-rendered SPA over supabase, so `fetch-voicearena` reads the
project url and its public browser token out of the app bundle at fetch time
rather than carrying a pinned copy: the bundle filename is content-hashed and
changes on every deploy, so a pinned key would go stale silently.

**every speech key space is filtered to open weights**, and that filter is
load-bearing rather than tidy. these boards are dominated by hosted endpoints,
and a vendor's API SKU shares a family name with the checkpoint it grew from
while being neither the same weights nor the same stack. artificial analysis
scores `qwen3-tts-vc-realtime` at 925 elo on alibaba cloud; this registry
carries gguf conversions of the open Qwen3-TTS at a different codec rate. those
names match on every fuzzy test there is, so the guard cannot be a matching
rule -- a row the source itself marks closed-weights is never offered to the
matcher at all. `tests/collectors` holds the case.

the open-weights Qwen3-TTS is therefore **unscored**: it is on none of these
three boards, nor on TTSDS2, whose published results are a 2024-era field. that
is a gap in the sources, not a number waiting to be joined.

**the two error rates are stored inverted.** every facet on the dashboard is
higher-is-better, because the percentile pass has no notion of direction: it
ranks a cohort by value and calls the top of it best. a WER stored verbatim
would rank the worst transcriber first and would do it silently, since 4% and 8%
are both plausible-looking numbers in a column. so `aaWerIndex` is carried as
`(1 - wer) * 100` under the label `transcription accuracy` and voice arena's
`corpusErrorPct` as `100 - pct` per language, each with the arithmetic in its
`ref.note`. an elo needs no such treatment and gets none.

## the image source

`artificial-analysis-image.json` is the same site's text-to-image arena, and the
only board here that scores generation. one elo per model, with the confidence
interval and the appearance count beside it -- a model with 700 votes and one
with 15,000 are not comparable at one decimal place.

its payload ships **twenty rows per model**: the overall board plus nineteen
prompt categories, identically shaped, all marked `isCurrent`, each computed
over its own slice of the votes and each landing two hundred elo below the
headline. keying by name alone would keep whichever arrived last, so the
collector keeps the row with the most `appearances` -- on z-image turbo that is
7377 against 655 to 880 per category, and the elo it carries is the one the
rendered table shows. `tests/collectors` brackets a real row between two
category rows, so taking the first or the last fails.

the open-weights filter applies here too, through the board's own
`openWeightsUrl`: it is both the openness flag and the most precise name any of
these boards publishes, a repo path. krea 2 is on the board and is not matched,
because artificial analysis reports no weights for it.

**lmarena rates pictures too, and had been captured all along.** `fetch-lmarena`
keeps every board it finds, media ones included, so
`text_to_image-overall-raw` -- 76 entries over 6.1m votes -- has been in
`lmarena.json` since that collector was written and nothing read it. it is a
second opinion rather than a confirmation: artificial analysis puts z-image
above krea 2 and this board puts it below, so both are carried and neither is
averaged into the other.

joining it needed the licence allowlist fixed. lmarena publishes a licence
string and no open-weights flag, and the image half is where "is this
downloadable" and "is this a free licence" come apart: krea 2 ships under a
community licence and ideogram 4 under one called `Ideogram Open Model`,
neither of which is free and both of which have public ggufs this registry
pins. reading them as closed hid two models the board scores.

`gguf-voices.json` is one of two captures read out of gguf BYTES rather than off
an api. a synthesis model that ships speakers names them in its own header --
`qwen3tts.spk_names`, `kokoro.voices` -- and huggingface's api serves a parse of
that header carrying three fields, none of them this one. so the collector does
a ranged GET and walks the KV table itself, widening the read from 1mb only for
the talkers that inline a 150k-token vocabulary.

it is keyed by `repo:quant`, not by model, because the voices belong to the
FILE: the khimaros qwen3-tts conversions carry no `spk_names` at all where
cstr's carry nine, so the same checkpoint answers differently depending on
which rung is served. kokoro ships fifty.

worth knowing what this is NOT: crispasr's `GET /v1/voices` enumerates the
`*.wav` and `*.gguf` stems in `--voice-dir`, which is the voice-CLONING
registry. it can never list the speakers baked into a model, and this can never
list a cloned one. neither is a substitute for the other, and llama-tools
carries this list as `/v1/models` metadata for that reason.

`gguf-tensors.json` is the other, and it borrows the voices reader's parser to
step over the same KV table and reach the tensor infos behind it. a quant's NAME
is a label its publisher chose: `Qwen3.8-27B-UD-Q4_K_XL` is nine ggml types with
Q5_K over 42% of the weights, while a `Q4_K_M` on a same-size model is a plain
Q4_K/Q6_K split, and both land near 5.2 bits per weight by different routes. the
tensor table says which, and gives bits per weight off the block geometry rather
than as file size over parameter count -- the derived one counts the f32 norms
and the embedding and output tensors as if they were quantized body.

it is keyed `repo:tag` on the same tags `files_by_tag` produces, so a rung is
the same thing to both collectors, and both resolve the same roster: repos.txt
unioned with every repo the registry's `quants:` and `components:` name. reading
repos.txt alone left 30 registry-only repos unread, which on the page is a
ladder drawn with sizes and no layer mix at all -- the columns are dropped
rather than blanked, so nothing said the data was missing.

the cost is the tokenizer vocabulary, which sits in FRONT of the tensor table
and has to be transferred to reach it: 62-327 KiB for a speech model, 7.7-10.7
MiB for a text model with a large vocab, and a 64 MiB widening for the few whose
header exceeds that. it goes through `httpcache --immutable` rather than a
`--max-age` window, because a file at a given revision is the same bytes forever
and a conditional request each is a cost with no possible answer but "no". a
rung already in the capture is then skipped without any request, which makes the
http bodies disposable -- `rm research/.cache/gtensors-*` costs a re-download
only of whatever is asked for again.

whisper.cpp is the one repo this reads nothing from. it publishes 33 ggml `.bin`
weights and not a single gguf; the sizer counts them on purpose, since a
`.gguf`-only filter dropped the repo outright, but ggml is a different container
with no GGUF tensor table in it, so a rung with no gguf in it is skipped rather
than fetched and reported unreadable.

`gbench.json` holds the gert labs GBENCH rankings, which score models by having
them play complex games against each other. worth carrying alongside artificial
analysis because the task distribution is generated rather than curated: there
is no public problem set to train against, and outcomes are decided by play
rather than by a grader. it has three parts:

- `rankings` -- the open-weights leaderboard per mode (combined, agentic coding)
- per-mode sub-objects (`agentic_coding`, `oneshot_coding`, `decision_making`)
  with gscore, confidence interval, failure breakdown and match counts
- `by_language` -- per-language success rates rolled up from per-game results,
  for all 11 languages rather than the 8 the site's compare view shows

`gbench-compare-observed.json` holds the site's own published per-language
compare values, which are not reproducible from the API; see its `_provenance`.

the full per-language breakdown is kept rather than just the languages MODELS.md
discusses, so a later question about c++ or python needs no refetch.

`lmarena.json` holds all 11 arena boards keyed by board id, plus a model index
with organization and license. it is the only source here scoring models by
human preference rather than by a grader, which is why it is carried -- and it
carried at only 0.10, because nine of the twenty roster models are not on the
board at all. board ids say whether the ratings are style-controlled
(`-style_control`) or raw. vote counts are kept per entry and matter: across
the boards they run from 227 to 11.1 million, and on the text board alone from
897 to 124,894, so two adjacent ratings are not equally well established.

`swe-rebench.json` holds resolved rates per model per *task-date window*, which
is what makes it worth carrying separately from AA's scicode. because
swe-rebench rebuilds its task set from pull requests merged after the fact, a
model can be scored on tasks that postdate its own release --
`analyze-contamination` does that comparison. zero-sample windows are dropped
(69% of the published grid), leaving 12,440 real ones across 116 models and
five languages.

`tbench.json` is the only source here that goes below the benchmark. every other
file scores a model with one number per suite; this one carries which of
terminal-bench 2.0's 90 tasks each submission passed, 14,340 trials over 73
submissions. the leaderboard's own page has only the aggregate, but the
submissions behind it are a public huggingface dataset, and each run's
`result.json` lists the passes and failures by task name. that dataset is 121gib
of trajectories and verifier logs, so `fetch-tbench` pulls only the job-level
result files, ~7kb each.

a row there is a submission -- an agent crossed with a model -- rather than a
model, because the same model is on the board several times under different
harnesses and the harness moves the score. both keys are kept so an analysis can
pool or separate them.

`epoch.json` is the epoch.ai benchmarking hub, and it is two sources in one
file. `eci` is the Epoch Capabilities Index: a latent-ability score fitted
across benchmarks rather than a benchmark itself, so models that ran different
suites still land on one scale. `eci_fit` carries the per-benchmark
difficulties and slopes behind that fit, because a fitted index is not quotable
without it. `benchmarks` holds ~75 per-benchmark result files, each tagged
`epoch` or `external`: the first are Epoch's own runs on its own harness
(chess puzzles, mystery games, FrontierMath, GPQA diamond, SWE-bench verified),
the second are leaderboards it mirrors (terminal-bench, DeepSWE, aider polyglot,
METR time horizons). The internal runs are the reason to carry it -- like
GBENCH they are somebody else measuring, which is what a model card is not.

epoch was written off in an earlier survey as client-rendered with no payload.
that was true of the dashboard and false of the site: `/benchmarks/use-this-data`
links a CC-BY zip of the whole hub, updated daily, which plain curl fetches.

the last four files answer a different question from everything above them:
not "how good is this model" but "does it run, and what else exists".

`hf-discussions.json` is the only source here where a failure is attached to a
specific quant of a specific repo -- reddit argues about models, the discussion
tab on `unsloth/Laguna-S-2.1-GGUF` says UD-Q5_K_L emits no tokens under rocm on
strix halo. keyed by the same repos.txt the sizes come from, so the two line
up. the listing has no bodies, so the most-discussed dozen per repo are fetched
in full.

`github-issues.json` covers llama.cpp, where backend bugs get diagnosed. the
search api returns full issue bodies inline, so there is no per-issue follow-up.
queries overlap heavily and the per-query cap is 30, so the printed "30 of 1290"
is a real truncation, not a total.

`level1techs.json` is a second community sample that skews toward people who
own the hardware. discourse `search.json` gives topics, `t/<id>.json` gives
every post, and search blurbs are truncated so the topics are fetched whole.

`sentiment.json` counts model mentions across all four community corpora, and
keeps them APART. the forums do not measure the same thing: reddit argues about
which model is best, the huggingface discussion tab reports whether a specific
quant loads at all, level1techs publishes no post bodies so only its titles can
be matched, and hacker news carries no per-comment score. muse glimmer reads
73% approval on reddit and 0% on the discussion tab, and pooling those would
average away the only useful thing either of them said.

each `by_source` block carries mentions, distinct threads, the positive and
negative sentence counts, approval, the score percentile within thread and
depth, the model/task co-occurrence counts, and up to eight quoted references
with a url. a quote has to read as prose to be kept -- five words, no path, no
command line -- because a huggingface thread is half shell transcript and eight
lines of one person's `--n-gpu-layers` is not a consensus. one thread can
supply at most two of them.

the TOP-LEVEL fields stay reddit-only and byte-identical to what they were.
the composite weights sentiment on a redundancy analysis measured against
reddit alone, so widening the aggregate would have silently re-ranked
MODELS.md; the other three forums are additive.

`usecase.json` is the rollup a consumer reads instead of redoing these joins:
850 facets over the 54 models, each one a (source, benchmark) value with the
model's percentile among the registry models carrying the same facet, a cohort
size, and a `ref` naming the source, the file and a url. the gbench
per-language rates are here too, which is the only source in the corpus that
says a model is better at rust than at clojure. the joins themselves are
imported from `build-tables` rather than restated -- two definitions of "this
model's gbench score" is exactly the drift this repo exists to remove.

it does not blend them. weighing coding against community approval is the
reader's call, so the components stay separable and the viewer applies weights
at read time. `usecase-assessed.json` holds the written judgement and is
SOURCE: `analyze-usecase --missing` lists models without one, a recompute
cannot lose it, and it stays machine-readable so a generated MODELS.md can read
the prose rather than parse a document.

`hf-catalog.json` is the only collector that can discover anything: every other
one looks up models already on the roster. it carries the trending GGUF listing
plus every GGUF repo from the publishers in publishers.txt, which is how the
`-MTP-GGUF` repos got noticed -- they are separate repos with identically-named
files 0.42gib larger, and the roster had been sizing the wrong one.

`data/chat-templates/` holds the templates themselves, one `.jinja` per repo,
byte for byte. Everything else here is a summary of a source; this is the
source, so a later question is asked of the file rather than of the network.
It carries both sides, because they are not the same file: the base repo's
`chat_template.jinja` and huggingface's parse of the gguf header, which is what
llama.cpp actually loads. 41 of 48 gguf repos ship a template that differs from
its base repo's, and the differences are not cosmetic -- unsloth patches a
`{#- Unsloth fixes - developer role, tool calling #}` block into the qwen
family that upstream has no trace of.

`template-probes.json` is what those templates say when you RUN them.
`analyze-chat-templates` renders each one against 18 fixed conversations, every
message carrying a unique marker, and reads the outcome off the result: the
template raised, or it rendered and the marker is there, or it rendered and the
marker is gone. That last case is the one worth having a corpus for -- 9 of the
41 unsloth gguf templates silently drop a developer message, and a consumer
sees a 200 and a model that never saw its instruction.

The same execution answers the thinking vocabulary, which is why
`thinking.accepts` is now derived for 11 models rather than typed off a card.
Setting each candidate level and comparing against a deliberately invalid
control separates three cases a reader cannot: the level raises (the template
enforces a vocabulary), it renders differently from the control (recognised),
or it renders identically (accepted and ignored). Upstage's card documents
`reasoning_effort="none"` for a direct response; the template branches on
`medium|high|xhigh` and does nothing whatever for `none`. Only the verbatim
templates still need a typed list, because they genuinely accept any string.

Levels that render byte-identically are reported as `equivalent`, because two
names for one prompt are not two levels. That is what a widened guard is in
every case here: unsloth's qwen3.8 accepts a `high` upstream rejects, and maps
it onto `xhigh` before the guard, so the model sees three levels either way and
nobody is reaching an untrained setting by asking for it.

The same run answers what the template does when the client sends NOTHING:
render it with the knob absent, and whichever accepted level matches that byte
for byte is the `default`. 17 of the 84 templates answer, and the answer is
rarely the cheap end -- kimi k3 defaults to `max`, qwen3.8-27b to `xhigh`,
gpt-oss to `medium`, hy3 to `no_think`. It is the one thing a verbatim template
does state: gpt-oss interpolates any string at all, so its vocabulary lives
only in openai's docs, but its default is in the file. Where the unset render
matches the control instead, no default is reported -- omitting the knob leaves
thinking off rather than at a level, which is a different fact.

A boolean gate is probed the same way, and that is where most of the roster
lives: 25 of the 41 text models read `enable_thinking` and nothing graded. 19
of them render their thinking prompt when the knob is unset and 6 do not, so
`kind: boolean` carries `default: true` or `default: false` and the question
"what happens if my client says nothing" has an answer for 34 of the 36 models
that have a knob at all.

Three templates read both a gate and a graded knob -- qwen3.8-27b, deepseek v4
flash and kimi k3 -- and the registry records both, because the graded
vocabulary has no `off` in it. Turning thinking off is the gate's job, and a
consumer holding only the graded name would send `reasoning_effort: "off"`
into a guard that raises.

Sampler sets are deduplicated by their values. A card states the same numbers
in prose, again in a code block and again in a table, and that is one
recommendation rather than four; the first label wins because it is the one
with the prose around it.

`model-facts.json` carries an `attn` block per model -- kv heads, head dim, and
the split between layers holding a full cache and layers holding a windowed or
recurrent one -- because that split is what a kv cache costs. Counting every
layer as global overstates gemma 4 31b several times over and kimi k3 by nearly
four, so the full and windowed layers are counted from whatever the config
states and the window is kept beside them. 37 of the 50 models answer; the rest
publish no config this can read.

`gguf-sizes.json` is keyed by repo, then by quant tag, with values in bytes.
these are summed byte totals of the real files, so sharded quants aggregate and
`mmproj:` entries are kept separate. nominal parameter counts are not a
substitute: UD-* quants mix precisions per tensor, and gpt-oss-120b is within
2gib of the same size at every tag because it is natively MXFP4.

## analysis

```
./build-tables                     # the MODELS.md size tables, from the committed json
./build-tables --table speed       # decode estimates, bandwidth over active weights
./build-tables --budget 96         # every table at a different memory budget
./dashboard-table --table ranking  # the ranking, by RUNNING docs/index.html
./dashboard-table --table weights  # the same rows under each of the page's presets
./analyze-task-mentions            # model/task co-occurrence counts from reddit
./analyze-task-mentions --task debugging   # the sentences behind one column
./analyze-task-mentions --sentiment        # reception, by thread-and-depth percentile
./analyze-task-mentions --json data/sentiment.json   # feeds build-tables
./analyze-contamination            # pre- vs post-release scores, vs the cohort
./analyze-contamination --lang rust --markdown
./analyze-operational              # what breaks: model x symptom, all sources
./analyze-operational --strix      # only reports naming this hardware
./analyze-operational --model hy3  # the reports themselves, with state and age
./analyze-operational --strix --open --min-engagement 2   # what survives filtering
./build-tables --table unscored    # models no benchmark suite has measured
./analyze-catalog --candidates     # trending gguf repos the roster does not track
./analyze-catalog --coverage       # which publisher has quantized which model
../scripts/resolve-ids --write         # match registry models to each source's ids
./refresh-tables                   # re-run every generated table in MODELS.md
./refresh-tables --check           # exit 1 if any of them is stale
./analyze-self-report              # card claims vs third-party measurement
./analyze-self-report --cross-card # where two cards disagree about one model
./analyze-correlations             # do the tracked sources disagree at all?
./analyze-correlations --redundancy        # what each source adds over AA
./analyze-correlations --scope aa          # AA internals, where n is large
./analyze-correlations --scope aa --regress 'intelligenceIndex~scicode,terminalbenchV21'
./analyze-tbench                   # which terminal-bench tasks track the other sources
./analyze-tbench --ref 'epoch ECI' # rank by one reference instead of the mean
./analyze-tbench --task fix-git    # the models behind one row
./analyze-tbench --stability       # is that ranking real, or fitted to 25 models?
./analyze-chat-templates           # role support, base repo vs gguf
./analyze-chat-templates --sequences   # all 18 ordering probes, per template
./analyze-chat-templates --thinking    # the level vocabulary each knob takes
./analyze-chat-templates --diverged    # where a gguf disagrees with its base
./analyze-chat-templates --render REPO --probe 'mid dev'   # the prompt itself
./match-models --lexicon           # the shared model alias table
./match-models --sources           # the same models keyed per data source
```

the composite is not here. it lives in `docs/index.html`, opens on the weights
in `scripts/build-viewer`, and reaches MODELS.md through `./dashboard-table`,
which boots the page under node and prints what it shows. this file carried a
second one for a long time -- its own weights, its own normalization, its own
flat memory budget -- and it disagreed with the page about first place inside a
document generated from both.

AA's *intelligence index* is deliberately not a component. regressed over the
161 AA models carrying all three, `II ~ 0.406*coding + 0.413*agentic` with
R^2 = 0.9845, so including it would double-count for 1.5% of new information.
the same check puts most other AA fields at >=0.82 correlation with those two
(terminal-bench 0.99, GDPval 0.99), which is why AA is treated as one axis of
evidence rather than several. only tau2-banking (0.88) and ifbench (0.42) stand
apart.

two more deliberate behaviours: missing components are dropped and the
remaining weights renormalized (reported as the `data` column) rather than
scored as zero, and a GBENCH result under 1000 matches is treated as missing --
hy3 has 24 against deepseek's 46,375. `--weights` exists because a composite
that cannot be poked at should not be trusted; the weighting sensitivity is
tabulated in MODELS.md.

`refresh-tables` exists because adding one model changes six tables and the
ones nobody remembers to regenerate are the ones that go stale. each generated
block in MODELS.md carries the command that produced it in an HTML comment; the
script re-runs those and writes the output back, and `--check` fails if the
document is behind the data.

`analyze-correlations` exists because a composite over four numbers is only
worth building if the numbers disagree. it works on two populations that must
not be mixed: `--scope aa` correlates AA's own fields across the ~600 models it
carries, which is where a coefficient is actually estimable, and `--scope
roster` joins every source on the 18 models MODELS.md tracks, which is the
decision-relevant view and badly underpowered. every cell carries its n and a
Fisher confidence interval for that reason. spearman leads because the
composite only uses these numbers to order models.

joining across sources needs exact ids, and each source invents its own, so
they live in `match-models --sources` next to the free-text lexicon rather than
being re-typed per script. an empty id there means the source does not carry
the model, which is a recorded fact rather than a lookup failure.

`--redundancy` is the summary worth reading: it regresses each source on AA's
coding and agentic indices and reports what is left. GBENCH comes out 4%
unexplained, which is what moved it off the composite's largest weight, and
swe-rebench and lmarena disagree with AA the most, which is why they are in the
composite at all.

`analyze-tbench` asks the same question one level down: not whether the sources
disagree, but whether a suite agrees with itself. it ranks each terminal-bench
task by how well its pass/fail pattern orders models the way AA, epoch, lmarena
and GBENCH do, pooling submissions per model because the reference scores are
per model. the whole suite's accuracy sits at rho +0.72 against AA's
intelligence index (n=25), +0.86 against epoch ECI, +0.74 against GBENCH; the
best single tasks -- `circuit-fibsqrt`, `torch-pipeline-parallelism`,
`large-scale-text-editing`, `write-compressor`, `make-mips-interpreter` -- match
that on their own, 11 of them clear a bonferroni-corrected threshold against AA
alone, and 26 of the 89 land within 0.20 of zero, most of them because 21 tasks
are passed by more than 90% of runs and cannot separate anybody.
`configure-git-webserver` is inverted at -0.37: gpt-5.2 and claude opus 4.6 fail
it where qwen3.5-9b and gpt-5-nano pass.

`--stability` is the part worth running before quoting any of that. all five
references that resolve agree with each other about the ranking (rho +0.76 to
+0.90 over the 89-task vectors), so the pattern is a property of the tasks
rather than of one leaderboard. a sixth is asked for and does not resolve:
scicode reaches too few of these 25 models to index, which is the same coverage
problem that decides which AA evals the composite weights. but the models are
the sample here, and there are 25 of them: a split-half over models reproduces
the ranking at only +0.48, and 89 tasks tested at once need |rho| >= 0.63 for a
bonferroni-corrected p<0.05. what does survive out of sample is the set rather
than the order -- a top-5 chosen on half the models scores +0.78 on the other
half against the full suite's +0.74, and a top-20 scores +0.72. a quarter of
terminal-bench carries what all of it says.

`analyze-operational` carries each report's state, age and engagement, because
a bug report is not a fact about the present: of the 98 strix-halo documents,
26 are already closed, 46 are over 30 days old and 13 have no engagement beyond
the author. one issue in this capture was opened and closed the same day and
still reads as a live constraint from its title alone. `--open
--min-engagement 2` is the filter that makes the corpus quotable.

`analyze-task-mentions` exists because two quotes are an anecdote. it counts how
often each model is named in the same *sentence* as each task across every
captured comment, so the task-fit section has a denominator. sentence scope
rather than comment scope is deliberate: a comment listing five models and five
tasks would otherwise invent twenty-five pairings nobody made. that makes the
counts conservative -- read a cell as "at least this many people said it".

`--sentiment` adds how well those mentions were *received*, which needs care.
reddit publishes a net score only (no up/down split, and it is fuzzed), and raw
score is dominated by which thread a comment is in: here the top comment scores
1943 in one thread and 10 in another, and the 10 is the monthly "Best Local
LLMs" thread. reply depth matters as much -- laguna's lowest-scoring mentions
turned out to be ordinary endorsements buried three levels deep, not
disagreement. so scores are ranked as percentiles within (thread, depth), and
`--quotes MODEL` prints the best and worst received mentions so any claim can
be eyeballed before it is believed. the rare negative score (223 of 13,534) is
the cleanest signal in the set.

## refreshing

```
cd research
./fetch-artificial-analysis
./fetch-gguf-sizes                 # registry quants and components, unioned with repos.txt
./fetch-gguf-tensors               # the same roster, read again for its types
./fetch-hackernews
./fetch-gbench
./fetch-lmarena
./fetch-swerebench
./fetch-tbench                     # per-task rewards, ~250 small files behind an etag
./fetch-epoch                      # one cc-by zip; etag revalidates to 304
./fetch-model-facts                # derived: arch, params, ctx, mtp, thinking knob
./fetch-chat-templates             # the templates themselves, base repo and gguf header
./fetch-model-cards                # what models claim about themselves
./fetch-hf-discussions             # repos.txt again, so it lines up with the sizes
./fetch-github-issues              # ~7s/query: unauthenticated search is 10/min
./fetch-level1techs
./fetch-hf-catalog                 # publishers.txt; discovery, not lookup
./fetch-hf-catalog --sort createdAt --out data/hf-catalog-new.json
./fetch-hf-catalog --tracked       # what it counts as already carried, and why a repo is absent
./fetch-reddit --harvest 10 --comments 120 --front 14
```

everything needs only curl and python3. no browser, no api keys. the one
exception is `analyze-chat-templates`, which needs jinja2, because a jinja
template cannot be executed by reimplementing jinja. `fetch-chat-templates`
reuses the cache keys `fetch-model-facts` already writes, so whichever of the
two runs second transfers nothing.

reddit is worth a note, because what worked stopped working. `www.reddit.com`
returns an SPA shell and its `.json` endpoints 403 regardless of user agent;
**old.reddit served fully rendered HTML to plain curl** for a long time, and
does not any more -- a logged-out request 302s to `/login/?reason=lor2`, and
since redirects are followed every url comes back 200 with ~321kb of `Welcome
to Reddit`. a 200 is why that read as a quiet day on the subreddit for a whole
sweep rather than as a dead collector.

so `fetch-reddit` reads the **api** when `AIMBOT_REDDIT_CLIENT_ID` and
`AIMBOT_REDDIT_SECRET` are set (a `script` app from
https://www.reddit.com/prefs/apps; see `.env.example`). the token is app-only --
`client_credentials`, acting as no user -- because nothing here reads anything a
logged-out visitor could not. with them unset it still scrapes, and says which
of the two `0 parsed` means: a parser reading nothing out of a real page is a
markup change to chase, a parser handed a login page is not.

an earlier version drove a real chrome under xvfb on the assumption that the
json 403 applied site-wide. that was both unnecessary and worse: partway through
a long run reddit began failing those page loads with
`ERR_HTTP_RESPONSE_CODE_FAILURE`, which looks like throttling aimed at the
automated client. curl was steady while the html lasted.

`--front N` adds the other half of the sub: the hot, new and top-week listings.
search only ever returns what `QUERIES` already asks about and lags by hours, so
a release nobody wrote a query for is otherwise invisible -- the listings caught
muse glimmer's second day and the qwen3.8-27b announcement. listing entries
carry score, comment count and post time as `data-*` attributes, so those come
out exact rather than scraped from "42 points". the N most-discussed posts not
already captured get their comments pulled.

the model names searched for are DERIVED, not typed: `roster.model_queries`
reads `registry/models.yaml` and yields one query per model from its
`name.short`, every kind of it. the four collectors that search a forum --
reddit, hacker news, level1techs and github issues -- all read that one list,
because four hand-kept ones drift and the drift is invisible. it had: 13 model
names against 63 text models, so 51 of them had nobody asking, deepseek v4.1
flash among them the week it landed. a model was still SCORED when it came up
in somebody else's thread, since sentiment matches `name.match` over everything
captured -- what was lost is the threads actually about it.

what stays hand-written beside them is the questions no model name covers: the
box, the practice, the size class. edit `QUERIES` for those, and `THREADS` for
the ids MODELS.md quotes; `TASK_QUERIES` drives `--harvest`.

the cost is real. 170 model queries land on top of each collector's topical
list, so a cold sweep makes ~174 reddit searches, ~179 on hacker news and
level1techs, and ~190 against the github search api at its 10-a-minute
unauthenticated limit -- twenty minutes for that stage alone. every one is
cached for `--max-age`, so the second run in a window pays for none of it.

`fetch-gbench` needs no browser: the site is client rendered, but it feeds from
a public JSON API that carries every model's per-language breakdown at once.

artificial analysis, lmarena and swe-rebench are all next.js apps with no
public api, shipping their data inline as an RSC flight payload. `rsc-extract`
is the shared filter for that: give it a url and a literal `--match`, and it
emits the JSON object enclosing each occurrence, one per line. the three
collectors differ only in what they match and how they shape the result.

## caching

nothing refetches what it already has.

`httpcache` wraps curl with an etag / last-modified cache in `research/.cache`
(gitignored) and every collector reaches it, directly or through `rsc-extract`.
huggingface and epoch send etags, so repeated `fetch-gguf-sizes` and
`fetch-epoch` runs revalidate to `304 not modified` and transfer nothing.
artificial analysis, gert labs, lmarena, swe-rebench and hn algolia send none,
so those use a time-based `--max-age` instead. `--path` prints the
cached file's path rather than its body, which is what makes a zip readable:
stdout is decoded as text with errors replaced, so binary survives the cache
but not the pipe. if a fetch fails and a cached copy
exists, the cached body is served and the failure goes to stderr, so a collector
degrades to stale data rather than writing a truncated file.

an etag makes a revalidation free in bytes but not in round trips, and the
hub-facing collectors make ~1900 of them a sweep: one `curl` per url, serially,
0.32s each of which 0.22s is dns and tls. so `--max-age` is what actually keeps
a re-run off the network, and it is set from how fast the data behind it moves
rather than uniformly:

| collector | window | why |
| --- | --- | --- |
| `fetch-model-facts`, `fetch-chat-templates` | 48h | config and template files, which move when a repo is re-uploaded. the two share cache keys, so the windows must agree |
| `fetch-model-cards`, `fetch-quant-sweeps` | 48h | cards, edited in the days after release and then still. also shared keys |
| `fetch-gguf-sizes` | 48h | a quantizer adds rungs early, then stops |
| `fetch-gguf-tensors` | 48h listings, immutable contents | the tree listing gains rungs; the bytes of a file at a revision never change, so its header is cached by url and only `--refresh` goes back |
| `fetch-llama-support` | 48h | reads the same gguf headers as chat templates, under the same keys, so it transfers nothing after that one. the git history it joins them against is local |
| `fetch-tbench` | 6h listings, 30d contents | a listing gains submissions and re-runs; the files inside a published job never change, and there are five of them per listing |
| `fetch-tts-arena`, `fetch-voicearena` | 24h | an arena moves only as fast as people vote, and a rating built on 600 votes does not turn over in an afternoon |

48h rather than 24 because the point is a sweep run the next day, and anything
shorter than the gap between two of them never saves a request. a model added
since the last sweep has no cached body at all, so it is fetched whatever the
window says. `--refresh` is what to reach for when a card is known to have moved
sooner.

httpcache reports every request on stderr and no collector swallows it, so
`304 not modified` and `cache fresh (Nd old)` scroll past as proof the cache is
working. a silent pause is a collector that is genuinely waiting.

`fetch-reddit` caches at two levels: httpcache for the HTTP fetch, and its own
output file, where any search or thread already captured and younger than
`--max-age` (7 days) is skipped entirely. the listings are the exception and
are always refetched, since finding what is new is the whole point of them. reddit 429s a fast loop -- one
`--refresh` run cost 29 threads before backoff was added -- so httpcache retries
with exponential backoff and `--delay` paces requests.

pass `--refresh` to any collector to ignore all of it.

## caveats

- artificial analysis reports most scores as 0-1 fractions (`terminalbenchV21`,
  `tau2`, `tauBanking`, `scicode`) and `intelligenceIndex` as a 0-100 index.
  MODELS.md scales the fractions to percentages.
- it retired `codingIndex` and `agenticIndex`, which were the two the composite
  leaned on. `fetch-artificial-analysis` no longer asks for them and nothing
  here maps another eval onto their names: scicode and `terminalbenchV21` carry
  the weight instead, chosen on how much of THIS roster they cover.
- the leaderboard row went narrow with them, so the text file is two boards
  merged per model -- `models` for the creator and the decode speed, and
  `model-detail` off a `/models/<slug>` page for the license, the parameter
  counts, the weights url and the per-eval scores.
- `deprecated: true` does not mean bad. it means artificial analysis has
  superseded the entry, usually because the lab shipped a newer model. several
  deprecated entries (minimax m2.7, glm-4.7) are still the best thing that fits
  a given memory budget.
- reddit comment scores are as displayed at capture time and drift.
- a terminal-bench submission is one run or five, so a per-task rate is anything
  from a single trial to twenty-five. `tbench.json` keeps the trial count beside
  every reward for that reason.
- submitters fill in their own metadata and some of it is wrong: the
  `Ante__Gemini-3.1-Pro-Preview` submission names gemini-3-pro-preview inside.
  `fetch-tbench` records what the metadata says rather than what the directory
  is called, so a mislabelled submission pools with the wrong model.
- a template's answer about the developer role is not the SERVER's answer.
  llama.cpp rewrites `developer` to `system` before rendering, for every
  template whose source does not contain `<|channel|>` -- that is, everything
  except gpt-oss (`common/chat.cpp`, `workaround::map_developer_role_to_system`).
  So under llama-server the developer handling unsloth patched in is
  unreachable, and what actually decides the outcome is whatever the template
  does with an extra SYSTEM message.
- probes run under jinja2, which is what transformers uses. llama.cpp has its
  own jinja (`common/jinja/`) and the two need not agree on every edge; where a
  template only renders under a mutable sandbox that is recorded rather than
  reported as broken. llama.cpp probes its own templates the same way, by
  rendering them and watching which values get read (`common/jinja/caps.cpp`).
- `leading_system_max: unlimited` means a fourth leading system message
  survived, not that a hundredth would.
- `analyze-tbench` joins terminal-bench model names to the other sources by
  normalized spelling, averaging AA's reasoning-effort variants when only the
  base name is given. fine-tunes nobody else measures (TermiGen-32B,
  gpt-oss-20b-rl) simply drop out; `--unmatched` lists them.
