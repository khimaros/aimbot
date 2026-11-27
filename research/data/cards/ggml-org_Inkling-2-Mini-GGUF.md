---
pipeline_tag: image-text-to-text
tags:
- gguf
- quantized
base_model:
- thinkingmachines/Inkling-2-Mini
---

# Inkling 2 Mini

Run with https://llama.app

```bash
llama serve -hf ggml-org/Inkling-2-Mini-GGUF:NVFP4
```

### Source models
- https://huggingface.co/thinkingmachines/Inkling-2-Mini

### Files

| Quant | Size | Notes |
|---|---|---|
| BF16 | 52.2 GB | 16-bit precision. The NVFP4 and MXFP8 experts of the original checkpoint are upcast to BF16 |
| Q8_0 | 27.8 GB | Near-lossless. All weight matrices at Q8_0 |
| NVFP4 | 17.6 GB | Original NVFP4 experts in layers 0-19, everything else at Q8_0 |
| IQ4_NL | 17.6 GB | imatrix-calibrated. 4-bit experts in layers 0-19, everything else at Q8_0 |
| mmproj (BF16, Q8_0) | 642 / 346 MB | Vision encoder |

### Notes
- Inkling 2 Mini is a looped mixture-of-experts model (128 experts, 8 active per token) with image input. It has 24 layers: layers 6-17 form a loop core that runs 3 times per token, so each token goes through 48 layer evaluations with the weights of 24. Each pass keeps its own KV and convolution cache.
- The original checkpoint stores the routed experts of layers 0-19 in NVFP4 and those of layers 20-23 in MXFP8. The NVFP4 output preserves those NVFP4 experts (`ffn_gate_up_exps`, `ffn_down_exps` of layers 0-19) with their per-expert scales and stores all other weight matrices at Q8_0. The IQ4_NL output quantizes those same experts to IQ4_NL instead. The loop controller weights stay at F32.
- The IQ4_NL is calibrated with an [imatrix](imatrix.gguf) computed from the BF16 on [bartowski's v6 calibration data](https://gist.github.com/bartowski1182/e26453c0404e24eb317543ec5360f87a), with the conversations rendered through the model's chat template.
- KL divergence against the BF16 on wikitext-2 (40 x 512 tokens): Q8_0 0.0030 (97.6% same top token), NVFP4 0.0029 (97.6% same top token), IQ4_NL 0.0095 (95.5% same top token).
- Reasoning depth is set with `reasoning_effort`: `none`, `minimal`, `low`, `medium`, `high` (the default), `xhigh` or `max`, or a number from 0.0 to 0.99.
