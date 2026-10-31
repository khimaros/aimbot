---
license: apache-2.0
language:
- en
- zh
pipeline_tag: image-text-to-text
tags:
- minicpm-ocr
- ocr
- document-parsing
- gguf
- llama.cpp
- multimodal
- quantized
base_model:
- openbmb/MiniCPM-V-4.6
base_model_relation: quantized
---

<div align="center">

<p align="center">
  <a href="https://github.com/OpenBMB/MiniCPM"><img src="https://raw.githubusercontent.com/OpenBMB/MiniCPM-OCR/main/assets/minicpm-ocr/minicpm-logo.jpg" width="300" alt="MiniCPM logo"></a>
</p>

Official Demo([CN](https://platform.modelbest.cn/console/playground/document-parse) / [Global](https://platform.modelbest.ai/console/playground/document-parse)) · Basic Demo([CN](http://82.157.64.212:10111/playground/document-parse) / [Global](https://huggingface.co/spaces/openbmb/MiniCPM-OCR))
\
[GitHub](https://github.com/OpenBMB/MiniCPM-OCR) · [Free API](https://platform.modelbest.ai/console/docs/api/document-parse) · [Usage](https://github.com/OpenBMB/MiniCPM-OCR#using-minicpm-ocr) · [DSpark](https://huggingface.co/openbmb/MiniCPM-OCR-1.0-DSpark) · [Skill](https://github.com/OpenBMB/MiniCPM-OCR#skill)

</div>

> **This repository hosts the GGUF build of [MiniCPM-OCR 1.0](https://huggingface.co/openbmb/MiniCPM-OCR-1.0) for
> [llama.cpp](https://github.com/ggml-org/llama.cpp).** For the original weights, the full model
> card, and benchmarks, see the base repository.

**MiniCPM-OCR 1.0** (1.3B) parses documents into text, tables, formulas, charts, and seals, and
supports key information extraction, for Chinese and English documents and PDFs.

## Files

Every tier needs the vision projector as well — `--model` takes the LLM GGUF, `--mmproj` takes
the projector:

| File | Size | Notes |
| :--- | ---: | :--- |
| `mmproj-model-f16-4x.gguf` | 0.901 GB | vision projector, **4× downsample** — required |
| `MiniCPM-OCR-1_0-F16.gguf` | 1.516 GB | reference, no quantization |
| `MiniCPM-OCR-1_0-Q8_0.gguf` | 0.812 GB | near-lossless |
| `MiniCPM-OCR-1_0-Q6_K.gguf` | 0.630 GB | good quality/size balance |
| `MiniCPM-OCR-1_0-Q5_K_M.gguf` | 0.578 GB | smaller, still strong |
| `MiniCPM-OCR-1_0-Q5_K_S.gguf` | 0.563 GB |  |
| `MiniCPM-OCR-1_0-Q5_1.gguf` | 0.595 GB |  |
| `MiniCPM-OCR-1_0-Q5_0.gguf` | 0.563 GB |  |
| `MiniCPM-OCR-1_0-Q4_K_M.gguf` | 0.529 GB | smallest recommended |
| `MiniCPM-OCR-1_0-Q4_K_S.gguf` | 0.505 GB |  |
| `MiniCPM-OCR-1_0-Q4_1.gguf` | 0.532 GB |  |
| `MiniCPM-OCR-1_0-Q4_0.gguf` | 0.501 GB |  |

The projector is 4× only; there is no 16× variant for this model.

### Which tier

| Tier | Table / dense text / XML |
| :--- | :--- |
| F16 | baseline |
| Q8_0 | lossless / ≈lossless — recommended balance |
| Q4_K_M | lossless on tables, small degradation on dense text; closing-tag slashes may drop in code-heavy documents |

Prefer Q8_0 for code- or XML-heavy pages.

## Usage

```bash
llama-server \
  --model ./MiniCPM-OCR-1_0-Q8_0.gguf \
  --mmproj ./mmproj-model-f16-4x.gguf \
  --host 0.0.0.0 --port 18499 \
  --ctx-size 40960 \
  --n-gpu-layers 999
```

`--n-gpu-layers 999` offloads everything to GPU; use `0` for CPU-only.

```bash
llama-mtmd-cli \
  -m ./MiniCPM-OCR-1_0-Q8_0.gguf \
  --mmproj ./mmproj-model-f16-4x.gguf \
  --image page.png -p "Text Recognition:" \
  --jinja -ngl 99 -c 8192 --temp 0
```

**Thinking is already disabled inside the embedded chat template** — no extra flag is needed, and
`enable_thinking` cannot turn it back on. (If you convert the weights yourself instead of using
these files, start the server with `--chat-template-kwargs '{"enable_thinking": false}'`.)

### Prompts

| Region | Prompt |
| :--- | :--- |
| Text block / paragraph / title / page | `Text Recognition:` |
| Table | `Table Recognition:` |
| Display formula | `Formula Recognition:` |

### SDK with a llama.cpp backend

```bash
minicpmvocr parse --config sdk/minicpmvocr/configs/minicpmvocr.yaml \
  --backend llamacpp --server-url http://127.0.0.1:18499 \
  --model minicpm-ocr \
  --set layout.device=cuda:0 \
  --set pipeline.queue_mode=serial \
  --set pipeline.max_workers=1 \
  --input doc.pdf --output doc.md
```

`llama-server` handles one request at a time by default, so keep `queue_mode=serial` and
`max_workers=1`.

## Performance

Single RTX 5090 (32 GB), F16 weights: model + projector load ≈2.3 s; one table crop
(1,312 prompt / 265 output tokens) ≈1.0 s; VRAM ≈26 GB at `--ctx-size 40960`.
CPU-only (48 threads): one table image end-to-end (layout + recognition + assembly) ≈21 s.

Build llama.cpp and further options: [llama.cpp deployment guide](https://github.com/OpenBMB/MiniCPM-OCR/blob/main/docs/llamacpp_deploy.md).

## Related checkpoints

| Format | Hugging Face | ModelScope |
| :--- | :--- | :--- |
| BF16 (original) | [🤗](https://huggingface.co/openbmb/MiniCPM-OCR-1.0) | [ModelScope](https://modelscope.cn/models/OpenBMB/MiniCPM-OCR-1.0) |
| GGUF (llama.cpp) **(this repo)** | [🤗](https://huggingface.co/openbmb/MiniCPM-OCR-1.0-gguf) | [ModelScope](https://modelscope.cn/models/OpenBMB/MiniCPM-OCR-1.0-gguf) |
| AWQ W4A16 | [🤗](https://huggingface.co/openbmb/MiniCPM-OCR-1.0-AWQ) | [ModelScope](https://modelscope.cn/models/OpenBMB/MiniCPM-OCR-1.0-AWQ) |
| GPTQ W4A16 | [🤗](https://huggingface.co/openbmb/MiniCPM-OCR-1.0-GPTQ) | [ModelScope](https://modelscope.cn/models/OpenBMB/MiniCPM-OCR-1.0-GPTQ) |
| DSpark draft (BF16) | [🤗](https://huggingface.co/openbmb/MiniCPM-OCR-1.0-DSpark) | [ModelScope](https://modelscope.cn/models/OpenBMB/MiniCPM-OCR-1.0-DSpark) |
| DSpark draft (GGUF) | [🤗](https://huggingface.co/openbmb/MiniCPM-OCR-1.0-DSpark-gguf) | [ModelScope](https://modelscope.cn/models/OpenBMB/MiniCPM-OCR-1.0-DSpark-gguf) |

Speculative decoding works in llama.cpp with the
[DSpark draft GGUF](https://huggingface.co/openbmb/MiniCPM-OCR-1.0-DSpark-gguf) via `--spec-type draft-dspark`.

## FAQ

Installation, model downloads, GPU memory, input formats, and unexpected outputs:
[FAQ](https://github.com/OpenBMB/MiniCPM-OCR/blob/main/docs/faq_en.md).

## License

Model weights, code, and documentation are released under the
[Apache License 2.0](https://github.com/OpenBMB/MiniCPM-OCR/blob/main/LICENSE).