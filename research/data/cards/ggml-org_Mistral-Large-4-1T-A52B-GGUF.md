---
license: other
license_name: mistral-ecosystem-open-weight-license
license_link: https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B/blob/main/LICENSE
pipeline_tag: image-text-to-text
tags:
- gguf
- quantized
base_model:
- mistralai/Mistral-Large-4-1T-A52B
---

# Mistral Large 4

Run with https://llama.app

```bash
llama serve -hf ggml-org/Mistral-Large-4-1T-A52B-GGUF:IQ2_XXS
```

### Source models
- https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B

### Related models
- [ggml-org/Mistral-Large-4-1T-A52B-NVFP4-GGUF](https://huggingface.co/ggml-org/Mistral-Large-4-1T-A52B-NVFP4-GGUF): GGUF of the NVFP4 release, with the original NVFP4 experts and the DSpark draft head
- [mistralai/Mistral-Large-4-1T-A52B-NVFP4](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B-NVFP4): Mistral's NVFP4 release

### Files

| Quant | Size | Notes |
|---|---|---|
| BF16 | 2.10 TB | Lossless upcast of the FP8 release |
| Q8_0 | 1.12 TB | Near-lossless |
| Q4_K_M | 635 GB | 4-bit quant |
| Q2_K | 381 GB | 2-bit quant. Fits in 512 GB of unified memory |
| IQ2_XXS | 298 GB | imatrix-calibrated. Fits in 512 GB of unified memory |
| mmproj (BF16, F16) | 3.4 / 3.4 GB | Vision encoder |

### Notes
- Mistral Large 4 is a 1T-parameter mixture-of-experts model (128 routed experts, 4 active per token, plus 1 shared expert; ~52B active parameters) with image input and a 1M-token context window.
- The source checkpoint is block-scaled FP8. All GGUFs here are quantized from it; for a version that keeps the original NVFP4 experts, see [ggml-org/Mistral-Large-4-1T-A52B-NVFP4-GGUF](https://huggingface.co/ggml-org/Mistral-Large-4-1T-A52B-NVFP4-GGUF).
- The IQ2_XXS output quantizes the routed expert gate/up projections to IQ2_XXS and the expert down projections to IQ2_XS. Attention, the sparse-attention indexer, the shared experts, the dense first layer, the embeddings and the output head are kept at Q8_0.
- The IQ2_XXS is calibrated with an [imatrix](imatrix-mistral.gguf) computed on 36 chunks of 8,192 tokens.
- Reasoning depth is set with `reasoning_effort`: `low`, `medium` or `high` (the default). Reasoning cannot be turned off.
- Recommended sampling (stored in the GGUF metadata): `temperature 1.0`, `top_p 0.95`.
