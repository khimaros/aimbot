# MODEL COMPARISON

open weights models for a 128gb strix halo, ranked for overall intelligence,
agentic use and coding. every source captured 2026-08-16.

## the short version

the size ladder mostly does not pay on this box. squeezed into the same ~105gib
weight budget, everything from 124b to 310b converges: on quant-adjusted
intelligence, ranks 2 through 6 span 38.8 to 37.1, a spread well inside the
error of the estimate. two findings come out of that.

- **deepseek v4 flash 0731 escapes the convergence.** it tops every scored component
  and leads the composite at 90.5 against 68.3 for the next model, even after
  the 8 percent it pays at 2.94 bpw. first place under every weighting tried.
  the only case here where cramming a large model in at low precision wins.
- **qwen3.6 27b is much the cheapest, and second or third depending on the
  weighting.** it sits 3rd at 67.6 to minimax m2.7's 68.3 -- 0.7 points, still
  inside the noise floor -- and which of the two leads turns on one number:
  swe-rebench, whose tasks postdate both models, scores minimax 51.8 against its
  34.3. qwen3.6 27b takes second under four of the seven weightings tried. what
  does not move is the value case -- 27.1gib against 103.1, at 3.8x the
  effective intelligence per gigabyte of anything near it. below the top three
  the order is weight-dependent and should not be read as a ranking.

so run both, and let the 97gib and 27gib footprints decide which is resident.
they fit together; two of the ~100gib models do not.

the models that look strongest on raw AA scores are the ones this box can only
run badly. inkling small leads the cluster on effective intelligence and lands 6th once
coverage is counted: four of the seven components do not measure it at all.
hy3 drops from 2nd on paper to 6th on quant-adjusted intelligence because 2.72
bpw costs it 12 percent.

### what to run

1. **deepseek v4 flash 0731 at UD-IQ3_XXS (97.1gib)** as the primary model for
   anything that matters, with the dspark drafter alongside it. the ~10gib
   sidecar fits at this quant: UD-IQ3_XXS was already the step down from
   UD-IQ3_S (108.1gib) taken to make room for it, and the two options cost
   about the same resident memory. deepseek's compressed attention makes its kv
   cache far cheaper than the generic reserve below assumes, which is what
   leaves the headroom.
