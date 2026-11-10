---
license: apache-2.0
library_name: transformers
pipeline_tag: image-text-to-text
base_model: Qwen/Qwen3-Omni-30B-A3B-Instruct
base_model_relation: finetune
tags:
- clef
- cloudflare
- systemone
- decision-model
- qwen3-omni
- post-train
- image-text-to-typed-output
- multimodal
- audio
- video
- structured-output
- classification
- custom-code
---

# Clef-Omni

- **Announcement:** [Clef-omni model relase on the Cloudflare blog](https://blog.cloudflare.com/clef-faster-cheaper-multimodal)

Clef-Omni is a 30B-A3B mixture-of-experts multimodal model that turns a state and a schema of typed
questions into decisions. It reads the state as text, JSON, images, audio, or video, and returns a
probability for every allowed option of every question in a single forward pass. There is no
free-form text generation and no output parsing.

The Clef-Omni API is fully compatible with Jev and SystemOne.

Clef-Omni is post-trained from
[Qwen/Qwen3-Omni-30B-A3B-Instruct](https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Instruct). See
[Clef](https://huggingface.co/Cloudflare/clef) and [Clef-Flash](https://huggingface.co/Cloudflare/clef-flash)
for the dense image and video variants.

## Model

- **Backbone:** the Qwen/Qwen3-Omni-30B-A3B-Instruct thinker with its vision and audio encoders, stored
  as standard sharded safetensors. The base model's speech-output weights (talker and code2wav) are
  included unchanged but are not used; `load_release_model` does not load them.
- **Joint schema head:** a small transformer head that reads the backbone's final hidden states,
  routes evidence from the state to each question, and scores all options of all questions jointly.
- **Output:** one logit per allowed option for each question. Apply a softmax per question to get
  probabilities.

## Files

| File | Purpose |
|---|---|
| `model-*.safetensors`, `model.safetensors.index.json`, `config.json`, `generation_config.json` | Backbone, including the vision and audio encoders |
| `joint_head.safetensors`, `joint_head_config.json` | Joint schema head |
| `joint_schema_model.py` | Record encoding, media decoding, batching, the model, `load_release_model`, and `systemone` |
| `tokenizer.json`, `tokenizer_config.json`, `chat_template.jinja`, `processor_config.json` | Tokenizer and image/audio/video processor |
| `LICENSE` | Apache-2.0 license |

## Usage

Tested with `torch` 2.11 and `transformers` 5.10.2 on a single H200; the backbone needs about 64 GB
of GPU memory in bfloat16. Image inputs also need `pillow`, and audio and video files need `av`.

```python
import sys

import torch
from huggingface_hub import snapshot_download

path = snapshot_download("Cloudflare/clef-omni")
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

`systemone` takes a Jev/SystemOne `POST /v1/systemone` request body and returns the same response
body: `model`, `answers` keyed by question ID, and `usage`. A `choice` answer has `choice`,
`confidence`, and `probabilities`; a `score` answer has the expected `score`, `confidence`, `legend`,
and `probabilities`; a `noul` answer has the probability of true. `instructions` is optional, and
`images`, `audio`, and `videos` (base64 data URLs) may be added to the request.

```python
from joint_schema_model import systemone

response = systemone(model, processor, {
    "model": "clef-omni",
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

### Images, audio, and video

Add `images`, `audio`, or `videos` to the record and pass the processor to `encode_record`. Each item
can be a file path, URL, base64 data URL, or raw bytes. Images may also be PIL images, audio may be
16 kHz mono sample arrays, and videos may be RGB frame arrays sampled at 2 frames per second. Video
files are sampled at 2 frames per second, and their soundtracks are heard alongside the frames when
every video in the record has one. Optional processor arguments go in `media_kwargs`.

```python
record = {
    "state": {"task": "Review the attached call recording and dashcam clip."},
    "audio": ["call.wav"],
    "videos": ["dashcam.mp4"],
    "questions": {
        "glass": {"type": "noul", "instructions": "Is glass breaking in the audio clip?"},
        "collision": {"type": "noul", "instructions": "Does the video show a collision?"},
    },
}
encoded = encode_record(processor.tokenizer, record, processor=processor)
```

Text-only and multimodal records can be mixed in the same batch.

### SGLang

Use SGLang (coming soon!)

## Input format

| Field | Description |
|---|---|
| `state` | Any JSON value or string describing the situation |
| `images` | Optional list of images |
| `audio` | Optional list of audio clips |
| `videos` | Optional list of videos |
| `media_kwargs` | Optional keyword arguments for the processor |
| `questions` | Mapping of question ID to question |

Each question has:

- `type`: `noul` (true/false), `choice` (named options), or `score` (ordered options)
- `instructions`: what to decide; optional, and the question ID is used when it is omitted
- `criteria`: for `choice`, a mapping of option ID to description; for `score`, a list of option
  descriptions indexed from 0; for `noul`, optional descriptions for `true` and `false`

`encode_record` accepts `max_length` (default 64,000 tokens) and `max_state_tokens` to bound the input.

## Results

### Decision Index

Per-benchmark results from our internal run of the [Decision Index](https://clef-evals.workers-ai-mle.workers.dev) 0.2.1 suite. Scores are percentages; ForecastBench is a Brier score, where lower is better. The best value in each row is in bold.

| Benchmark | Clef-Omni | Clef | Clef-flash | Jev |
|---|---|---|---|---|
| BFCL (case exact accuracy) | 98.2 | 98.5 | **98.8** | 95.8 |
| ToolRet (nDCG@10) | 66.6 | **69.2** | 66.4 | 65.3 |
| API-Bank (accuracy) | 92.7 | 91.9 | **93.1** | 88.2 |
| BANKING77 (macro-F1) | **94.8** | 94.2 | 90.9 | 79.7 |
| CLINC150+OOS (macro-F1) | **97.7** | 97.4 | 66.8 | 89.3 |
| RouterBench (selected quality) | **79.9** | 79.7 | **79.9** | **79.9** |
| Home appliance simulator (case exact accuracy) | 69.3 | 83.0 | **97.7** | 52.3 |
| SGD/SGD-X (macro-F1) | 39.2 | **43.8** | 34.2 | 43.0 |
| ContractNLI (macro-F1) | 80.3 | 81.4 | **84.3** | 71.7 |
| ANLI (macro-F1) | 65.5 | 69.8 | 59.1 | **74.8** |
| BPoMP (accuracy) | 96.8 | **96.9** | 95.4 | 90.6 |
| Humicroedit (accuracy) | 70.1 | 66.7 | **75.1** | 61.9 |
| POP909-CL (accuracy) | 2.6 | 15.8 | 1.6 | **18.1** |
| cfcolor (accuracy) | 62.9 | **66.0** | 65.8 | 64.7 |
| MMLU (accuracy) | **92.7** | 90.3 | 91.8 | 91.7 |
| GPQA Diamond (accuracy) | 47.4 | 48.0 | 51.0 | **78.3** |
| ARC-Easy (accuracy) | **99.8** | 99.0 | 99.5 | 99.3 |
| ARC-Challenge (accuracy) | 97.8 | 97.7 | **98.3** | 97.8 |
| WinoGrande (accuracy) | 96.7 | 93.5 | **97.5** | 92.0 |
| HellaSwag (accuracy) | **99.1** | 98.2 | 98.6 | 94.5 |
| GSM8K (accuracy) | 79.0 | **80.8** | 67.3 | 79.9 |
| ChessBench (accuracy) | 22.1 | **24.7** | 23.0 | 17.2 |
| MuSR (accuracy) | 83.8 | 83.5 | **86.0** | 66.1 |
| SATA-Bench (case exact accuracy) | 31.9 | 33.8 | **36.7** | 26.4 |
| BRIGHT (nDCG@10) | 42.0 | 45.9 | 39.3 | **47.5** |
| Amazon ESCI (macro-F1) | **57.8** | 57.5 | 57.4 | 55.2 |
| ACOS (per-review F1) | 28.4 | **33.3** | 25.9 | 29.5 |
| FinEntity (macro-F1) | 96.3 | 96.2 | **97.1** | 87.0 |
| VAST (macro-F1) | 50.9 | 59.5 | 49.6 | **64.6** |
| NLI4CT (macro-F1) | 76.8 | 82.9 | 78.6 | **84.1** |
| CRUXEval (accuracy) | **88.8** | 86.7 | 86.1 | 73.0 |
| CLadder (accuracy) | 97.2 | 94.0 | **97.7** | 72.6 |
| ForecastBench (Brier, lower is better) | 11.7 | 13.9 | **10.6** | 17.4 |
| Habermas Machine (accuracy) | 67.8 | 68.7 | **71.8** | 45.9 |
| PhishNChips (accuracy) | 73.2 | **79.6** | 75.0 | 62.5 |
| MMLU-Pro (accuracy) | 70.6 | 65.9 | 65.3 | **82.7** |
| BBH (accuracy) | 69.0 | 73.7 | 68.9 | **92.9** |
| RAGTruth (hallucination F1) | 42.0 | **79.4** | 35.6 | 76.5 |
| HoVer (accuracy) | 64.2 | 65.2 | 61.2 | **72.9** |
| When2Call MCQ (accuracy) | 63.3 | 72.4 | 65.6 | **81.0** |
| New Yorker (accuracy) | 64.2 | 69.5 | 66.1 | **70.1** |

### Workflow evals

Decision accuracy on four end-to-end business workflows from [Typesafe Evals](https://evals.typesafe.ai/), scored against consensus reference labels. All models are scored on the same dataset revision and case cohort.

| Workflow | Metric | Clef-Omni | Clef | Clef-flash | Jev |
|---|---|---:|---:|---:|---:|
| Invoice processing | Exact actions | 60.2 | **64.7** | 57.1 | 61.8 |
| Invoice processing | Primary action | 82.0 | **86.2** | 73.3 | 83.1 |
| Customer service | Exact actions | 71.6 | 76.3 | **77.0** | 76.0 |
| Security incidents | Exact actions | 61.7 | **62.9** | 61.7 | 61.7 |
| Agent trace observability | Primary action | 65.8 | 68.5 | 69.8 | **71.6** |

## License

Released under the Apache-2.0 license, following the base model
[Qwen/Qwen3-Omni-30B-A3B-Instruct](https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Instruct).
