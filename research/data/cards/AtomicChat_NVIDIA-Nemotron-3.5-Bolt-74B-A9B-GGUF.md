---
base_model: nvidia/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-BF16
base_model_relation: quantized
quantized_by: AtomicChat
pipeline_tag: image-text-to-text
library_name: gguf
license: other
tags:
- atomic-dynamic
- gguf
- llama.cpp
- nvidia
- imatrix
- quantized
- conversational
- atomic-chat
---

# NVIDIA Nemotron 3.5 Bolt 74B-A9B · Atomic Dynamic GGUF
<p style="margin-top: 0; margin-bottom: 0;">
  <em><b>Atomic Dynamic</b> (AD) quants, built from NVIDIA's original BF16 weights with our own importance matrix. At 21.9 GB, <code>AD-IQ1_M_S</code> stays closer to the original than NVIDIA's own 22.0 GB 2-bit file, measured side by side on one stand. The <a href="https://huggingface.co/datasets/AtomicChat/calib-corpora">calibration corpora</a> behind our builds are public.</em>
</p>
<div style="display: flex; gap: 8px; align-items: center; margin-top: 10px; margin-bottom: 10px;">
  <a href="https://atomic.chat/?utm_source=huggingface&utm_medium=referral&utm_campaign=hf_nvidia_nemotron_3_5_bolt_74b_a9b&utm_content=btn_atomic"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_atomic.png" width="162" alt="Atomic Chat"></a>
  <a href="https://discord.gg/8wGSsvmg4V"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_discord.png" width="119" alt="Discord"></a>
  <a href="https://github.com/AtomicBot-ai/Atomic-Chat"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_github.png" width="115" alt="GitHub"></a>
</div>
<ul style="margin: 0 0 12px 0;">
  <!-- TODO(editorial): guide bullet: link to the atomic.chat blog guide for this model, if there is one -->
  <li>Every file here was measured against the BF16 original on the same stand as the other publishers' files.</li>
  <li>See our quantization analysis below for measurements and instructions.</li>
</ul>
<hr style="margin: 0 0 16px 0;">

<img src="https://huggingface.co/AtomicChat/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-GGUF/resolve/main/atomic-dynamic-kld.png" alt="Atomic Dynamic vs other GGUF builds of Bolt: mean KL divergence to the BF16 original against size on disk" width="100%">

Lower is closer to the original. Each purple point is a file in this repo; the grey
ones are other GGUF files of this model, downloaded and measured with exactly the
same reference, text and llama.cpp build. NVIDIA's 2-bit file (the one Unsloth and
LM Studio ship too) is a quantization-aware-trained checkpoint, so its distance to
the BF16 weights also includes what that training changed; see below.

## What is Atomic Dynamic

Atomic Dynamic is how we decide which tensor gets which bits. The files use only
standard llama.cpp quantization types: upstream llama.cpp with `nemotron_h_moe`
support reads them, no fork and no special build.

- **The experts take the compression, nothing else does.** About 89% of this
  model's weights are experts. The Mamba-2 projections, attention, the latent
  projections and the shared expert stay at q8_0 or q6_k down to the 2-bit files,
  and every bit saved goes to the experts instead.
- **Bits follow the measured activity, not the position.** The blocks that get
  extra precision are the ones the importance matrix ranks highest.
- **Calibrated on the real chat format.** The importance matrix is collected on the
  BF16 weights over a corpus rendered through this model's own chat template,
  with the special tokens read as tokens.
- **No silent type swaps.** We check every tensor's type in the finished file.
- **Measured against everyone.** Each file is set against the other publishers'
  files before it goes up.

## Pick a file

