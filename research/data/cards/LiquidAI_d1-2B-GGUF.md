---
library_name: gguf
license: other
license_name: lfm1.0
license_link: LICENSE
language:
- en
- ar
- zh
- fr
- de
- it
- ja
- ko
- pt
- es
- vi
- th
- id
- hi
- ru
- pl
pipeline_tag: image-text-to-text
base_model: LiquidAI/d1-2B
tags:
- liquid
- lfm3
- edge
- decision
- classification
- extraction
- calibration
- system-one
- multimodal
- decision-model
- gguf
- llama.cpp
---

<div align="center">
  <img
    src="https://huggingface.co/LiquidAI/d1-2B/resolve/main/assets/liquid-ai-banner.webp"
    alt="Liquid AI"
    style="width: 100%; max-width: 100%; height: auto; display: block; margin: 0;"
  />
  <div align="center" style="display: flex; justify-content: center; align-items: center; gap: 1.25em; margin: 8px 0 1.7rem; padding: 0; line-height: 1.3;">
    <a href="https://console.liquid.ai/dashboard" style="display: inline-flex; align-items: center; gap: 6px;"><img src="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2216%22 height=%2216%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke-width=%222.2%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22%3E%3Cstyle%3Epath%7Bstroke:%23000%7D%40media (prefers-color-scheme:dark)%7Bpath%7Bstroke:%23d1d5dc%7D%7D%3C/style%3E%3Cpath d=%22m8 6-6 6 6 6m8-12 6 6-6 6m-2-14-4 16%22/%3E%3C/svg%3E" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>API</strong></a>
    <a href="https://playground.liquid.ai/" style="display: inline-flex; align-items: center; gap: 6px;"><img src="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2216%22 height=%2216%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke-width=%222.2%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22%3E%3Cstyle%3Epath%7Bstroke:%23000%7D%40media (prefers-color-scheme:dark)%7Bpath%7Bstroke:%23d1d5dc%7D%7D%3C/style%3E%3Cpath transform=%22translate(3 0)%22 d=%22M8 5.5v13L19 12 8 5.5Z%22/%3E%3C/svg%3E" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>Try</strong></a>
    <a href="https://docs.liquid.ai/lfm/getting-started/welcome" style="display: inline-flex; align-items: center; gap: 6px;"><img src="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2216%22 height=%2216%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke-width=%222.2%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22%3E%3Cstyle%3Epath%7Bstroke:%23000%7D%40media (prefers-color-scheme:dark)%7Bpath%7Bstroke:%23d1d5dc%7D%7D%3C/style%3E%3Cpath d=%22M12 6c-3-2-6-2.5-10-2v15c4-.5 7 0 10 2m0-15c3-2 6-2.5 10-2v15c-4-.5-7 0-10 2V6Z%22/%3E%3C/svg%3E" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>Docs</strong></a>
    <a href="https://www.liquid.ai/blog/open-d1" style="display: inline-flex; align-items: center; gap: 6px;"><img src="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2216%22 height=%2216%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke-width=%222.2%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22%3E%3Cstyle%3Epath%7Bstroke:%23000%7D%40media (prefers-color-scheme:dark)%7Bpath%7Bstroke:%23d1d5dc%7D%7D%3C/style%3E%3Cpath transform=%22translate(1 0)%22 d=%22m16 3 5 5L8 21H3v-5L16 3Zm-3 3 5 5%22/%3E%3C/svg%3E" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>Blog</strong></a>
  </div>
</div>

# d1-2B-GGUF

GGUF version of [d1-2B](https://huggingface.co/LiquidAI/d1-2B) for local inference on CPUs and GPUs.

d1-2B is a decision model for text, pictures, and video, built on [LFM3-VL-2B](https://huggingface.co/LiquidAI/LFM3-VL-2B). It returns calibrated answers in one forward pass, without generating tokens.

Find architecture and usage details in the [original model card](https://huggingface.co/LiquidAI/d1-2B).

## Use with llama.cpp
<hr style="margin: -0.7em 0 1.2em 0; border: 0; border-top: 1px solid rgba(127, 127, 127, 0.3);" />

> [!NOTE]
> Supported in [llama.cpp](https://github.com/ggml-org/llama.cpp) [b11960](https://github.com/ggml-org/llama.cpp/releases/tag/b11960) ([v0.8.0](https://github.com/ggml-org/llama.cpp/releases/tag/v0.8.0)) and newer.

llama.cpp answers `noul`, `choice` and `score` questions over a state (text or JSON), pictures or a video. Video input needs `ffmpeg` in `PATH`. Multiple choice (`"multiple": true`), extraction, estimates and boxes are not supported yet.

```bash
llama-server -hf LiquidAI/d1-2B-GGUF:Q8_0 -b 8192 -ub 8192
```

A question is read in one batch, so `-b` and `-ub` must hold its state and media. A picture takes at most half of `-ub`: 8192 keeps the full budget of 4096 tokens per picture, smaller values lower it.

Then send questions to the `/v1/systemone` endpoint.

### Text

```bash
curl http://127.0.0.1:8080/v1/systemone -H "Content-Type: application/json" -d '{
  "state": "I was charged twice this month, please refund one of them.",
  "questions": {
    "refund":  {"type": "noul", "instructions": "Is the customer asking for a refund?"},
    "team":    {"type": "choice", "instructions": "Which team should handle this?",
                "criteria": {"billing": "Charges, refunds, invoices", "technical": "App or site faults",
                             "fraud": "Suspected unauthorised use"}},
    "urgency": {"type": "score", "instructions": "How urgent is this?",
                "criteria": ["Can wait", "Today", "Blocking the customer now"]}
  }
}'
```

### Image + Text

```bash
curl -sL -o cats.jpg http://images.cocodataset.org/val2017/000000039769.jpg  # two cats on a sofa

curl http://127.0.0.1:8080/v1/systemone -H "Content-Type: application/json" -d @- <<JSON
{
  "state": "Photo attached to a pet-sitting request.",
  "images": ["data:image/jpeg;base64,$(base64 < cats.jpg | tr -d '\n')"],
  "questions": {
    "pet":  {"type": "choice", "instructions": "Which animals are in the photo?",
             "criteria": {"cats": "Cats", "dogs": "Dogs", "birds": "Birds"}},
    "sofa": {"type": "noul", "instructions": "Are the animals on a sofa?"}
  }
}
JSON
```

### Video + Text

```bash
curl -sL -o reading.mp4 https://huggingface.co/datasets/raushan-testing-hf/videos-test/resolve/4cba700bd771f44d72b549253da025c32e944d42/sample_demo_1.mp4  # a child reading a book

curl http://127.0.0.1:8080/v1/systemone -H "Content-Type: application/json" -d @- <<JSON
{
  "state": null,
  "files": ["data:video/mp4;base64,$(base64 < reading.mp4 | tr -d '\n')"],
  "questions": {
    "activity": {"type": "choice", "instructions": "What is the child doing?",
                 "criteria": {"reading": "Reading a book", "eating": "Eating", "sleeping": "Sleeping"}},
    "glasses":  {"type": "noul", "instructions": "Is the child wearing glasses?"}
  }
}
JSON
```

The state can be `null` when the pictures or the video are the whole state.
