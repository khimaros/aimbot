---
license: other
license_name: muse-model-license
license_link: LICENSE.md
pipeline_tag: image-text-to-text
tags:
- gguf
- quantized
base_model:
- meta-models/Muse-Spark-Open-816B-A42B
---

# Muse Spark Open

Run with https://llama.app

```bash
llama serve -hf ggml-org/Muse-Spark-Open-816B-A42B-GGUF:Q2_K
```

### Source models
- https://huggingface.co/meta-models/Muse-Spark-Open-816B-A42B

### Files

| Quant | Size | Notes |
|---|---|---|
| BF16 | 1.64 TB | Original precision |
| Q8_0 | 872 GB | Near-lossless. All weight matrices at Q8_0 |
| Q4_K_S | 470 GB | 4-bit quant |
| Q2_K | 304 GB | imatrix-calibrated. Fits in 512 GB of unified memory |
| mmproj (BF16, F16, Q8_0) | 4.1 / 4.1 / 2.2 GB | Vision and audio encoders |

### Notes
- Muse Spark Open is an 816B-parameter mixture-of-experts model (256 experts, ~42B active per token) with image and audio input.
- The Q2_K output quantizes the routed expert gate/up projections to Q2_K and the expert down projections to Q3_K. The per-layer latent projections (`ffn_latent_down`, `ffn_latent_up`) and the attention output gate (`attn_gate`) are kept at Q8_0.
- The Q2_K is calibrated with an [imatrix](imatrix.gguf) computed from the Q8_0 on [bartowski's v6 calibration data](https://gist.github.com/bartowski1182/e26453c0404e24eb317543ec5360f87a).
- Reasoning depth is set with `reasoning_effort`: `low`, `medium`, `high` or `xhigh` (the default). A system prompt containing a `Reasoning strength: N.` line overrides `reasoning_effort`.
- Recommended sampling (stored in the GGUF metadata): `temperature 1.0`, `top_p 1.0`, `top_k 64`.