2. **qwen3.6 27b at Q8_0 (27.1gib) with MTP** as the daily driver. 3rd on the
   composite and 5th on quant-adjusted intelligence, from a quarter the memory
   of anything above it, so it stays resident alongside deepseek rather than
   replacing it. it trails minimax m2.7 by 0.2 points and passes it under four
   of seven weightings; minimax needs 103.1gib either way, which on this box
   makes it deepseek's competitor, not this one's. dense, so it needs the MTP drafter to be usable here: 7.4 t/s
   without, 18.1 t/s with. **take the quant from
   `unsloth/Qwen3.6-27B-MTP-GGUF`, not `unsloth/Qwen3.6-27B-GGUF`.** the two
   repos ship identically-named files, but the MTP head is inside the weights
   rather than in a sidecar, so the plain repo is 0.42gib smaller and cannot
   speculate at all. earlier versions of this document sized the plain repo and
   quoted 26.6gib; the number that matters is 27.1. **its successor is ranked
   here but barely measured**: qwen3.8 27b is the same 27.8b dense shape at the
   same 27.1gib, and only two of the seven components carry it -- its own card
   and reddit. see [what is coming](#what-is-coming).
3. **ling 3.0 flash, somewhere between AD-Q4_K_M (73.9gib) and AD-Q6_K
   (100.1gib)**, if agentic tool use is the priority. it is the one model here
   that fits at a precision where quantization is free -- even the 73.9gib quant
   is 5.12 bpw, against deepseek's 2.94 -- and its tau2-banking of 27.2 is
   second only to deepseek's. 5.1b active makes it the fastest of the ~100gib
   models at 36 t/s, and there is a ROCmFP4-STRIX-MTP build tuned for this
   hardware. two caveats: no unsloth or bartowski quant, and only 9 mentions
   across 161 reddit threads, so almost nobody has stress-tested it.
4. **retire qwen3 coder next.** superseded on every measured axis by
   qwen3.6 27b at a third of the size.
5. **treat gpt-oss-120b as a speed tier, not a capability tier.** it is the
   fastest large model here and near the bottom on capability.

three caveats before the detail:

- **the ties are decided by axes these tables do not measure** -- context
  length, tokens-to-completion, tool-calling reliability. hy3 is the clearest
  case: it ranks sixth here, and the handful of people who have actually run it
  on a 128gb box rate it far higher. that is three voices against a number, so
  weigh it accordingly.
- **harness choice swings terminal-bench results by more than 50 percent** for
  the same model, which is larger than every gap below. test two candidates in
  your own harness before trusting any ranking, including this one.
- **the benchmaxxing finding is anticlimactic.** claimed-vs-measured gaps are
  small (worst -6.6 points). the durable signal is the spread between coding
  scores and hallucination scores, not inflated claims.

## the ranking

a composite of every independent signal available, computed at **the quant that
fits a 105gib weight budget** rather than at full precision.

<!-- generated by research/build-tables --table score -->

| model | score | quant | size (gib) | eff coding | eff agentic | gbench | arena | swe-reb | sentiment | card | data | (eff II) |
|---|--:|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| deepseek v4 flash 0731 | **90.5** | UD-IQ3_XXS | 97.1 | 63.6 | 44.5 | 0.585 | 1435 | 38.5 | 4.7 | 68 | 7/7 | 47.6 |
| minimax m2.7 | **68.3** | UD-IQ4_NL | 103.1 | 50.6 | 24.9 | 0.459 | 1416 | 51.8 | 4.7 | - | 6/7 | 37.4 |
| qwen3.6 27b | **67.6** | Q8_0 | 27.1 | 53.2 | 27.2 | 0.452 | - | 34.3 | 4.9 | 78 | 6/7 | 37.3 |
| hy3 | **61.7** | Q2_K_XL-mtp | 94.6 | 51.7 | 27.6 | - | 1457 | - | 4.1 | - | 4/7 | 37.1 |
| muse glimmer | **57.2** | Q8_0 | 27.6 | 48.5 | 22.7 | - | 1426 | - | 5.2 | - | 4/7 | 34.7 |
| inkling small | **56.9** | UD-IQ3_S | 100.1 | 49.9 | 30.1 | - | - | - | 3.2 | - | 3/7 | 38.8 |
| ling 3.0 flash | **56.4** | AD-Q6_K | 100.1 | 50.1 | 29.0 | - | - | - | 3.3 | - | 3/7 | 37.4 |
| qwen3.8 27b | **55.3** | Q8_0 | 27.1 | - | - | - | - | - | 5.3 | 80 | 2/7 | - |
| mimo v2.5 | **53.8** | UD-Q2_K_XL | 95.9 | 49.2 | 21.2 | 0.400 | 1434 | - | 3.1 | - | 5/7 | 33.0 |
| qwen3.5 122b a10b | **50.5** | UD-Q6_K_XL | 104.7 | 45.2 | 21.0 | - | 1417 | - | 4.3 | 77 | 5/7 | 32.5 |
| solar open2 250b | **50.4** | Q2_K | 88.9 | 41.5 | 25.8 | - | - | - | - | - | 2/7 | 34.8 |
| qwen3.6 35b a3b | **45.5** | Q8_0 | 35.2 | 41.5 | 21.4 | 0.271 | - | 30.1 | 4.0 | 71 | 6/7 | 31.8 |
| step 3.7 flash | **41.6** | UD-IQ4_NL | 90.6 | 38.1 | 20.9 | 0.322 | - | - | 2.5 | - | 4/7 | 29.7 |
| mistral medium 3.5 | **39.6** | UD-Q6_K_XL | 101.7 | 46.4 | 19.0 | 0.298 | 1427 | - | 0.9 | - | 5/7 | 30.0 |
| qwen3 coder next | **39.3** | Q8_0 | 79.0 | 35.9 | 8.8 | - | - | 47.7 | 3.7 | - | 4/7 | 21.1 |
| gemma 4 31b | **36.7** | UD-Q8_K_XL | 32.6 | 43.1 | 14.3 | 0.145 | 1451 | 22.4 | 3.4 | 81 | 7/7 | 29.4 |
| gemma 4 26b a4b | **35.6** | Q8_0 | 25.0 | 38.9 | 10.9 | 0.126 | 1438 | - | 4.1 | 73 | 6/7 | 25.8 |
| nemotron 3.5 lightning | **28.8** | Q8_0 | 32.6 | 26.5 | 13.7 | - | - | - | - | 35 | 3/7 | 23.4 |
| gpt-oss-120b | **19.8** | UD-Q8_K_XL | 60.0 | 30.4 | 13.4 | 0.131 | 1352 | 26.8 | 3.6 | - | 6/7 | 24.1 |
| nemotron 3 super | **16.4** | UD-Q5_K_XL | 100.2 | 37.3 | 8.7 | 0.196 | 1360 | - | 0.9 | 59 | 6/7 | 25.4 |

**read `data` before the score.** it is how many of the seven components were
actually measured; the rest are imputed at the set median. that keeps a model
from being rewarded or punished for going unmeasured, but it also means a
low-coverage row is mostly reporting the middle of the set: qwen3.8 27b's 55.3
rests on two real numbers and five imputed ones, and nothing below 4/7 should be
read as a ranking position. `eff II` is shown for reference and is deliberately
**not** part of the score; see below.

### how the score is built

| component | weight | source | new info over AA |
|---|--:|---|--:|
| effective coding | 0.25 | AA coding index x quant retention | - |
| effective agentic | 0.25 | AA agentic index x quant retention | - |
| GBENCH | 0.15 | gert labs, agentic coding board where played | 8% |
| lmarena | 0.10 | style-controlled arena, human preference | 32% |
| swe-rebench | 0.10 | resolved rate on post-release task windows | 78% |
| sentiment | 0.15 | r/LocalLLaMA mention volume x reception | 85% |
| model card | 0.05 | what the vendor claims, bias-corrected | - |

each component is min-max normalized across this set, then averaged by weight.
**the weights come from the last column**, which is measured rather than
asserted -- see [how independent the sources
are](#how-independent-the-sources-actually-are). GBENCH was on 0.35 until that
check found AA already predicts 94% of it; it keeps a premium over its 6%
because being played rather than graded is a real anti-contamination property,
but it no longer outvotes the sources it agrees with.

**the intelligence index is excluded, and that is the load-bearing decision
here.** regressed across the 159 AA models that carry all three:

```
II ~ 5.60 + 0.411*coding + 0.408*agentic        R^2 = 0.9846
```

coding and agentic explain 98.4% of the intelligence index. including it as a
third component would count the same measurement twice in exchange for 1.5% of
new information. every other AA field lands 0.82 or higher against the index on
the same check -- see [how independent the sources
are](#how-independent-the-sources-actually-are), which regenerates all of this
rather than quoting it.

so **artificial analysis contributes one axis of evidence, not several.** the
other choices:

- **a missing component is imputed, not dropped.** this decides more than the
  weights do. dropping it and renormalizing the rest looks neutral and is not:
  it pushes the missing weight onto whatever the model *does* have, so a model
  measured twice has each measurement counted harder than a model measured six
  times. that is precisely how a partial-coverage source moves ranks on absence,
  and it is measurable here -- under renormalization qwen3.8 27b takes **first
  place outright** on 2/7 coverage, on nothing but its own card and a reddit
  score, ahead of the model measured on all seven; hy3 rises to 3rd on 4/7,
  carried by the highest arena rating in the set. under median imputation they
  sit 8th and 4th. `--missing renormalize` reproduces the old behaviour.
  imputation has its own bias in the other direction, flattering a model whose
  measured components are bad, which is why `data` is in the table and
  low-coverage rows should not be read as ranked.

- **everything is quant-adjusted first.** scoring models at a precision this
  box cannot run them at is the error the rest of this document is about.
- **GBENCH is still weighted above its independent contribution** because it is
  the only measurement here that is played rather than graded: there is no
  public problem set to train against. a gscore is ignored below 1000 matches --
  hy3 has 24 against deepseek's 46,372, so hy3 is imputed there rather than
  scored on noise.
- **lmarena and swe-rebench enter at 0.10 each.** they were excluded for
  coverage, 8 and 13 of the 20 missing, and that has not changed -- what changed
  is knowing they are the two sources that disagree with AA most. a low weight
  plus median imputation bounds how far their gaps can move a rank.
- **sentiment is capped at 0.15.** real-world validation, and also a popularity
  contest with a 5-to-216 sample range. volume is log-scaled and multiplied by
  reception, so widely discussed *and* well received beats either alone.
- **the score is a position within this set, not an absolute.** min-max means
  the leader approaches 100 by construction. deepseek's 90.5 says it tops every
  component, not that it is 34% better than qwen3.6 27b. it also means **a
  component re-scales when the set changes**, with no model's measurement
  moving: an earlier capture extended card coverage from 18 models to 21, which
  alone took deepseek's card column from 95 to 68 and shifted every score that
  depends on it. treat gaps under ~2 points as noise in the membership, not a
  finding about the models.

`research/build-tables --table score` regenerates it, and `--weights` overrides
any component, e.g. `--weights gbench=0.55,sentiment=0.10`.

### what a model says about itself

model cards are the weakest evidence here and are carried anyway, because they
are often the only numbers a new model has: qwen3.8 27b shipped with nine
benchmark claims and nothing else, and scoring it purely on imputation said less
than its own card does. so `card` is a component, at 0.05 -- half the weight of
anything else.

the discount is measured rather than assumed. `research/analyze-self-report`
joins card claims to artificial analysis and epoch on (model, benchmark):

- **67 claims have a third-party match. the median claim runs +1.0 over the
  measurement and 42 of 67 overstate.** the median is used rather than the mean
  (+3.5): a handful of benchmark-variant mismatches -- "HLE" is published both
  with and without tools -- put a long tail on the distribution that is
  measurement noise rather than overstatement. 1.0 is subtracted from every
  claim before it is scored.
- that figure reproduces what the qwen3.8 card shows directly: all three of its
  numbers for a rival lab's model (muse glimmer, on gpqa, HLE and
  terminal-bench) match AA to the decimal, while its five numbers for qwen's own
  qwen3.6 27b run +0.9 to +10.6 above AA. the competitor column was copied and
  the home column was re-run.

a claim is normalized against the other models claiming *the same* benchmark,
so a model cannot gain by choosing easy ground -- only by beating the models
that chose the same ground.

**cards also disagree with each other.** `--cross-card` finds 46 cases where
two cards report the same third model and differ, by up to 25 points, so a
generational delta must come from within one card rather than by differencing
two. the largest are HLE, where "with tools" and "without" are both published as
"HLE".

### how independent the sources actually are

the paragraph above argues that AA is one axis rather than several. the same
question applies to the composite as a whole, and it had never been measured:
if the components agree, the weights are decoration.

`research/analyze-correlations --redundancy` regresses each source on AA's
coding and agentic indices and reports what is left over. read the last column
as "how much of this source AA does not already tell you":

<!-- generated by research/analyze-correlations --redundancy --min-n 5 --markdown -->

| source | n | r2 vs AA coding+agentic | new information |
|---|--:|--:|--:|
| epoch ECI | 7 | 0.985 | 1% |
| gbench | 13 | 0.961 | 4% |
| lmarena | 12 | 0.547 | 45% |
| swe-rebench | 9 | 0.476 | 52% |
| reddit mentions | 19 | 0.121 | 88% |
| sentiment | 19 | 0.089 | 91% |
| reddit reception | 19 | 0.036 | 96% |

**this is what moved the weighting.** GBENCH held 0.35, the largest single
weight, on the argument that it is played rather than graded. that argument is
about *how* it measures, and it stands. but on the models this document ranks,
AA already explains 96% of it: rank correlation is +0.92 against AA coding and
+0.93 against terminal-bench. it would have held 35% of the weight while
supplying 4% of a source's worth of independent evidence, so it now holds 0.15.

meanwhile the two sources deliberately kept **out** of the composite are the
two that disagree most with AA. swe-rebench is 52% unexplained, which is what
you would expect from a suite whose tasks are rebuilt from pull requests merged
after the models shipped. lmarena is 45% unexplained, being the only source
here scoring by human preference.

three things follow, and only the first is a change:

- **it explains the stability.** [the weighting
  sweep](#how-much-the-weighting-decides-the-answer) finds deepseek first under
  every weighting and one model second under six of seven. that is not
  robustness in the usual sense -- it is what happens when the components are
  largely the same measurement. the ranking is stable because the evidence is
  correlated, not because it is overwhelming, and the one place it did move
  when the weights changed was the place the least-correlated source votes.
- **the exclusions are still right, for a different reason than stated.**
  lmarena and swe-rebench are out on coverage: 8 and 13 of the 20 are
  missing, so folding them in moves ranks on absence. that reason has not
  changed. but they were also implicitly treated as redundant, and they are the
  opposite. if their coverage improves they should go in, and the case is
  stronger than it looked.
- **epoch stays a cross-check, and this is why.** on the eight roster models it
  scores, ECI orders them almost identically to AA's intelligence index
  (rho +0.98), and AA's coding and agentic indices explain 98.5% of it. that is
  a fitted cross-benchmark index behaving exactly as a fitted cross-benchmark
  index should; it is confirmation, not a fifth axis.

the same tool on AA's own fields, where n is large enough to trust:

<!-- generated by research/analyze-correlations --scope aa --pair intelligenceIndex --markdown --no-ci -->

| metric a | metric b | n | spearman | pearson |
|---|---|--:|--:|--:|
| intelligenceIndex | agenticIndex | 160 | +0.98 | +0.98 |
| intelligenceIndex | terminalbenchV21 | 200 | +0.98 | +0.97 |
| intelligenceIndex | codingIndex | 220 | +0.97 | +0.98 |
| intelligenceIndex | gdpvalNormalized | 198 | +0.97 | +0.97 |
| intelligenceIndex | gpqa | 573 | +0.95 | +0.86 |
| intelligenceIndex | tauBanking | 166 | +0.94 | +0.91 |
| intelligenceIndex | scicode | 565 | +0.93 | +0.87 |
| intelligenceIndex | mmmuPro | 240 | +0.93 | +0.87 |
| intelligenceIndex | lcr | 498 | +0.93 | +0.88 |
| intelligenceIndex | hle | 565 | +0.85 | +0.92 |
| intelligenceIndex | omniscienceAccuracy | 477 | +0.84 | +0.85 |
| intelligenceIndex | ifbench | 448 | +0.82 | +0.78 |
| intelligenceIndex | critpt | 477 | +0.82 | +0.76 |

nothing in AA falls below +0.82. a benchmark suite that scores 14 things and
ranks models the same way on all 14 is reporting one thing, and that is the
strongest argument in this document for carrying sources that are *worse* than
AA but measured differently.

### inside one benchmark: which terminal-bench tasks carry it

the same question one level down. terminal-bench publishes an aggregate, but
the submissions behind its leaderboard are public, so the pass or fail of each
of its 90 tasks can be recovered -- 73 submissions, 14,340 trials, in
`research/data/tbench.json`. `research/analyze-tbench` then asks of each task:
does passing it order models the way AA, epoch, lmarena and GBENCH do?

| task | pass rate | AA II | epoch ECI | gbench | lmarena |
|---|--:|--:|--:|--:|--:|
| *(the whole 90-task suite)* | 0.56 | +0.72 | +0.85 | +0.71 | +0.70 |
| circuit-fibsqrt | 0.81 | +0.68 | +0.75 | +0.76 | +0.69 |
| torch-pipeline-parallelism | 0.38 | +0.65 | +0.80 | +0.75 | +0.69 |
| large-scale-text-editing | 0.82 | +0.67 | +0.75 | +0.65 | +0.64 |
| write-compressor | 0.65 | +0.56 | +0.78 | +0.64 | +0.77 |
| make-mips-interpreter | 0.38 | +0.73 | +0.84 | +0.62 | +0.70 |
| ... | | | | | |
| fix-git | 0.99 | +0.23 | +0.00 | +0.10 | -0.14 |
| configure-git-webserver | 0.61 | -0.37 | -0.29 | -0.04 | -0.35 |

**a quarter of the suite carries what all of it says.** the best single tasks
match the whole suite's agreement with every external source, and they are the
mid-difficulty long-horizon ones: build an interpreter, shard a training job,
implement a compressor. 34 of the 89 scorable tasks land within 0.20 of zero,
mostly because 23 of them are passed by more than 90% of runs and cannot
separate anybody -- `fix-git`, `git-leak-recovery` and `nginx-request-logging`
are three sysadmin one-liners contributing nothing but runtime.
`configure-git-webserver` is worse than nothing: it is inverted, and the models
failing it are gpt-5.2 and claude opus 4.6 while qwen3.5-9b and gpt-5-nano pass,
which is the signature of a brittle verifier rather than a hard task.

**believe the set, not the order.** `analyze-tbench --stability` runs the checks
that matter. the five references agree with each other about the ranking
(rho +0.74 to +0.87 across the 89-task vectors), so this is a property of the
tasks and not of one leaderboard. but the models are the sample here and there
are only 25 of them: a split-half over models reproduces the ranking at +0.48,
and 89 simultaneous tests need |rho| >= 0.63 to clear a corrected threshold,
which 11 tasks do. what survives out of sample is the *set* -- a top-10 chosen
on half the models scores +0.73 on the other half against the full suite's
+0.72, a top-20 scores +0.77.

**what this does and does not license.** it is a caveat about the benchmark,
not a re-scoring of anything above: the terminal-bench leaderboard is mostly
closed frontier models, and only 15 of its 73 submissions are open weights. of
the twenty models ranked above, two appear on it at all -- minimax m2.7 and
qwen3.6 35b a3b, one run each. so this supports reading AA's terminal-bench
column as a coarse instrument -- and it strengthens the
[harness caveat](#the-short-version), since a suite whose
signal lives in 20 tasks is a suite where a harness that mishandles two of them
moves the number.

**what would break these numbers.** the roster is 7 to 20 models, so every
cross-source cell has a confidence interval wide enough to matter --
`analyze-correlations` prints them, and gbench against AA coding at n=13 is
+0.76 to +0.98. the roster is also a restricted range: every model in it is near the top of the
field and inside one memory budget, which is the population the answer is
wanted for but not one that supports a general claim about the benchmarks.

and a high rank correlation does not mean the sources agree about any
particular model. this capture is itself the argument: GBENCH used to put mimo
v2.5 at 0.480 against qwen3.6 27b's 0.402, and now has them the other way round
at 0.350 and 0.411, on a quarter of a million matches each. hy3 has no
admissible gscore at all, on 24. the 4% is where the individual disagreements
live, and they move between captures -- worth reading one at a time rather than
averaging away.

### how much the weighting decides the answer

less than it did before dropping the intelligence index, which is itself
evidence that removing the double-count was right:

<!-- generated by research/build-tables --table weights -->
| weighting | top four |
|---|---|
| default | deepseek v4 flash 0731 > **minimax m2.7** > qwen3.6 27b > hy3 |
| the old weights (gbench 0.35, no arena/swe-reb) | deepseek v4 flash 0731 > **qwen3.6 27b** > minimax m2.7 > hy3 |
| coding-focused (0.45) | deepseek v4 flash 0731 > **qwen3.6 27b** > minimax m2.7 > hy3 |
| agentic-focused (0.45) | deepseek v4 flash 0731 > **qwen3.6 27b** > minimax m2.7 > hy3 |
| swe-rebench-heavy (0.25) | deepseek v4 flash 0731 > **minimax m2.7** > qwen3.6 27b > hy3 |
| arena-heavy (0.25) | deepseek v4 flash 0731 > **qwen3.6 27b** > minimax m2.7 > hy3 |
| sentiment dropped | deepseek v4 flash 0731 > **minimax m2.7** > qwen3.6 27b > hy3 |

**deepseek v4 flash 0731 is first under every weighting tried.** below it the second
place is genuinely undecided: qwen3.6 27b takes it under four of the seven and
minimax m2.7 under three, on a default gap of 0.2 points.

that mechanism is worth stating plainly, because it is one number.
**swe-rebench scores minimax m2.7 at 51.8 against qwen3.6 27b's 34.3** -- and
swe-rebench is the one source here whose tasks are rebuilt from pull requests
merged *after* these models shipped, so it is the hardest of the seven to have
trained against. weighting it heavily is what promotes minimax; dropping
sentiment does the same thing from the other side, by removing the component
qwen3.6 27b leads on.

the caution runs the same way whichever is second. the gap is 0.2 points on a
scale where **gaps under ~2 points are membership noise**, so neither ordering
is a verdict. and minimax m2.7 costs 103.1gib against 27.1 -- whatever it does
on the composite it loses [effective intelligence per
gigabyte](#effective-intelligence-at-this-budget) by a factor of four.
**qwen3.6 27b is the value pick either way**, which was always a different
claim from being second on the composite.

below the top two the order is not stable, and should not be read as one. use
the composite to rule models out; for choosing between neighbours, the
[capability detail](#capability-detail) and your own harness matter more.

### what the composite changes

against the plain quant-adjusted intelligence ranking, two models move a long
way:

- **qwen3.6 27b rises to 2nd** from 5th. it is 2nd on effective coding and the
  most-discussed model in the corpus, from a file a quarter the size of its
  neighbours.
- **inkling small falls to 6th** from 2nd. it leads the cluster on effective
  intelligence and then has almost nothing corroborating it: GBENCH and lmarena
  list the flagship `inkling` rather than Small, swe-rebench does not carry it,
  and it publishes no card claims, so four of seven components are imputed at
  the set median, on 14 reddit mentions. this is the clearest case of a rank
  resting on one axis.

### three late additions

`research/analyze-catalog` plus an audit of AA against the roster turned up
three models that belonged here and were missing. all are now in every table
above:

- **mistral medium 3.5** (14th, 39.6). the more surprising omission: it has
  complete AA data *and* a GBENCH score *and* an lmarena rating, which is
  better coverage than several models that were already ranked. it lands
  mid-table because it is a **dense 128b** -- it fits at UD-Q6_K_XL (101.7gib)
  but reads every parameter per token, which the bandwidth model puts at about
  **1 t/s**. it is the slowest thing on this roster by a wide margin.
- **nemotron 3.5 lightning** (18th, 28.8, on 3/7 components). released the day
  it was first captured, so it still has no GBENCH result and no community
  mentions, and its score comes from AA and its own card with the rest imputed.
  at 31.6b total / 3.6b active with a 1m context it is structurally interesting
  and thinly evidenced; revisit it rather than reading 28.8 as a verdict.

- **solar open2 250b** (11th, 50.4, on 2/7 components). released 2026-08-12,
  so like nemotron it has no GBENCH result and no mentions yet. it is here as a
  deliberate edge case: it is the only model on the roster that **fits without
  being runnable**. Q2_K is 88.9gib, comfortably inside the budget, but it is
  **dense 250b**, so it reads every parameter per token and the speed table
  puts it near 2 t/s. the composite has no speed term and ranks it 11th; that
  is the clearest example in this document of why the [speed](#speed) table is
  not optional reading.

there is no unsloth quant for nemotron 3.5 lightning or solar open2 250b, so
the roster points at bartowski and prometheusAIR respectively -- both a step
down in quant provenance from the rest of the table.

### capability detail

same order, broken out by capability. `coding` and `agentic` are quant-adjusted
by the same retention factor as the headline table -- that transfer is best
justified for coding, since the curve was fitted on aider polyglot, itself a
coding benchmark. `TB2.1` (terminal-bench 2.1), `tau-bank` (tau2-bench banking),
`gdpval` (GDPval-AA, real professional tasks) and `hallu` (omniscience, negative
means the model asserts more than it knows) are left raw -- adjusting them would
be extrapolation.

<!-- generated by research/build-tables --table fit -->

| model | coding | agentic | TB2.1 | tau-bank | gdpval | hallu |
|---|--:|--:|--:|--:|--:|--:|
| deepseek v4 flash 0731 | 63.6 | 44.5 | 78.7 | 39.4 | 52.9 | -14.3 |
| minimax m2.7 | 50.6 | 24.9 | 55.4 | 9.9 | 33.0 | 0.8 |
| qwen3.6 27b | 53.2 | 27.2 | 60.7 | 16.7 | 32.0 | -20.0 |
| hy3 | 51.7 | 27.6 | 64.4 | 22.9 | 35.7 | -18.5 |
| muse glimmer | 48.5 | 22.7 | 51.7 | 23.5 | 22.7 | -32.9 |
| inkling small | 49.9 | 30.1 | 55.1 | 18.8 | 38.4 | -8.9 |
| ling 3.0 flash | 50.1 | 29.0 | 55.4 | 27.2 | 30.4 | -17.9 |
| qwen3.8 27b | - | - | - | - | - | - |
| mimo v2.5 | 49.2 | 21.2 | 63.7 | 8.7 | 32.5 | -9.8 |
| qwen3.5 122b a10b | 45.2 | 21.0 | 47.6 | 15.3 | 24.4 | -41.5 |
| solar open2 250b | 41.5 | 25.8 | 44.2 | 21.6 | 31.1 | -1.8 |
| qwen3.6 35b a3b | 41.5 | 21.4 | 44.9 | 9.3 | 27.8 | -22.2 |
| step 3.7 flash | 38.1 | 20.9 | 39.3 | 12.0 | 25.9 | -37.3 |
| mistral medium 3.5 | 46.4 | 19.0 | 50.6 | 15.1 | 21.7 | -36.8 |
| qwen3 coder next | 35.9 | 8.8 | 38.2 | 5.4 | 10.8 | -62.4 |
| gemma 4 31b | 43.1 | 14.3 | 43.4 | 14.8 | 15.5 | -47.9 |
| gemma 4 26b a4b | 38.9 | 10.9 | 39.0 | 12.0 | 13.4 | -50.8 |
| nemotron 3.5 lightning | 26.5 | 13.7 | 24.3 | 8.9 | 16.2 | -17.7 |
| gpt-oss-120b | 30.4 | 13.4 | 26.2 | 12.8 | 15.0 | -49.2 |
| nemotron 3 super | 37.3 | 8.7 | 38.6 | 10.3 | 9.9 | -41.5 |

adjusting changes who wins at coding. on paper hy3 (58.8) and mimo v2.5 (56.8)
beat qwen3.6 27b (53.7); at the quants that fit, **qwen3.6 27b comes second at
53.2**, ahead of hy3 at 51.7 and mimo at 49.2, out of a file a quarter their
size. only deepseek v4 flash 0731 stays clear of the pack.

## picks

every pick below is read off the quant-adjusted table, not the paper scores.
where the two disagree it is called out, because the disagreements are the
useful part.

**overall intelligence: deepseek v4 flash 0731 at UD-IQ3_XXS.** 47.6 effective
against 38.8 for the next model, a lead of nearly 9 points that survives the 8%
it pays at 2.94 bpw. it also leads GDPval-AA at 52.9 where nothing else clears
39. GBENCH, which is played rather than graded, puts it second on its
open-weights agentic coding board behind kimi k3, which does not fit here, so
the lead is not an artifact of one scoring method.

284b total but 13b active, so it decodes at roughly the speed of a 13b dense
model. MIT licensed. the `dspark` drafter fits alongside it at this quant.

the reason it fits where the arithmetic below suggests it should not is the
attention design. v4 uses compressed sparse attention plus heavily compressed
attention, and deepseek reports the 1m-token setting costing 27% of what the
naive form would; people running it locally describe the kv cache as "really
efficient, almost no need to quantise that". so the ~14gib kv reserve used for
the weight budget is pessimistic for this model specifically, and UD-IQ3_XXS
plus the 10.2gib dspark sidecar sits inside the ceiling. UD-IQ3_S (108.1gib) is
the alternative use of the same memory: one step more precision, no drafter.

two caveats from people running it. first, there is a live complaint that it
ignores rules files and skill definitions, which the thread largely attributes
to deepseek shipping no official jinja template, leaving each quant publisher
to write their own; pin a known-good template rather than trusting the gguf
default. second, if 97.1gib is too tight, the community's answer for this
class of machine is
[dwarfstar](https://huggingface.co/Rednalreden/DeepSeek-V4-Flash-0731-dwarfstar-q2-gguf),
a single 80.8gib file that keeps Q8 attention projections, shared experts and
output layer while dropping the routed experts to IQ2_XXS. 13.7k downloads.
that buys 16gib of context headroom for 2-bit routed experts. see
[forum sentiment](#deepseek-v4-flash-strong-with-a-real-complaint).

**agentic use: deepseek v4 flash 0731, then ling 3.0 flash.** the agentic column
separates these models far more than the intelligence column does: 44.5 adjusted
for deepseek against 30.1 for the next. below it the ordering is decided by
tau2-banking, the hardest and least saturated eval here, where ling 3.0 flash
scores 27.2 against minimax m2.7's 9.9 and mimo v2.5's 8.7 -- a gap far wider
than their near-identical effective II suggests.

**coding: deepseek v4 flash 0731 (63.6 adjusted), then qwen3.6 27b (53.2).** this is
where adjusting changes the answer. on paper hy3 (58.8) and mimo v2.5 (56.8)
both beat qwen3.6 27b (53.7), and an earlier version of this document
recommended them on that basis. at the quants that actually fit, they land at
51.7 and 49.2 while qwen3.6 27b barely moves, out of a file a quarter the size.
on raw terminal-bench 2.1 it scores 60.7, behind deepseek (78.7), hy3 (64.4)
and mimo v2.5 (63.7) -- all of them ~95gib models, so it is the best of what
can share the box. the paper ranking is an artifact of scoring models at a
precision this box cannot run them at.

**the hy3 disagreement.** hy3 is 6th on quant-adjusted intelligence because
Q2_K_XL costs it 12%, and 4th on the composite -- but on 4/7 components, since
its GBENCH result is excluded for sample size and swe-rebench never ran it. it
holds the single highest arena rating in the set (1457), which is why it rises
to 3rd the moment missing components are renormalized away instead of imputed. a small number of people running it on 128gb machines
rate it first for coding -- three clearly positive reports, against a similar
number who found it slow or preferred deepseek (counted in
[forum sentiment](#hy3-has-loud-advocates-on-128gb-and-not-many-of-them)):

> "Significantly better coder than deepseek-v4-flash. Keep using
> deepseek-v4-flash only if speed is the primary concern."
> -- [r/LocalLLaMA](https://old.reddit.com/r/LocalLLaMA/comments/1usy9ie/)

both can be true: AA measures the unquantized model, the retention curve is
transferred from a different architecture, and hy3 at 21b active has more
compute per token than anything else in the fitting set. the real costs
reported are context and speed, not quality -- roughly 190k context against
deepseek's 1m, and throughput that "drops off brutally as context grows".
worth testing directly rather than trusting either ranking, and nobody in that
thread had run it on strix halo.

**best value: qwen3.6 27b at Q8_0.** 27.1gib for 37.3 effective puts it within
1.5 points of models four to ten times its size. it beats qwen3.5 397b a17b
(34.3), a model fourteen times larger from the same lab two releases earlier.
it also leaves 70gib free, which is enough to keep a second model resident or
to run a 262k context without thinking about it.

**speed: qwen3.6 35b a3b or gpt-oss-120b.** 3b and 5.1b active respectively.
see the speed table below.

**avoid: qwen3 coder next.** an II of 21.3, the worst hallucination score in
the set at -62.4, and 79gib at Q8. qwen3.6 27b is better on every axis at a
third of the size. the coder-specific line has been overtaken by the general
models.

## what each model is actually good at

the benchmark tables rank models on one axis. the people running them daily do
not use them that way: they assign roles.

this section is from r/LocalLLaMA -- 161 threads, 12,822 comments, captured
2026-08-16. it is opinion rather than measurement, but it is counted opinion:
`research/analyze-task-mentions` counts how often each model is named in the
same sentence as each task, so a claim here has a denominator.

### how often each model comes up

| model | mentions | top-level | median rel | agentic | planning | long ctx |
|---|--:|--:|--:|--:|--:|--:|
| qwen3.6 27b | 307 | 138 | 42 | 18 | 20 | 6 |
| deepseek v4 flash 0731 | 267 | 97 | 42 | 14 | 11 | 6 |
| qwen3.8 27b | 171 | 89 | 51 | 6 | 16 | 4 |
| qwen3.6 35b a3b | 141 | 61 | 40 | 11 | 8 | 11 |
| muse glimmer | 108 | 43 | 55 | 9 | 9 | 1 |
| glm-5.2 | 104 | 46 | 51 | 1 | 1 | 1 |
| qwen3.5 122b a10b | 82 | 35 | 48 | 2 | 1 |  |
| gemma 4 31b | 65 | 33 | 40 | 2 |  |  |
| laguna s 2.1 | 64 | 16 | 31 | 2 | 4 |  |
| gemma 4 26b a4b | 61 | 28 | 50 | 4 | 1 | 1 |
| kimi k3 | 58 | 26 | 41 |  |  |  |
| qwen3 coder next | 52 | 28 | 46 | 4 | 2 | 1 |
| hy3 | 48 | 25 | 52 | 4 | 5 | 1 |
| gpt-oss-120b | 47 | 23 | 46 |  | 1 | 1 |
| minimax m3 | 46 | 20 | 25 | 2 |  | 1 |
| bonsai 27b | 34 | 10 | 34 | 1 |  | 1 |
| gemma 4 12b | 27 | 11 | 38 | 1 | 2 | 1 |
| minimax m2.7 | 24 | 12 | 73 | 1 | 1 |  |
| glm-4.5-air | 17 | 7 | 42 | 1 |  |  |
| qwen3.5 397b a17b | 17 | 10 | 56 | 1 |  |  |
| mimo v2.5 | 14 | 5 | 56 | 1 | 1 | 1 |
| inkling small | 14 | 4 | 60 |  |  |  |
| ornith 1.0 35b | 13 | 6 | 29 | 2 | 1 |  |
| ling 3.0 flash | 9 | 6 | 71 | 1 |  |  |
| step 3.7 flash | 8 | 5 | 57 |  | 1 |  |
| nemotron 3 super | 6 | 4 | 24 |  |  |  |
| qwen-agentworld 35b a3b | 6 | 0 | 84 | 1 |  | 1 |
| mistral medium 3.5 | 5 | 2 | 24 |  |  |  |
| ternary bonsai 27b | 3 | 0 | 74 |  |  |  |
| fable-fusion 711 | 3 | 1 | 42 |  |  |  |

`median rel` is the median percentile of a model's mentions against comments at
the same reply depth in the same thread. 50 is unremarkable. it is scored that
way because raw upvotes are close to meaningless across threads: in this corpus
the top comment scores 1943 in one thread and 10 in another, and the 10 is the
monthly "Best Local LLMs" thread, the most on-topic one in the set. depth
matters as much -- checking laguna's lowest-scoring mentions found them to be
ordinary endorsements buried three levels into reply chains, not disagreement.

read the mentions and top-level columns first; they are the robust ones. the
task columns are sparse because people name a model in one sentence and the
task in the next, which sentence-scoped matching deliberately does not join.

three things stand out:

- **qwen3.6 27b is discussed more than anything else that fits, by 15%**, and
  has the most top-level mentions, 1.42x the next model. deepseek v4 flash 0731 has
  been closing that gap across the last four captures (43% -> 28% -> 18% -> 15%).
- **laguna s 2.1 and minimax m3 are the outliers on reception.** laguna has 64
  mentions but only 16 top-level and a median percentile of 31; minimax m3 is
  lower still at 25. their advocates are mostly replying to someone else rather
  than being upvoted in their own right.
- **the models the tables rank highly are barely discussed.** ling 3.0 flash
  has 9 mentions, inkling small 14, mimo v2.5 14, minimax m2.7 24. either the
  community has not caught up with them, or they do not hold up in use. nothing
  here distinguishes those two, and it is the single biggest gap between the
  benchmark ranking and the lived one.

a caveat on all of it: reddit publishes a net score only, so a controversial +5
and an ignored +5 are indistinguishable. the cleanest signal in the corpus is
the negative score, precisely because it is rare -- 188 of 12,745 scored
comments. qwen3.6 27b and hy3 carry three each, the most of any model here,
which for qwen3.6 27b is what being the most-discussed model also buys.

### the monthly community highlight

["Best Local LLMs - August 2026"](https://old.reddit.com/r/LocalLLaMA/comments/1vkmhyl/)
organises picks by size tier, which maps onto memory budget better than any
benchmark does. condensed, for tiers this box can reach:

| tier | picks |
|---|---|
| XL, coding + agentic | ling 3.0, laguna s 2.1 |
| M, agentic non-coding, 24gb | gemma 4 31b, gemma 4 26b |
| M, coding, <64gb | qwen3.6 27b |
| S, non-coding | gemma 4 e4b |
| creative writing | skyfall 4.2 (a gemma 4 31b finetune), glm 4.7 |

two things stand out. **gemma is preferred over qwen for long context**, with a
specific claim: "Gemma acts like a real Big model, works great with big context
(not like Qwen 27b and 35b which breaks down over 80k context)". if you intend
to actually use a 262k window, test that before committing. and **creative
writing is the one category where older models win** -- glm 4.7 over the entire
glm-5 series, on the grounds that "creative writing isn't (easily) benchmarked",
so nobody tuned for it.

### by role

roles that show up repeatedly, with the count of supporting mentions:

| role | model | support |
|---|---|---|
| generalist coding | qwen3.6 27b Q8 | strong: most-mentioned model, "unbeatable reliability" |
| architecture / planning | laguna s 2.1, deepseek v4 flash 0731 | moderate: laguna "makes wiser architectural decisions", 4 planning mentions |
| debugging | gemma 4 31b | weak: 2 independent reports calling it "a great detective" |
| adversarial review | hy3 | weak: 1 detailed report, "cares much less about pleasing the user" |
| translation / prose | gemma 4 26b a4b | weak: 2 reports, one a full book translation |
| vision / documents | gemma 4 26b a4b QAT | weak: 3 mentions, all positive |
| fast / disposable | qwen3.6 35b a3b | strong: 67 mentions, top of the chat/assistant column |
| long-horizon agentic | deepseek v4 flash 0731 | strong: 71 mentions, 4 agentic, 3 long-context |

the "support" column is the honest part. only the top and bottom rows rest on
more than a handful of people; the middle of the table is two or three reports
each and should be treated as a hypothesis to test, not a finding.

### the pairings people actually run

role assignment shows up more often than single-model use:

- **planner plus executor.** "deepseek v4 flash q2kxl (planning) with qwen 3.6
  27 q8 (executor) and it honestly feels no worse than the frontier models".
  this is the pattern this hardware suits, since the footprints are 80-97gib
  and 27gib.
- **writer plus debugger.** "GLM-4.5-Air writes/edits the code, and
  Gemma-4-31B-it finds and fixes its bugs".
- **plan/act swap on failure.** "I find Qwen3.6 27B and Gemma4 31B trade blows.
  I will swap Plan/Act roles if either gets stuck".
- **main model plus adversary.** hy3 run "not as main agent but as an
  'independent adversary'" against a frontier model.
- **fast model for the cheap half.** "when I need some really quick help on
  something, and it's not a big or important task, and doesn't involve
  architectural decisions, I'll use qwen-3.6-27b. Its too fast to not have".

### laguna s 2.1 is genuinely disputed

worth isolating because the disagreement is unusually sharp, and it is in the
strixhalo.yaml roster. in the same thread:

> "Laguna S 2.1 runs great on my 3090 + 64gb ddr4 [...] This is without a doubt
> the best model I have ever run locally." [6]

> "Laguna S blows 3.6 27B out of the water on benchmarks like DeepSWE. Real
> usage confirms that." [1]

against:

> "Laguna performs worse than Qwen 3.6. There is a lot of weird promotion of it
> oddly, but give it a try. Doesn't take long to realize it is benchmaxxed." [1]

with a plausible reconciliation from a third commenter: laguna is weaker
zero-shot but better at matching an existing codebase, "It understands how
developers work, where they want their code". someone else runs laguna XS 2.1
on a 64gb strix halo and reports it trading blows with qwen3.6 27b. GBENCH
rates laguna s 2.1 at 0.239, 88th of 97 on that board, which is more consistent
with the sceptics than the enthusiasts.

### the caveat that undercuts all of it

> "we see on terminal bench 2 and sanity harness more than 50% swings with the
> same model in a different framework and open source models are particularly
> sensitive to a 'bad' agentic framework. [...] whichever model is 'best'
> changes dramatically depending on the framework you choose and not in obvious
> ways."
> -- [r/LocalLLaMA](https://old.reddit.com/r/LocalLLaMA/comments/1reds0p/) [32]

a 50% swing from harness choice is larger than every gap in the tables above.
that is a strong argument for testing two or three candidates in your own
harness rather than trusting any ranking, including this one.

## a second opinion: GBENCH

[gert labs GBENCH](https://gertlabs.com/rankings?ow=1) scores models by making
them play complex games against each other. that is worth carrying alongside
artificial analysis for one reason: the task distribution is generated rather
than curated, so there is no public problem set to train against, and outcomes
are decided by play rather than by a grader. it is the closest thing here to a
benchmark that cannot be benchmaxxed.

the open-weights agentic coding board, top of the fitting set:

| rank | model | gscore | avg percentile |
|--:|---|--:|--:|
| 1 | kimi k3 | 72.3 | 76.5 |
| 2 | deepseek v4 flash 0731 | 58.5 | 65.5 |
| 3 | glm-5.2 | 57.3 | 64.2 |
| 5 | mimo v2.5 pro | 56.3 | 65.2 |
| 7 | minimax m2.7 | 45.9 | 53.7 |
| 8 | qwen3.6 27b | 45.2 | 52.5 |
| 11 | mimo v2.5 | 40.0 | 49.8 |

it broadly agrees with artificial analysis on the two picks: deepseek v4 flash 0731
is the best thing that fits, and qwen3.6 27b punches above its size. it used to
disagree on mimo v2.5, rating it well above qwen3.6 27b where AA had them
close; two captures ago that reversed, and this one widens the reversal to five
gscore points, which is a caution about quoting a single gscore as a settled
fact.

### per-language: the coding pick depends on the language

the site's compare view publishes per-language breakdowns. deepseek v4 flash
0731 against qwen3.6 27b, agentic coding mode:

| language | deepseek v4 flash 0731 | qwen3.6 27b |
|---|--:|--:|
| c# | 91.1 | 61.9 |
| go | 90.5 | 78.5 |
| javascript | 83.7 | 64.1 |
| **rust** | **71.5** | **56.9** |
| ocaml | 57.3 | 54.0 |
| python | 82.1 | **89.6** |
| typescript | 73.3 | **81.0** |
| kotlin | 51.4 | **68.1** |

there is no single "better coder" here. deepseek takes c#, go, javascript and
rust; qwen takes python, typescript and kotlin. **for rust specifically the gap
is 14.6 points in deepseek's favour**, its third-largest margin. against
minimax m2.7 deepseek also leads on rust, 71.5 to 64.5.

three caveats, in descending order of how much they should bother you:

1. **these numbers are not reproducible from the public api.** aggregating game
   percentiles weighted by matches over agentic-coding games reproduces some
   cells well (deepseek rust 71.7 against 71.5 published) and others badly
   (qwen3.6 27b rust 75.5 against 56.9 published). the exact formula is not
   documented, so the table is quoted as published rather than recomputed.
2. **per-language sample sizes are small.** the api reports 4 to 21 submissions
   per language per model. a 14-point gap on that base is suggestive, not
   settled.
3. **the aggregate and the head-to-head disagree.** the same compare view
   reports deepseek ranking higher in 5 of 6 games, while qwen wins the
   pairwise match count 64 to 43. deepseek is better at the games where the
   spread is wide; qwen wins more individual matches.

also from that comparison, and relevant to running either locally: deepseek was
faster (58s against 70s per task) and emitted 2.5x more code (33.0 KB against
13.3 KB), which is worth knowing if you have opinions about diff size.

the full per-language and per-game data for all 97 models is committed at
`research/data/gbench.json`, and the published compare values at
`research/data/gbench-compare-observed.json`, so a later question about c++ or
java needs no refetch.

## a third opinion: lmarena, and why it is not in the composite

AA grades answers against a problem set and GBENCH decides them by play.
lmarena does neither: it counts which of two blind responses a human preferred.
that is the only source here measuring what people like rather than what scores
well, and nothing about it can be trained against directly.

the text board below is style-controlled, meaning lmarena has regressed out
response length and formatting -- without that, preference rewards a chatty
model over a terse correct one.

<!-- generated by research/build-tables --table arena -->
| model | composite rank | text elo | votes | webdev elo |
|---|--:|--:|--:|--:|
| deepseek v4 flash 0731 | 1 | 1435 | 49,112 | - |
| minimax m2.7 | 2 | 1416 | 58,418 | 1397 |
| qwen3.6 27b | 3 | - | - | - |
| hy3 | 4 | 1457 | 4,664 | 1522 |
| muse glimmer | 5 | 1426 | 3,733 | 1359 |
| inkling small | 6 | - | - | - |
| ling 3.0 flash | 7 | - | - | - |
| qwen3.8 27b | 8 | - | - | - |
| mimo v2.5 | 9 | 1434 | 44,647 | 1438 |
| qwen3.5 122b a10b | 10 | 1417 | 28,449 | 1358 |
| solar open2 250b | 11 | - | - | - |
| qwen3.6 35b a3b | 12 | - | - | - |
| step 3.7 flash | 13 | - | - | - |
| mistral medium 3.5 | 14 | 1427 | 11,022 | 1265 |
| qwen3 coder next | 15 | - | - | - |
| gemma 4 31b | 16 | 1451 | 5,899 | 1364 |
| gemma 4 26b a4b | 17 | 1438 | 5,812 | 1362 |
| nemotron 3.5 lightning | 18 | - | - | - |
| gpt-oss-120b | 19 | 1352 | 30,775 | - |
| nemotron 3 super | 20 | 1360 | 7,536 | - |

**it is a component at 0.10, and the reason it is not more is coverage.** nine
of the twenty are not on the board at all, including qwen3.6 27b -- the model
this document recommends second. at 0.10 the composite renormalizes over what
is present and doubling the weight to 0.20 swaps only 2nd and 3rd, two models
already 0.7 points apart, which is the bound working: absence cannot move an
answer far. it earns its place
because it is one of the two sources that disagree with AA most.

two things the table does say, which the other sources do not:

- **hy3 tops the roster on human preference** (1457 text, 1522 webdev, the
  highest of any model here on either board) despite having no admissible
  GBENCH score and ranking 4th on the composite. that is a second independent
  signal pointing the same way as its 128gb advocates, and it moves hy3 from
  "loud minority" to "liked by two populations that do not overlap".
- **the vote counts are wildly uneven and worth reading first.** minimax m2.7
  has 58,418 votes and hy3 4,664, and muse glimmer's rating rests on 3,733. an
  elo on a few thousand votes is a much weaker claim than the number's
  precision suggests.

`research/data/lmarena.json` holds all 11 boards for 456 models.

## speed

decode is bandwidth bound. bytes read per token is approximately
`active_params * bpw / 8`, and llama.cpp realizes 160-200gb/s of the 256gb/s
peak on this hardware. estimates below use 160gb/s and are conservative by
about 20-30% against the measured anchors.

<!-- generated by research/build-tables --table speed -->

| model | active | bpw | gb/token | est. t/s | measured |
|---|--:|--:|--:|--:|---|
| gpt-oss-120b | 5.1b | 4.41 | 2.81 | 57 | 55 |
| qwen3.6 35b a3b | 3b | 8.40 | 3.15 | 51 |  |
| qwen3 coder next | 3b | 8.51 | 3.19 | 50 |  |
| nemotron 3.5 lightning | 3.6b | 8.86 | 3.99 | 40 |  |
| gemma 4 26b a4b | 3.8b | 8.53 | 4.05 | 40 |  |
| ling 3.0 flash | 5.1b | 6.94 | 4.42 | 36 |  |
| deepseek v4 flash 0731 | 13b | 2.94 | 4.77 | 34 |  |
| minimax m2.7 | 10b | 3.85 | 4.82 | 33 |  |
| inkling small | 12b | 3.23 | 4.85 | 33 |  |
| mimo v2.5 | 15b | 2.66 | 4.98 | 32 |  |
| step 3.7 flash | 11b | 3.93 | 5.41 | 30 |  |
| hy3 | 21b | 2.72 | 7.13 | 22 |  |
| qwen3.5 122b a10b | 10b | 7.19 | 8.99 | 18 |  |
| nemotron 3 super | 12.7b | 7.14 | 11.33 | 14 |  |
| qwen3.6 27b (dense) | 27.8b | 8.36 | 29.05 | 6 | 7.4 |
| qwen3.8 27b (dense) | 27.8b | 8.36 | 29.05 | 6 |  |
| muse glimmer (dense) | 30b | 7.90 | 29.61 | 5 |  |
| gemma 4 31b (dense) | 30.7b | 9.13 | 35.02 | 5 |  |
| solar open2 250b (dense) | 250b | 3.05 | 95.43 | 2 |  |
| mistral medium 3.5 (dense) | 128b | 6.82 | 109.16 | 1 |  |

the dense entries are the warning. qwen3.6 27b has the best score-per-byte in
the set and one of the worst tokens-per-second, because a dense model reads
every weight for every token. at Q8 it is measured at 7.4 t/s on this
hardware, which is too slow for interactive agentic work. at Q4_K_XL it
measures 11.7 t/s.

**speculative decoding changes the dense math.** with MTP enabled, qwen3.6 27b
goes from 7.4 to 18.1 t/s at Q8 (2.44x) and 11.7 to 21.2 t/s at lower quant
(1.81x) on strix halo. models shipping a drafter are worth a second look:

| model | drafter | claimed speedup |
|---|---|---|
| qwen3.6 27b / 35b a3b | MTP sidecar | 1.8-2.4x measured on strix halo |
| gemma 4 26b a4b | `mtp-` sidecar in repo | |
| muse glimmer | `dflash-kquant.gguf` in repo | 3.1x claimed (on a 5090) |
| deepseek v4 flash 0731 | `dspark` sidecar | ~2x claimed |
| ling 3.0 flash | MTP, in the ROCmFP4-STRIX build | |
| laguna s 2.1 | `DFlash-BF16`, cross-repo | up to 8x claimed, needs a forked llama.cpp |

a drafter costs memory that comes out of the same budget. dspark is roughly
10gib, which is one quant step for deepseek v4 flash 0731: UD-IQ3_XXS plus the
sidecar costs about what UD-IQ3_S costs on its own. that trade is worth taking
here, since ~2x decode beats one step of precision at the flat end of the
retention curve.

## does it actually run here

everything above measures how good a model is. this section is about whether
it works on this hardware, which is a separate question and the one that has
actually cost time. it is drawn from three sources the benchmark tables cannot
see: huggingface per-repo discussions, llama.cpp issues, and the level1techs
forum -- 851 documents, of which **90 name strix halo, rdna3.5 or gfx1151**.
`research/analyze-operational --strix` regenerates the counts.

**read this section more sceptically than the rest of the document.** the other
sources aggregate: a benchmark runs every model through one harness, and the
reddit counts have a denominator. this one is a pile of individual claims, most
from one person, on one configuration, at one moment. of the 90 strix-halo
documents, **24 are already closed, 46 are more than 30 days old, and 14 have
no engagement beyond the person who filed them.** an unreplicated bug report is
a lead to verify on your own machine, not a finding.

two entries in an earlier version of this table did not survive that test, and
they are worth keeping visible as calibration:

- **muse glimmer "not supported on the vulkan build"**
  ([#26865](https://github.com/ggml-org/llama.cpp/issues/26865)) was opened
  *and closed on the same day*, and the owner of the machine this document is
  written for reports it loading fine on vulkan. it was a real error message
  for about a day.
- **hy3 "needs a patched llama.cpp"** came from a comment 27 days old; hy3 is
  supported by default now. the pi-bench numbers below still stand, but the
  build obstacle does not.

what is left after filtering to reports that are still open and that somebody
other than the author engaged with (`--open --min-engagement 2`, 47 of 90):

| model | report | state | source |
|---|---|---|---|
| deepseek v4 flash 0731 | garbled output under rocm on strix halo | open 34d, 27 comments | [#25436](https://github.com/ggml-org/llama.cpp/issues/25436) |
| deepseek v4 flash 0731 | `vk::DeviceLostError` after 2-3 turns on vulkan (RADV_STRIXHALO); qwen3.6 27b and gemma 4 31b on the same box are fine | open 28d, 19 comments | [#25664](https://github.com/ggml-org/llama.cpp/issues/25664) |
| deepseek v4 flash 0731 | the dspark drafter fails to load on recent llama-server; unsloth replied "still experimental" | open 8d, 6 comments | [hf 26](https://huggingface.co/unsloth/DeepSeek-V4-Flash-0731-GGUF/discussions/26) |
| laguna s 2.1 | UD-Q5_K_L emits no tokens under rocm | open 12d, 1 comment | [hf 23](https://huggingface.co/unsloth/Laguna-S-2.1-GGUF/discussions/23) |

the deepseek rows are the only ones with real corroboration, and even there the
`DeviceLostError` has a known manual patch -- so the honest summary is that
deepseek v4 flash 0731 is the model on this roster most likely to need you to fix
something before it runs, not that it cannot run.

### hy3 on strix halo, which nobody had tried

the [forum sentiment](#hy3-has-loud-advocates-on-128gb-and-not-many-of-them)
section notes that hy3's advocates were arguing from other hardware. the
huggingface discussions have the missing measurement, from someone running it
on this box against a 50-task coding benchmark:

| quant | size | pi-bench pass | avg duration |
|---|--:|--:|--:|
| IQ1_M + MTP | 89.4gb | 58.0% (29/50) | 20m 30s |
| Q2_K_XL + MTP | ~100gb | 68.0% (34/50) | 17m 53s |
| UD128 (IQ3) | 116.7gb | 68.0% (34/50) | 14m 20s |

so **Q2_K_XL matches the 116.7gb quant on pass rate**, which is the quant this
document scores it at, and the 1-bit version costs 10 points. that is the
single most useful measurement in this section: it says the quant hy3 is ranked
at here is not the thing holding it back.

hy3 also runs at about 14 t/s on a strix halo under rocm. the same thread
reports needing a patched llama.cpp to load it -- but that report is from
2026-07-15 and hy3 is supported by default now, so treat the throughput number
and not the build advice.

### prefill, not decode, is the practical limit

the [speed](#speed) table estimates decode, because decode is what bandwidth
arithmetic predicts. the reports say time-to-first-token is what makes a model
unpleasant. measured on strix halo with deepseek v4 flash 0731:

- UD-IQ2_M at the full 1m context: **11.49 t/s decode**. the bandwidth model in
  the speed table predicts 38 t/s for that quant -- it is *smaller* than the
  UD-IQ3_XXS this document recommends, so it should be the faster of the two.
  the measurement is 3.3x below the estimate, and the difference is context:
  the estimate assumes attention over an empty one.
- prompt processing falls from 113 tok/s at 512 tokens to **73 tok/s at 7.4k**,
  and a separate 128gb reporter puts time-to-first-token at "1-2 minutes"

so read the speed table as an upper bound that a long context takes most of,
not as a throughput figure. it is the one table here with no measured anchor
for the large models, and this is the evidence that it needs one.

both numbers come from people posting their full llama.cpp configuration, which
is in `research/data/hf-discussions.json` if you want to copy it rather than
rediscover it.

## models nothing has scored

every ranking above is downstream of artificial analysis: `build-tables` joins
AA against the gguf sizes, and a model AA has not measured cannot appear at
all. that is a property of the method, not a judgement, and it is worth making
visible because **two of the models below are running on the target machine
right now** and were silently absent from this document until the hub catalog
surfaced them.

checked, not assumed: none of these four appears in artificial analysis, GBENCH,
lmarena or swe-rebench. there is no benchmark number to quote for any of them.

<!-- generated by research/build-tables --table unscored -->

| model | quant | size (gib) | total / active | downloads | likes | note |
|---|---|--:|---|--:|--:|---|
| ornith 1.0 35b | Q8_0 | 34.4 | 35b / ? | 255,448 | 143 | qwen3.5-moe arch despite the bare 35B; active params not published |
| qwen-agentworld 35b a3b | Q8_0 | 34.4 | 34.7b / 3b | 403,800 | 226 | moe, 34.7b total confirmed from the base repo |
| bonsai 27b | F16 | 50.1 | 27.8b / 27.8b | 1,638,186 | 778 | a qwen3.6-27b derivative, so dense and the same shape |
| ternary bonsai 27b | F16 | 50.1 | 27.8b / 27.8b | 698,543 | 1217 | ternary weights; the quant curve here does not model that |

what the columns are worth: size and parameter counts are file facts, and
downloads and likes measure adoption, which is not quality -- `bonsai 27b` has
more downloads than most of the ranked roster and no published evaluation
whatsoever. treat the table as an inventory of what exists, and the reason to
run your own harness.

#### qwen3.8 27b, from the only evidence that exists

it **is** in [the ranking](#the-ranking), at 55.3 on 2/7 components -- reddit
sentiment and its own model card, with the other five imputed at the set median.
no independent suite has measured it, so everything below is a file fact, a
first-week report, or a vendor claim carrying the discount
[measured for vendor claims](#what-a-model-says-about-itself).

**its card claims a large generational gain, and the comparison has to be read
within one card.** these are qwen's numbers for both models, taken from the
qwen3.8 card so that both columns ran on the same harness:

| benchmark | qwen3.8 27b | qwen3.6 27b | delta |
|---|--:|--:|--:|
| deepswe | 42.2 | 13.3 | +28.9 |
| gpqa | 89.2 | 87.8 | +1.4 |
| hle | 30.8 | 24.0 | +6.8 |
| ifbench | 79.5 | 69.1 | +10.4 |
| livecodebench | 90.3 | 83.9 | +6.4 |
| osworld | 84.3 | 63.9 | +20.4 |
| swebench_pro | 61.7 | 53.5 | +8.2 |
| swebench_verified | 79.0 | 49.3 | +29.7 |
| terminalbench | 73.0 | 63.4 | +9.6 |

do NOT get these deltas by differencing the two cards. the qwen3.8 card reports
qwen3.6 27b at 49.3 on swe-bench verified where qwen3.6's own card claims 71.3,
and at 63.4 on terminal-bench where its own card says 59.3 -- qwen re-evaluated
the baselines on a refined benchmark and said so in a footnote. across the
corpus `analyze-self-report --cross-card` finds **46 places where two cards
disagree about the same model**, by as much as 25 points. differencing cards
measures the harness, not the model.

what survives that caution is still a large claim: +9.6 on terminal-bench and
+8.2 on swe-bench pro are modest, while +29.7 on swe-bench verified, +28.9 on
DeepSWE and +20.4 on OSWorld are not credible as pure capability gains in a
model with the same architecture and parameter count. the card's own headline
feature -- "broader support for popular harnesses" -- is the likelier
explanation for the agentic rows, and that is a real usability gain rather than
a measurement of intelligence.

**it lands in exactly the slot qwen3.6 27b holds.** 27.8b dense against 27.8b
dense, 27.1gib at Q8_0 against 27.1gib -- the same box, the same budget, the
same quant. the incumbent keeps the recommendation until something measures the
successor.

**it is qwen3.6 27b's architecture, retrained.** `config.json` is the same
`Qwen3_5ForConditionalGeneration`, 64 layers, hidden 5120, 27.8b dense, same
262144 window. qwen's own blog calls it extra post-training on the same base,
and the subreddit worked this out within hours. the practical consequence is
that nothing about *fitting* it changes -- and it is why the speed numbers
below are surprising.

**the packaging trap is gone.** the nextn head ships inside the main gguf (65
blocks against 64 hidden layers, `blk.64` carrying `nextn.eh_proj` and its
norms) rather than in a separate `-MTP-GGUF`. for qwen3.6 that split was two
repos with identically-named files 0.42gib apart, and this document sized the
wrong one until it was caught; here there is only one repo to get right.

**quantization is nearly free at Q8_0, measured.** ubergarm published
perplexity over the same 580 chunks of wiki.test.raw at three precisions:

| quant | size (gib) | bpw | ppl | vs bf16 |
|---|--:|--:|--:|--:|
| BF16 | 50.9 | 16.00 | 6.9540 | - |
| Q8_0 | 27.0 | 8.50 | 6.9554 | +0.02% |
| IQ4_KS | 15.7 | 4.73 | 6.9938 | +0.57% |

that is the first retention measurement in this document taken on the model it
describes rather than transferred from [the deepseek v3.1
curve](#the-arithmetic), and it agrees with it: Q8_0 costs essentially nothing.

**the default reasoning effort is unusable here, and that is the headline.**
the chat template defaults `reasoning_effort` to `xhigh`, and reports of what
that costs are consistent across hardware: 15,000 thinking words where qwen3.6
spent 3,000 on the same prompt; a flappy-bird clone at 21k tokens against
qwen3.6's 4.5k; one trace of 52k thinking tokens; another user hitting the
262144 window at xhigh and having to drop to medium. at the 7-18 t/s this box
gets on a 27b dense, 52k thinking tokens is between 48 minutes and 2 hours.
`reasoning_effort: medium` is the fix, and medium is also the neutral setting:
xhigh and low each inject a system instruction, medium injects nothing.

**it is slower than qwen3.6 27b at the same quant, despite the same
architecture.** two independent reports: 45 t/s to 35 t/s on a 2080ti at
UD-Q4_K_XL with MTP, and 45-50 t/s to 30 t/s on a 3060 Ti + 4070 Ti Super.
a third reporter with R9700s says the speeds are identical. the likely
reconciliation is MTP draft acceptance -- one full log shows 0.546 acceptance
at mean accepted run 2.64, which is also why the config drafts 3 tokens rather
than the 6 it uses for qwen3.6.

**a chat-template bug shipped and was fixed in place.** llama.cpp raised
`Jinja Exception: System message must be at the beginning` against any harness
sending a system message mid-conversation. unsloth's UD-* quants had the
corrected template from the start and the plain quants did not; the maintainer
patched them the same day. **this repo pins `Q8_0`, one of the affected files**,
so a copy pulled before the fix needs refetching.

**what the community says about quality is not settled.** one reporter had Opus
4.8 review its reasoning traces and rate it comparable to Opus 4.6; another says
qwen3.6 wrote a bug-free minesweeper in one prompt where 3.8 "takes about twenty
times longer to think and constantly produces bugs". both are single trials.

**two llama.cpp issues name it.** [#26941](https://github.com/ggml-org/llama.cpp/issues/26941)
(merged) added `reasoning_effort` to the jinja template inputs -- before it,
llama.cpp handled only `none` and *discarded every other value*, which is why
first-week reports on whether the effort control worked contradicted each other.
[#27076](https://github.com/ggml-org/llama.cpp/issues/27076) (open, no comments)
is a `ggml_vulkan: device lost` running Q4_K_M under pi on an RX 6900 XT. that
is RDNA2 rather than this box, but it is the same backend and the same failure
class as [#25664](https://github.com/ggml-org/llama.cpp/issues/25664), the
deepseek device-lost already tracked below.

three things the table itself says:

- **ornith 1.0 35b is an MoE, not a dense 35b.** its base repo declares
  `Qwen3_5MoeForConditionalGeneration`, which the bare "35B" in the name hides.
  that matters here more than anywhere: dense 35b would sit at the bottom of
  the [speed](#speed) table, and an MoE of that size near the top. the active
  parameter count is not published, so the speed table still cannot include it.
- **bonsai 27b is a qwen3.6-27b derivative**, so its shape is known exactly even
  though its quality is not. the repo publishes only F16 and Q1_0 -- nothing in
  between -- which is why the table shows 50.1gib for a model whose base runs
  in 27.
- **the community fine-tune tier is much larger than this.**
  `DavidAU/Qwen3.6-27B-Fable-Fusion-711-*` alone has 2.9m downloads and 2,015
  likes, and [an independent writeup](https://blog.robai.net/27bevals/)
  measures seven 27B builds -- base, Tess-4, Aeon, ThinkingCap, and
  Fable-Fusion in both bf16 and Q8 -- on one vLLM methodology with WikiText-2
  perplexity, tool-eval, GSM8K/MMLU/IFEval and long-context recall. none of
  those builds is in any of the four benchmark sources here, so this document
  has nothing to say about them yet. that is the largest known gap in it.

## does not fit

| model | total / active | II | smallest published quant | verdict |
|---|---|---:|---|---|
| kimi k3 | 2800b / 104b | 59.7 | UD-IQ1_S, 594gb | 5x over budget |
| glm-5.2 | 753b / 40b | 52.6 | UD-IQ1_S, ~223gb | 2x over budget |
| deepseek v4 pro | 1600b / 49b | 53.2 | - | far over |
| minimax m3 | 428b / 23b | 45.4 | UD-IQ2_M, 125.0gib | 15gib over; iq1 only |
| motif 3 | 314b / 13.2b | 47.4 | Q3_K_M-mixed, 132.5gib | 13gib over the machine; no q2 published |
| qwen3.8 2.4t a95b | 2400b / 95b | 57.7 | - | 20x over budget |
| nex-n2-pro | 397b / 17b | 42.1 | - | over at any usable quant |
| nemotron 3 ultra 550b | 550b / 55b | 38.3 | - | far over |
| qwen3.5 397b a17b | 397b / 17b | 34.3 | - | over at any usable quant |

**motif 3 is the new painful one, and it arrived during this capture.**
released 2026-08-12 with open weights, 314b total on 13.2b active -- almost
exactly deepseek v4 flash 0731's shape, which fits here at 97.1gib -- and an
intelligence index of 47.4, which would place it second on this roster. it
misses only because nobody has published a small enough quant: the smallest is
Q3_K_M-mixed at 132.5gib, over the 119.2gib the machine physically has, and
there is no unsloth, bartowski or ggml-org repo at all yet, only a community
one. a UD-IQ3_XXS of a 314b model would land near 107gib on deepseek's ratio.
this is the roster entry most likely to change in the next week.

a second same-day release worth naming: **deepseek v4 pro** was refreshed on
2026-08-13 to an intelligence index of 53.2, up from the 45.3 of the april
build (which artificial analysis has re-slugged `deepseek-v4-pro-0424`). at
1600b it is not a candidate here, but it is the ceiling that v4 flash -- the
model this document recommends -- is distilled from, so it is the number to
watch for a future flash refresh.

minimax m3 is the older painful one. at an intelligence index of 45.4 it sits
between motif 3 and deepseek v4 flash 0731, and it misses by roughly 15gib: UD-IQ2_M
at 125.0gib exceeds the 119.2gib the machine physically has, and even UD-IQ1_M
is 119.6gib, still over. so there is no quant of it that fits with any context
at all, and 1-bit would cost about 22% of the model's score anyway, landing it
below deepseek v4 flash 0731 at IQ3.

## quantization: size versus intelligence

### the arithmetic

file size in gib is `params_b * bpw / 8 * (1e9 / 2^30)`, so roughly
`params_b * bpw / 8.6`. that gives the tradeoff its shape: at a fixed budget,
bits per weight and parameter count are inversely proportional. doubling
parameters at the same budget means halving precision.

### what precision actually costs

unsloth's per-quant sweep of qwen3.5 35b a3b, measuring perplexity and
kl divergence against the bf16 original:

| quant | size (gib) | bpw | ppl | mean kld |
|---|---:|---:|---:|---:|
| IQ2_XXS | 9.09 | 2.08 | 7.716 | 0.1846 |
| Q2_K_XL | 12.04 | 2.75 | 7.044 | 0.0970 |
| IQ3_XXS | 13.12 | 3.00 | 6.783 | 0.0501 |
| IQ3_S | 14.13 | 3.23 | 6.772 | 0.0457 |
| Q3_K_XL | 16.06 | 3.67 | 6.725 | 0.0308 |
| Q4_K_M | 18.49 | 4.23 | 6.605 | 0.0192 |
| Q4_K_XL | 19.17 | 4.38 | 6.592 | 0.0137 |
| Q5_K_XL | 23.22 | 5.31 | 6.549 | 0.0069 |
| Q6_K_XL | 28.22 | 6.45 | 6.539 | 0.0041 |
| Q8_K_XL | 36.04 | 8.24 | 6.535 | 0.0026 |

kld falls by 70x from 2-bit to 8-bit while the file grows 4x. the curve is
steep below 3.5 bpw and nearly flat above 5. Q6 to Q8 costs 28% more bytes
for a kld improvement of 0.0015, which is not detectable in use.

note the ordering: Q4_K_XL is both smaller and better than Q4_K_M in kld
terms. dynamic quants beat flat ones at equal size, which is the whole reason
to prefer `UD-*`.

### what precision costs on a real task

kld is a per-token proxy. the only public sweep that puts a task score against
bit width is unsloth's aider polyglot run on deepseek v3.1 (671b):

| precision | size gb | bpw | aider polyglot | retention |
|---|---:|---:|---:|---:|
| bf16 | 1342 | 16.0 | 71.6 | 1.000 |
| 5-bit | 484 | 5.77 | 70.7 | 0.987 |
| 4-bit | 396 | 4.72 | 69.7 | 0.974 |
| 3-bit | 284 | 3.39 | 68.4 | 0.955 |
| 2-bit | 245 | 2.92 | 65.8 | 0.919 |
| 1-bit | 185 | 2.21 | 55.7 | 0.778 |

the shape matters more than the absolute numbers. between 8 and 4 bits the
model loses under 3% of its score. between 3 and 2 bits it loses another 4%.
below 2.5 bits it falls off a cliff, losing 22% by 1-bit. the practical rule:
**3 bpw is the floor for a model you intend to trust, 4 bpw is the floor for
agentic work, and anything above 6 bpw is wasted budget.**

### the same measurement on an agentic benchmark

"flat score, amplified failures" (arxiv 2607.27275) is the study that answers
the question directly. it runs gemma 4 31b, gemma 4 26b a4b, qwen3.6 27b and
qwen3.6 35b a3b through tau2-bench at bf16, fp8 and int4.

the headline result is that **task scores barely move**:

| domain | model | bf16 | int4 | delta |
|---|---|---:|---:|---:|
| telecom | gemma 4 31b | 66.7 | 65.4 | n.s. |
| telecom | qwen3.6 27b | 96.3 | 96.9 | n.s. |
| retail | gemma 4 31b | 47.5 | 52.1 | n.s. |
| retail | qwen3.6 27b | 53.3 | 54.2 | n.s. |

all differences statistically insignificant. this is the result usually cited
as "4-bit is free". the study's point is that it is an artifact of the error
budget. underneath the flat scores, process-level failures roughly double:

- gemma 4 31b telecom, tool-name hallucination: 19.51% -> 38.26% of calls,
  a 2.5x rise in event volume (649 -> 1646 events)
- gemma 4 26b a4b telecom: 19.26% -> 23.05%
- qwen3.5 27b telecom: 0.26% -> 1.21%

the benchmark's default tolerance of 10 failed calls per episode absorbs the
extra errors. tighten it and the gap appears:

| allowed failures | bf16 vs int4 gap |
|---|---:|
| K=10 (default) | 1.3 points |
| K=5 | 7.5 points |
| K=2 | 16.7 points |

three findings from that paper carry directly into how to quantize on this
box:

1. **the cliff is between 8-bit and 4-bit weights.** fp8 produced no
   significant score change or channel movement in almost every cell. the
   entire degradation appears at int4.
2. **quantization amplifies existing failures rather than inventing new ones.**
   the bf16 and int4 hallucinated-tool distributions correlate at 0.97, and
   only 0.18% of int4 events invoked a tool that never appeared at bf16. a
   model that is already sloppy about tool names gets much sloppier; a model
   that is clean stays clean. qwen3.5 27b went from 0.26% to 1.21%, still
   negligible.
3. **retention is unchanged but failure volume is not.** recovery rate held at
   55% across both precisions while int4 generated 2.5x more failed calls per
   episode. the model is equally good at recovering from a mistake and makes
   far more of them.

the practical consequence for a long agentic rollout is that per-step damage
compounds. published work on long-horizon agents finds that doubling task
duration quadruples the failure rate rather than doubling it. a quant that
looks free on a single-turn eval is not free across a 50-step session.

### effective intelligence at this budget

combining the two: applying the retention curve to each model's AA intelligence
index at the largest quant that fits. these are the `eff II` numbers the
[headline composite](#the-ranking) is built from. it is an estimate -- the curve
was measured on one model and one benchmark, and the tau2 study above shows
task-level scores degrade less than process-level quality -- so treat the
ordering as meaningful and the absolute values as indicative.

<!-- generated by research/build-tables --table effective -->

| model | total / active | quant | size (gib) | bpw | AA II | retention | effective II |
|---|---|---|--:|--:|--:|--:|--:|
| deepseek v4 flash 0731 | 284b / 13b | UD-IQ3_XXS | 97.1 | 2.94 | 51.8 | 0.920 | **47.6** |
| inkling small | 266b / 12b | UD-IQ3_S | 100.1 | 3.23 | 41.2 | 0.943 | **38.8** |
| ling 3.0 flash | 124b / 5.1b | AD-Q6_K | 100.1 | 6.94 | 37.8 | 0.988 | **37.4** |
| minimax m2.7 | 230b / 10b | UD-IQ4_NL | 103.1 | 3.85 | 38.9 | 0.962 | **37.4** |
| qwen3.6 27b | 27.8b / 27.8b | Q8_0 | 27.1 | 8.36 | 37.7 | 0.990 | **37.3** |
| hy3 | 299b / 21b | Q2_K_XL-mtp | 94.6 | 2.72 | 42.2 | 0.879 | **37.1** |
| solar open2 250b | 250b / 250b | Q2_K | 88.9 | 3.05 | 37.4 | 0.929 | **34.8** |
| muse glimmer | 30b / 30b | Q8_0 | 27.6 | 7.90 | 35.1 | 0.990 | **34.7** |
| mimo v2.5 | 310b / 15b | UD-Q2_K_XL | 95.9 | 2.66 | 38.0 | 0.867 | **33.0** |
| qwen3.5 122b a10b | 125b / 10b | UD-Q6_K_XL | 104.7 | 7.19 | 32.8 | 0.989 | **32.5** |
| qwen3.6 35b a3b | 36b / 3b | Q8_0 | 35.2 | 8.40 | 32.1 | 0.990 | **31.8** |
| mistral medium 3.5 | 128b / 128b | UD-Q6_K_XL | 101.7 | 6.82 | 30.4 | 0.988 | **30.0** |
| step 3.7 flash | 198b / 11b | UD-IQ4_NL | 90.6 | 3.93 | 30.9 | 0.963 | **29.7** |
| gemma 4 31b | 30.7b / 30.7b | UD-Q8_K_XL | 32.6 | 9.13 | 29.7 | 0.991 | **29.4** |
| gemma 4 26b a4b | 25.2b / 3.8b | Q8_0 | 25.0 | 8.53 | 26.1 | 0.991 | **25.8** |
| nemotron 3 super | 120.6b / 12.7b | UD-Q5_K_XL | 100.2 | 7.14 | 25.7 | 0.989 | **25.4** |
| gpt-oss-120b | 117b / 5.1b | UD-Q8_K_XL | 60.0 | 4.41 | 24.1 | 1.000 | **24.1** |
| nemotron 3.5 lightning | 31.6b / 3.6b | Q8_0 | 32.6 | 8.86 | 23.6 | 0.991 | **23.4** |
| qwen3 coder next | 79.7b / 3b | Q8_0 | 79.0 | 8.51 | 21.3 | 0.990 | **21.1** |
| qwen3.8 27b | 27.8b / 27.8b | Q8_0 | 27.1 | 8.36 | - | 0.990 | **-** |

gpt-oss-120b takes no penalty because it is natively MXFP4 with
quantization-aware training. its 4.41 bpw is the trained precision, not a
lossy conversion, which is also why every quant of it in the unsloth repo is
within 2gib of every other. kimi k3 uses the same approach.

the ordering changes in two places once quantization is accounted for. **hy3
drops from 2nd on paper to 6th**, because 2.72 bpw costs it 12%. **mimo v2.5
drops from 5th to 9th** for the same reason. both are models large enough that
this box can only run them badly. meanwhile ling 3.0 flash and qwen3.6 27b
climb, because they fit at a precision where quantization is nearly free.

ranks 2 through 6 land within 1.7 points of each other, which is well inside
the error of a retention curve transferred from another model. read that band
as a tie and pick on the other axes: context, speed, tool-calling reliability.

### the floor scales with active parameters

the retention curve above is a function of bits per weight only, and that is
its main weakness. r/LocalLLaMA's objection to exactly this kind of table is
that a sparse MoE at 2 bits is hurt worse than the curve suggests, because
each token is computed by a small slice of the network and there is less
redundancy left to absorb the error:

> "12B active just isn't enough for such a heavy quant to still be solvent on
> any remotely long-horizon task. If you can't fit a Q4/nvfp4 at minimum the
> model isn't worth using."
> -- [r/LocalLLaMA](https://old.reddit.com/r/LocalLLaMA/comments/1vbajj8/)

that is consistent with the tau2-bench result above, where damage showed up in
process quality rather than final score, and with the compounding argument for
long rollouts. it means the effective-II column probably flatters inkling small
(12b active at 3.23 bpw), mimo v2.5 (15b at 2.66) and hy3 (21b at 2.72), and
that the honest floor is nearer 3.5 bpw for a 10-15b-active MoE than the 3.0
the curve alone would allow.

no published sweep varies active parameters and bit width together, so this
stays qualitative.

### the decision rule

for a fixed memory budget, prefer the largest model that still fits at 3.5 bpw
or above. below that, the quantization penalty grows faster than the
capability gained by adding parameters.

deepseek v4 flash 0731 is the exception that proves the rule: at 2.94 bpw it takes
an 8% penalty and still wins by nearly 9 points, because the gap between it and
everything else is so large. hy3 and mimo v2.5 are the rule working as
intended, giving up their paper advantage to the quantizer.

two refinements from practitioners:

**quantization sensitivity is model-specific, and gemma 4 is a bad case.**

> "Gemma 4 is way more sensitive to quantization than Qwen 3.6. So for Qwen I
> can use a smaller quant and Q8 KV to get more context, without much
> degradation."
> -- [r/LocalLLaMA](https://old.reddit.com/r/LocalLLaMA/comments/1t4nkez/)

that matches the tau2-bench study, where gemma 4 31b's tool-name hallucination
doubled at int4 while qwen3.5 27b's went from 0.26% to 1.21%. a single
retention curve cannot capture this. the practical version: qwen tolerates
aggressive quantization, gemma should be run at Q6 or better.

**Q8 over Q4 is not automatically worth it.** one independent harness
comparison found Q8 scoring slightly *worse* than Q4 on average while running
slower, though on 16 tasks without repeats, which the author and commenters
both flagged as too noisy to conclude from. the defensible reading is that
above roughly 4.5 bpw the quality difference is inside the noise of most
evaluations, so the tiebreaker should be speed and context headroom rather
than bits. the tables here pin dense models at Q8 because the memory is
available, not because Q8 is measurably better than Q6.

### kv cache quantization

the weight budget assumed q8_0 kv. that is the right default here. published
sweeps on long-horizon agentic coding show 4-bit kv cache costing 7-8 points
on 50-step tasks and 2-bit costing 18-22 points, with the damage scaling with
the number of steps rather than the context length. q8_0 kv halves the cache
against f16 for no measurable loss; going below q8 to buy weight budget trades
against exactly the capability agentic work depends on.

## benchmaxxing

### self-reported versus independently measured

comparing each lab's own terminal-bench number against artificial analysis's
run of terminal-bench 2.1:

| model | claimed | AA measured | delta |
|---|---:|---:|---:|
| deepseek v4 flash 0731 | 82.7 | 78.7 | -4.0 |
| kimi k3 | 88.3 | 85.0 | -3.3 |
| qwen3.6 27b | 59.3 | 60.7 | +1.4 |
| qwen3.6 35b a3b | 51.5 | 44.9 | -6.6 |
| qwen3.5 122b a10b | 49.4 | 47.6 | -1.8 |
| qwen3.5 397b a17b | 52.5 | 51.3 | -1.2 |
| nemotron 3 super | 31.0 | 38.6 | +7.6 |
| nemotron 3.5 lightning | 24.6 | 24.3 | -0.2 |

the honest conclusion is that these gaps are small. claimed numbers on this
particular benchmark hold up reasonably. the largest overstatement is
qwen3.6 35b a3b at -6.6, and part of that is the 2.0 to 2.1 version
difference; the largest gap in either direction is nemotron 3 super at +7.6,
where the lab *under*-claimed. anyone expecting the card numbers to collapse
under third-party testing will not find that here.

every row is a card that publishes terminal-bench and a model AA has measured,
which is what the joined data supports: six of the fourteen cards carrying a
terminal-bench claim have no AA counterpart, including qwen3.8 27b's 73.0.

### where it actually happened

**minimax m2.5** is the documented case. minimax claimed 80.2% on swe-bench
verified. openai sampled 27.6% of the tasks and published an audit within
eleven days finding flawed tests and training contamination; meta fair had
flagged repository leaks earlier via github issue #465; academic groups
published quantitative studies putting the inflation at 6.2 percentage points.
minimax m2.5 is now deprecated on artificial analysis. m2.7 and m3, the
successors, have not attracted the same criticism, and m2.7 publishes no card
claims at all in this capture -- AA measures its terminal-bench at 55.4 with
nothing to compare it against.

the broader finding from openai's audit generalizes past minimax: every
frontier model tested could reproduce verbatim gold patches or problem
statement specifics for some swe-bench verified tasks. swe-bench verified
should be read as contaminated for every model on this list.

### measuring it instead of alleging it

swe-bench verified is a fixed, public, four-year-old task set, which is what
makes the accusation above unfalsifiable from the outside.
[swe-rebench](https://swe-rebench.com/) rebuilds its tasks continuously from
pull requests merged after the fact and publishes results *per task-date
window*, so a model can be scored separately on tasks that predate its release
and tasks that cannot have been in its training data.

that comparison needs two corrections before it means anything, both applied by
`research/analyze-contamination`. later windows are not equally hard, so each
measurement is scored as a residual against the field on that same window; and
the field itself improves over time, which biases every model's drop-off
negative, so the result is centred on the cohort median. what is left is: did
this model lose more ground on unseen tasks than its contemporaries did?

the largest drop-offs across the 34 models with enough windows on both sides:

| model | released | pre-release | post-release | relative |
|---|---|--:|--:|--:|
| Qwen3-Next-80B-A3B-Instruct | 2025-09-11 | -0.4 | -17.3 | **-13.5** |
| Claude Opus 4.6-high | 2026-02-05 | +14.2 | +0.1 | **-10.7** |
| Kimi K2 Instruct 0905 | 2025-09-05 | +14.3 | +0.6 | **-10.2** |
| DeepSeek-V3-0324 | 2025-03-24 | +11.8 | -0.2 | **-8.5** |
| MiniMax M3 | 2026-05-31 | -2.8 | -12.1 | **-5.8** |
| ... | | | | |
| GLM-5.2 [high] | 2026-05-16 | +2.7 | +17.1 | **+17.8** |

read these as leads, not verdicts. the method cannot separate contamination
from a model that simply generalizes badly to unfamiliar code, several rows
rest on three windows on one side, and GLM-5.2's +17.8 is built on three
post-release windows -- more likely noise than a model that improves on
unfamiliar work.

**the roster barely appears here, and that is the finding.** of the twenty
models this document ranks, only gemma 4 31b has enough windows either side of
its own release to qualify, at -2.3, which is unremarkable. everything else on
the roster is too recent: released mid-2026, they have almost no task windows
predating them. so this method retires accusations about *last year's* models
rather than settling anything about this year's -- worth re-running in six
months, when the current roster has a pre-release history to be compared
against.

`research/data/swe-rebench.json` holds 12,440 windows for 116 models, split
per language (go, java, python, rust, typescript).

**minimax m3** drew "frontier claims, unverified benchmarks" coverage at
release for publishing scores against gpt-5.5 with no third-party
confirmation. AA has since measured it at 45.4, which is strong and roughly
consistent with the claims.

### what the community accuses, and who it clears

the accusation gets levelled constantly, so it is worth recording where it
actually sticks in r/LocalLLaMA rather than treating "benchmaxxed" as noise.

**laguna s 2.1 is the live accusation.** "Laguna performs worse than Qwen 3.6.
There is a lot of weird promotion of it oddly, but give it a try. Doesn't take
long to realize it is benchmaxxed." this is contested by several people who
rate it highly (see
[laguna is genuinely disputed](#laguna-s-21-is-genuinely-disputed)), but the
third-party numbers side with the sceptic: laguna s 2.1 sits at 0.239 gscore on
GBENCH, 88th of 97 models on that board, while poolside's own materials put it
far higher.
of everything in the strixhalo.yaml roster, this is the model whose paper
claims are least corroborated.

**deepseek v4 flash 0731 is the one that gets explicitly cleared.** from the august
highlight thread: "Nobody says the obvious, Deepseek v4 flash 0731. This blows
everything out of the water right now, **and one of the few where independent
benchmarks match what the lab published**." that matches what this document
found independently: a -4.0 gap between deepseek's claimed terminal-bench and
AA's measurement, the smallest of any model with a large claim, and a #2
ranking on GBENCH where nobody can train on the problem set.

**qwen draws a structural complaint rather than a fraud accusation.** the charge
is not fabricated numbers but optimising for what is measured: "the Qwen team
optimizes for benchmarks [...] I find them worse than Gemma for literally
anything else". the specific mechanism people name is verbosity, and separately
that "Qwen 27b and 35b [...] breaks down over 80k context" -- neither of which
any headline benchmark captures.

### the structural signal

a more useful benchmaxxing detector than claim-versus-measurement is the
spread between a model's scores on saturated benchmarks and on resistant ones.
mmlu, gsm8k and humaneval cluster at 88-99% for everything here and
differentiate nothing. the resistant end is tau2-banking, terminal-bench hard,
and AA's omniscience score, which measures whether a model knows what it does
not know.

sorted by that hallucination axis, negative meaning the model asserts more
than it knows:

| model | hallu | coding | reading |
|---|---:|---:|---|
| minimax m2.7 | +0.8 | 52.6 | calibrated |
| inkling small | -8.9 | 52.9 | calibrated |
| mimo v2.5 | -9.8 | 56.8 | calibrated |
| deepseek v4 flash 0731 | -14.3 | 69.1 | good for its score |
| ling 3.0 flash | -17.9 | 50.6 | fine |
| hy3 | -18.5 | 58.8 | fine |
| qwen3.6 27b | -20.0 | 53.7 | fine |
| qwen3.6 35b a3b | -22.2 | 41.9 | fine |
| muse glimmer | -32.9 | 49.0 | overconfident |
| step 3.7 flash | -37.3 | 39.6 | overconfident |
| nemotron 3 super | -41.5 | 37.7 | overconfident |
| qwen3.5 122b a10b | -41.5 | 45.7 | overconfident |
| gemma 4 31b | -47.9 | 43.4 | very overconfident |
| gpt-oss-120b | -49.2 | 30.4 | very overconfident |
| gemma 4 26b a4b | -50.8 | 39.3 | very overconfident |
| qwen3 coder next | -62.4 | 36.2 | worst in set |

the models with a decent coding score and a terrible hallucination score are
the ones to be suspicious of. **gemma 4 26b a4b** posts 39.3 coding and 39.0
terminal-bench while scoring -50.8 on hallucination and 11.0 on the agentic
index, the second lowest here. it presents well on short benchmarks and falls
apart on anything requiring sustained tool use. its own lab's cited
swe-bench verified figure is 17.4%.

**qwen3 coder next** is the clearest case. a coder-branded model with -62.4
hallucination, 5.4 on tau2-banking and an II of 21.3.

**gpt-oss-120b** deserves a specific note because its reputation exceeds its
measurements. II 24.1, coding 30.4, terminal-bench 26.2, hallucination -49.2.
it is fast and it fits, and on this hardware those are real virtues, but it
is not competitive on capability with anything above it in the table. it is a
2025 model still being recommended in 2026 roundups.

**qwen3.6 35b a3b** is worth flagging in the other direction. its card claims
swe-bench verified 73.4, close to the 27b's 77.2, but AA measures its agentic
index at 21.6 against the 27b's 27.5 and its tau2-banking at 9.3 against 16.7.
the 3b-active model's benchmark numbers survive third-party testing less well
than its dense sibling's. the paper scores suggest they are near peers; the
resistant benchmarks say they are not.

## forum sentiment

drawn from r/LocalLLaMA (scraped via old.reddit) and hacker news (algolia api),
january-august 2026. scores in brackets are reddit comment scores.

### qwen3.6 27b is the consensus daily driver

nothing else in this set comes close on reputation. "qwen 3.6 27b is the sweet
spot for local development" hit 1192 points on hn; the reddit threads are
larger still. the recurring phrasing is reliability rather than peak
capability:

> "Qwen3.6-27B is still my daily driver (at Q8_0, unquantized KV cache) for
> its unbeatable reliability and the fact that I can still use most of my VRAM
> for a second verifier model, my 7B FIM autocomplete model, and other tasks."
> [14]

> "3.6 27B is still the current king for reasonable local hosting (Deepseek v4
> Flash is just a bit out of reach of reasonable consumer hardware atm)" [128]

the MTP thread ("2.5x faster inference with Qwen 3.6 27B using MTP - finally a
viable option for local agentic coding", 1237 points) is what moved it from
too-slow to usable on unified memory.

### hy3 has loud advocates on 128gb, and not many of them

"Tencent-HY3 is the real deal on 128GB!" (288 points) is the most directly
relevant thread to this hardware, and the enthusiasm in it is real. the top
reply, from someone who reviewed it on video:

> "Significantly better coder than deepseek-v4-flash. Keep using
> deepseek-v4-flash only if speed is the primary concern. Decent amount better
> than MiniMax M3. Thinks a lot, which makes it feel slow. [...] Deepseek can
> fit 1million context whereas I can only get like 190k on Hy3." [88]

the counter-report is that hy3 degrades badly with context: "its speed drops
off brutally as context grows due to the architecture choices" [4]. another
user runs it not as the main agent but as an adversarial reviewer against a
frontier model, where it "catches his cowboy-asserted style bullshit better"
than deepseek or qwen [4].

**how thin is this?** across 134 threads there are 47 sentences mentioning hy3,
of which roughly three are both positive and specific to a 128gb machine -- the
OP above (running a macbook m5 max, not a strix halo), the video reviewer, and
one person calling it "by far the best model under 500b, and easily the best
model for 128GB even with a small quant" [5].

the dissent is about as well supported. from another thread: "Even 128GB is
getting weird. It's not quite enough to run good quants of the 300B class
models i.e. Hy3/DS4 Flash" [95]. someone listing their month-later stack has
"HY3-Q4 (kinda slow on my hardware, but decent?)" in the maybe pile [7].
another: "I've found Deepseek V4 flash at Q8 better than Hy3" [2]. and inside
the hy3 thread itself, the most detailed responder says qwen3.6 27b "is still
my daily driver" [14].

so this is not a cohort that has picked hy3. it is a small number of
enthusiastic reports against a similar number of lukewarm ones, on a model this
box can only run at 2.72 bpw. it is the clearest divergence from the
quant-adjusted table, which ranks hy3 sixth, but it is a reason to test rather
than a reason to believe.

### deepseek v4 flash 0731: strong, with a real complaint

"Deepseek v4 flash 0731 still not holding up" (162 points, 217 comments)
argues the model ignores rules files and skill definitions:

> "The biggest issue with preview was its inability to follow rules prompts and
> skills. It seems like no matter what you do it ignores them. [...] That's the
> only problem with these models and why they're not actually frontier level
> and not just benchmaxxed."

the thread pushes back hard. the most useful diagnosis is that deepseek
shipped no official jinja template, so every quant publisher wrote their own:

> "IMO DeepSeek kinda messed up by not providing an official Jinja template.
> Looking at Bartowski and Unsloth .ggufs, they have different Jinjas, one of
> which is rather barren and the other is full of [...] pleas and commands."
> [53]

unsloth's reply is that they validated theirs against 4000 conversations
for equivalence with the official implementation [15]. multiple heavy users
report no such problem: "DS4 Flash has been our workhorse and its been
reliable" [118]. the practical takeaway is to pin a known-good template rather
than assume the gguf's default is right.

there is also a community quant built specifically for this class of machine:
`Rednalreden/DeepSeek-V4-Flash-0731-dwarfstar-q2-gguf`, a single 80.8 gib file
with IQ2_XXS experts but Q8 attention projections, shared experts and output
layer. 13.7k downloads. "Try dwarf star. It's deepseek v4 optimized for 128 gb
builds. I switch between this and qwen 27b" [8]. it buys 16 gib of context
headroom over UD-IQ3_XXS at the cost of 2-bit routed experts.

### heavy quants of big models are unpopular

the strongest methodological pushback in the subreddit is against exactly the
comparison this document is making. on a post pitting inkling small at Q2
against qwen3.6 27b:

> "12B active just isn't enough for such a heavy quant to still be solvent on
> any remotely long-horizon task. If you can't fit a Q4/nvfp4 at minimum the
> model isn't worth using. And even those show heavy accumulated error if you
> have long context" [11]

> "This is not a model comparison. This is a VRAM-fitting comparison." [7]

the defense, also upvoted: "If you 'only' have 128 GB of RAM like Strix Halo,
M5 Max, or DGX Spark, this is absolutely a good comparison between models you
can run" [14]. both are right; the disagreement is about what the reader is
choosing between. this document assumes the reader is choosing what to load on
one 128gb box, which is the second framing.

### qwen has a benchmaxxing reputation, gemma has a token-efficiency one

the kaitchup dense shoot-off thread (191 points) is the sharpest version:

> "It's showing that the Qwen's are more benchmaxxed, and Gemma 4 31B is far
> more efficient with token use. So even though Gemma is a little slower for
> inference because of its size, you're basically getting things done faster."

> "the Qwen team optimizes for benchmarks. Other than a better by default
> frontend (they are RLmaxxed for this) [...] I find them worse than Gemma for
> literally anything else: raw coding, translation, general knowledge" [25]

with a specific mechanism: "Qwen waffles for sure with its thinking and it
genuinely needs the context size efficiency it has because it will happily
reach 200k context working on something that Gemma is at less than 100k for"
[16]. the opposing view is present too ("GEMMA4's instruction compliance is
much worse than qwen3.6, especially in terms of code writing" [7]), so treat
this as contested rather than settled.

tokens-to-completion is an axis none of the benchmark tables here capture, and
on bandwidth-limited hardware it matters as much as tokens per second.

### the 80-160b gap is the top hardware complaint

"We need a 80-160B model urgently. The unified memory device market needs more
Models" (655 points) is the sentiment that best describes this box's problem:

> "we have GPUs sitting between 64-128GB doing nothing useful because every
> model is either too small to bother with or too big to fit. Someone please
> cook a 100B sparse MoE." [146]

with a persuasive explanation for why the gap exists: model sizes cluster at
27b and 31b because that is what fits an 80gb h100, not because it is optimal
for anyone at home [54]. the ask is specifically "a model with Qwen 3.6
density, but scaled up to a 100B+ MoE" [26], which does not yet exist.

### muse glimmer, released 2026-08-10

too new to have a settled reputation. early reports are split. positive: "been
trying Q4_K_XL on a single 3090 this morning w/ pi for agentic coding, and so
far it seems to be performing great. Definitely on-par with 3.6 27B" [46], and
"stupid fast and has very small kv cache size" [10]. negative: "I've been using
the BF16 model through vllm and I haven't been very impressed [...] it's
painful to use and made a ton of mistakes Laguna would never make" [9], and
"skilled in the use of tools, but limited in intelligence" [7]. censorship
complaints are common ("Glimmer seems pretty censored?", 145 points). with
dflash it is reported at 60-150 t/s decode on a 3090 against 40 t/s without.

**its reception fell as the sample grew, even though its volume tripled**,
which is the clearest argument in this document for not scoring a model on its
launch week. tracked across three captures a day apart:

| capture | mentions | median rel | composite |
|---|--:|--:|--:|
| 2026-08-10 | 27 | 68 | 57.4 (5th) |
| 2026-08-11 (first pass) | 43 | 54 | 53.5 (6th) |
| 2026-08-11 (with listings) | 79 | 56 | 58.5 (5th) |

the launch-day cohort liked it distinctly more than everyone who arrived after.
the composite recovered only because *volume* nearly tripled -- more people
discussing it at a lower reception percentile -- so the two inputs moved in
opposite directions and largely cancelled. reading the launch-day 68 as its
reception would have been wrong by 12 points.

artificial analysis now scores it too: 35.1 intelligence, 49.0 coding, 22.9
agentic, which is mid-pack rather than front-running, against a day-one thread
titled "Muse-Glimmer-30B finally beats 3.6-27B for the size" (290 points, 150
comments). the thread is worth reading; the claim in its title is not yet
supported by anything measured here -- qwen3.6 27b is ahead on effective
coding (53.2 vs 48.5), agentic (27.2 vs 22.7) and composite, at a similar size.

### on benchmarks generally

"Confirmed: SWE Bench is now a benchmaxxed benchmark" (455 points) is the
canonical thread. the top comments converge on the same structural fix rather
than on blaming a particular lab:

> "benchmarks need to be seeded or have a private counterpart. Have a public
> seed so that people can independently verify [...] Then have a private seed
> that only the benchmarking website knows. If results drop, then you know a
> model was overfit" [101]

> "Private bench isn't sufficient, the data needs to be sourced privately as
> well. For example, SWEBenchPro tasks [...] were partially sourced from open
> source code bases which have the implementations, so it can be trained on
> even if the questions are private." [37]

[swe-rebench](https://swe-rebench.com), which refreshes its problem set
continuously, gets recommended as the live alternative [61]. the cynical
position is well represented: "benchmarks have no meanings when it comes to
LLM. just organize your own set of tests for the specific tasks you require"
[15].

one novel idea worth tracking is [Encode Bench](https://old.reddit.com/r/LocalLLaMA/comments/1v3dpsk/),
which asks models to return answers as base64. it correlates 0.91 with the AA
intelligence index and 0.94 with the agentic index, and because nobody trains
for it, it has not been gamed. the top reply proposes exactly the use this
document needs: "This might be a good benchmark to rank quantizations of the
same model" [72].

### strix halo specifically

the community reads the box as an MoE machine that disappoints on dense
models, which matches the speed table above. published measurements include
gpt-oss-120b at 55 t/s, qwen3-30b-a3b at ~100 t/s, and a 109b model at
18.3 t/s. rocm remains rough as of april 2026 first-impressions reports;
vulkan is slower but more reliable. unsloth added AMD support 21 days ago
(669 points), and vllm rocm landed in lemonade as an experimental backend.
nobody in the hy3 thread itself had tried it on strix halo, though a user in
another thread mentions running hy3 there alongside laguna and ds4 flash, in
passing and without a quality judgement.

## what is coming

one release will likely date this document within weeks, and one already has.

**qwen3.8-27b** landed while this capture was being written. announced
2026-08-02 alongside qwen3.8-max (2729 points), the ggufs were still empty
placeholder repos on 2026-08-13 -- `barozp/Qwen3.8-27B-GGUF` and a matching
`-MTP-GGUF`, zero files between them -- and `unsloth/Qwen3.8-27B-GGUF` was
created that same day and filled out on 2026-08-14 with the full quant ladder
from UD-IQ2_XXS to BF16 plus an mmproj for vision. it is sized in [models nothing has scored](#models-nothing-has-scored)
and in `registry/models.yaml` at Q8_0, the right
place for it: **artificial analysis, GBENCH, lmarena and swe-rebench have all
still scored nothing**, so it has no ranking here and cannot get one from this
document's own sources. what it has instead is uptake --
`unsloth/Qwen3.8-27B-GGUF` is at 1.9m downloads, bartowski and ggml-org both
shipped their own on 2026-08-14, and a dozen abliterated derivatives followed
within two days. treat the qwen3.6 27b recommendation as standing until one of
them measures the successor. the top of the line, **qwen3.8 2.4t a95b**
(II 57.7), landed open on 2026-08-12 and is twenty times too large for this box.

**longcat-flash-lite-sparse** (meituan) is a 69b-a3b with a ~983k context
window, weights up but no ggufs yet. that is squarely in the 80-160b gap this
hardware needs filled.

**glm 5.3** was announced on 2026-08-15, the largest new thread in this capture
at 1633 points, and it is an API release: the top comment restates that z.ai
"stated that weights will be forthcoming". artificial analysis has not scored
it and the hub carries no GGUF for it, so there is nothing here to rank. a
glm-5.2 air variant, which the subreddit repeatedly asks for, is still
unconfirmed.

**qwen3.8 35b a3b** has been sighted but not released (1148 points). it would
land in the same slot as qwen3.6 35b a3b -- the MoE alternative to the dense
27b, and the one people with less memory than this box actually want. the
thread's top comment is somebody on 8gb of vram reporting 27 t/s from the
a3b shape against "molasses" from a dense 27b, which is the whole argument for
it.

## method

### what is included

only models that (a) publish open weights, (b) have GGUF quants from a
recognized publisher, and (c) fit in the practical resident budget of a
128gb strix halo. models that need more memory than the box has are listed
in [does not fit](#does-not-fit) rather than silently dropped.

benchmark numbers come from artificial analysis unless marked otherwise.
their runs are third party and use one harness across all models, so they
are comparable in a way that model cards are not. self reported card numbers
appear only in [benchmaxxing](#benchmaxxing), where the gap between the two
is the point.

three further sources cross-check AA rather than feed it: GBENCH (played, not
graded), lmarena (human preference) and swe-rebench (tasks dated after a
model's release). only GBENCH is in the composite; the other two are reported
alongside it, for reasons given in each section.

**a note on comparing captures.** between 2026-08-10 and 2026-08-11 artificial
analysis set `agenticIndex` to null for 38 models, dropping the sample behind
the double-counting regression from 181 models to 143; by 2026-08-14 it had
recovered to 159. the fit barely moves across all of that (R^2 0.9856 ->
0.9838 -> 0.9846, coefficients 0.415/0.407 -> 0.413/0.406 -> 0.411/0.408), so
the conclusion stands, but a reader diffing two captures of
`research/data/artificial-analysis.json` should expect the sample size to move.
no model on this roster lost its agentic score; the nulled entries are
non-reasoning variants and small models.

### the memory envelope

128gb of unified memory is 119.2gib. the practical ceiling for a llama-server
process is about 110gib once the display, the page cache and the compute
buffers are accounted for. what is left for weights depends on the kv cache,
which varies far more between models than the weights do:

```
119.2 gib  total
-  9    gib  host, display, compute buffers
-  5    gib  kv cache, compressed-attention model at long ctx
= 105   gib  weights          <- the budget used in this document
```

**105gib is a measured figure, not a derived one.** the earlier version of this
document reserved 14gib for kv and used 96gib, which turned out to be too
conservative: deepseek v4 flash 0731 runs UD-IQ3_XXS (97.1gib) alongside a
10.2gib dspark drafter, so 107.3gib resident, and glm-4.5-air has been run at
~109gib. models using compressed attention (deepseek v4's CSA plus HCA, ling
3.0's latent kv) spend far less on cache than the generic reserve assumes.

a model with a conventional attention stack at 262k context will not have this
much room. treat 105gib as the ceiling for the compressed-attention MoEs that
dominate the fitting list, and re-derive it if you run something else at long
context. `research/build-tables --budget N` regenerates every table at a
different figure.

### how much the budget choice matters

not much, which is the useful part. moving the budget from 96gib to 105gib
upgrades five models by one quant step -- deepseek v4 flash 0731 from UD-Q2_K_XL to
UD-IQ3_XXS (45.6 to 47.6 effective), inkling small from IQ3_XXS to IQ3_S (37.9
to 38.8), minimax m2.7, qwen3.5 122b and nemotron 3 super each by a fraction --
and changes the ordering only between minimax m2.7 and qwen3.6 27b, which were
0.2 apart to begin with.

the headline conclusion survives at either budget: deepseek v4 flash 0731 leads by
about 9 points, and everything from rank 2 to rank 6 sits inside a band of
about 1.7 points that includes a 27.1gib dense model.

two hardware facts drive every recommendation below:

- **bandwidth, not compute, is the limit.** roughly 256gb/s peak, and llama.cpp
  realizes 160-200gb/s of it. decode speed is set by how many bytes of weights
  are read per token, which for an MoE is the active parameters, not the total.
- **total parameters cost memory, active parameters cost time.** a 284b model
  with 13b active occupies as much memory as a 284b dense model but decodes
  about 20x faster. this is why every serious candidate here is an MoE.

### quant publisher coverage

<!-- generated by research/analyze-catalog --coverage -->

| model | AngelSlim | AtomicChat | DavidAU | LiquidAI | antirez | bartowski | ggml-org | huihui-ai | meta-models | mradermacher | ornith-ai | prism-ml | unsloth |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bonsai 27b |  |  |  |  |  |  |  |  |  |  |  | yes |  |
| deepseek v4 flash 0731 |  | yes |  |  |  | yes | yes | yes |  |  |  |  | yes |
| fable-fusion 711 |  |  | yes |  |  |  |  |  |  | yes |  |  |  |
| gemma 4 12b |  | yes |  |  |  | yes | yes | yes |  |  |  |  | yes |
| gemma 4 26b a4b |  | yes |  |  |  | yes | yes | yes |  | yes |  |  | yes |
| gemma 4 31b |  | yes | yes |  |  | yes | yes | yes |  | yes |  |  | yes |
| glm-4.5-air |  |  |  |  |  | yes |  |  |  |  |  |  | yes |
| glm-5.2 |  |  |  |  | yes |  |  | yes |  |  |  |  | yes |
| gpt-oss-120b |  |  | yes |  |  | yes | yes |  |  |  |  |  | yes |
| hy3 | yes | yes |  |  |  | yes |  |  |  |  |  |  |  |
| inkling small |  | yes |  |  |  |  |  |  |  |  |  |  | yes |
| kimi k3 |  | yes |  |  |  |  |  |  |  |  |  |  | yes |
| laguna s 2.1 |  | yes |  |  | yes | yes | yes | yes |  |  |  |  | yes |
| ling 3.0 flash |  | yes |  |  |  |  |  |  |  |  |  |  |  |
| mimo v2.5 |  |  |  |  |  | yes |  | yes |  |  |  |  | yes |
| minimax m2.7 |  |  |  |  |  | yes |  |  |  |  |  |  | yes |
| minimax m3 |  |  |  |  |  | yes | yes |  |  |  |  |  | yes |
| mistral medium 3.5 |  |  |  |  |  | yes |  |  |  |  |  |  | yes |
| muse glimmer |  | yes |  |  |  | yes |  |  | yes | yes |  |  | yes |
| nemotron 3 super |  |  |  |  |  | yes | yes |  |  |  |  |  | yes |
| nemotron 3.5 lightning |  | yes |  |  |  | yes | yes |  |  | yes |  |  | yes |
| ornith 1.0 35b |  | yes |  |  |  | yes |  | yes |  |  | yes |  | yes |
| qwen-agentworld 35b a3b |  | yes |  |  |  |  |  |  |  |  |  |  | yes |
| qwen3 coder next |  | yes |  |  |  | yes | yes |  |  |  |  |  | yes |
| qwen3.5 122b a10b |  |  |  |  |  | yes |  | yes |  |  |  |  | yes |
| qwen3.5 397b a17b |  |  |  |  |  | yes |  | yes |  |  |  |  | yes |
| qwen3.6 27b |  | yes | yes |  |  | yes | yes | yes |  | yes |  |  | yes |
| qwen3.6 35b a3b |  | yes |  |  |  | yes | yes | yes |  | yes |  |  | yes |
| qwen3.8 27b |  | yes |  |  |  | yes | yes | yes |  | yes |  |  | yes |
| step 3.7 flash |  |  |  |  |  | yes |  |  |  |  |  |  | yes |
| ternary bonsai 27b |  |  |  |  |  |  |  |  |  |  |  | yes |  |

generated by searching 1,410 GGUF repos from 13 publishers, so a blank means no
repo whose name matches, not a verified absence. the four columns to trust are
unsloth, bartowski, mradermacher and ggml-org; the rest publish either their own
model (AngelSlim ships hy3, AtomicChat ling 3.0) or community variants.

unsloth's `UD-*` dynamic quants measurably beat flat imatrix at the same file
size (see [quantization](#quantization-size-versus-intelligence)), so prefer
them where they exist. bartowski is the fallback and is consistently
imatrix-calibrated. mradermacher's `i1-*` repos cover the long tail but are
the least benchmarked of the three.

**two roster models have no unsloth quant at all**: hy3 (AngelSlim, tencent's
own team, plus bartowski) and ling 3.0 flash (AtomicChat only, and nothing
else in the table). ling 3.0 flash is recommended third in this document on
one publisher's quant, with 8 reddit mentions -- that is the thinnest evidence
base behind any pick here.

### what the roster is missing

the roster is hand-curated, which biases it toward models somebody wrote a
release post about. `research/fetch-hf-catalog` asks the hub the opposite
question -- what is being downloaded in GGUF form right now -- and
`analyze-catalog --candidates` filters it to plausible additions. three things
fell out that this document had wrong or absent:

- **`unsloth/Qwen3.6-27B-MTP-GGUF` is a different repo from
  `unsloth/Qwen3.6-27B-GGUF`**, with identically-named files 0.42gib larger.
  the MTP head is in the weights, not a sidecar, so the plain repo cannot
  speculate. every size for qwen3.6 27b in this document was 0.42gib low until
  this capture. unsloth did not repeat the split for qwen3.8 27b: there is one
  repo, and its `blk.64` is the nextn head.
- **ornith 1.0 35b and qwen-agentworld 35b a3b are absent from this document
  and present in `registry/models.yaml`** -- they are run on the
  target machine and were never ranked, because artificial analysis does not
  score either one. neither does GBENCH. so the composite structurally cannot
  see them, which is a limit of the method rather than a judgement about the
  models. `ornith-ai/Ornith-1.0-35B-GGUF` has 3.9m downloads.
- **hardware-specific requantizations exist and are easy to miss.** sorting by
  creation date rather than downloads surfaces
  `kingjones777/Muse-Glimmer-30B-ROCmFP4-Strix-Halo-DFlash-GGUF` and
  `JoJoLabs/Qwen3.6-27B-MTP-ROCmFPX-GGUF`, both built for this box within a day
  of the model landing. they are unevaluated, but they are the answer to the
  muse glimmer vulkan problem above if they work.

two ling 3.0 flash quants are worth knowing about:
`raulvidis/Ling-3.0-flash-ROCmFP4-STRIX-MTP-GGUF` is built specifically for
this hardware with the MTP sidecar included.

## sources

- [artificial analysis intelligence index](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index)
- [artificial analysis: glm-5.2 leads open weights](https://artificialanalysis.ai/articles/glm-5-2-is-the-new-leading-open-weights-model-on-the-artificial-analysis-intelligence-index)
- [unsloth dynamic v2.0 ggufs](https://unsloth.ai/blog/dynamic-v2)
- [unsloth qwen3.5 gguf benchmarks](https://unsloth.ai/docs/models/qwen3.5/gguf-benchmarks)
- [unsloth dynamic ggufs on aider polyglot](https://unsloth.ai/docs/basics/unsloth-dynamic-2.0-ggufs/unsloth-dynamic-ggufs-on-aider-polyglot)
- [unsloth: deepseek-v4 how to run locally](https://unsloth.ai/docs/models/deepseek-v4)
- [unsloth: kimi k3 how to run locally](https://unsloth.ai/docs/models/kimi-k3)
- [flat score, amplified failures: quantized llm agents (arxiv 2607.27275)](https://arxiv.org/html/2607.27275v1)
- [kv cache quantization and long-horizon agentic coding](https://dasroot.net/posts/2026/05/kv-cache-quantization-agentic-coding-long-horizon/)
- [local llm quantization quality benchmarks 2026](https://presenc.ai/research/local-llm-quantization-quality-benchmarks-2026)
- [minimax m2.5 benchmark fraud debate](https://www.aicerts.ai/news/minimax-m2-5-sparks-ai-benchmark-fraud-debate/)
- [minimax m3: frontier claims, unverified benchmarks](https://www.techtimes.com/articles/317532/20260601/minimax-m3-open-weight-coding-model-frontier-claims-unverified-benchmarks.htm)
- [what is benchmaxxing](https://ctaio.dev/en/labs/benchmaxxing/)
- [amd strix halo backend benchmarks](https://kyuz0.github.io/amd-strix-halo-toolboxes/)
- [benchmarking llama.cpp MTP on strix halo](https://calebcoffie.com/blog/benchmarking-llama-cpp-mtp-on-strix-halo)
- [strix halo setup and benchmark guide](https://github.com/hogeheer499-commits/strix-halo-guide)
- [ryzen ai max+ 395 for local llms](https://runaihome.com/blog/ryzen-ai-max-395-strix-halo-local-llm-2026/)
- model cards: [qwen3.6-27b](https://huggingface.co/Qwen/Qwen3.6-27B), [qwen3.6-35b-a3b](https://huggingface.co/Qwen/Qwen3.6-35B-A3B), [deepseek-v4-flash](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash), [minimax-m2.7](https://huggingface.co/MiniMaxAI/MiniMax-M2.7), [muse-glimmer-30b](https://huggingface.co/meta-models/Muse-Glimmer-30B)
- artificial analysis per-model page: [muse glimmer](https://artificialanalysis.ai/models/muse-glimmer)
- [gert labs GBENCH rankings](https://gertlabs.com/rankings?ow=1), [agentic coding board](https://gertlabs.com/rankings?ow=1&mode=agentic_coding), and its public `api/v1/global/rankings`
- [lmarena leaderboard](https://lmarena.ai/leaderboard) (human preference, style-controlled text board)
- [swe-rebench](https://swe-rebench.com/) (swe tasks rebuilt continuously from post-hoc pull requests)
- [terminal-bench 2.0 leaderboard](https://www.tbench.ai/leaderboard/terminal-bench/2.0) and the [submission dataset](https://huggingface.co/datasets/harborframework/terminal-bench-2-leaderboard) behind it, which is where the per-task results live
- [llama.cpp issues](https://github.com/ggml-org/llama.cpp/issues) and huggingface per-repo discussion tabs
- [level1techs forum](https://forum.level1techs.com/) (a hardware forum, so the strix halo posters own one)
- the huggingface hub model listing, for what exists rather than what was announced

### r/LocalLLaMA threads quoted

| thread | points |
|---|--:|
| [the best model is the one you can actually run](https://old.reddit.com/r/LocalLLaMA/comments/1ux9xze/) | 2107 |
| [qwen3.8-27b announced alongside qwen3.8-max](https://old.reddit.com/r/LocalLLaMA/comments/1ve0psn/) | 2729 |
| [introducing muse glimmer](https://old.reddit.com/r/LocalLLaMA/comments/1vkgsum/) | 1611 |
| [2.5x faster inference with qwen 3.6 27b using MTP](https://old.reddit.com/r/LocalLLaMA/comments/1t57xuu/) | 1237 |
| [qwen3.6-27b vs coder-next](https://old.reddit.com/r/LocalLLaMA/comments/1t2ab5y/) | 1136 |
| [we need a 80-160b model urgently](https://old.reddit.com/r/LocalLLaMA/comments/1u8kr2o/) | 655 |
| [qwen 3.5 craters on hard coding tasks](https://old.reddit.com/r/LocalLLaMA/comments/1reds0p/) | 556 |
| [confirmed: SWE bench is now a benchmaxxed benchmark](https://old.reddit.com/r/LocalLLaMA/comments/1swfdbj/) | 455 |
| [tencent-hy3 is the real deal on 128GB](https://old.reddit.com/r/LocalLLaMA/comments/1usy9ie/) | 288 |
| [muse glimmer benchmark](https://old.reddit.com/r/LocalLLaMA/comments/1vkxpnd/) | 250 |
| [dense model shoot-off: gemma 4 31b vs qwen3.6/5 27b](https://old.reddit.com/r/LocalLLaMA/comments/1t4nkez/) | 191 |
| [early signs that muse-glimmer-30b might quantize very well](https://old.reddit.com/r/LocalLLaMA/comments/1vkn16q/) | 180 |
| [hy3 1bit 89-93 GB](https://old.reddit.com/r/LocalLLaMA/comments/1uxm2d8/) | 175 |
| [deepseek v4 flash 0731 still not holding up](https://old.reddit.com/r/LocalLLaMA/comments/1vct09w/) | 162 |
| [base64 encode bench vs AA intelligence index](https://old.reddit.com/r/LocalLLaMA/comments/1v3dpsk/) | 152 |
| [inkling-small-276b-12b effort max vs qwen3.6-27b](https://old.reddit.com/r/LocalLLaMA/comments/1vbajj8/) | 126 |
| [what's still in your stack a month later](https://old.reddit.com/r/LocalLLaMA/comments/1va1zoc/) | 122 |
| [deepseek v4 flash 0731 / hy3 / qwen3.6 27b for agentic coding](https://old.reddit.com/r/LocalLLaMA/comments/1v6jlva/) | 83 |
| [70-80b contenders](https://old.reddit.com/r/LocalLLaMA/comments/1vc4d23/) | 58 |

### local data

everything above is captured under [research/](research/README.md) and
committed, so the comparison can be audited or re-derived without refetching:

| file | contents |
|---|---|
| `research/data/artificial-analysis.json` | 608 models, 348 open weights, scores and params |
| `research/data/gbench.json` | 97 models, per-language and per-mode game results |
| `research/data/gbench-compare-observed.json` | published per-language compare values |
| `research/data/gguf-sizes.json` | real byte totals per quant tag for 70 repos |
| `research/data/reddit-localllama.json` | 38 searches, 3 listings, 161 threads, 12,822 comments with reply depth |
| `research/data/hackernews.json` | 9 queries, 54 stories with top comments |
| `research/data/lmarena.json` | 11 boards, 456 models, elo with vote counts |
| `research/data/swe-rebench.json` | 116 models, 12,440 task-date windows, 5 languages |
| `research/data/tbench.json` | terminal-bench 2.0: 73 submissions x 90 tasks, 14,340 per-task trials |
| `research/data/hf-discussions.json` | 542 discussions across 28 repos, 256 with full threads |
| `research/data/github-issues.json` | 321 llama.cpp issues with bodies, 20 queries |
| `research/data/level1techs.json` | 165 topics, 600 posts from 9 searches |
| `research/data/hf-catalog.json` | 300 trending + 1411 publisher repos, for discovery |
| `research/data/hf-catalog-new.json` | the same listing by creation date, for same-day releases |
| `research/data/epoch.json` | epoch.ai: 819 ECI rows and 74 benchmarks, 10 of them epoch's own runs |
| `research/data/model-facts.json` | derived per-model facts: arch, params, native ctx, mtp, thinking knob |

the tables in this document are generated from those files by
`research/build-tables`. the collection scripts and refresh instructions are in
[research/README.md](research/README.md).
