---
library_name: transformers
inference: false
extra_gated_description: >-
  To learn more about how we process your personal data, please read our <a
  href="https://poolside.ai/legal/privacy">Privacy Policy</a>.
tags:
- laguna-xs-2.1
- vllm
license: openmdw-1.1
pipeline_tag: text-generation
---

<p align="center">
  <img alt="poolside-banner" src="https://poolside.ai/assets/laguna/laguna-xs2-1-banner.svg" width="800px">
</p>

<p align="center">
  <a href="https://openrouter.ai/poolside/laguna-xs-2.1"><strong>Use on OpenRouter</strong></a> ·
  <a href="https://poolside.ai/blog/introducing-laguna-xs-2-1"><strong>Release blog post</strong></a>
</p>

<br>

# Laguna XS 2.1
Laguna XS 2.1 is a 33B total parameter Mixture-of-Experts model with 3B activated parameters per token designed for agentic coding and long-horizon work on a local machine. This model is an upgraded version of our [Laguna XS.2](https://huggingface.co/poolside/Laguna-XS.2) model with a +5.4% jump on SWE-bench Multilingual as well as stronger performance on terminal-style tasks.

> [!NOTE]
> For more details on how we train, including on data automixing and async off-policy agent RL, check out our recent [technical report](https://poolside.ai/assets/laguna/laguna-m1-xs2-technical-report.pdf).

>[!NOTE]
>Laguna XS 2.1 is released under OpenMDW-1.1, a fully permissive license. Use it, modify it, and build commercial products on it. No permission required.
If you want more than the weights: production support, latency and cost optimization, or output indemnification, [talk to us](https://poolside.ai/contact?utm_source=hf&utm_medium=modelcard_cta). 


## Highlights
- **Mixed SWA and global attention layout**: Laguna XS 2.1 uses sigmoid gating with per-layer rotary scales, enabling mixed SWA (Sliding Window Attention) and global attention layers in a 3:1 ratio (across 40 total layers)
- **KV cache in FP8**: KV cache quantized to FP8, reducing memory per token
- **Native reasoning support**: Interleaved thinking between tool calls with support for enabling and disabling thinking per-request
- **Local-ready**: At 33B total parameters and 3B activated, Laguna XS 2.1 is compact enough to run on a Mac with 36 GB of RAM. Available on [Ollama](https://ollama.com/library/laguna-xs-2.1) and [llama.cpp](https://github.com/ggml-org/llama.cpp/pull/25165). High-quality FP8, NVFP4 and INT4 quantized variants available ([see the collection](https://huggingface.co/collections/poolside/laguna-xs-21))
- **OpenMDW-1.1 license**: Use and modify the model and associated materials freely for commercial and non-commercial purposes ([learn more about OpenMDW](https://openmdw.ai/))

---

## Model overview

- Training: pre-training, post-training and reinforcement learning stages
- Number of parameters: 33B total with 3B activated per token
- Optimizer: Muon
- Layers: 40 layers (10 layers with global attention, 30 layers with sliding window attention)
- Experts: 256 experts with 1 shared expert
- Sliding Window: 512 tokens
- Modality: text-to-text
- Context window: 262,144 tokens
- Reasoning support: interleaved thinking with preserved thinking

## Benchmark results

<p align="center">
  <img alt="benchmarks" src="https://poolside.ai/assets/laguna/laguna-xs2-1-chart.svg" width="800px">
</p>

| Model                     | Size (total params.) | SWE-bench Verified | SWE-bench Multilingual | SWE-Bench Pro (Public Dataset) | Terminal-Bench 2.0 |
|---------------------------|----------------------|--------------------|------------------------|--------------------------------|--------------------|
| **Laguna XS 2.1**         | 33B                  | 70.9%              | 63.1%                  | 47.6%                          | 37.5%              |
| **Laguna XS.2**           | 33B                  | 69.9%              | 57.7%                  | 46.3%                          | 35.7%              |
| Qwen3.6-35B-A3B           | 35B                  | 73.4%              | 67.2%                  | 49.5%                          | 51.5%              |
| North Mini Code           | 30B                  | 67.6%              | -                      | 40.2%                          | 36.0%              |
| MAI-Code-1-Flash          | 137B                 | 71.6%              | 65.5%                  | 51.2%                          | 54.8%              |
| gpt-oss-120B              | 120B                 | -                  | -                      | 16.2%                          | 18.7%              |
| Claude Haiku 4.5          | -                    | 73.3%              | -                      | 39.5%                          | 29.8%              |
| GPT-5.4 Nano              | -                    | -                  | -                      | 52.4%                          | 46.3%              |

*We used the highest publicly-referenced scores for all comparison models across each benchmark. In all cases these were official scores published in release blog posts or equivalent, with the exception of gpt-oss-120b and Claude Haiku 4.5 where the highest published (verified) scores for SWE-Bench Pro and Terminal-Bench 2.0 are from their respective official leaderboards.*

<details>
<summary>Expand for benchmarking methodology</summary>

All benchmarking for Laguna XS 2.1 was completed using Laude Institute’s Harbor Framework with our [agent harness](https://github.com/poolsideai/pool), with a maximum of 500 steps and sandboxed execution. The same sampling parameters were used for all Laguna XS 2.1 benchmarking: temperature=1.0, top_k=20 and top_p=1, with thinking mode enabled and a context length of 256K tokens. All tasks were run in their own sandbox using 8 GB RAM/2 CPUs, with the exception of Terminal-Bench 2.0, which used 48 GB RAM/32 CPUs.

Some base task images and verifiers were patched to fix infrastructure reliability issues inherent in task setup, such as rate limits on third-party dependencies in external registries used by the verifier. All four agentic benchmarks were run with patched images. We also ran a reward-hack judge post-hoc on Laguna XS 2.1 evaluation runs and did not find significant reward hacking after joint judge review and manual review.

- SWE-bench Verified: mean pass@1 averaged over 4 attempts per task
- SWE-bench Multilingual: mean pass@1 averaged over 4 attempts per task
- SWE-Bench Pro: mean pass@1 averaged over 2 attempts per task
- Terminal-Bench 2.0: mean pass@1 averaged over 5 attempts per task; 48 GB RAM/32 CPUs

</details>

## Usage

Laguna XS 2.1 has launch-day support in vLLM, SGLang, Transformers and Llama.cpp, and TRT-LLM thanks to the support of the team at NVIDIA.

The fastest way to get started is using OpenRouter.

> [!NOTE]
> We are providing free inference for a limited time for Laguna XS 2.1, as well as our larger 225B model, Laguna M.1. Visit our [provider page on OpenRouter](https://openrouter.ai/poolside/) to get started.

### pool

**pool** is a lightweight terminal-based coding agent and a dual [Agent Client Protocol](https://agentclientprotocol.com/get-started) client-server.

Download and install for macOS and Linux:

```shell
curl -fsSL https://downloads.poolside.ai/pool/install.sh | bash
```

Launch and `> Log in with Poolside` to get a free, limited-use API key.

Alternatively, use Poolside models alongside the wide catalog of models available on OpenRouter by selecting `> Log in with OpenRouter`.

```shell
pool login
```

Use in any [ACP client](https://agentclientprotocol.com/get-started/clients). Configure Zed and JetBrains automatically:

```shell
pool acp setup --editor zed|jetbrains
```

Use pool with Ollama with one-command setup:

```shell
ollama pull laguna-xs-2.1
ollama launch pool --model laguna-xs-2.1
```

#### Feedback and issues

Submit feedback with `/feedback` and read the [full documentation on GitHub](https://github.com/poolsideai/pool).

### Local deployment

Laguna XS 2.1 is supported in vLLM, SGLang, Transformers and Llama.cpp, and TRT-LLM thanks to the support of the team at NVIDIA. Use Laguna-XS 2.1 with Ollama (with MLX support) and the mlx-lm framework for the best experience on your local machine.

#### vLLM

Serve Laguna XS 2.1 locally with vLLM and query it from any OpenAI-compatible client (see [Controlling reasoning](#controlling-reasoning) for tool calls, streaming, and reasoning extraction):

> [!NOTE]
> Laguna XS 2.1 support is available in vLLM 0.21.0 and later ([vllm-project/vllm#41129](https://github.com/vllm-project/vllm/pull/41129)).

> [!IMPORTANT]
> Use a vLLM build that includes [vllm-project/vllm#47311](https://github.com/vllm-project/vllm/pull/47311). Without that fix, the `poolside_v1` tool parser silently drops Laguna XS 2.1 tool calls that have no newline after the function name, and the raw tool-call markup leaks into the response. On an older build, pass `--tool-call-parser glm47` (the GLM 4.7 parser) instead.

```shell
pip install 'vllm>=0.21.0'

vllm serve \
    --model poolside/Laguna-XS-2.1 \
    --tool-call-parser poolside_v1 \
    --reasoning-parser poolside_v1 \
    --enable-auto-tool-choice \
    --served-model-name laguna \
    --default-chat-template-kwargs '{"enable_thinking": true}'
```

See the [vLLM recipes page](https://recipes.vllm.ai/poolside/Laguna-XS-2.1) for additional deployment guidance.

> [!NOTE]
> **Optional: speculative decoding with DFlash.** For lower latency, pair Laguna XS 2.1 with the [DFlash speculator](https://huggingface.co/poolside/Laguna-XS-2.1-DFlash), a 5-layer Llama-style draft model that proposes up to 7 tokens per step at ~70% per-position acceptance on coding tasks. vLLM support is in progress in [vllm-project/vllm#46853](https://github.com/vllm-project/vllm/pull/46853); once it lands, add `--speculative-config '{"model":"poolside/Laguna-XS-2.1-DFlash","num_speculative_tokens":7,"method":"dflash"}'` to the serve command above.

#### SGLang

Laguna XS 2.1 is supported in SGLang via [sgl-project/sglang#24204](https://github.com/sgl-project/sglang/pull/24204). See the [SGLang cookbook entry](https://docs.sglang.io/cookbook/autoregressive/Poolside/Laguna-XS-2.1) for a serving recipe.

```shell
git clone https://github.com/sgl-project/sglang.git
cd sglang
pip install -e "python[all]"

python -m sglang.launch_server \
  --model-path poolside/Laguna-XS-2.1 \
  --tp-size 8 \
  --mem-fraction-static 0.7 \
  --reasoning-parser poolside_v1 \
  --trust-remote-code
```

> [!NOTE]
> **Optional: speculative decoding with DFlash.** The [DFlash speculator](https://huggingface.co/poolside/Laguna-XS-2.1-DFlash) can be paired with Laguna XS 2.1 for lower latency. SGLang support was added in [sgl-project/sglang#29446](https://github.com/sgl-project/sglang/pull/29446). Add `--speculative-algorithm DFLASH \ --speculative-draft-model-path poolside/Laguna-XS-2.1-DFlash-FP8` to the serve command above.

#### Transformers

Laguna XS 2.1 is supported in Transformers `v5.7.0` and later ([huggingface/transformers#45673](https://github.com/huggingface/transformers/pull/45673)).

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "poolside/Laguna-XS-2.1"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    dtype=torch.bfloat16,
    device_map="auto",
)

messages = [
    {"role": "user", "content": "Write a Python retry wrapper with exponential backoff."},
]

# Reasoning is on by default; pass enable_thinking=False to skip the <think> block.
inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt",
    enable_thinking=True,
).to(model.device)

outputs = model.generate(
    inputs,
    max_new_tokens=1024,
    do_sample=True,
    temperature=1.0,
    top_k=20,
)

response = tokenizer.decode(outputs[0][inputs.shape[-1]:], skip_special_tokens=True)
print(response)
```

#### TRT-LLM

Laguna XS 2.1 support is merged into TensorRT-LLM ([NVIDIA/TensorRT-LLM#13559](https://github.com/NVIDIA/TensorRT-LLM/pull/13559)) and ships in the `v1.3.0rc16` pre-release wheels and later.

> [!NOTE]
> A stable `v1.3.0` has not been released yet, so install a pre-release wheel from NVIDIA's package index (the latest stable, `v1.2.x`, does not include Laguna XS 2.1 support). To build from source instead, see the TensorRT-LLM build documentation. Laguna XS 2.1 support is on `main`.

Install the **CUDA-13 `torch` build first**, then TensorRT-LLM. The default PyPI `torch` is a CUDA-12 build whose `cuda-bindings` pin conflicts with TRT-LLM's `cuda-python 13.x`, so a bare `pip install tensorrt-llm` fails to resolve; installing the cu130 `torch` up front avoids it.

```shell
# 1. CUDA-13 torch build (pins cuda-bindings 13.x, matching TRT-LLM's cuda-python)
pip install 'torch==2.10.0' torchvision --index-url https://download.pytorch.org/whl/cu130

# 2. TRT-LLM from NVIDIA's index (torch already satisfied, so it is not replaced)
pip install --pre 'tensorrt-llm>=1.3.0rc16' \
    --extra-index-url https://pypi.nvidia.com \
    --extra-index-url https://download.pytorch.org/whl/cu130
```

This resolves to `tensorrt-llm 1.3.0rc20` with `torch 2.10.0+cu130`, `cuda-python 13.0.3`, and `transformers 5.5.4`.

Load the checkpoint directly with `trust_remote_code=True`. No `transformers` compatibility overlay is required: `v1.3.0rc16+` pins `transformers 5.5.4`, which provides the symbols Laguna XS 2.1's config needs (earlier TRT-LLM releases pinned `transformers 4.57`, which did not).

```python
from tensorrt_llm import LLM, SamplingParams

llm = LLM(
    model="poolside/Laguna-XS-2.1",
    trust_remote_code=True,
    tensor_parallel_size=1,
)

sampling = SamplingParams(max_tokens=1024, temperature=1.0, top_k=20)
out = llm.generate(["Write a Python retry wrapper with exponential backoff."], sampling)
print(out[0].outputs[0].text)
```

Or serve with an OpenAI-compatible endpoint:

```shell
trtllm-serve poolside/Laguna-XS-2.1 --port 8000 --trust-remote-code --tool_parser poolside_v1 --reasoning_parser laguna
```

The Laguna XS 2.1 tool-call and reasoning parsers are built into TRT-LLM `>=1.3.0rc16` (shipped with [#13559](https://github.com/NVIDIA/TensorRT-LLM/pull/13559)), so no extra install is needed. Note that the flag names differ from vLLM's (`--tool_parser`, and the reasoning parser is `laguna`, not `poolside_v1`).

The same recipe works for the [FP8](https://huggingface.co/poolside/Laguna-XS-2.1-FP8) and [NVFP4](https://huggingface.co/poolside/Laguna-XS-2.1-NVFP4) variants: quantization is detected automatically from `quantization_config`, no extra flags required.

> [!NOTE]
> **Optional: speculative decoding with DFlash.** The [DFlash speculator](https://huggingface.co/poolside/Laguna-XS-2.1-DFlash) can be paired with Laguna XS 2.1 for lower latency. TRT-LLM support is in progress in [NVIDIA/TensorRT-LLM#15666](https://github.com/NVIDIA/TensorRT-LLM/pull/15666).

#### llama.cpp

> [!NOTE]
> Requires building llama.cpp from the upstream PR that adds Laguna XS 2.1 support until it lands ([ggml-org/llama.cpp#25165](https://github.com/ggml-org/llama.cpp/pull/25165)).

Official GGUF conversions (BF16 and Q4\_K\_M) are available at [poolside/Laguna-XS-2.1-GGUF](https://huggingface.co/poolside/Laguna-XS-2.1-GGUF).

```shell
# Build llama.cpp from the PR branch
git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
git fetch origin pull/25165/head:laguna && git checkout laguna
cmake -B build && cmake --build build -j

# Download a GGUF and serve an OpenAI-compatible endpoint
huggingface-cli download poolside/Laguna-XS-2.1-GGUF Laguna-XS-2.1-Q4_K_M.gguf --local-dir ~/models/Laguna-XS-2.1-GGUF
./build/bin/llama-server -m ~/models/Laguna-XS-2.1-GGUF/Laguna-XS-2.1-Q4_K_M.gguf --jinja --port 8000
```

#### Ollama

Available on the [Ollama library](https://ollama.com/library/laguna-xs-2.1).

    ollama run laguna-xs-2.1          # default — Q4_K_M (imatrix)
    ollama run laguna-xs-2.1:q8_0     # higher precision
    ollama run laguna-xs-2.1:bf16     # full precision

Reasoning and tool-calling work out of the box via the built-in `laguna` template.

> [!NOTE]
> **macOS (Metal) users:** `ollama run` may currently return empty output on Apple Silicon (a Metal f16 overflow in the MoE down-projection; fix pending in [ggml-org/llama.cpp#25389](https://github.com/ggml-org/llama.cpp/pull/25389)). Until it ships, use a Linux/CUDA host or the `/api/generate` endpoint with `"raw": true`.

#### Atomic Chat

Laguna XS 2.1 is also available in [Atomic Chat](https://atomic.chat/), a desktop app for running local models with a simple chat UI. To try it, download Atomic Chat, open the app, and choose Laguna XS 2.1 from the recommended models.

## Controlling reasoning

Laguna XS 2.1 has native reasoning support and is designed to work best with *preserved thinking*, where `reasoning` content from prior assistant messages is preserved in the message history. This model will generally reason before calling tools and between tool calls.

Reasoning may not be generated in follow-up steps if prior thinking blocks are dropped (i.e., thinking is not preserved) when messages are reconstructed over multiple steps.

<details>
<summary>Expand for example</summary>

```python
import json
from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="...",
)

model = "poolside/laguna-xs-2.1"

tools = [{"type": "function", "function": {
  "name": "shell",
  "description": "Execute a bash command and return the output.",
  "parameters": {"type": "object", "properties": {"cmd": {"type": "string"}}, "required": ["cmd"]},
}}]

messages = [
  {"role": "system", "content": "You are a coding agent with access to a shell tool."},
  {"role": "user", "content": "Run uname -a"},
]

# Thinking is enabled by default when the server sets --default-chat-template-kwargs {"enable_thinking": True}
# When using OpenRouter's Chat API (https://openrouter.ai/api/v1), this flag is set by default
response = client.chat.completions.create(
  model=model,
  messages=messages,
  tools=tools,
  stream=True,
)

reasoning, content, tool_calls = "", "", []
for chunk in response:
  delta = chunk.choices[0].delta
  if hasattr(delta, "reasoning_content") and delta.reasoning_content:
    reasoning += delta.reasoning_content
  if hasattr(delta, "content") and delta.content:
    content += delta.content
  if hasattr(delta, "tool_calls") and delta.tool_calls:
    for tc in delta.tool_calls:
      if tc.index >= len(tool_calls):
        tool_calls.append({"id": tc.id, "function": {"name": "", "arguments": ""}})
      if tc.function.name:
        tool_calls[tc.index]["function"]["name"] = tc.function.name
      if tc.function.arguments:
        tool_calls[tc.index]["function"]["arguments"] += tc.function.arguments

print(f"Reasoning: {reasoning}\nContent: {content}\nTool calls: {tool_calls}\n")

# Return reasoning in the next request for best performance
messages.append({
  "role": "assistant",
  "content": content,
  "reasoning_content": reasoning,
  "tool_calls": [{"id": tc["id"], "type": "function", "function": tc["function"]} for tc in tool_calls]
})

messages.append({
  "role": "tool",
  "tool_call_id": tool_calls[0]["id"],
  "content": json.dumps({"stdout": "Darwin arm64", "exit_code": "0"})
})

response = client.chat.completions.create(
  model=model,
  messages=messages,
  tools=tools,
  stream=True,
)

reasoning, content = "", ""
for chunk in response:
  delta = chunk.choices[0].delta
  if hasattr(delta, "reasoning_content") and delta.reasoning_content:
    reasoning += delta.reasoning_content
  if hasattr(delta, "content") and delta.content:
    content += delta.content

print(f"Reasoning: {reasoning}\nContent: {content}")
```

</details>

### Disabling reasoning

You can disable thinking by setting `enable_thinking` to `False` in a request or by not providing `--default-chat-template-kwargs {"enable_thinking": True}` or equivalent when starting the server.

<details>
<summary>Expand for example</summary>

```python
from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="poolside/laguna-xs-2.1",
  messages=[
    {"role": "user", "content": "Write a retry wrapper with exponential backoff."}
  ],
  extra_body={
    "chat_template_kwargs": { "enable_thinking": False },
  },
  stream=True
)

for chunk in completion:
    print(chunk.choices[0].delta)
```

</details>

For agentic coding use cases, we recommend enabling thinking and preserving reasoning in message history as outlined in the [Controlling reasoning](#controlling-reasoning) section.

## License

This model is licensed under the [OpenMDW-1.1 License](https://huggingface.co/poolside/Laguna-XS-2.1/blob/main/LICENSE.md).

## Intended and Responsible Use 

Laguna XS 2.1 is designed for software engineering and agentic coding use cases, and you are responsible for confirming that it is appropriate for your intended application. Laguna XS 2.1 is subject to the [OpenMDW-1.1 License](https://huggingface.co/poolside/Laguna-XS-2.1/blob/main/LICENSE.md), and should be used consistently with Poolside's [Acceptable Use Policy](https://poolside.ai/legal/acceptable-use-policy). We advise against circumventing Laguna XS 2.1 safety guardrails without implementing substantially equivalent mitigations appropriate for your use case.

Please report security vulnerabilities or safety concerns to [security@poolside.ai](mailto:security@poolside.ai).