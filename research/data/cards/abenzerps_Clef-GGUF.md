---
license: apache-2.0
base_model: Cloudflare/clef
base_model_relation: quantized
pipeline_tag: image-text-to-text
library_name: gguf
tags:
- gguf
- llama.cpp
- qwen3.5
- multimodal
- clef
- cloudflare
---

# Clef GGUF

GGUF quantizations of [Cloudflare/clef](https://huggingface.co/Cloudflare/clef), a 27B multimodal decision model post-trained from Qwen3.8-27B. For image or video input, use the included multimodal projector (`clef-mmproj-BF16.gguf`).

## GGUF files

| Quantization | File | Size | Notes |
| --- | --- | ---: | --- |
| IQ1_M | [clef-IQ1_M.gguf](clef-IQ1_M.gguf) | 7.63 GB | Ultra-low-memory option |
| IQ2_M | [clef-IQ2_M.gguf](clef-IQ2_M.gguf) | 10.0 GB | Smallest recommended option |
| Q2_K | [clef-Q2_K.gguf](clef-Q2_K.gguf) | 10.7 GB | Maximum-compression K-quant |
| IQ3_M | [clef-IQ3_M.gguf](clef-IQ3_M.gguf) | 12.6 GB | Importance-aware compact option |
| Q3_K_M | [clef-Q3_K_M.gguf](clef-Q3_K_M.gguf) | 13.3 GB | Standard Q3 K-quant |
| Q4_0 | [clef-Q4_0.gguf](clef-Q4_0.gguf) | 15.5 GB | Standard 4-bit quantization |
| Q4_K_M | [clef-Q4_K_M.gguf](clef-Q4_K_M.gguf) | 16.5 GB | Recommended default K-quant |
| Q5_K_M | [clef-Q5_K_M.gguf](clef-Q5_K_M.gguf) | 19.2 GB | Higher-quality Q5 option |
| Q6_K | [clef-Q6_K.gguf](clef-Q6_K.gguf) | 22.1 GB | High-quality option |
| Q8_0 | [clef-Q8_0.gguf](clef-Q8_0.gguf) | 28.6 GB | Near-lossless reference quantization |
| Vision projector | [clef-mmproj-BF16.gguf](clef-mmproj-BF16.gguf) | 931 MB | Required for image/video input |

## Usage

Use a current [llama.cpp](https://github.com/ggml-org/llama.cpp) build with the included [chat template](chat_template.jinja).

```bash
llama-cli \
  -m clef-Q4_K_M.gguf \
  -c 4096 -n 512 --temp 1.0 --top-p 0.95 \
  --jinja --chat-template-file chat_template.jinja \
  -p "Explain why reproducible builds matter."
```

For image input:

```bash
llama-mtmd-cli \
  -m clef-Q4_K_M.gguf \
  -mm clef-mmproj-BF16.gguf \
  --image image.jpg -p "Describe this image."
```

<details>
<summary>Original Python / Transformers Usage</summary>

Tested with `torch` 2.11 and `transformers` 5.10.2 on a single H200. Image and video inputs also need `pillow`.

```python
import sys

import torch
from huggingface_hub import snapshot_download

path = snapshot_download("Cloudflare/clef")
sys.path.insert(0, path)
from joint_schema_model import collate_records, encode_record, load_release_model

model, processor = load_release_model(path, device="cuda")

record = {
    "state": {"invoice": {"vendor": "Acme", "total": 1250.0, "currency": "USD", "status": "overdue"}},
    "questions": {
        "status": {
            "type": "choice",
            "instructions": "What is the invoice status?",
            "criteria": {"paid": "Invoice is paid.", "overdue": "Invoice is past due.", "draft": "Not sent."},
        },
        "large": {"type": "noul", "instructions": "Is the total above 1000 USD?"},
    },
}

encoded = encode_record(processor.tokenizer, record, processor=processor)
batch = collate_records([encoded], processor.tokenizer.pad_token_id, torch.device("cuda"))
with torch.inference_mode():
    logits = model(batch)[0]

for question, question_logits in zip(encoded.questions, logits):
    probabilities = question_logits.float().softmax(-1).tolist()
    print(question.question_id, dict(zip(question.option_ids, probabilities)))
```

### Jev / SystemOne API
`systemone` takes a Jev/SystemOne `POST /v1/systemone` request body and returns the same response body: `model`, `answers` keyed by question ID, and `usage`. A `choice` answer has `choice`, `confidence`, and `probabilities`; a `score` answer has the expected `score`, `confidence`, `legend`, and `probabilities`; a `noul` answer has the probability of true. `instructions` is optional, and `images` and `videos` may be added to the request.

```python
from joint_schema_model import systemone

response = systemone(model, processor, {
    "model": "clef",
    "state": "Our checkout started returning errors and orders are blocked.",
    "questions": {
        "department": {
            "type": "choice",
            "instructions": "Which team should handle the message?",
            "criteria": {"billing": "Payments or invoices", "technical": "Bugs or outages"},
        },
        "urgency": {"type": "score", "criteria": ["Can wait", "This week", "Today"]},
        "outage": {"type": "noul", "instructions": "Is a service down?"},
    },
})
print(response["answers"])
```

### Images and video
Add `images` (PIL images) or `videos` (frame arrays) to the record and pass the processor to `encode_record`. Optional processor arguments go in `media_kwargs`.

```python
from PIL import Image

record = {
    "state": {"task": "Review the attached receipt."},
    "images": [Image.open("receipt.jpg")],
    "questions": {
        "legible": {"type": "noul", "instructions": "Is the receipt total legible?"},
    },
}
encoded = encode_record(processor.tokenizer, record, processor=processor)
```

Text-only and multimodal records can be mixed in the same batch.

| Field | Description |
|---|---|
| `state` | Any string or JSON value describing the situation to decide on |
| `images`, `videos` | Optional lists of images or video frame arrays |
| `media_kwargs` | Optional keyword arguments for the image/video processor |
| `questions` | Mapping of question ID to question |

Each question has:

- `type`: `noul` (true/false), `choice` (named options), or `score` (ordered options)
- `instructions`: what to decide; optional, and the question ID is used when it is omitted
- `criteria`: for `choice`, a mapping of option ID to description; for `score`, a list of option descriptions indexed from 0; for `noul`, optional descriptions for `true` and `false`

`encode_record` accepts `max_length` (default 16,384 tokens) and `max_state_tokens` to bound the input.

</details>

## Benchmarks

<details>
<summary>Decision Index & Workflow Evals</summary>

### Decision Index
Per-benchmark results from our internal run of the [Decision Index](https://clef-evals.workers-ai-mle.workers.dev) 0.2.1 suite. Scores are percentages; ForecastBench is a Brier score, where lower is better. The last two rows are request latency in milliseconds, where lower is better. The best value in each row is in bold.

| Benchmark | Clef | Clef-flash | Jev | DiffusionGemma Jev | Kev 9B | Laya |
|---|---|---|---|---|---|---|
| BFCL (case exact accuracy) | 98.5 | **98.8** | 95.8 | 96.5 | 94.5 | 38.1 |
| ToolRet (nDCG@10) | **69.2** | 66.4 | 65.3 | 61.2 | 64.3 | 12.8 |
| API-Bank (accuracy) | 91.9 | **93.1** | 88.2 | 83.7 | 56.3 | 11.5 |
| BANKING77 (macro-F1) | **94.2** | 90.9 | 79.7 | 74.3 | 84.8 | 14.3 |
| CLINC150+OOS (macro-F1) | **97.4** | 66.8 | 89.3 | 83.5 | 79.0 | 3.2 |
| RouterBench (selected quality) | 79.7 | 79.9 | 79.9 | 79.0 | **80.0** | 57.1 |
| Home appliance simulator (case exact accuracy) | 83.0 | **97.7** | 52.3 | 42.0 | 25.0 | 0.0 |
| SGD/SGD-X (macro-F1) | 43.8 | 34.2 | 43.0 | 40.6 | **64.0** | 42.4 |
| ContractNLI (macro-F1) | 81.4 | **84.3** | 71.7 | 76.0 | 57.8 | 29.0 |
| ANLI (macro-F1) | 69.8 | 59.1 | **74.8** | 66.4 | 56.3 | 48.7 |
| BPoMP (accuracy) | **96.9** | 95.4 | 90.6 | 86.9 | 67.0 | 51.6 |
| Humicroedit (accuracy) | 66.7 | **75.1** | 61.9 | 63.0 | 55.8 | 47.2 |
| POP909-CL (accuracy) | 15.8 | 1.6 | **18.1** | 2.5 | 10.8 | 5.1 |
| cfcolor (accuracy) | **66.0** | 65.8 | 64.7 | 58.2 | 56.3 | 52.3 |
| MMLU (accuracy) | 90.3 | **91.8** | 91.7 | 79.3 | 75.3 | 30.7 |
| GPQA Diamond (accuracy) | 48.0 | 51.0 | **78.3** | 44.9 | 38.8 | 27.6 |
| ARC-Easy (accuracy) | 99.0 | **99.5** | 99.3 | 98.2 | 97.7 | 47.0 |
| ARC-Challenge (accuracy) | 97.7 | **98.3** | 97.8 | 94.5 | 93.7 | 28.6 |
| WinoGrande (accuracy) | 93.5 | **97.5** | 92.0 | 73.6 | 73.2 | 50.5 |
| HellaSwag (accuracy) | 98.2 | **98.6** | 94.5 | 83.3 | 81.9 | 33.1 |
| GSM8K (accuracy) | **80.8** | 67.3 | 79.9 | 50.3 | 48.7 | 21.6 |
| ChessBench (accuracy) | **24.7** | 23.0 | 17.2 | 14.2 | 11.2 | 7.7 |
| MuSR (accuracy) | 83.5 | **86.0** | 66.1 | 61.2 | 57.9 | 43.2 |
| SATA-Bench (case exact accuracy) | 33.8 | **36.7** | 26.4 | 27.5 | 26.7 | 0.3 |
| BRIGHT (nDCG@10) | 45.9 | 39.3 | **47.5** | 42.9 | 38.5 | 19.9 |
| Amazon ESCI (macro-F1) | **57.5** | 57.4 | 55.2 | 53.4 | 49.2 | 24.4 |
| ACOS (per-review F1) | **33.3** | 25.9 | 29.5 | 24.5 | 18.3 | 3.5 |
| FinEntity (macro-F1) | 96.2 | **97.1** | 87.0 | 89.0 | 88.4 | 61.0 |
| VAST (macro-F1) | 59.5 | 49.6 | **64.6** | 55.7 | 55.4 | 40.5 |
| NLI4CT (macro-F1) | 82.9 | 78.6 | **84.1** | 78.4 | 74.9 | 47.7 |
| CRUXEval (accuracy) | **86.7** | 86.1 | 73.0 | 64.7 | 51.2 | 40.2 |
| CLadder (accuracy) | 94.0 | **97.7** | 72.6 | 67.8 | 62.0 | 52.9 |
| ForecastBench (Brier, lower is better) | 13.9 | **10.6** | 17.4 | 29.6 | 17.6 | 41.1 |
| Habermas Machine (accuracy) | 68.7 | **71.8** | 45.9 | 45.0 | 39.4 | 33.4 |
| PhishNChips (accuracy) | 79.6 | 75.0 | 62.5 | **85.4** | 50.7 | 50.1 |
| MMLU-Pro (accuracy) | 65.9 | 65.3 | **82.7** | 56.9 | 51.1 | 13.6 |
| BBH (accuracy) | 73.7 | 68.9 | **92.9** | 70.7 | 65.2 | 34.1 |
| RAGTruth (hallucination F1) | **79.4** | 35.6 | 76.5 | 70.4 | 46.2 | 48.8 |
| HoVer (accuracy) | 65.2 | 61.2 | **72.9** | 70.9 | 58.8 | 55.8 |
| When2Call MCQ (accuracy) | 72.4 | 65.6 | **81.0** | 75.4 | 49.6 | 11.9 |
| New Yorker (accuracy) | 69.5 | 66.1 | **70.1** | 63.6 | 58.1 | 27.1 |
| Median latency (ms) | 209.3 | 38.8 | 524.1 | 84.4 | 51.4 | **5.8** |
| p95 latency (ms) | 238.6 | **122.4** | 536.0 | 211.2 | 187.9 | 222.5 |

### Workflow evals
Decision accuracy on four end-to-end business workflows from [Typesafe Evals](https://evals.typesafe.ai/), scored against consensus reference labels. All models are scored on the same dataset revision and case cohort.

| Workflow | Metric | Clef | Clef-flash | Jev |
|---|---|---:|---:|---:|
| Invoice processing | Exact actions | **64.7** | 57.1 | 61.8 |
| Invoice processing | Primary action | **86.2** | 73.3 | 83.1 |
| Customer service | Exact actions | 76.3 | **77.0** | 76.0 |
| Security incidents | Exact actions | **62.9** | 61.7 | 61.7 |
| Agent trace observability | Primary action | 68.5 | 69.8 | **71.6** |

</details>

## Source

- Model: [Cloudflare/clef](https://huggingface.co/Cloudflare/clef)
- Base model: [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B)
- License: [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0)
- Checksums: [SHA256SUMS](SHA256SUMS)
