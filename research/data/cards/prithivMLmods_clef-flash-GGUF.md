---
license: apache-2.0
language:
- en
base_model:
- Cloudflare/clef-flash
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

# **clef-flash-GGUF**

> **Clef-Flash** is Cloudflare's 9B multimodal decision model, post-trained from Qwen3.5-9B, with a smaller sibling Clef (the larger variant) alongside it. It reads a state as text, JSON, images or video, plus a schema of typed questions (`noul`, `choice` or `score`), and returns a probability for every allowed option in a single forward pass. A small joint schema head on the backbone's final hidden states routes evidence to each question and scores all options together. There is no free-form generation and no parsing, and the API is compatible with Jev and SystemOne. It can be served with SGLang through `/v1/systemone`. On the card's run of the Decision Index 0.2.1 suite, it has the best score in its table on many rows. These include BFCL (98.8), API-Bank (93.1), the home appliance simulator (97.7 vs Jev's 52.3), ContractNLI (84.3), MMLU (91.8), WinoGrande (97.5), CLadder (97.7) and ForecastBench (10.6 Brier, lower is better). Its median latency is 38.8 ms against 524.1 ms for Jev. It trails Jev and the larger Clef on knowledge-heavy and retrieval tasks, notably GPQA Diamond (51.0 vs Jev's 78.3), MMLU-Pro (65.3 vs 82.7), BBH (68.9 vs 92.9), HoVer and When2Call. It is also weak on GSM8K (67.3), CLINC150+OOS (66.8), RAGTruth (35.6) and POP909-CL (1.6). On the four Typesafe workflow evals it is mixed against Jev. For example, it is ahead on customer-service exact actions (77.0 vs 76.0) but behind on invoice processing primary action (73.3 vs 83.1). These are Cloudflare's own internal runs. The weights are Apache 2.0.

> [!NOTE]
> This is a Decision Model GGUF that supports the llama.cpp `v1/systemone` API endpoint.

## Model Files

| File Name | Quant Type | File Size | File Link | Description |
|-----------|------------|-----------|-----------|-------------|
| clef-flash.BF16.gguf | BF16 | 18.2 GB | [Link](https://huggingface.co/prithivMLmods/clef-flash-GGUF/blob/main/clef-flash.BF16.gguf) | Full BF16 weights. Highest quality, largest file size. |
| clef-flash.Q3_K_L.gguf | Q3_K_L | 4.99 GB | [Link](https://huggingface.co/prithivMLmods/clef-flash-GGUF/blob/main/clef-flash.Q3_K_L.gguf) | Lower quality but usable, good for low RAM availability. |
| clef-flash.Q3_K_M.gguf | Q3_K_M | 4.66 GB | [Link](https://huggingface.co/prithivMLmods/clef-flash-GGUF/blob/main/clef-flash.Q3_K_M.gguf) | Low quality. |
| clef-flash.Q4_K_M.gguf | Q4_K_M | 5.72 GB | [Link](https://huggingface.co/prithivMLmods/clef-flash-GGUF/blob/main/clef-flash.Q4_K_M.gguf) | Good quality, default size for most use cases, *recommended*. |
| clef-flash.Q4_K_S.gguf | Q4_K_S | 5.38 GB | [Link](https://huggingface.co/prithivMLmods/clef-flash-GGUF/blob/main/clef-flash.Q4_K_S.gguf) | Slightly lower quality with more space savings, *recommended*. |
| clef-flash.Q5_K_M.gguf | Q5_K_M | 6.56 GB | [Link](https://huggingface.co/prithivMLmods/clef-flash-GGUF/blob/main/clef-flash.Q5_K_M.gguf) | High quality, *recommended*. |
| clef-flash.Q5_K_S.gguf | Q5_K_S | 6.39 GB | [Link](https://huggingface.co/prithivMLmods/clef-flash-GGUF/blob/main/clef-flash.Q5_K_S.gguf) | High quality, *recommended*. |
| clef-flash.Q6_K.gguf | Q6_K | 7.46 GB | [Link](https://huggingface.co/prithivMLmods/clef-flash-GGUF/blob/main/clef-flash.Q6_K.gguf) | Very high quality, near perfect, *recommended*. |
| clef-flash.mmproj-bf16.gguf | mmproj-bf16 | 922 MB | [Link](https://huggingface.co/prithivMLmods/clef-flash-GGUF/blob/main/clef-flash.mmproj-bf16.gguf) | Multimodal projection file in BF16 format. Used for vision/language models. |

## Run with llama.cpp (SystemOne API)

### 1. Start the Server

Launch `llama-server` with the GGUF model and wait for the health check endpoint to report ready.

```python
import subprocess, time, requests

MODEL_PATH = "/data/llama.cpp/gguf-new/clef-flash.Q5_K_M.gguf"
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
    "model": "/data/llama.cpp/gguf-new/clef-flash.Q5_K_M.gguf",
    "answers": {
        "route": {
            "type": "choice",
            "choice": "billing",
            "probabilities": {
                "billing": 0.9623896424268241,
                "shipping": 0.016386611483623886,
                "technical": 0.02122374608955196
            },
            "confidence": 0.9435844636402362
        },
        "angry": {
            "type": "noul",
            "noul": 0.3006857290560717
        },
        "urgency": {
            "type": "score",
            "score": 2.07962027224278,
            "legend": {
                "0": "can wait",
                "1": "this week",
                "2": "today",
                "3": "right now"
            },
            "probabilities": {
                "0": 0.037682813278991895,
                "1": 0.20006727342403852,
                "2": 0.407196741072167,
                "3": 0.3550531722248026
            },
            "confidence": 0.36951392779317516
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