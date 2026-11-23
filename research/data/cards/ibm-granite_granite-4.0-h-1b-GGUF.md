---
license: apache-2.0
library_name: llama.cpp
tags:
- language
- granite-4.0
- gguf
base_model:
- ibm-granite/granite-4.0-h-1b
---

### granite-4.0-h-1b (GGUF)

> [!NOTE]
> This repository contains models that have been converted to the GGUF format with various quantizations from an IBM Granite base model.
>
> Please reference the base model's full model card here:
> https://huggingface.co/ibm-granite/granite-4.0-h-1b

### Running with llama.cpp

The examples below use the `Q8_0` quantization (`granite-4.0-h-1b-Q8_0.gguf`). Other quantizations in this repository work the same way; only the file name changes. See the [llama.cpp documentation](https://github.com/ggml-org/llama.cpp) for complete usage and options, including the [`llama cli`](https://github.com/ggml-org/llama.cpp/blob/master/tools/cli/README.md) and [`llama serve`](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md) flag references.

**example: llama cli**

Start an interactive chat:

```bash
llama cli -m granite-4.0-h-1b-Q8_0.gguf
```

Or run a single prompt and exit:

```bash
llama cli -m granite-4.0-h-1b-Q8_0.gguf -p "Explain what a GGUF file is in two sentences." --single-turn
```

---

**example: llama serve using OpenAI API**

1. Start llama serve with the model

```bash
llama serve -m granite-4.0-h-1b-Q8_0.gguf \
  --port 8080
```

2. Send a chat request to the llama serve /v1/chat/completions endpoint

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      { "role": "user", "content": "Explain what a GGUF file is in two sentences." }
    ]
  }'
```

The response is a JSON message with the generated text in the `choices[0].message.content` field.

---

### llama.cpp recommended parameters for granite-4.0-h-1b

**Set the context length explicitly with `-c` / `--ctx-size`.** While this model can support arbitrarily long context since it does not use positional embeddings, it was trained on text up to 128k, so we recommend limiting context to 131072 at runtime.

```bash
llama cli -m granite-4.0-h-1b-Q8_0.gguf -c 131072
```

```bash
llama serve -m granite-4.0-h-1b-Q8_0.gguf -c 131072 --port 8080
```

#### Build Information

- **llama.cpp build tag:** `b11798`
- **Transformers version:** `5.20.2`