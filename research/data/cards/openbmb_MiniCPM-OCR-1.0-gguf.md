---
license: apache-2.0
language:
- en
- zh
pipeline_tag: image-text-to-text
library_name: minicpm-ocr
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

Demo ([CN](https://platform.modelbest.cn/console/playground/document-parse) / [Global](https://platform.modelbest.ai/console/playground/document-parse)) · [GitHub](https://github.com/OpenBMB/MiniCPM-OCR) · [Free API](https://platform.modelbest.ai/console/docs/api/document-parse) · [SDK usage](#use-with-the-minicpm-ocr-sdk) · [DSpark](https://huggingface.co/openbmb/MiniCPM-OCR-1.0-DSpark) · [Skill](https://github.com/OpenBMB/MiniCPM-OCR#skill)

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

## Parsing pipeline

MiniCPM-OCR 1.0 parses full documents as a **two-stage pipeline** orchestrated by the [`minicpm-ocr` SDK](https://pypi.org/project/minicpm-ocr/). The two stages use separate models, run in separate environments, and may run on different machines:

- **Stage 1 — Layout detection (SDK environment).** The PP-DocLayoutV3 layout model detects document regions — text, tables, formulas, charts, seals — and determines reading order; the SDK crops each region. It runs locally inside the SDK environment and requires PaddlePaddle / PaddleX.
- **Stage 2 — Region recognition (inference service).** The SDK sends each cropped region over HTTP to a MiniCPM-OCR 1.0 inference service — served by vLLM, SGLang, llama.cpp, or Ollama — with a prompt matching the region type, then assembles the recognized content into the final Markdown / JSON in reading order.

<p align="center"><img src="assets/parsing_pipeline.svg" alt="Parsing pipeline: in the minicpm-ocr SDK environment, the PP-DocLayoutV3 layout model detects and crops document regions; each cropped region is sent over HTTP to a separate recognition service running MiniCPM-OCR 1.0 (vLLM, SGLang, llama.cpp, or Ollama); the SDK then assembles the recognized text, tables, formulas, charts, and seals into Markdown and JSON in reading order." width="90%"></p>

See the [model guide](https://github.com/OpenBMB/MiniCPM-OCR/blob/main/docs/minicpm_ocr_1dot0_en.md) for more on architecture, parsing workflow, deployment options, and benchmark breakdowns.

## Quick start

### Use with the MiniCPM-OCR SDK

> **Required before using either the CLI or Python API:** deploy and start the OCR model service first, and wait until it is ready to accept requests. The SDK examples below are clients of that running service; they do not deploy or start the OCR model service automatically.

Use the official `minicpm-ocr` SDK to parse local images or PDFs with this
GGUF checkpoint. The SDK detects layout with PP-DocLayoutV3, recognises each
region, and saves structured JSON and Markdown in reading order.

Install Python 3.10+ and the SDK:

```bash
pip install "minicpm-ocr[all]"
```

Install minicpm-ocr for your platform using the
[installation guide](https://github.com/OpenBMB/MiniCPM-OCR/blob/main/docs/minicpm_ocr_tutorial_en.md#1-set-up-the-sdk-environment).

#### Prerequisite: deploy and start the model service

Before running the SDK, start a llama.cpp recognition service using this
repository's `MiniCPM-OCR-1_0-Q8_0.gguf` and the required
`mmproj-model-f16-4x.gguf` vision projector. Follow the
[llama.cpp deployment guide](https://github.com/OpenBMB/MiniCPM-OCR/blob/main/docs/llamacpp_deploy.md).
For the SDK examples below, configure the service with `--port 8080`,
`--alias minicpm-ocr`, `--ctx-size 8192`, `--parallel 1`, and
`--jinja --reasoning off`. If you keep the guide's port `18499`, change the SDK
URL to match. DSpark setup, when used, is covered by the same guide.

The SDK uses the `llamacpp` backend, an 8192-token context, and one recognition
request at a time. Layout detection runs on CPU in these examples; the
recognition service can independently use Metal, CUDA, or CPU. If you increase
the service context per request slot, update `engine.max_model_len` accordingly.

#### CLI

**Start the model service described above and wait until it is ready before running this command.**
Save a local image as `demo.png`, then run:

```bash
minicpmvocr parse demo.png \
  --backend llamacpp \
  --server-url http://127.0.0.1:8080 \
  --model minicpm-ocr \
  --device cpu \
  --set engine.max_model_len=8192 \
  --workers 1 \
  --set pipeline.queue_mode=serial \
  --set pipeline.overlap_layout=false \
  --set run.run_root=output \
  --output output/demo.md
```

The CLI automatically downloads PP-DocLayoutV3 to `models/PP-DocLayoutV3_infer/`
when needed. The final Markdown is saved to `output/demo.md`; structured JSON
and per-page Markdown are kept in `output/<run_tag>/results_json/` and
`output/<run_tag>/output/`.

#### Python API

**The model service described above must already be running before you execute this Python example.**
Set `engine.server_url` and `engine.model_name` to match that service.

The same pipeline is available from Python:

```python
from importlib.resources import files
from pathlib import Path

from minicpmvocr import load_config, pipelined_run
from minicpmvocr.layouts.download import ensure_layout_model


def main():
    layout_model = ensure_layout_model(Path("models/PP-DocLayoutV3_infer"))

    cfg = load_config(
        str(files("minicpmvocr").joinpath("configs/minicpmvocr.yaml")),
        overrides={
            "input": {"file_path": str(Path("demo.png").resolve())},
            "engine": {
                "type": "llamacpp",
                "server_url": "http://127.0.0.1:8080",
                "model_name": "minicpm-ocr",
                "max_model_len": 8192,
            },
            "layout": {
                "model_dir": str(layout_model),
                "device": "cpu",
            },
            "pipeline": {
                "overlap_layout": False,
                "queue_mode": "serial",
                "max_workers": 1,
            },
            "run": {"run_root": str(Path("output").resolve())},
        },
    )

    pipelined_run(cfg)

    print("JSON directory:", cfg["_meta"]["result_json_dir"])
    print("Markdown directory:", cfg["_meta"]["output_dir"])


if __name__ == "__main__":
    main()
```

`ensure_layout_model()` reuses or downloads the official layout model.
Results are written to `output/<run_tag>/results_json/` and
`output/<run_tag>/output/`. To parse a PDF, replace `demo.png` with its local path.

For CUDA layout detection, change `--device cpu` to `--device cuda:0` in the CLI,
or set `layout.device` to `cuda:0` in Python, after installing the matching
PaddlePaddle runtime. Keep SDK recognition concurrency aligned with the
llama.cpp service's request slots.

Run `minicpmvocr parse --help` for CLI options, or see the
[SDK API reference](https://github.com/OpenBMB/MiniCPM-OCR/blob/main/docs/minicpm_ocr_sdk_api_en.md)
for configuration and document-level Markdown export.

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