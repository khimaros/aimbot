---
license: apache-2.0
language:
  - en
  - zh
pipeline_tag: image-text-to-text
tags:
  - minicpm-ocr
  - ocr
  - quality-assessment
  - gguf
  - llama.cpp
  - multimodal
  - quantized
base_model: openbmb/MiniCPM-OCR-Jev
base_model_relation: quantized
---

<div align="center">

<p align="center">
  <a href="https://github.com/OpenBMB/MiniCPM"><img src="https://raw.githubusercontent.com/OpenBMB/MiniCPM-OCR/main/assets/minicpm-ocr/minicpm-logo.jpg" width="300" alt="MiniCPM logo"></a>
</p>

[GitHub](https://github.com/OpenBMB/MiniCPM-OCR) · [Usage](https://github.com/OpenBMB/MiniCPM-OCR/blob/main/docs/minicpm_ocr_jev_tutorial_en.md)

</div>

> **This repository hosts the GGUF build of [MiniCPM-OCR Jev](https://huggingface.co/openbmb/MiniCPM-OCR-Jev) for
> [llama.cpp](https://github.com/ggml-org/llama.cpp).** For the original weights and the full
> model card, see the base repository.

**MiniCPM-OCR Jev** (2B) scores OCR candidates for text, formula, and table regions, returning a
quality score from 0 to 1.

## Files

| File | Size | Notes |
| :--- | ---: | :--- |
| `mmproj-model-f16.gguf` | 0.671 GB | vision projector — required |
| `MiniCPM-OCR-Jev-F16.gguf` | 3.776 GB | reference |
| `MiniCPM-OCR-Jev-Q8_0.gguf` | 2.012 GB | near-lossless |
| `MiniCPM-OCR-Jev-Q6_K.gguf` | 1.556 GB |  |
| `MiniCPM-OCR-Jev-Q5_K_M.gguf` | 1.411 GB |  |
| `MiniCPM-OCR-Jev-Q5_K_S.gguf` | 1.374 GB |  |
| `MiniCPM-OCR-Jev-Q5_1.gguf` | 1.460 GB |  |
| `MiniCPM-OCR-Jev-Q5_0.gguf` | 1.374 GB |  |
| `MiniCPM-OCR-Jev-Q4_K_M.gguf` | 1.274 GB | smallest recommended |
| `MiniCPM-OCR-Jev-Q4_K_S.gguf` | 1.212 GB |  |
| `MiniCPM-OCR-Jev-Q4_1.gguf` | 1.288 GB |  |
| `MiniCPM-OCR-Jev-Q4_0.gguf` | 1.202 GB |  |
| `MiniCPM-OCR-Jev-IQ4_XS.gguf` | 1.202 GB | imatrix |
| `MiniCPM-OCR-Jev-IQ4_NL.gguf` | 1.236 GB | imatrix |
| `MiniCPM-OCR-Jev-IQ3_M.gguf` | 1.059 GB | imatrix |
| `MiniCPM-OCR-Jev-IQ3_XS.gguf` | 1.027 GB | imatrix |

## Usage

```bash
llama-server \
  --model ./MiniCPM-OCR-Jev-Q8_0.gguf \
  --mmproj ./mmproj-model-f16.gguf \
  --host 0.0.0.0 --port 18498 \
  --ctx-size 40960 \
  --n-gpu-layers 999
```

Check `verdict` in the response — only `scored` means scoring actually ran.

Deployment details: [llama.cpp guide for Jev](https://github.com/OpenBMB/MiniCPM-OCR/blob/main/docs/llamacpp_deploy_jev_en.md).

## Related checkpoints

| Format | Hugging Face | ModelScope |
| :--- | :--- | :--- |
| BF16 (original) | [🤗](https://huggingface.co/openbmb/MiniCPM-OCR-Jev) | [ModelScope](https://modelscope.cn/models/OpenBMB/MiniCPM-OCR-Jev) |
| GGUF (llama.cpp) **(this repo)** | [🤗](https://huggingface.co/openbmb/MiniCPM-OCR-Jev-gguf) | [ModelScope](https://modelscope.cn/models/OpenBMB/MiniCPM-OCR-Jev-gguf) |
| AWQ W4A16 | [🤗](https://huggingface.co/openbmb/MiniCPM-OCR-Jev-AWQ) | [ModelScope](https://modelscope.cn/models/OpenBMB/MiniCPM-OCR-Jev-AWQ) |
| GPTQ W4A16 | [🤗](https://huggingface.co/openbmb/MiniCPM-OCR-Jev-GPTQ) | [ModelScope](https://modelscope.cn/models/OpenBMB/MiniCPM-OCR-Jev-GPTQ) |

## FAQ

Installation, model downloads, GPU memory, input formats, and unexpected outputs:
[FAQ](https://github.com/OpenBMB/MiniCPM-OCR/blob/main/docs/faq_en.md).

## License

Model weights, code, and documentation are released under the
[Apache License 2.0](https://github.com/OpenBMB/MiniCPM-OCR/blob/main/LICENSE).