Every number below is measured, not estimated. How we measured it is at the
bottom, and the raw logs are in
[the metrics repo](https://huggingface.co/datasets/AtomicChat/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-GGUF-metrics)
so you can check any of it yourself.

`KL divergence` is how far the quantized model's predictions drift from the
original weights. Lower is better, and zero means identical. `top-1` is how
often it picks the same next word the original would have picked.

| File | Size | KL divergence | top-1 |
|---|---:|---:|---:|
| `AD-Q8_0` | 78.9 GB | 0.00840 | 95.82% |
| `AD-Q6_K` | 72.5 GB | 0.00870 | 95.73% |
| `AD-Q5_K_M` | 61.1 GB | 0.01024 | 95.36% |
| `AD-Q4_K_M` | 51.7 GB | 0.01472 | 94.34% |
| `AD-IQ4_XS` | 46.6 GB | 0.01717 | 93.83% |
| `AD-IQ3_M` | 40.2 GB | 0.02800 | 92.12% |
| `AD-IQ3_XXS` | 36.3 GB | 0.03716 | 90.97% |
| `AD-IQ2_M` | 31.5 GB | 0.06282 | 88.28% |
| `AD-IQ2_XS` | 29.1 GB | 0.08262 | 86.60% |
| `AD-IQ2_XXS` | 26.7 GB | 0.11004 | 84.67% |
| `AD-IQ2_XXS_S` | 23.0 GB | 0.15133 | 82.10% |
| `AD-IQ1_M` | 22.5 GB | 0.18169 | 80.42% |
| `AD-IQ1_M_S` | 21.9 GB | 0.19411 | 79.71% |

`AD-` marks an **Atomic Dynamic** layout. The rest of the name is the type of the
expert up projections, the largest tensor group; `_S` marks the smaller of two
files built around the same type. The exact type of every tensor is in `ladder/`
in the metrics repo. Compare files by size on disk, not by name.

Above about 60 GB the files differ very little: on this model even `AD-Q8_0`
drifts 0.0084 from the original, and `AD-Q5_K_M` 0.0102.

## Which one fits your card

The file has to fit, and so does the context. Only 8 of the 88 layers are
attention; the Mamba layers keep a fixed-size state. The attention cache is about
8 KB per token, 0.1 GB at 8k context and 0.2 GB at 32k, plus about 1 GB of
compute buffers.

| Memory for the model (GPU or unified) | Largest file that fits |
|---|---|
| 24 GiB | `AD-IQ2_XXS_S` (23.0 GB on disk) |
| 32 GiB | `AD-IQ2_M` (31.5 GB on disk) |
| 40 GiB | `AD-IQ3_XXS` (36.3 GB on disk) |
| 48 GiB | `AD-IQ4_XS` (46.6 GB on disk) |
| 64 GiB | `AD-Q5_K_M` (61.1 GB on disk) |
| 80 GiB and up | `AD-Q6_K` (72.5 GB) or `AD-Q8_0` (78.9 GB on disk) |

> [!TIP]
> If you are choosing between two neighbouring files, take the larger one. The
> steps between them cost one or two gigabytes and buy noticeably fewer wrong words.

## Running it

```bash
llama-server -m NVIDIA-Nemotron-3.5-Bolt-74B-A9B-AD-IQ2_XS.gguf -ngl 99 -c 8192
```

The chat template is inside every file, llama.cpp applies it on its own.
<!-- TODO(editorial): prompt format block and the thinking toggle, if the family has one -->

## Speed

<!-- TODO(editorial): llama-bench prompt and generation t/s at 8k and 32k for the recommended file -->

## Images

This model reads images, not only text. That needs one extra file, the vision
projector, which is separate from the quant and shared by all of them:

- `mmproj-NVIDIA-Nemotron-3.5-Bolt-74B-A9B-F16.gguf` (1.73 GB) for most people
- `mmproj-NVIDIA-Nemotron-3.5-Bolt-74B-A9B-BF16.gguf` (1.73 GB) if your setup prefers bfloat16
- `mmproj-NVIDIA-Nemotron-3.5-Bolt-74B-A9B-Q8_0.gguf` (0.97 GB) if memory is tight

The Q8_0 projector against F16, on 12 photos with `AD-Q8_0` and greedy decoding: short answers
about the main subject meant the same in all 12 (10 word for word, 2 with a synonym). Long
descriptions start the same but are worded differently (1 of 12 identical); we found no factual
errors, though one count got vaguer ("three teddy bears" became "several"). For the closest
match to the original, use F16.

Download it once alongside whichever quant you picked:

```bash
llama-mtmd-cli \
  -m NVIDIA-Nemotron-3.5-Bolt-74B-A9B-AD-IQ2_XS.gguf \
  --mmproj mmproj-NVIDIA-Nemotron-3.5-Bolt-74B-A9B-F16.gguf \
  --image your-photo.jpg -ngl 99 -c 8192 \
  -p "What is in this image?"
```

Image input was checked only with `AD-Q8_0` (the 12 photos above). Video input was not tested.

<!-- TODO(editorial): family specific vision flags (e.g. --image-min-tokens) and the demo image test -->

## How these compare to other builds

We downloaded the other GGUF files of this model and measured them with the same
reference logits, held-out text, context, chunk count and llama.cpp commit as ours:

| Ours | Size | KL divergence | top-1 | Theirs | Size | KL divergence | top-1 |
|---|---:|---:|---:|---|---:|---:|---:|
| `AD-IQ1_M_S` | 21.94 GB | 0.19411 | 79.71% | NVIDIA `24GB` IQ2_XXS (also in Unsloth's and LM Studio's repos) | 22.02 GB | 0.21954 | 79.14% |
| `AD-IQ4_XS` | 46.57 GB | 0.01717 | 93.83% | darioooooo0o `Q4_K_M-static` | 48.34 GB | 0.01889 | 93.36% |

NVIDIA's 2-bit file is not a quantization of the BF16 weights we measure against:
NVIDIA trained the model further to suit 2-bit experts (quantization-aware training)
and published that checkpoint. Its distance to the BF16 original therefore mixes two
things, the rounding and what the training changed, and a lower number for ours
does not prove our file answers better than theirs. What it does show is that
`AD-IQ1_M_S` reproduces the BF16 model more closely than that file does, and is
80 MB smaller.

So we also asked all of them the same 2000 MMLU questions (greedy, one-letter
answers, thinking off) and compared every pair on the questions where they
disagree (McNemar's test; p below 0.05 means the difference is unlikely to be
chance):

| File | Size | MMLU | against BF16 | against NVIDIA's file |
|---|---:|---:|---|---|
| BF16 original | 148 GB | 81.35% | | |
| NVIDIA `24GB` IQ2_XXS | 22.02 GB | 80.45% | -0.90 pp, p=0.13 | |
| `AD-IQ1_M_S` | 21.94 GB | 79.75% | -1.60 pp, p=0.013 | -0.70 pp, p=0.34 |
| `AD-IQ2_XS` | 29.08 GB | 80.80% | -0.55 pp, p=0.32 | +0.35 pp, p=0.63 |

At 22 GB the two files cannot be told apart on MMLU, but NVIDIA's training shows:
its loss against the original is within noise and ours is not. If MMLU-style
knowledge is what you need at 22 GB, NVIDIA's file is the safer pick; ours stays
closer to the original's token choices. At 29 GB, `AD-IQ2_XS` is within noise of the
original.

## What we found while building these

- Every expert width in this model is a multiple of 256, so the expert tensors
  take llama.cpp's full set of k- and i-quants; no type had to be swapped.
- Below 24 GB, the non-expert part decides the file: our smallest files take the
  Mamba projections to iq4_xs, the shared experts and the embedding to q6_k, and
  keep attention, the latent projections and the output head at q8_0.

## The calibration data

Our importance matrix comes from a corpus we built for this model and
published: [AtomicChat/calib-corpora](https://huggingface.co/datasets/AtomicChat/calib-corpora),
recipe `nemotron-bolt-moe`. It is 4,589,438 tokens across 2,820 documents:

| Part | Share |
|---|---:|
| agentic and tool use | 24.0% |
| multilingual | 19.6% |
| code | 17.4% |
| reasoning | 13.1% |
| long context | 11.1% |
| vocabulary sweep | 5.9% |
| structured data | 4.4% |
| graphics | 4.4% |

Every conversation is rendered through **this model's own chat template**, so
the chat markup appears as the single tokens the model actually sees.

> [!IMPORTANT]
> If you build your own importance matrix from this corpus, pass
> `--parse-special` to `llama-imatrix`. Without it the chat markup is read as
> ordinary punctuation.

## How we measured

Reference: the original BF16 weights, converted to GGUF and run unquantized.
Perplexity on the held-out set is 7.8206 plus or minus 0.04476.

Held-out text: `eval_neutral` from our calibration dataset, never used for
calibration. 95 chunks at 4096 context.

Metric: per-token KL divergence of each file's predictions against the
reference, plus top-1 agreement.

Hardware: 8x A100-SXM4-40GB.

The raw logits of the reference are published in the metrics repo, split into
parts because of the file size limit. With them you can measure your own build
against exactly the same point we did:

```bash
cat base-neutral.kld.*.part > base-neutral.kld

llama-perplexity -m your-quant.gguf -f eval_neutral.txt \
  --kl-divergence-base base-neutral.kld --kl-divergence -c 4096 -ngl 99
```

## Reproducing a file

The importance matrix was collected on the BF16 weights rather than on a
quantized copy, split across 3 workers and merged. Splitting by chunk
range gives the same result as one long run, because the statistic is a sum:

```bash
llama-imatrix -m NVIDIA-Nemotron-3.5-Bolt-74B-A9B-BF16.gguf -f calib_train.txt -o shard-0.gguf \
  -ngl 99 -c 512 -b 8192 -ub 8192 --parse-special --from-chunk 0 --chunks 2988

llama-imatrix -m NVIDIA-Nemotron-3.5-Bolt-74B-A9B-BF16.gguf --in-file shard-0.gguf,shard-1.gguf,... \
  -o imatrix.gguf
```

Then, for `AD-IQ2_XS`:

```bash
llama-quantize \
  --imatrix imatrix.gguf \
  --tensor-type '^token_embd\.weight$=q8_0' \
  --tensor-type '^output\.weight$=q8_0' \
  --tensor-type '^blk\.(76|79|81|83|85|87)\.ffn_down_exps\.weight$=iq3_s' \
  --tensor-type '^blk\.(76|79|81|83|85|87)\.ffn_up_exps\.weight$=iq3_xxs' \
  --tensor-type '^blk\.\d+\.ffn_down_exps\.weight$=iq2_s' \
  --tensor-type '^blk\.\d+\.ffn_up_exps\.weight$=iq2_xs' \
  --tensor-type '^blk\.\d+\.ffn_latent_(down|up)\.weight$=q8_0' \
  --tensor-type '^blk\.\d+\.ffn_(down|up)_shexp\.weight$=q8_0' \
  --tensor-type '^blk\.\d+\.attn_(q|k|v|qkv|output)\.weight$=q8_0' \
  --tensor-type '^blk\.\d+\.ssm_(in|out)\.weight$=q6_k' \
  --override-kv \
  nemotron_h_moe.context_length=int:262144 \
  NVIDIA-Nemotron-3.5-Bolt-74B-A9B-BF16.gguf NVIDIA-Nemotron-3.5-Bolt-74B-A9B-AD-IQ2_XS.gguf IQ2_XS
```

The rules for every other file are in `ladder/` in the metrics repo, next to
its quantization log. The first rule that matches a tensor wins.

## Model details

88 layers (40 Mamba-2, 40 mixture-of-experts with 240 to 496 experts per layer,
8 attention), hidden size 4096, vocabulary 131,072. NVIDIA's config sets a maximum
context of 262,144 tokens, and every file here carries that value; we measured at
4096 and did not test long context.

We converted the weights with llama.cpp's converter at cd0a5b6a plus a small fix
for Bolt's per-layer block configuration; running the files needs no patch.

Needs a recent llama.cpp with `nemotron_h_moe` architecture support. Built and tested with llama.cpp b11668 (cd0a5b6a1).
