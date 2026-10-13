---
base_model: openbmb/MiniCPM-V-4.7-35B-A3B
base_model_relation: quantized
quantized_by: AtomicChat
pipeline_tag: image-text-to-text
library_name: gguf
license: apache-2.0
tags:
- gguf
- llama.cpp
- minicpm
- openbmb
- imatrix
- quantized
- conversational
- atomic-chat
---

# How to Run MiniCPM V 4.7 35B A3B Locally
<p style="margin-top: 0; margin-bottom: 0;">
  <em>Built from openbmb's original weights with our own importance matrix. The <a href="https://huggingface.co/datasets/AtomicChat/calib-corpora">calibration corpora</a> behind our builds are public.</em>
</p>
<div style="display: flex; gap: 8px; align-items: center; margin-top: 10px; margin-bottom: 10px;">
  <a href="https://atomic.chat/?utm_source=huggingface&utm_medium=referral&utm_campaign=hf_minicpm_v_4_7_35b_a3b&utm_content=btn_atomic"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_atomic.png" width="162" alt="Atomic Chat"></a>
  <a href="https://discord.gg/8wGSsvmg4V"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_discord.png" width="119" alt="Discord"></a>
  <a href="https://github.com/AtomicBot-ai/Atomic-Chat"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_github.png" width="115" alt="GitHub"></a>
</div>
<ul style="margin: 0 0 12px 0;">
  <li>You can now run MiniCPM in <a href="https://atomic.chat/?utm_source=huggingface&utm_medium=referral&utm_campaign=hf_minicpm_v_4_7_35b_a3b&utm_content=bullet_app">Atomic Chat</a>.</li>
  <li>See our quantization analysis below for measurements and instructions.</li>
</ul>
<hr style="margin: 0 0 16px 0;">

## Pick a file

