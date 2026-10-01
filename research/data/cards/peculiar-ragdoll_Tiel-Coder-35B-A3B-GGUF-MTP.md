---
license: mit
base_model: ornith-ai/Ornith-1.5-35B-A3B
base_model_relation: quantized
pipeline_tag: image-text-to-text
library_name: gguf
language:
  - en
  - zh
tags:
  - gguf
  - llama.cpp
  - qwen35moe
  - moe
  - imatrix
  - unsloth-dynamic
  - mtp
  - speculative-decoding
  - agentic-coding
  - token-efficient
  - vision
---

<div align="center">
  <img src="assets/tiel_banner_eyebrow.png" alt="TielCoder — Ornith-1.5 35B-A3B, sharpened, dynamically quantized" width="100%">
</div>

<div align="center">
  <img src="assets/card_tiel_swe.png" alt="SWE-bench-Live: Tiel solves 12 of 25, level with Opus 4.6 and ahead of KAT-Coder, Nail, stock Qwen3.6-35B-A3B and Ornith" width="100%">
</div>

# Straight to the point

*Tiel* is the fast coder of the arsenal. At 4-bit quantization and 23 GB it fixes real codebase issues at the rate (and speed, with
the right GPU) of Opus 4.6 medium, while holding the best multi-turn conversation of any local model we
have measured. It is also cheerfully bad at trivia.

Pick it for work. Pick something else for exams.

