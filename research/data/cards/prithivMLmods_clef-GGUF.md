---
license: apache-2.0
language:
- en
base_model:
- Cloudflare/clef
pipeline_tag: image-text-to-text
library_name: transformers
tags:
- text-generation-inference
- llama-cpp
- clef
- cloudflare
- systemone
- decision-model
- qwen3.5
- qwen3.8
- post-train
- image-text-to-typed-output
- multimodal
- structured-output
- classification
- custom-code
---

# **clef-GGUF**

> Clef is a 27B multimodal decision model from Cloudflare, post-trained from Qwen/Qwen3.8-27B (Apache-2.0). It reads a state given as text, JSON, images, or video, plus a schema of typed questions (`noul` for true/false, `choice` for named options, `score` for ordered options). In a single forward pass it returns a probability for every allowed option of every question. A small joint schema head sits on the backbone's final hidden states, routes evidence from the state to each question, and scores all options jointly, so there is no free-form text generation or output parsing. It exposes a Jev/SystemOne-compatible `/v1/systemone` API, either through the included `joint_schema_model.py` or by serving with SGLang, for example on a single H200. On the Decision Index 0.2.1 suite it leads or is near the top on many benchmarks, including BANKING77, CLINC150+OOS, BPoMP, GSM8K, CRUXEval, and RAGTruth. It trails Jev on harder reasoning benchmarks such as GPQA Diamond, MMLU-Pro, and BBH. Its median latency is about 209 ms, versus about 39 ms for the smaller Clef-Flash. It also does well on Typesafe workflow evals such as invoice processing and security incidents.

> [!NOTE]
> This is a Decision Model GGUF that supports the llama.cpp `v1/systemone` API endpoint.

## Model Files

| File Name | Quant Type | File Size | File Link | Description |
|-----------|------------|-----------|-----------|-------------|
| clef.BF16.gguf | BF16 | 54.1 GB | [Link](https://huggingface.co/prithivMLmods/clef-GGUF/blob/main/clef.BF16.gguf) | Full BF16 weights. Highest quality, largest file size. |
| clef.Q3_K_L.gguf | Q3_K_L | 14.4 GB | [Link](https://huggingface.co/prithivMLmods/clef-GGUF/blob/main/clef.Q3_K_L.gguf) | Lower quality but usable, good for low RAM availability. |
| clef.Q4_K_M.gguf | Q4_K_M | 16.6 GB | [Link](https://huggingface.co/prithivMLmods/clef-GGUF/blob/main/clef.Q4_K_M.gguf) | Good quality, default size for most use cases, *recommended*. |
| clef.Q5_K_M.gguf | Q5_K_M | 19.3 GB | [Link](https://huggingface.co/prithivMLmods/clef-GGUF/blob/main/clef.Q5_K_M.gguf) | High quality, *recommended*. |
| clef.Q6_K.gguf | Q6_K | 22.2 GB | [Link](https://huggingface.co/prithivMLmods/clef-GGUF/blob/main/clef.Q6_K.gguf) | Very high quality, near perfect, *recommended*. |
| clef.mmproj-bf16.gguf | mmproj-bf16 | 931 MB | [Link](https://huggingface.co/prithivMLmods/clef-GGUF/blob/main/clef.mmproj-bf16.gguf) | Multimodal projection file in BF16 format. Used for vision/language models. |

## Run with llama.cpp (SystemOne API)

### 1. Start the Server

Launch `llama-server` with the GGUF model and wait for the health check endpoint to report ready.

```python
import subprocess, time, requests

MODEL_PATH = "/data/llama.cpp/gguf-new/clef.BF16.gguf"
BASE_URL = "http://127.0.0.1:8080"

server = subprocess.Popen(
    [
        "/data/llama.cpp/build/bin/llama-server",
        "-m", MODEL_PATH,
        "--host", "127.0.0.1",
        "--port", "8080",
        "-ngl", "99",
    ],
    stdout=open("/data/llama-server.log", "w"),
    stderr=subprocess.STDOUT,
)

for _ in range(120):
    try:
        if requests.get(f"{BASE_URL}/health", timeout=2).status_code == 200:
            print("server ready")
            break
    except requests.exceptions.RequestException:
        pass
    time.sleep(2)
else:
    print("server not ready, check /data/llama-server.log")
```

### 2. Query the `/v1/systemone` Endpoint

Send a `POST` request with a `state` context and structured `questions` (`choice`, `noul`, or `score`).

```bash
curl -s http://127.0.0.1:8080/v1/systemone \
  -H "Content-Type: application/json" \
  -d '{
    "state": "Customer message: I was charged twice for my order last week and nobody has replied.",
    "questions": {
      "route": {
        "type": "choice",
        "instructions": "Which team should handle this?",
        "criteria": {
          "billing": "payments, charges, refunds, invoices",
          "shipping": "delivery, tracking, lost or late parcels",
          "technical": "bugs, errors, login problems"
        }
      },
      "angry": {
        "type": "noul",
        "instructions": "Is the customer angry?"
      },
      "urgency": {
        "type": "score",
        "instructions": "How urgent is this?",
        "criteria": ["can wait", "this week", "today", "right now"]
      }
    }
  }' | python3 -m json.tool
```

### 3. Example Response

```json
{
    "model": "/data/llama.cpp/gguf-new/clef.BF16.gguf",
    "answers": {
        "route": {
            "type": "choice",
            "choice": "billing",
            "probabilities": {
                "billing": 0.986925514312472,
                "shipping": 0.004216381856971574,
                "technical": 0.008858103830556456
            },
            "confidence": 0.980388271468708
        },
        "angry": {
            "type": "noul",
            "noul": 0.4533679942395585
        },
        "urgency": {
            "type": "score",
            "score": 1.9306460948859892,
            "legend": {
                "0": "can wait",
                "1": "this week",
                "2": "today",
                "3": "right now"
            },
            "probabilities": {
                "0": 0.015693993665993344,
                "1": 0.24625676944977132,
                "2": 0.529758385216488,
                "3": 0.20829085166774733
            },
            "confidence": 0.5140643915504947
        }
    },
    "usage": {
        "input_tokens": 354,
        "output_tokens": 0
    }
}
```

## llama.cpp

LLM inference in C/C++ — https://github.com/ggml-org/llama.cpp

Quantized using llama.cpp by [prithivMLmods](https://huggingface.co/prithivMLmods).