Every number below is measured, not estimated. How we measured it is at the
bottom, and the raw logs are in
[the metrics repo](https://huggingface.co/datasets/AtomicChat/MiniCPM-V-4.7-35B-A3B-GGUF-metrics)
so you can check any of it yourself.

`KL divergence` is how far the quantized model's predictions drift from the
original weights. Lower is better, and zero means identical. `top-1` is how
often it picks the same next word the original would have picked.

| File | Size | KL divergence | top-1 |
|---|---:|---:|---:|
| `Q8_0` | 36.9 GB | 0.00516 | 97.49% |
| `AD-Q6_K` | 29.1 GB | 0.00605 | 97.18% |
| `AD-Q6_K-Q5_K` | 26.2 GB | 0.00806 | 96.72% |
| `AD-Q5_K-Q4_K` | 22.1 GB | 0.01501 | 95.47% |
| `AD-Q5_K-IQ4_XS` | 21.5 GB | 0.01584 | 95.41% |
| `AD-Q4_K-IQ4_XS` | 20.1 GB | 0.01972 | 94.94% |
| `AD-IQ4_XS-IQ3_S` | 17.6 GB | 0.03874 | 92.86% |
| `AD-IQ3_S-IQ3_XXS` | 15.5 GB | 0.06381 | 90.82% |
| `AD-IQ3_XXS-IQ2_S` | 13.7 GB | 0.11015 | 87.99% |
| `AD-IQ2_S-IQ2_XS` | 12.3 GB | 0.16634 | 85.29% |
| `AD-IQ2_XS-IQ2_XXS` | 11.3 GB | 0.21942 | 83.17% |
| `AD-IQ2_XXS-IQ1_M` (research) | 10.1 GB | 0.34928 | 78.57% |

`AD-IQ2_XXS-IQ1_M` is a 1-bit experts layout: it matches the original's token choice 78.6% of the time. It fits a 12 GB card, but treat it as an experiment.

`AD-` marks an **Atomic Dynamic** layout. The name says what the two largest
tensor groups got: `AD-<ffn_down>-<ffn_up>`, collapsed to one name when both
match. Nothing is named after a type it does not contain.

## Against llama.cpp's plain presets

The same reference, held-out text, machine and llama.cpp build; the plain presets are made with no
importance matrix:

| Plain preset | Size | KL divergence | top-1 | AD file | Size | KL divergence | top-1 |
|---|---:|---:|---:|---|---:|---:|---:|
| `Q4_K_M` | 21.2 GB | 0.04455 | 92.23% | `AD-Q4_K-IQ4_XS` | 20.1 GB | 0.01972 | 94.94% |
| `Q5_K_M` | 24.7 GB | 0.01966 | 94.68% | `AD-Q5_K-Q4_K` | 22.1 GB | 0.01501 | 95.47% |
| `Q6_K` | 28.5 GB | 0.00949 | 96.40% | `AD-Q6_K-Q5_K` | 26.2 GB | 0.00806 | 96.72% |

`AD-Q4_K-IQ4_XS` is a gigabyte smaller than `Q4_K_M` and drifts less than half as far: as far as
`Q5_K_M`, which is 4.6 GB larger. Each AD file in this table is smaller than the plain preset next to
it and closer to the original, so the plain presets are only here, not in the repo. Every AD layout here keeps attention, the shared expert, the
embedding and the output head at q8_0 and spends the savings on the routed experts, which are 93% of
the weights.

## Which one fits your card

The file has to fit, and so does the context. This model keeps 20 KB of
attention cache per token, which is 0.2 GB at 8k context and 0.6 GB at 32k. Budget
for both.

| Your card | File | Leaves room for |
|---|---|---|
| 12 GB | `AD-IQ2_XS-IQ2_XXS` | around 16k context |
| 16 GB | `AD-IQ3_S-IQ3_XXS` | around 24k context |
| 24 GB | `AD-Q5_K-Q4_K` | around 120k context |
| 32 GB | `AD-Q6_K` | around 192k context |
| 48 GB and up | `Q8_0` | full context |

> [!TIP]
> If you are choosing between two neighbouring files, take the larger one. The
> steps between them cost one or two gigabytes and buy noticeably fewer wrong words.

## Running it

```bash
llama-server -m MiniCPM-V-4.7-35B-A3B-AD-Q4_K-IQ4_XS.gguf -ngl 99 -c 8192 --jinja
```

The chat template is inside every file, llama.cpp applies it on its own. With `--jinja` it starts every answer in thinking mode; turn it off per request with `"chat_template_kwargs": {"enable_thinking": false}`.

## Images and video

This model reads images, not only text. That needs one extra file, the vision
projector, which is separate from the quant and shared by all of them:

- `mmproj-MiniCPM-V-4.7-35B-A3B-F16.gguf` for most people
- `mmproj-MiniCPM-V-4.7-35B-A3B-BF16.gguf` if your setup prefers bfloat16

Download it once alongside whichever quant you picked:

```bash
llama-mtmd-cli \
  -m MiniCPM-V-4.7-35B-A3B-AD-Q4_K-IQ4_XS.gguf \
  --mmproj mmproj-MiniCPM-V-4.7-35B-A3B-F16.gguf \
  --image your-photo.jpg -ngl 99 -c 8192 \
  -p "What is in this image?"
```

## The calibration data

Our importance matrix comes from a corpus we built for this model and
published: [AtomicChat/calib-corpora](https://huggingface.co/datasets/AtomicChat/calib-corpora),
recipe `minicpm-v-4.7-moe`. It is 4,906,667 tokens across 2,896 documents:

| Part | Share |
|---|---:|
| agentic and tool use | 22.4% |
| multilingual | 18.4% |
| code | 16.4% |
| reasoning | 12.2% |
| vocabulary sweep | 11.7% |
| long context | 10.5% |
| structured data | 4.3% |
| graphics | 4.1% |

Every conversation is rendered through **this model's own chat template**, so
the chat markup appears as the single tokens the model actually sees.

> [!IMPORTANT]
> If you build your own importance matrix from this corpus, pass
> `--parse-special` to `llama-imatrix`. Without it the chat markup is read as
> ordinary punctuation.

## How we measured

Reference: the original BF16 weights, converted to GGUF and run unquantized.
Perplexity on the held-out set is 8.6549 plus or minus 0.06668.

Held-out text: `eval_neutral` from our calibration dataset, never used for
calibration. 87 chunks at 4096 context.

Metric: per-token KL divergence of each file's predictions against the
reference, plus top-1 agreement.

Hardware: 2x H100 80GB HBM3.

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
quantized copy, split across 8 workers and merged. Splitting by chunk
range gives the same result as one long run, because the statistic is a sum:

```bash
llama-imatrix -m MiniCPM-V-4.7-35B-A3B-BF16.gguf -f calib_train.txt -o shard-0.gguf \
  -ngl 99 -c 512 -b 2048 -ub 2048 --parse-special --from-chunk 0 --chunks 1198

llama-imatrix -m MiniCPM-V-4.7-35B-A3B-BF16.gguf --in-file shard-0.gguf,shard-1.gguf,... \
  -o imatrix.gguf
```

Then, for `AD-Q4_K-IQ4_XS`:

```bash
llama-quantize \
  --imatrix imatrix.gguf \
  --tensor-type '^token_embd\.weight$=q8_0' \
  --tensor-type '^output\.weight$=q8_0' \
  --tensor-type '^blk\.\d+\.ffn_down_exps\.weight$=q4_k' \
  --tensor-type '^blk\.\d+\.ffn_(gate|up)_exps\.weight$=iq4_xs' \
  --tensor-type '^blk\.\d+\.ffn_(gate|down|up)_shexp\.weight$=q8_0' \
  --tensor-type '^blk\.\d+\.attn_(q|k|v|qkv|gate|output)\.weight$=q8_0' \
  --tensor-type '^blk\.\d+\.ssm_(out|alpha|beta)\.weight$=q8_0' \
  --override-kv general.file_type=int:30 \
  MiniCPM-V-4.7-35B-A3B-BF16.gguf MiniCPM-V-4.7-35B-A3B-AD-Q4_K-IQ4_XS.gguf Q8_0
```

The rules for every other file are in `ladder/` in the metrics repo, next to
its quantization log. The first rule that matches a tensor wins.

## Model details

40 layers, hidden size 2048, vocabulary 248,144, context 262,144.

Needs llama.cpp at or after `69f201a` (MiniCPM-V 4.7 support, ggml-org/llama.cpp#29416); older builds run text only and get image positions wrong. Built and tested with llama.cpp b11574 (8bb3cf0d2).
