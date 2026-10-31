---
license: other
language:
- en
- fr
- de
- es
- pt
- it
- ja
- ko
- ru
- zh
- ar
- fa
- id
- ms
- ne
- pl
- ro
- sr
- sv
- tr
- uk
- vi
- hi
- bn
- bg
- hr
- cs
- da
- nl
- et
- fi
- el
- hu
- ga
- lv
- lt
- mt
- sk
- sl
tags:
- vLLM
- SGLang
- transformers
- llama.cpp
---

# Mistral Large 4 - Le Chonk

Mistral Large 4 is our largest and most capable model to date: a 1 trillion-parameter natively multimodal Mixture-of-Experts model with 49 billion active parameters per token (52 billion including embeddings and output layers), trained from scratch on 3,800 NVIDIA Grace Blackwell GPUs in Mistral's own datacenters in Europe.

Mistral Large 4 unifies instruction following, reasoning, coding, and agentic workflows in a single set of weights. While a generalist model, it shows especially good performance on workloads such as cybersecurity, finance, and law, and it surpasses frontier closed models on visual grounding. It is natively fluent in 160+ languages, including every official language of the European Union.

Find more information on our [blog](https://mistral.ai/news/mistral-large-4-oss/). The model is also served on the [Mistral API](https://docs.mistral.ai/models/mistral-large-4-0) as `mistral-large-4`.

> [!Note]
> The checkpoint ships with an embedded DSpark speculative decoding draft head — see [Speculative decoding (DSpark)](#speculative-decoding-dspark).

> [!Note]
> A quantized [NVFP4 checkpoint](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B-NVFP4) is also available, with a smaller memory footprint, faster inference and same performance. It targets Blackwell GPUs and supports vLLM and SGLang.

## Key Features

Mistral Large 4 includes the following architectural choices:

- **~1T total / ~52B active parameters**: granular Mixture-of-Experts with 128 routed experts (4 active per token) and 1 shared expert.
- **1M context length**, for long-context workloads.
- **Multimodal input**: accepts text and image input, with text output. Pixtral-style vision encoder trained to handle variable image sizes and aspect ratios.
- **Instruct and Reasoning functionalities** with function calls, reasoning effort configurable per request.

Mistral Large 4 offers the following capabilities:

- **Reasoning Mode**: three reasoning efforts — `low`, `medium`, `high` (default) — so the same model can answer a quick chat reply or work through a complex agentic run.
- **Vision**: analyzes images, charts, technical drawings, and documents, with state-of-the-art visual grounding among open weights.
- **Multilingual**: natively fluent in 160+ languages, including all official languages of the European Union.
- **System Prompt**: strong adherence and support for system prompts.
- **Agentic**: native function calling, JSON output, and strict JSON schema enforcement.
- **Cybersecurity**: state of the art among open-weight models for security work, while refusing malicious requests.
- **Large Context Window**: supports a 1M context window.

We release this model under the [**Mistral Ecosystem Open-Weight License**](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B/blob/main/LICENSE): a modified version of the MIT license, for both commercial and non-commercial use — operating a Model-as-a-Service business requires a separate commercial license with Mistral.

## Recommended Settings

- **Reasoning Effort**:
  - `'low'` / `'medium'` / `'high'` — default is `'high'`.
  - Use `reasoning_effort="high"` for complex prompts and agentic usage, `'low'` for fast chat replies and `'medium'` for day to day usage.
- **Sampling**: for all reasoning efforts, we recommend the following sampling parameters:
  - `temperature=1.0`
  - `top_p=0.95`
- **System Prompt**: define a clear environment and use case, including guidance on how to effectively leverage tools in agentic systems.
- **Tools**: keep the set of tools well-defined and limit their number to the minimum required for the use case.
- **Context**: the checkpoint supports a 1M context window.

## Benchmarks

We compared Mistral Large 4 with recent open-weight models. We report results on agentic coding and global intelligence here; for more benchmarks, especially on cybersecurity, finance and law, see our [blog post](https://mistral.ai/news/mistral-large-4-oss/).

### Agentic Coding

Mistral Large 4 delivers frontier coding performance with significantly fewer tokens, making sophisticated coding agents more economical to run at scale.

On the Artificial Analysis Coding Agent Index, ML4 scores **48%**, effectively tied with the leading open-weight model, GLM-5.3, while using **47%** fewer tokens per task on average.

![Artificial Analysis - Coding Agent Index](images/coding_index.png)

### Global Intelligence

On the Artificial Analysis Intelligence Index v5, Mistral Large 4 scores **26**, the highest among western open-weight models. The leading open-weight models from China score higher on this aggregate index, but Mistral Large 4 is particularly strong on coding and cybersecurity, as shown in our [blog post](https://mistral.ai/news/mistral-large-4-oss/).

![Artificial Analysis - Intelligence Index v5](images/intelligence_index.png)

## Demo Gallery

[Le Chonk Gallery](https://mistralai-ml4-le-chonk-gallery.hf.space/) is a live gallery of demo Spaces built with Mistral Large 4, from us and from the community: coding, vision and grounding, tool calls, JSON schema, multilingual, and more. Any Space tagged `Le_chonk` appears there.

Official demos run on the Mistral API with a small shared free budget per visitor for the first week of the release, so you can try the model without paying. You can also use your own Mistral API key.

To build a demo, we recommend [Mistral Vibe](https://github.com/mistralai/mistral-vibe), our coding agent powered by Mistral Large 4.

## Usage

You can find Mistral Large 4 support on multiple libraries for inference and fine-tuning.

We **thank** all the ecosystem folks who helped us throughout this release to integrate Le Chonk into their frameworks.

The model can be deployed with:

- [`vllm (recommended)`](https://github.com/vllm-project/vllm): See [here](#vllm-recommended) or [vLLM's recipes](https://recipes.vllm.ai/mistralai/Mistral-Large-4-1T-A52B).
- [`SGLang`](https://github.com/sgl-project/sglang): See [here](#sglang) or SGLang’s [cookbook](https://docs.sglang.io/cookbook/autoregressive/Mistral/Mistral-Large-4).
- [`transformers`](https://github.com/huggingface/transformers): See [here](#transformers) or [Hugging Face’s blog post](https://huggingface.co/blog/mistral-large4).
- [`llama.cpp`](https://github.com/ggml-org/llama.cpp): See GGUFs and instructions [here](https://huggingface.co/ggml-org/Mistral-Large-4-1T-A52B-GGUF).

Fine-tune the model via:

- [`Axolotl`](https://github.com/axolotl-ai-cloud/axolotl): See [here](https://docs.axolotl.ai/docs/models/mistral-large-4.html).
- [`Unsloth`](https://unsloth.ai/): See [here](https://unsloth.ai/docs/models/mistral-large-4) for a guide and [here](https://huggingface.co/unsloth/Mistral-Large-4-1T-A52B-GGUF) for their GGUFs.
- [`TRL`](https://github.com/huggingface/trl): See [here](https://huggingface.co/blog/mistral-large4#fine-tuning-with-trl).

> [!Note]
> For optimal performance, we recommend using the Mistral AI API if local serving is subpar.

## vLLM (Recommended)

We recommend using Mistral Large 4 with the [vLLM library](https://github.com/vllm-project/vllm) for production-ready inference.

See also the [vLLM recipe for Mistral Large 4](https://recipes.vllm.ai/mistralai/Mistral-Large-4-1T-A52B) for ready-made serving configurations.

### Installation

Use the official vLLM Docker image, which includes support for Mistral Large 4:

```bash
docker pull vllm/vllm-openai:mistral-large-4
```

### Serve the Model

We recommend a server/client setup:

```bash
docker run --runtime nvidia --gpus all \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -p 8000:8000 \
  --ipc=host \
  vllm/vllm-openai:mistral-large-4 \
  --model mistralai/Mistral-Large-4-1T-A52B \
  --tensor-parallel-size 8 \
  --tool-call-parser mistral \
  --reasoning-parser mistral \
  --enable-auto-tool-choice \
  --gpu-memory-utilization 0.85
```

Key parameter notes:

- `--tool-call-parser mistral` and `--reasoning-parser mistral`: required for tool usage and to separate reasoning from content in responses.
- If you run short of GPU memory, lower `--max-model-len` and/or `--max-num-seqs` (concurrency). See the [vLLM guide on conserving memory](https://docs.vllm.ai/en/latest/configuration/conserving_memory/#context-length-and-batch-size).

### Ping the Server

`max_completion_tokens` includes reasoning tokens as well as visible output tokens.

<details>
<summary>Instruction Following</summary>

```py
from openai import OpenAI

# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

model = client.models.list().data[0].id

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "Write me a sentence where every word starts with the next letter in the alphabet - start with 'a' and end with 'z'.",
        }
    ],
    reasoning_effort="low",  # Increase with 'medium' or 'high'.
    temperature=1.0,
    top_p=0.95,
    max_completion_tokens=4096,
)

print("REASONING")
print("~~~~~~~~~")
print(response.choices[0].message.reasoning)
print("CONTENT")
print("~~~~~~~")
print(response.choices[0].message.content)
```

</details>

<details>
<summary>Strict JSON Schema</summary>

Mistral Large 4 enforces response formats natively, including strict JSON schemas.

```py
from openai import OpenAI

# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

model = client.models.list().data[0].id

response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "user", "content": "What is 1 + 1? Answer as JSON."}
    ],
    reasoning_effort="medium",
    temperature=1.0,
    top_p=0.95,
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "arithmetic_answer",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {"answer": {"type": "string"}},
                "required": ["answer"],
                "additionalProperties": False,
            },
        },
    },
    max_completion_tokens=16384,
)

print(response.choices[0].message.content)
```

</details>

<details>
<summary>Vision and Tool Call</summary>

Let's solve some equations thanks to our simple Python calculator tool.

```py
import json

from openai import OpenAI

# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

model = client.models.list().data[0].id

image_url = "https://math-coaching.com/img/fiche/46/expressions-mathematiques.jpg"

def my_calculator(expression: str) -> str:
    return str(eval(expression))

tools = [
    {
        "type": "function",
        "function": {
            "name": "my_calculator",
            "description": "A calculator that can evaluate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to evaluate.",
                    },
                },
                "required": ["expression"],
            },
        },
    }
]

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Thanks to your calculator, compute the results for the equations that involve numbers displayed in the image.",
            },
            {"type": "image_url", "image_url": {"url": image_url}},
        ],
    }
]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    tools=tools,
    tool_choice="auto",
    reasoning_effort="high",
    temperature=1.0,
    top_p=0.95,
)

tool_calls = response.choices[0].message.tool_calls

results = []
for tool_call in tool_calls:
    function_name = tool_call.function.name
    function_args = tool_call.function.arguments
    if function_name == "my_calculator":
        result = my_calculator(**json.loads(function_args))
        results.append(result)

messages.append({"role": "assistant", "tool_calls": tool_calls})
for tool_call, result in zip(tool_calls, results):
    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_call.function.name,
            "content": result,
        }
    )

response = client.chat.completions.create(
    model=model,
    messages=messages,
    reasoning_effort="high",
    temperature=1.0,
    top_p=0.95,
)

print("REASONING")
print("~~~~~~~~~")
print(response.choices[0].message.reasoning)
print("CONTENT")
print("~~~~~~~")
print(response.choices[0].message.content)
```

</details>

### Speculative decoding (DSpark)

The checkpoint ships a DSpark draft head next to the target weights: 3 dense MLA draft layers in BF16 that propose a block of 3 tokens with a recurrent Markov head.

To enable it, add the following argument to the serving command above:

```bash
--speculative-config '{"method": "dspark", "num_speculative_tokens": 3}'
```

`num_speculative_tokens` is set to 3, the depth of the draft block.

DSpark speeds up decoding without changing the target model's outputs: we measured up to **1.9x** higher throughput than serving the target model alone. Actual gains depend on hardware and workload.

## SGLang

Serve Mistral Large 4 with the [SGLang library](https://github.com/sgl-project/sglang) for production-ready inference. See also SGLang's [cookbook](https://docs.sglang.io/cookbook/autoregressive/Mistral/Mistral-Large-4).

### Installation

Use the official SGLang Docker image, which includes support for Mistral Large 4:

```bash
docker pull lmsysorg/sglang:mistral-large-4
```

### Serve the Model

```bash
sglang serve \
  --model-path mistralai/Mistral-Large-4-1T-A52B \
  --tp-size 8 \
  --mem-fraction-static 0.85 \
  --speculative-algorithm DSPARK \
  --max-running-requests 64 \
  --reasoning-parser auto \
  --tool-call-parser auto \
  --host 0.0.0.0 \
  --port 30000
```

> [!Note]
> Speculative decoding (DSpark) is on and this recipe pins `--max-running-requests` to **64**. Adjust it to match your target concurrency — if you remove the flag, SGLang falls back to **48**.

Key parameter notes:

- `--speculative-algorithm DSPARK`: enables the embedded DSpark draft head, which proposes blocks of 3 tokens. Remove this flag to serve without speculation.
- `--tp-size 8`: example tensor-parallel size for a node of 8 GPUs; adjust to your topology.
- `--reasoning-parser auto` and `--tool-call-parser auto`: let SGLang pick the reasoning and tool-call parsers for this model.

## Transformers

For more details, check [Hugging Face’s blog post](https://huggingface.co/blog/mistral-large4).

Install Transformers from `main`:

```bash
uv pip install git+https://github.com/huggingface/transformers
```

<details>
<summary>Python Inference Snippet</summary>

Save the following as `script.py`:

```py
import os
from transformers import AutoProcessor, AutoModelForMultimodalLM, DistributedConfig

distributed_config = DistributedConfig(
    tp_size=int(os.environ["WORLD_SIZE"]),
    ep_size=int(os.environ["WORLD_SIZE"]),
)

model_id = "mistralai/Mistral-Large-4-1T-A52B"
processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForMultimodalLM.from_pretrained(
    model_id,
    distributed_config=distributed_config,
    dtype="auto",
)

# only text
text_messages = [
    {
        "role": "user",
        "content": "Who are you?"
    }
]

# text + image
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "image": "https://huggingface.co/datasets/huggingface/cats-image/resolve/main/cats_image.jpeg",
            },
            {
                "type": "text",
                "text": "How many cats are in the image?",
            },
        ],
    },
]

inputs = processor.apply_chat_template(
    messages, # text_messages
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
    reasoning_effort="medium", # low, medium, high
).to(model.device).to(model.dtype)
input_len = inputs["input_ids"].shape[-1]

outputs = model.generate(**inputs, max_new_tokens=100)
if int(os.environ["RANK"]) == 0:
    print(processor.decode(outputs[0][input_len:], skip_special_tokens=False))
```

Then run it on 8 GPUs with `torchrun`:

```bash
torchrun --nproc-per-node 8 script.py
```

</details>

## Mistral-Vibe

Use Mistral Large 4 with [Mistral Vibe](https://github.com/mistralai/mistral-vibe), our open-source CLI coding assistant.

### Installation

Install Vibe with the one-line installer (Linux and macOS):

```bash
curl -LsSf https://mistral.ai/vibe/install.sh | bash
```

Or with `uv` or `pip`:

```bash
uv tool install mistral-vibe
# or
pip install mistral-vibe
```

Then run `vibe` in your project. On first launch it asks for your Mistral API key and saves it to `~/.vibe/.env`. To use Mistral Large 4 through the Mistral API, select `mistral-large-4` as the model.

### Local server

To use a local vLLM server instead, add this to `~/.vibe/config.toml`:

```toml
display_name = "Mistral Large 4 (local vLLM)"
description = "Mistral Large 4 mode using local vLLM"
safety = "neutral"

active_model = "mistral-large-4" # Make sure this is the only active_model entry
[[providers]]
name = "vllm"
api_base = "http://<your-host-url>:8000/v1"
api_key_env_var = ""
backend = "generic"
api_style = "reasoning"

[[models]]
name = "mistralai/Mistral-Large-4-1T-A52B"
provider = "vllm"
alias = "mistral-large-4"
thinking = "high"
thinking_levels = ["low", "medium", "high"]
temperature = 1.0
supports_images = true
max_context_length = 1048576
auto_compact_threshold = 800000

[tools.bash]
default_timeout = 1200
```

**Notes**:

- Replace `<your-host-url>` with your server's URL.
- Other inference backends are also supported. Please look at [Mistral Vibe repo](https://github.com/mistralai/mistral-vibe) for more info.

## License

This model is licensed under the [Mistral Ecosystem Open-Weight License](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B/blob/main/LICENSE).

*You must not use this model in a manner that infringes, misappropriates, or otherwise violates any third party’s rights, including intellectual property rights.*
