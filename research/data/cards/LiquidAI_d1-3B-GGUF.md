---
library_name: gguf
license: other
license_name: lfm1.0
license_link: LICENSE
language:
- ar
- zh
- en
- fr
- de
- hi
- id
- it
- ja
- ko
- pl
- pt
- ru
- es
- th
- vi
pipeline_tag: image-text-to-text
base_model: LiquidAI/d1-3B
tags:
- liquid
- lfm2.5
- edge
- decision
- classification
- calibration
- system-one
- multimodal
- gguf
- llama.cpp
---

<div align="center">
  <img
    src="https://cdn-uploads.huggingface.co/production/uploads/61b8e2ba285851687028d395/2b08LKpev0DNEk6DlnWkY.png"
    alt="Liquid AI"
    style="width: 100%; max-width: 100%; height: auto; display: inline-block; margin-bottom: 0.5em; margin-top: 0.5em;"
  />
  <div style="display: flex; justify-content: center; gap: 0.5em; margin-bottom: 1em;">
    <a href="https://playground.liquid.ai/"><strong>Try LFM</strong></a> •
    <a href="https://docs.liquid.ai/lfm/getting-started/welcome"><strong>Docs</strong></a> •
    <a href="https://discord.com/invite/liquid-ai"><strong>Discord</strong></a>
  </div>
</div>

# d1-3B-GGUF

d1-3B is a decision model developed by [Liquid AI](https://www.liquid.ai/): it answers named, typed questions over a state (text, JSON or images) in one forward pass, with no generated tokens.

Find more details in the original model card: https://huggingface.co/LiquidAI/d1-3B

## 🏃 How to run d1-3B

Example usage with [llama.cpp](https://github.com/ggml-org/llama.cpp):

```bash
llama-server -hf LiquidAI/d1-3B-GGUF:Q8_0
```

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

The state can be `null` when the images are the whole state.