> **This is [Ornith-1.5-35B-A3B](https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B) re-quantized
> dynamically with our own imatrix and carrying the [Sharp chat template](https://huggingface.co/peculiar-ragdoll/Qwen-Sharp-Chat-Templates)**
> inside the GGUF. Find the non-MTP GGUFs [here](https://huggingface.co/peculiar-ragdoll/Tiel-Coder-35B-A3B-GGUF), and the non-MTP MLX
> version [here](https://huggingface.co/peculiar-ragdoll/Tiel-Coder-35B-A3B-MLX-oQ4e).
> **The uncensored and improved CyberTiel is out now!** [Get it here](https://huggingface.co/peculiar-ragdoll/Cyber-Tiel-Coder-35B-A3B-GGUF-MTP).

## The numbers

<div align="center">
  Where it sits against the other local builds
  <img src="assets/card_tiel_local.png" alt="SWE-bench-Live: Qwen3.8-27B solves 16 of 25 at 50.2 minutes per attempt, Dirk 15 at 20.1, TielCoder 12 at 8.6, stock Qwen3.6-35B-A3B 8 at 5.5" width="100%">
  Multi-turn conversation
  <img src="assets/card_tiel_claw.png" alt="Claw-Eval multi-turn: Tiel 67.2 overall against Ornith 65.3 and Nail 60.5, over 114 scored conversations each" width="100%">
  Reasoning and knowledge
  <img src="assets/card_tiel_mmlu.png" alt="MMLU-Pro: Tiel 73.7 against Nail 84.0, both at 4-bit, with the control arm isolating the template" width="100%">
</div>

**Where it stands.** On 25 SWE-bench-Live problems Tiel fixes 12 — the same as Opus 4.6 (medium),
four more than Ornith-1.5 itself, three more than Nail, and four more than Sonnet 5 (medium). Among
models of its own class it is first; the ones ahead are dense 27Bs and Opus 5. Its time per attempt
is also steadier than Nail's: an 8.6 minute median against 7.2, but a 12.3 minute mean against 15.7,
because it lacks Nail's tail of expensive attempts.

**How it talks.** On Claw-Eval's multi-turn tasks Tiel scores 67.2 against Nail's 60.5 and its own
base's 65.3, over 114 scored conversations each. It earns that by answering better rather than by
asking more: against the base it is 3.8 points up on answer quality and 5.1 down on clarifying
questions. The score weights answers four to one, so the trade pays — but if you want a model that
interrogates a vague request before acting, the base does that better.

**What it costs.** 73.7 on MMLU-Pro against Nail's 84.0, both at 4-bit. Most of that is inherited
rather than built: Ornith-1.5 scores 78.0 where stock Qwen3.6-35B-A3B scores 85.3. Our quantization
is not the cause — the same quant carrying Ornith's own template scores exactly what Ornith scores.
The remaining 4.3 points are the Sharp template buying shorter answers, which is the trade this
build exists to make.

**Which one.** Agentic coding, or long conversations that have to stay useful → Tiel. Exam-style
knowledge and hard reasoning → [Nail](https://huggingface.co/peculiar-ragdoll/Nail-Qwen3.6-35B-A3B-GGUF),
which is 10.3 points better on MMLU-Pro and 6.7 worse in conversation.
The most fixes per problem regardless of weight → [Dirk](https://huggingface.co/peculiar-ragdoll/Dirk-Qwen3.8-27B-GGUF),
the dense 27B that solves 15 of the same 25 — one behind stock Qwen3.8-27B, at 2.5x its speed.

## Run it

The MoE architecture makes *Tiel* fast, even on smaller GPUs with partial GPU offloading, and makes the context KV small in RAM (<5 GB RAM for 262k context at 16-bit KV precision) compared to 27B dense. We do not recommend going below UD-Q4 simply to fit the whole model in GPU VRAM: when you can fit the model and context KV across your RAM+VRAM, pick a Q4 quant or larger that you can run with a sizable context (131k-262k) in at least q8_0 KV, for agentic coding.

The "fits" column below is therefore about your **combined available RAM+VRAM**, after OS and other processes take their share.

| file | size | fits | notes |
|---|--:|:--|---|
| `Tiel-Coder-35B-A3B-MTP-UD-Q2_K_XL.gguf` | 12.7 GB | 16 GB | **THE LAST RESORT**; 2-bit gives up real ability, and struggles with agentic coding. Use anything larger, wherever it fits |
| `Tiel-Coder-35B-A3B-MTP-UD-IQ3_XXS.gguf` | 13.6 GB | 16 GB | **the 16 GB pick** — significantly better than Q2_K_XL for under a gigabyte more |
| `Tiel-Coder-35B-A3B-MTP-UD-Q3_K_XL.gguf` | 17.2 GB | 24 GB | 3-bit with plenty of context room; prefer IQ4_XS below unless you need the extra ~1 GB |
| `Tiel-Coder-35B-A3B-MTP-UD-IQ4_XS.gguf` | 18.1 GB | 24 GB | 4-bit quality with the most context headroom of any 4-bit tier |
| `Tiel-Coder-35B-A3B-MTP-UD-Q4_K_S.gguf` | 21.3 GB | 24 GB | tight 4-bit; useful when Q4_K_XL leaves too little room |
| `Tiel-Coder-35B-A3B-MTP-UD-Q4_K_XL.gguf` | 22.7 GB | 24-32 GB | **start here** — the benchmarked tier plus the head; snug on 24 GB, comfortable on 32 |
| `Tiel-Coder-35B-A3B-MTP-UD-Q5_K_XL.gguf` | 27.0 GB | 32 GB | the **32 GB** pick |
| `Tiel-Coder-35B-A3B-MTP-UD-Q6_K_XL.gguf` | 32.2 GB | 48 GB | near-lossless; will not leave usable context on 32 GB |
| `Tiel-Coder-35B-A3B-MTP-UD-Q8_K_XL.gguf` | 38.8 GB | 48 GB | reference |

Each tier is its stripped counterpart in [Tiel-Coder-35B-A3B-GGUF](https://huggingface.co/peculiar-ragdoll/Tiel-Coder-35B-A3B-GGUF) plus **0.4 GB** of
MTP head — the same block at the same precision (**Q3_K**) in every tier, because the recipe pins
it rather than letting it ride the tier's own bit-width. The head only *drafts*, so we swept its
precision from Q8_0 down to Q2_K and found draft acceptance flat down to Q3_K — 0.817/0.733 on
two prompts against 0.821/0.729 at Q8_0 — and slipping only at Q2_K (0.807/0.721). It therefore ships small,
quantized straight from the trained BF16 head, saving ~0.5 GB per tier at no measurable cost
to acceptance or speed.

To download and serve, replace the gguf names in the command below with your preferred quant:

```bash
hf download peculiar-ragdoll/Tiel-Coder-35B-A3B-GGUF-MTP \
  Tiel-Coder-35B-A3B-MTP-UD-Q4_K_XL.gguf mmproj-BF16.gguf --local-dir Tiel-MTP
llama-server -m Tiel-MTP/Tiel-Coder-35B-A3B-MTP-UD-Q4_K_XL.gguf -ngl 99 --jinja \
  --spec-type draft-mtp
```

`--spec-type draft-mtp` turns the head on at llama.cpp's defaults. Two knobs tune it, and what they
should be set to depends on your hardware — see below.

**The head does nothing unless you ask for it.** Without `--spec-type draft-mtp` llama.cpp ignores
those tensors entirely and you are running the base model carrying 0.4 GB of dead weight — in which
case take the [stripped ladder](https://huggingface.co/peculiar-ragdoll/Tiel-Coder-35B-A3B-GGUF) instead, which is the same model in
less space.

Sampling: `temperature 1.0`, `top_p 0.95`, `top_k 20`. For agentic coding we ran `temperature 0.6`.

**It can see.** Vision works exactly as on the base repo — `mmproj-BF16.gguf`, Ornith's own projector
passed through unmodified, shared by every tier.

## The multi-token-prediction head

Ornith-1.5 ships an MTP (`nextn`) block that drafts a token ahead of the main model, and this repo
exists to keep it.

**It was broken, and now it is not.** When our first ladder was baked, that block was untrained:
every matrix sat at a standard deviation of 0.020 with kurtosis 3.00 and a largest value of 5
standard deviations, which is a fresh random initialization. Drafts from random weights are accepted
at chance, so we stripped it. Ornith replaced it on **2026-08-23**, re-uploading a single shard with
a trained head. We measured the replacement rather than take the announcement on faith: kurtosis
**25.1** with a 98-sigma outlier, and **825** on the `nextn` projection. That is a trained network.

**What it did on our hardware.** Sweeping llama.cpp's two knobs on `UD-Q4_K_XL`, against the same
model with speculation switched off:

| `--spec-draft-n-max` | `--spec-draft-p-min` | tok/s | vs off | accepted |
|--:|--:|--:|--:|--:|
| — (off) | — | 77.4 | 1.00x | — |
| 1 | 0.0 | 94.4 | 1.22x | 83.3% |
| 3 | 0.0 | 89.9 | 1.16x | 59.9% |
| 8 | 0.0 | 46.5 | 0.60x | 30.2% |
| 1 | 0.8 | 85.3 | 1.10x | 96.0% |
| 3 | 0.8 | 86.0 | 1.11x | 92.7% |
| 8 | 0.8 | 82.3 | 1.06x | 90.1% |

Those are our numbers on our box, not a specification. The gain comes from verifying several tokens
in one forward pass instead of decoding them one at a time, so it turns on how your hardware prices
a batched pass against a single-token one — which moves with the GPU, the tier you run, the context
length, and whatever else is resident. Short drafts happened to win here and long ones lost badly;
that balance is precisely the part that differs between machines.

**So sweep it.** It takes a few minutes and the two knobs pull against each other:

- `--spec-draft-n-max` — how many tokens to draft per step. Drafting further ahead wins more when
  the guess lands and wastes more when it does not, and acceptance falls the further ahead you go.
- `--spec-draft-p-min` — discard a draft whose probability is below this. Raising it lifts the
  acceptance rate and wastes less verification, at the cost of drafting less often.

**Judge by tok/s, not by acceptance rate.** They come apart: our highest-acceptance setting
(96.0%) was slower than our fastest one (83.3%), because it bought that acceptance
by drafting less. Time it end to end against `--spec-type none` on prompts that look like your work.

## How the imatrix was made

Every tier is quantized against an importance matrix we generated ourselves, rather than a
borrowed one. The calibration corpus is 49 M characters drawn from
[eaddario/imatrix-calibration](https://huggingface.co/datasets/eaddario/imatrix-calibration) (MIT):
about three quarters `code_medium` and one quarter `combined_all_large`, interleaved so the two
alternate throughout rather than sitting in separate halves. That mix is deliberate — Tiel is meant
for coding, so the corpus leans that way, while the combined slice keeps maths, tool-calling and
non-English text represented so those paths are not the ones that get quantized carelessly.

The matrix was measured on a Q8_0 of the original BF16 weights, over 3,000 chunks of 512 tokens
(~1.5 M tokens), which is enough for every expert to be exercised many times over — this is a
256-expert mixture that routes 8 per token, so a short corpus would leave some experts barely seen.
The shipped tiers are then quantized from the BF16 source using that matrix. **These MTP tiers reuse that exact matrix**, unchanged: the fix upstream touched only the MTP tensors, which an importance matrix never covers anyway, so re-measuring would have produced the same file.

**The matrix itself ships here**, as `Tiel-Coder-35B-A3B.imatrix.gguf` (183 MiB, 510 tensors) — so a
tier we don't ship is one command away, without spending an hour and a half measuring your own:

```bash
hf download peculiar-ragdoll/Tiel-Coder-35B-A3B-GGUF Tiel-Coder-35B-A3B.imatrix.gguf --local-dir .
llama-quantize --imatrix Tiel-Coder-35B-A3B.imatrix.gguf Ornith-1.5-35B-BF16.gguf out.gguf IQ4_XS
```

Be clear about what that does *not* give you: the tiers in the table above are cut with per-tensor
Dynamic recipes layered on top of this matrix, and they carry the Sharp template. A plain
`llama-quantize` from the upstream BF16 reproduces neither.

eaddario's code slice is itself built from
[Open-Critic-GPT](https://huggingface.co/datasets/Vezora/Open-Critic-GPT),
[opc-sft-stage2](https://huggingface.co/datasets/OpenCoder-LLM/opc-sft-stage2),
[Magicoder-Evol-Instruct-110K](https://huggingface.co/datasets/ise-uiuc/Magicoder-Evol-Instruct-110K)
and [McEval-Instruct](https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct).

## Limitations

- **Exam scores are its weak axis.** If you are picking on MMLU-Pro, Nail is 10.3 points better.
- **It asks fewer clarifying questions than its base**, by 5.1 points. Terser is not always better;
  a vague request gets answered rather than questioned.
- Benchmarks are one run per problem on SWE-bench-Live and three seeds on MMLU-Pro. Treat small
  differences as noise.
- Chinese and English only, inherited from the base.

## Credits

- [**ornith-ai**](https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B) — the Ornith-1.5-35B-A3B weights (MIT).
- [**Unsloth**](https://huggingface.co/unsloth) — the Dynamic GGUF quantization method this reproduces.
- [**froggeric**](https://huggingface.co/froggeric/Qwen-Fixed-Chat-Templates) — the template lineage Sharp builds on.
- [**eaddario**](https://huggingface.co/datasets/eaddario/imatrix-calibration) — the calibration corpora the imatrix was measured on (MIT).
- [**llama.cpp**](https://github.com/ggml-org/llama.cpp) — `llama-quantize` / `llama-imatrix` / `llama-server`.

MIT, inheriting Ornith-1.5's license.
