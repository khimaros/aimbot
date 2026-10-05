---
license: apache-2.0
pipeline_tag: text-classification
tags:
- gguf
- quantized
- decision-model
base_model:
- SupersonicLabs/Julia-1
---

# Julia-1

Run with https://llama.app

```bash
llama serve -hf ggml-org/Julia-1-GGUF
```

This is a decision model, to be used via `/v1/systemone` API. See https://github.com/ggml-org/llama.cpp/pull/29818

### Source models
- https://huggingface.co/SupersonicLabs/Julia-1

> [!IMPORTANT]
> This model is automatically converted using https://github.com/ggml-org/convert
