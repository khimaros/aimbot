---
license: apache-2.0
base_model: FINAL-Bench/Darwin-27B-RSI
library_name: gguf
pipeline_tag: text-generation
tags:
- gguf
- llama.cpp
- q4_k_m
- darwin
- darwin-rsi
- recursive-self-improvement
- rsi
- no-human-labels
- reasoning
- thinking
- decision-index
- jev
- vidraft
- final-bench
---

<p align="center">
  <a href="https://vidraft.net"><img src="https://img.shields.io/badge/🌐_VIDRAFT-vidraft.net-111111?style=for-the-badge" alt="VIDRAFT"></a>
  <a href="https://huggingface.co/FINAL-Bench/Darwin-27B-RSI"><img src="https://img.shields.io/badge/🧬_BF16-Darwin--27B--RSI-blue?style=for-the-badge" alt="BF16"></a>
</p>

# Darwin-27B-RSI-GGUF

Q4_K_M GGUF of [FINAL-Bench/Darwin-27B-RSI](https://huggingface.co/FINAL-Bench/Darwin-27B-RSI) — Darwin-27B-Opus improved by Recursive Self-Improvement, with zero human-written answers.

| File | Quant | Size |
|---|---|---|
| `Darwin-27B-RSI-Q4_K_M.gguf` | Q4_K_M | 16.8 GB |

Internal checks show no GPQA Diamond accuracy difference between this Q4_K_M file and BF16. It was used as the reasoning path of **Darwin-27B-JEV** on the [Decision Index](https://huggingface.co/spaces/multimodalart/jev-decision-index), and lets the whole engine fit on one 96 GB GPU.

## Run

```bash
llama-server -m Darwin-27B-RSI-Q4_K_M.gguf --jinja -ngl 99 -c 65536 --port 7931
```

Thinking model: allow a generous token budget; read the answer after the reasoning block.

Not affiliated with TypeSafe AI or its Jev product. Developer: [VIDRAFT](https://vidraft.net) · [FINAL-Bench](https://huggingface.co/FINAL-Bench).
