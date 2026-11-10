---
license: mit
base_model: baselabs/mammoth-1
tags: [gguf, decision-model, magnitude, re-upload]
---

# mammoth-1 GGUF

Re-upload of [baselabs/mammoth-1](https://huggingface.co/baselabs/mammoth-1) (`61cec44`) as GGUF, with decision metadata
added for [Magnitude](https://magnitude.run). Weights are unchanged apart from quantization.

- `mammoth-1-Q4_K_M.gguf`
- `mammoth-1-Q5_K_M.gguf`
- `mammoth-1-Q6_K.gguf`
- `mammoth-1-Q8_0.gguf`

## Decision metadata

`decision.*` keys and a `tokenizer.chat_template.decision` template, taken from the source's
config, calibration and reference code. They let Magnitude serve the model with no model-specific code;
other runtimes ignore them.

Answers `noul`, `choice`, `score`, via Magnitude's `/v1/systemone` and `/v1/decisions`.

## License

MIT (`LICENSE`).
