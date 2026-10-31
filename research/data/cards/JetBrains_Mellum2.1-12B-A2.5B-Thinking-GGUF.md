---
base_model: JetBrains/Mellum2.1-12B-A2.5B-Thinking
base_model_relation: quantized
library_name: gguf
pipeline_tag: text-generation
language:
- en
tags:
- mellum
- gguf
- llama.cpp
- quantized
- moe
- thinking
- mtp
- speculative-decoding
license: apache-2.0
---

# Mellum2.1 Thinking — GGUF

This repository contains **GGUF** builds of
[`JetBrains/Mellum2.1-12B-A2.5B-Thinking`](https://huggingface.co/JetBrains/Mellum2.1-12B-A2.5B-Thinking) in every quantization we
publish, ready to run with [`llama.cpp`](https://github.com/ggml-org/llama.cpp),
Ollama, LM Studio, and other GGUF-compatible runtimes. Each variant is one
file; download the one you need. The repository also ships the model's
**multi-token prediction (MTP) head** for speculative decoding in llama.cpp;
see [Speculative decoding with the MTP head](#speculative-decoding-with-the-mtp-head).

Mellum2.1 Thinking is a Mixture-of-Experts reasoning model (64 experts, 8
activated per token, 131,072-token context) that emits its chain of thought
inside `<think>...</think>` blocks before the final answer. For the full model
description, evaluation results, and architecture details, see the original
model card: **[JetBrains/Mellum2.1-12B-A2.5B-Thinking](https://huggingface.co/JetBrains/Mellum2.1-12B-A2.5B-Thinking)**.

## Available quantizations

| File | Quantization | Description | Size | KLD vs BF16 ↓ | Top-token match ↑ |
|---|---|---|---|---|---|
| [`Mellum2.1-12B-A2.5B-Thinking-BF16.gguf`](https://huggingface.co/JetBrains/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-BF16.gguf) | `BF16` | 16-bit, no quantization (reference) | 24.3 GB | — | — |
| [`Mellum2.1-12B-A2.5B-Thinking-Q8_0.gguf`](https://huggingface.co/JetBrains/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-Q8_0.gguf) | `Q8_0` | 8-bit, effectively lossless | 12.9 GB | 0.008 | 96.1% |
| [`Mellum2.1-12B-A2.5B-Thinking-Q6_K.gguf`](https://huggingface.co/JetBrains/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-Q6_K.gguf) | `Q6_K` | 6-bit k-quant, very high quality | 10.9 GB | 0.020 | 93.9% |
| [`Mellum2.1-12B-A2.5B-Thinking-Q4_K_M.gguf`](https://huggingface.co/JetBrains/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-Q4_K_M.gguf) | **`Q4_K_M`** | 4-bit k-quant, balanced (recommended) | 8.1 GB | 0.075 | 88.0% |
| [`Mellum2.1-12B-A2.5B-Thinking-MXFP4_MOE.gguf`](https://huggingface.co/JetBrains/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-MXFP4_MOE.gguf) | `MXFP4_MOE` | MXFP4 4-bit on MoE experts, smallest | 7.0 GB | 0.115 | 85.6% |

KL divergence and top-token agreement are measured against the BF16 logits on
Wikitext-2 (`n_ctx=512`); lower KLD / higher agreement means closer to the
unquantized model.

## Download

```sh
hf download JetBrains/Mellum2.1-12B-A2.5B-Thinking-GGUF Mellum2.1-12B-A2.5B-Thinking-Q4_K_M.gguf --local-dir .
```

## Run with llama.cpp

```sh
# Pull and serve in one step (downloads the GGUF automatically; the suffix picks the quantization)
llama-server -hf JetBrains/Mellum2.1-12B-A2.5B-Thinking-GGUF:Q4_K_M \
  --ctx-size 131072 \
  --temp 0.6 --top-p 0.95 --top-k 20

# Or run a one-off prompt with a local file
llama-cli -m Mellum2.1-12B-A2.5B-Thinking-Q4_K_M.gguf \
  --ctx-size 131072 \
  --temp 0.6 --top-p 0.95 --top-k 20 \
  -p "Is 1024 a power of 2? Explain your reasoning."
```

The server exposes an OpenAI-compatible API on `http://localhost:8080/v1`:

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8080/v1", api_key="llama.cpp")

chat_response = client.chat.completions.create(
    model="JetBrains/Mellum2.1-12B-A2.5B-Thinking-GGUF",
    messages=[
        {"role": "user", "content": "Is 1024 a power of 2? Explain your reasoning."},
    ],
    max_tokens=81920,
    temperature=0.6,
    top_p=0.95,
    extra_body={"top_k": 20},
)
print(chat_response.choices[0].message.content)
```

## Speculative decoding with the MTP head

Mellum2.1 Thinking was trained with a multi-token prediction head: one extra
transformer block (same attention and MoE shape as a model layer) that predicts
the token after the one just sampled. llama.cpp uses it as a speculative draft
(`--spec-type draft-mtp`): the full model verifies every drafted token, so the
output is unchanged and generation is faster whenever drafts are accepted.

| File | Quantization | Description | Size |
|---|---|---|---|
| [`mtp-Mellum2.1-12B-A2.5B-Thinking-BF16.gguf`](https://huggingface.co/JetBrains/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/mtp-Mellum2.1-12B-A2.5B-Thinking-BF16.gguf) | `BF16` | MTP head only; draft file for every quantization above | 1.8 GB |
| [`mtp/Mellum2.1-12B-A2.5B-Thinking-MTP-BF16.gguf`](https://huggingface.co/JetBrains/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/mtp/Mellum2.1-12B-A2.5B-Thinking-MTP-BF16.gguf) | `BF16` | model and MTP head in one file | 25.2 GB |
| [`mtp/Mellum2.1-12B-A2.5B-Thinking-MTP-Q8_0.gguf`](https://huggingface.co/JetBrains/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/mtp/Mellum2.1-12B-A2.5B-Thinking-MTP-Q8_0.gguf) | `Q8_0` | model and MTP head in one file | 13.4 GB |
| [`mtp/Mellum2.1-12B-A2.5B-Thinking-MTP-Q6_K.gguf`](https://huggingface.co/JetBrains/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/mtp/Mellum2.1-12B-A2.5B-Thinking-MTP-Q6_K.gguf) | `Q6_K` | model and MTP head in one file | 11.3 GB |
| [`mtp/Mellum2.1-12B-A2.5B-Thinking-MTP-Q4_K_M.gguf`](https://huggingface.co/JetBrains/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/mtp/Mellum2.1-12B-A2.5B-Thinking-MTP-Q4_K_M.gguf) | `Q4_K_M` | model and MTP head in one file | 8.3 GB |
| [`mtp/Mellum2.1-12B-A2.5B-Thinking-MTP-MXFP4_MOE.gguf`](https://huggingface.co/JetBrains/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/mtp/Mellum2.1-12B-A2.5B-Thinking-MTP-MXFP4_MOE.gguf) | `MXFP4_MOE` | model and MTP head in one file | 7.3 GB |

The model weights in the combined files are identical to the quantizations
above; in them the head is quantized with the model, and the standalone head
file is BF16. These files need llama.cpp build `b11747` (19 October 2026) or
newer. Older builds, and Ollama, LM Studio, and other runtimes until they ship
such a build, cannot load them; they keep working with the quantizations in the
first table, which is also what `-hf …:Q4_K_M` and `ollama run hf.co/…`
resolve to. Without `--spec-type draft-mtp` nothing changes: the head is simply
not used.

```sh
# Serve with MTP speculative decoding; llama.cpp also fetches the mtp- draft file from this repository
llama-server -hf JetBrains/Mellum2.1-12B-A2.5B-Thinking-GGUF:Q4_K_M \
  --spec-type draft-mtp --spec-draft-n-max 1 \
  --ctx-size 131072 \
  --temp 0.6 --top-p 0.95 --top-k 20

# Local files: any quantization plus the draft file
llama-server -m Mellum2.1-12B-A2.5B-Thinking-Q4_K_M.gguf \
  -md mtp-Mellum2.1-12B-A2.5B-Thinking-BF16.gguf \
  --spec-type draft-mtp --spec-draft-n-max 1 \
  --ctx-size 131072 \
  --temp 0.6 --top-p 0.95 --top-k 20

# One combined file; the embedded head is the draft
llama-server -m mtp/Mellum2.1-12B-A2.5B-Thinking-MTP-Q4_K_M.gguf \
  --spec-type draft-mtp --spec-draft-n-max 1 \
  --ctx-size 131072 \
  --temp 0.6 --top-p 0.95 --top-k 20
```

`--spec-draft-n-max` sets how many tokens the head drafts per step; the head
predicts one token ahead, so start with 1. In the llama.cpp
[benchmarks](https://github.com/ggml-org/llama.cpp/pull/30612) of this head
(Apple M2 Max, Metal, 512 greedy tokens, mean over ten prompts) one drafted
token gave 1.05x the BF16 decoding speed, 1.04–1.10x on code prompts, and
1.00x for a Q4_K_M model with a Q8_0 head; two or more drafted tokens were
slower than plain decoding in every configuration. The `timings` object of each
server response reports `draft_n` and `draft_n_accepted`, the number of drafted
and accepted tokens.

## Run with Ollama

```sh
ollama run hf.co/JetBrains/Mellum2.1-12B-A2.5B-Thinking-GGUF:Q4_K_M
```

## License

Released under the Apache 2.0 license.

---

*For the full model card, evaluation results, and architecture details, refer to
the original model: [JetBrains/Mellum2.1-12B-A2.5B-Thinking](https://huggingface.co/JetBrains/Mellum2.1-12B-A2.5B-Thinking).*
