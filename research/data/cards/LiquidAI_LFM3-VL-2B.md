---
library_name: transformers
license: other
license_name: lfm1.0
license_link: LICENSE
pipeline_tag: image-text-to-text
tags:
- liquid
- lfm3
- edge
- conversational
- custom_code
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
base_model: LiquidAI/LFM3-1.7B-Base
---

<div align="center">
  <img
    src="https://huggingface.co/LiquidAI/LFM3-1.7B/resolve/main/assets/liquid-ai-banner.webp"
    alt="Liquid AI"
    style="width: 100%; max-width: 100%; height: auto; display: block; margin: 0;"
  />
  <div align="center" style="display: flex; justify-content: center; align-items: center; gap: 1.25em; margin: 8px 0 1.7rem; padding: 0; line-height: 1.3;">
    <a href="https://console.liquid.ai/dashboard" style="display: inline-flex; align-items: center; gap: 6px;"><img src="https://huggingface.co/LiquidAI/LFM3-1.7B/resolve/main/assets/icons/api.svg" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>API</strong></a>
    <a href="https://playground.liquid.ai/" style="display: inline-flex; align-items: center; gap: 6px;"><img src="https://huggingface.co/LiquidAI/LFM3-1.7B/resolve/main/assets/icons/try.svg" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>Try</strong></a>
    <a href="https://docs.liquid.ai/lfm/getting-started/welcome" style="display: inline-flex; align-items: center; gap: 6px;"><img src="https://huggingface.co/LiquidAI/LFM3-1.7B/resolve/main/assets/icons/docs.svg" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>Docs</strong></a>
    <a href="https://www.liquid.ai/blog/lfm3" style="display: inline-flex; align-items: center; gap: 6px;"><img src="https://huggingface.co/LiquidAI/LFM3-1.7B/resolve/main/assets/icons/blog.svg" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>Blog</strong></a>
  </div>
</div>

# LFM3-VL-2B

LFM3-VL-2B is a **vision-language model for on-device visual understanding**. It takes text, images, and video as input, and combines the [LFM3 language model](https://huggingface.co/LiquidAI/LFM3-1.7B-Base) with a new in-house vision encoder.

New in LFM3-VL-2B:

- **Video understanding:** the first LFM vision model that takes video as input. Ask questions about a recorded lecture, a walkthrough filmed on your phone, or a clip from a camera feed.
- **Thinking:** the model reasons step by step before it answers. This helps most with harder visual questions, such as math, charts, and multi-step problems.
- **Spatial and embodied reasoning:** the model finds objects and reasons about how they are placed relative to each other, a strong foundation for robotics applications.

Find more information about the LFM3 family in [our release blog post](https://www.liquid.ai/blog/lfm3).

## Model details
<hr style="margin: -0.7em 0 1.2em 0; border: 0; border-top: 1px solid rgba(127, 127, 127, 0.3);" />

The [LFM3 family](https://huggingface.co/collections/LiquidAI/lfm3) includes base, text, vision, audio, omni, and decision models.

<table style="width: 100%; display: table; border: 0; border-radius: 0; border-collapse: collapse;">
<thead style="border: 0;">
<tr style="border: 0;">
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Property</th>
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Specification</th>
</tr>
</thead>
<tbody style="border: 0;">
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><strong>Checkpoint</strong></td>
<td style="border: 0; padding: 0.55em 0.75em;">Post-trained vision-language model</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><strong>Parameters</strong></td>
<td style="border: 0; padding: 0.55em 0.75em;">1.92B: 1.73B language model, 164M vision encoder, 25M projector</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><strong>Language model</strong></td>
<td style="border: 0; padding: 0.55em 0.75em;">LFM3, 24 layers: 13 gated short convolutions, 5 sliding-window attention, 6 global attention</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><strong>Vision encoder</strong></td>
<td style="border: 0; padding: 0.55em 0.75em;">14 layers: 8 gated depthwise 2D convolutions, 6 bidirectional attention, 16×16 patches with 2D rotary embeddings</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><strong>Inputs</strong></td>
<td style="border: 0; padding: 0.55em 0.75em;">Text, images, and video at native resolution. Each 2×2 block of patches becomes one language token. Video is sampled at 2 fps, with 4 to 768 frames by default.</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><strong>Context length</strong></td>
<td style="border: 0; padding: 0.55em 0.75em;">128K tokens (input + output)</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><strong>Vocabulary</strong></td>
<td style="border: 0; padding: 0.55em 0.75em;">128,000 tokens</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><strong>Languages</strong></td>
<td style="border: 0; padding: 0.55em 0.75em;">English, Arabic, Chinese, French, German, Italian, Japanese, Korean, Portuguese, Spanish, Vietnamese, Thai, Indonesian, Hindi, Russian, Polish</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><strong>License</strong></td>
<td style="border: 0; padding: 0.55em 0.75em;"><a href="LICENSE">LFM Open License v1.0</a></td>
</tr>
</tbody>
</table>

LFM3-VL-2B is designed for on-device visual tasks: questions about video, reading documents, charts, and app screens, finding objects in an image, and spatial reasoning for robots. It is not recommended for coding, multi-turn conversations, or complex reasoning.

## Inference
<hr style="margin: -0.7em 0 1.2em 0; border: 0; border-top: 1px solid rgba(127, 127, 127, 0.3);" />

Choose a checkpoint variant for your inference framework and hardware.

<table style="width: 100%; display: table; border: 0; border-radius: 0; border-collapse: collapse;">
<thead style="border: 0;">
<tr style="border: 0;">
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Checkpoint</th>
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Framework</th>
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Description</th>
</tr>
</thead>
<tbody style="border: 0;">
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://huggingface.co/LiquidAI/LFM3-VL-2B">BF16</a></td>
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://docs.liquid.ai/deployment/gpu-inference/vllm">vLLM</a>, <a href="https://docs.liquid.ai/deployment/gpu-inference/sglang">SGLang</a>, <a href="https://docs.liquid.ai/deployment/gpu-inference/transformers">Transformers</a></td>
<td style="border: 0; padding: 0.55em 0.75em;">BF16 weights for GPU inference.</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://huggingface.co/LiquidAI/LFM3-VL-2B-GGUF">GGUF</a></td>
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://docs.liquid.ai/deployment/on-device/llama-cpp">llama.cpp</a>, <a href="https://docs.liquid.ai/deployment/on-device/lm-studio">LM Studio</a></td>
<td style="border: 0; padding: 0.55em 0.75em;">Local inference on CPUs and GPUs.</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://huggingface.co/LiquidAI/LFM3-VL-2B-MLX-4bit">MLX</a></td>
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://docs.liquid.ai/deployment/on-device/mlx">MLX-VLM</a></td>
<td style="border: 0; padding: 0.55em 0.75em;">4-bit quantization for Apple Silicon.</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://huggingface.co/LiquidAI/LFM3-VL-2B-ONNX">ONNX</a></td>
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://docs.liquid.ai/deployment/on-device/onnx">ONNX Runtime</a></td>
<td style="border: 0; padding: 0.55em 0.75em;">Cross-platform inference with ONNX Runtime.</td>
</tr>
</tbody>
</table>

**Sampling parameters:** `temperature=0.1, top_p=1.0, top_k=50, min_p=0.0, repetition_penalty=1.1`. For image and video preprocessing, use the values in `processor_config.json`.

**Transformers quick start** (`transformers>=5.21.0`):

```bash
pip install "transformers>=5.21.0" torch torchvision pillow
```

```python
import torch
from transformers import AutoModelForImageTextToText, AutoProcessor

model_id = "LiquidAI/LFM3-VL-2B"

model = AutoModelForImageTextToText.from_pretrained(
    model_id, dtype=torch.bfloat16, device_map="auto", trust_remote_code=True
)
processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "url": "https://placecats.com/300/200"},
            {"type": "text", "text": "Describe this image."},
        ],
    }
]

inputs = processor.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
).to(model.device)

with torch.inference_mode():
    output_ids = model.generate(
        **inputs,
        do_sample=True,
        temperature=0.1,
        top_k=50,
        repetition_penalty=1.1,
        max_new_tokens=16384,  # generate() needs an explicit limit; reasoning can be long
    )

generated_ids = output_ids[:, inputs["input_ids"].shape[1] :]
print(processor.batch_decode(generated_ids, skip_special_tokens=True)[0])
```

<details>
<summary><strong>On-device inference with llama.cpp</strong></summary>

For most on-device use cases, we recommend [llama.cpp](https://github.com/ggml-org/llama.cpp) b11960 or newer with the [GGUF checkpoints](https://huggingface.co/LiquidAI/LFM3-VL-2B-GGUF). To run it in a desktop app such as [Llama.app](https://llama.app) or [LM Studio](https://lmstudio.ai), click **Use this model** on the [GGUF page](https://huggingface.co/LiquidAI/LFM3-VL-2B-GGUF) and pick the app.

From a terminal, start a web chat UI and an OpenAI-compatible API at `http://localhost:8080`. With `-hf`, llama.cpp downloads the model and the matching vision projector (mmproj):

```bash
llama serve -hf LiquidAI/LFM3-VL-2B-GGUF:Q4_0 \
  --temp 0.1 --top-p 1.0 --top-k 50 --min-p 0.0 --repeat-penalty 1.1 \
  --no-reasoning-preserve --port 8080
```

To ask one question from the command line, use `llama cli` with the same flags, `--image <IMAGE PATH>` or `--video <VIDEO PATH>`, and `-p "<PROMPT>"`. Video input needs `ffmpeg` in `PATH`.

</details>

<details>
<summary><strong>GPU inference with vLLM and SGLang</strong></summary>

For high-throughput serving on GPU, use [vLLM](https://github.com/vllm-project/vllm) or [SGLang](https://github.com/sgl-project/sglang). Both serve an OpenAI-compatible API. Support for LFM3-VL in SGLang is in review in [sgl-project/sglang#46858](https://github.com/sgl-project/sglang/pull/46858), and support in vLLM is in progress. We will update this card when their releases support it.

**vLLM**:

```bash
vllm serve LiquidAI/LFM3-VL-2B \
  --reasoning-parser qwen3 \
  --enable-auto-tool-choice --tool-call-parser qwen3_coder \
  --chat-template-content-format openai \
  --structured-outputs-config '{"backend": "xgrammar", "disable_any_whitespace": true}' \
  --media-io-kwargs '{"video": {"video_backend": "qwen3_vl"}}'
```

**SGLang**:

```bash
sglang serve --model-path LiquidAI/LFM3-VL-2B --trust-remote-code \
  --reasoning-parser auto \
  --tool-call-parser auto \
  --constrained-json-disable-any-whitespace
```

Send an image-and-text request with the OpenAI client. Change `base_url` to `http://localhost:30000/v1` for SGLang, or `http://localhost:8080/v1` for llama.cpp:

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="EMPTY")

response = client.chat.completions.create(
    model="LiquidAI/LFM3-VL-2B",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": "https://placecats.com/300/200"}},
                {"type": "text", "text": "Describe this image."},
            ],
        }
    ],
    temperature=0.1,
    extra_body={"top_k": 50, "repetition_penalty": 1.1},
)
print(response.choices[0].message.content)
```

</details>

<details>
<summary><strong>Video frame rate and frame limit</strong></summary>

By default, LFM3-VL-2B samples video at 2 fps, with at least 4 and at most 768 frames per video. Each frame adds vision tokens, so for long videos a lower frame rate or frame limit uses less context and memory.

- **Transformers:** set the frame rate per call with `processor.apply_chat_template(..., processor_kwargs={"fps": 1})`. Set the frame limit when you load the processor: `AutoProcessor.from_pretrained(model_id, trust_remote_code=True, max_frames=128)`.
- **vLLM:** set a server default in `--media-io-kwargs`, for example `'{"video": {"video_backend": "qwen3_vl", "fps": 1, "max_frames": 128}}'`. Override it per request with `extra_body={"media_io_kwargs": {"video": {"fps": 1, "max_frames": 128}}}`.
- **SGLang:** change `fps`, `min_frames`, and `max_frames` under `video_processor` in `processor_config.json` in a local copy of the checkpoint.
- **llama.cpp:** always uses 2 fps and 4 to 768 frames for this model. `--video-fps` has no effect.

</details>

<details>
<summary><strong>Chat template</strong></summary>

LFM3-VL uses this ChatML format, generated from the checkpoint's [chat template](https://huggingface.co/LiquidAI/LFM3-VL-2B/blob/main/chat_template.jinja):

```text
<|startoftext|><|im_start|>system
You are a helpful assistant trained by Liquid AI.<|im_end|>
<|im_start|>user
<|vision_start|><|image|><|vision_end|>What species is in this picture?<|im_end|>
<|im_start|>assistant
<think>
```

Use `processor.apply_chat_template()` with `add_generation_prompt=True` to format messages automatically. The model thinks in a `<think>...</think>` block before it answers.

The template inserts `<|vision_start|><|image|><|vision_end|>` for each image and `<|vision_start|><|video|><|vision_end|>` for each video. Do not put these tags in your message content.

Reasoning from turns before the latest user message is removed unless `preserve_thinking=True`.

</details>

<details>
<summary><strong>Tool calling</strong></summary>

Pass function schemas through `tools=...` to `apply_chat_template()`. The template formats tool definitions and results automatically. Generated calls use XML:

```text
<tool_call>
<function=get_weather>
<parameter=city>
Paris
</parameter>
</function>
</tool_call>
```

> [!WARNING]
> LFM3's tool call format has changed from the custom LFM2/LFM2.5 format to a superset of `qwen3_coder`.

Execute the call in your application. Add the parsed assistant call to history as a `tool_calls` entry, then append the result as a `tool` message. Keep passing the tool schemas on subsequent requests and preserve the assistant's content and reasoning from the current tool-use turn.

`function.arguments` must be a Python mapping. Decode JSON strings with `json.loads()` before applying the template.

See the [Tool Use documentation](https://docs.liquid.ai/lfm/key-concepts/tool-use) for the full guide.

</details>

<details>
<summary><strong>Tool search</strong></summary>

LFM3 supports deferred tools. Set `defer_loading=True` to keep tool definitions out of the prompt until your harness's search tool returns their names as `tool_reference` parts. The chat template then inserts their definitions into `<additional_tools>`.

```python
tools = [
    search_tool,
    {"type": "function", "defer_loading": True, "function": get_weather_schema},
]
messages.append({
    "role": "tool",
    "tool_call_id": call_id,
    "content": [
        {"type": "text", "text": "Found 1 tool."},
        {"type": "tool_reference", "name": "get_weather"},
    ],
})
```

Your harness implements and runs the search. Keep the full `tools` list, including deferred tools, on every request.

See [Deferred tools and tool search](https://docs.liquid.ai/lfm/key-concepts/tool-search) for the full guide.

</details>

## Fine-tuning
<hr style="margin: -0.7em 0 1.2em 0; border: 0; border-top: 1px solid rgba(127, 127, 127, 0.3);" />

LFM3-VL-2B is designed for **easy customization** for a given domain, task, or application via [TRL](https://docs.liquid.ai/lfm/fine-tuning/trl).

<table style="width: 100%; display: table; border: 0; border-radius: 0; border-collapse: collapse;">
<thead style="border: 0;">
<tr style="border: 0;">
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Training</th>
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Use case</th>
<th scope="col" style="text-align: center; white-space: nowrap; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Notebook</th>
</tr>
</thead>
<tbody style="border: 0;">
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><strong>SFT</strong></td>
<td style="border: 0; padding: 0.55em 0.75em;">Extract structured JSON from receipt photos</td>
<td style="text-align: center; border: 0; padding: 0.55em 0.75em;"><a href="https://colab.research.google.com/github/Liquid4All/cookbook/blob/main/finetuning/notebooks/lfm3_vl_sft_with_trl.ipynb" title="SFT with TRL"><img src="https://colab.research.google.com/assets/colab-badge.svg" width="117" height="20" alt="Open in Colab" style="display: inline-block; width: 117px; height: 20px; margin: 0; vertical-align: middle;" /></a></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><strong>GRPO</strong></td>
<td style="border: 0; padding: 0.55em 0.75em;">Transcribe images of equations to LaTeX</td>
<td style="text-align: center; border: 0; padding: 0.55em 0.75em;"><a href="https://colab.research.google.com/github/Liquid4All/cookbook/blob/main/finetuning/notebooks/lfm3_vl_grpo_with_trl.ipynb" title="GRPO with TRL"><img src="https://colab.research.google.com/assets/colab-badge.svg" width="117" height="20" alt="Open in Colab" style="display: inline-block; width: 117px; height: 20px; margin: 0; vertical-align: middle;" /></a></td>
</tr>
</tbody>
</table>

## Performance
<hr style="margin: -0.7em 0 1.2em 0; border: 0; border-top: 1px solid rgba(127, 127, 127, 0.3);" />

### Benchmarks

Across 62 vision benchmarks, LFM3-VL-2B scores at least 8 points ahead of all models of similar size. It matches Gemma 4 12B, is within 2 points of GPT-5.6 Luna, and scores higher than Gemini 3.5 Flash Lite.

<div role="region" aria-labelledby="benchmarks" tabindex="0" style="width: 100%; max-width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch;">
<table style="width: 100%; min-width: 48rem; display: table; border: 0; border-radius: 0; border-collapse: collapse; font-size: calc(0.875em - 1pt);">
<thead style="border: 0;">
<tr style="border: 0;">
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Category</th>
<th scope="col" style="text-align: center; white-space: nowrap; background-color: rgba(108, 79, 224, 0.08); padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);"><strong>LFM3-VL<br>2B</strong></th>
<th scope="col" style="text-align: center; white-space: nowrap; background-color: rgba(108, 79, 224, 0.08); padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);"><strong>LFM3-VL<br>2B&nbsp;(no&nbsp;think)</strong></th>
<th scope="col" style="text-align: center; white-space: nowrap; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">LFM2.5-VL<br>3B</th>
<th scope="col" style="text-align: center; white-space: nowrap; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">MiniCPM-V&nbsp;4.7<br>1B</th>
<th scope="col" style="text-align: center; white-space: nowrap; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Qwen3.5<br>2B</th>
<th scope="col" style="text-align: center; white-space: nowrap; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Qwen3.5<br>4B</th>
<th scope="col" style="text-align: center; white-space: nowrap; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">InternVL3.5<br>4B</th>
<th scope="col" style="text-align: center; white-space: nowrap; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Gemma&nbsp;4<br>E2B</th>
<th scope="col" style="text-align: center; white-space: nowrap; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Gemma&nbsp;4<br>12B</th>
<th scope="col" style="text-align: center; white-space: nowrap; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">GPT-5.6<br>Luna</th>
<th scope="col" style="text-align: center; white-space: nowrap; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Gemini&nbsp;3.5<br>Flash&nbsp;Lite</th>
</tr>
</thead>
<tbody style="border: 0;">
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">General</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">66.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">56.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">57.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">59.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">64.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">73.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">61.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">56.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>74.0</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">72.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>74.1</strong></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">Perception</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><u>75.6</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">68.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">67.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">65.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">71.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>77.1</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">63.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">59.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">73.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">71.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">73.0</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">Document, OCR & Chart</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">83.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">71.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">71.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">73.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">79.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">84.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">72.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">72.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>85.7</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>84.4</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">82.3</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">Math & logical reasoning</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">68.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">41.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">40.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">51.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">61.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>78.4</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">46.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">51.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>79.3</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">77.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">66.7</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">Visual grounding</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>77.3</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">72.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">68.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">51.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">61.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">67.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">63.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">41.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>74.1</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">72.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">63.5</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">Embodied reasoning</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>64.4</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">57.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">48.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">45.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">51.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>63.2</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">48.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">41.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">59.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">61.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">50.3</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">GUI understanding</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>83.1</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">81.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">66.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">45.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">67.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">81.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">68.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">44.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">76.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>82.5</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">71.0</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">Video</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">61.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">54.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">41.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">53.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">57.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">67.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">59.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">46.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">58.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>72.8</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>70.0</u></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">Multilingual</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">84.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">76.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">81.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">77.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">78.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">83.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">79.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">73.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>86.1</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">82.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>85.8</u></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">Agentic</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">42.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">32.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">21.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">16.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">15.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">31.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">N/A</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">23.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">43.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>56.1</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>62.4</strong></td>
</tr>
</tbody>
<tbody style="border: 0;">
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em; border-top: 1px solid rgba(127, 127, 127, 0.25);"><strong>Average</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em; border-top: 1px solid rgba(127, 127, 127, 0.25);">71.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em; border-top: 1px solid rgba(127, 127, 127, 0.25);">62.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em; border-top: 1px solid rgba(127, 127, 127, 0.25);">57.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em; border-top: 1px solid rgba(127, 127, 127, 0.25);">57.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em; border-top: 1px solid rgba(127, 127, 127, 0.25);">64.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em; border-top: 1px solid rgba(127, 127, 127, 0.25);"><strong>73.4</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em; border-top: 1px solid rgba(127, 127, 127, 0.25);">61.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em; border-top: 1px solid rgba(127, 127, 127, 0.25);">53.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em; border-top: 1px solid rgba(127, 127, 127, 0.25);"><u>71.7</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em; border-top: 1px solid rgba(127, 127, 127, 0.25);"><strong>73.4</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em; border-top: 1px solid rgba(127, 127, 127, 0.25);">70.0</td>
</tr>
</tbody>
</table>
</div>

<details>
<summary><small>All 62 benchmarks</small></summary>

<div role="region" aria-labelledby="benchmarks" tabindex="0" style="width: 100%; max-width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch;">
<table style="width: 100%; min-width: 56rem; display: table; border: 0; border-radius: 0; border-collapse: collapse; font-size: calc(0.875em - 1pt);">
<thead style="border: 0;">
<tr style="border: 0;">
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Benchmark</th>
<th scope="col" style="text-align: center; white-space: nowrap; background-color: rgba(108, 79, 224, 0.08); padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);"><strong>LFM3-VL<br>2B</strong></th>
<th scope="col" style="text-align: center; white-space: nowrap; background-color: rgba(108, 79, 224, 0.08); padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);"><strong>LFM3-VL<br>2B&nbsp;(no&nbsp;think)</strong></th>
<th scope="col" style="text-align: center; white-space: nowrap; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">LFM2.5-VL<br>3B</th>
<th scope="col" style="text-align: center; white-space: nowrap; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">MiniCPM-V&nbsp;4.7<br>1B</th>
<th scope="col" style="text-align: center; white-space: nowrap; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Qwen3.5<br>2B</th>
<th scope="col" style="text-align: center; white-space: nowrap; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Qwen3.5<br>4B</th>
<th scope="col" style="text-align: center; white-space: nowrap; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">InternVL3.5<br>4B</th>
<th scope="col" style="text-align: center; white-space: nowrap; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Gemma&nbsp;4<br>E2B</th>
<th scope="col" style="text-align: center; white-space: nowrap; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Gemma&nbsp;4<br>12B</th>
<th scope="col" style="text-align: center; white-space: nowrap; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">GPT-5.6<br>Luna</th>
<th scope="col" style="text-align: center; white-space: nowrap; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Gemini&nbsp;3.5<br>Flash&nbsp;Lite</th>
</tr>
</thead>
<tbody style="border: 0;">
<tr style="border: 0;"><th scope="rowgroup" style="text-align: left; background-color: transparent; padding: 0.55em 0.75em; border: 0; font-weight: 600; padding-top: 1em; padding-bottom: 0.5em;">General</th><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; background-color: rgba(108, 79, 224, 0.08);"></td><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; background-color: rgba(108, 79, 224, 0.08);"></td><td colspan="9" aria-hidden="true" style="border: 0; padding: 0.55em 0.75em;"></td></tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MME</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">86.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">76.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">74.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">82.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">83.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>88.3</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">82.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">79.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">85.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">74.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>89.2</strong></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MMStar</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">74.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">62.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">63.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">68.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">71.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>76.6</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">65.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">61.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>77.7</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">72.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">73.1</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">SimpleVQA</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">36.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">27.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">32.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">36.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">38.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">45.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">33.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">28.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">42.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>53.2</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>56.9</strong></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">SEED-Bench (image)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">78.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">76.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">77.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">76.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">76.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">78.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">76.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">75.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>80.6</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">76.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>79.5</u></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MMBench (dev EN v1.1)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">86.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">76.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">81.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">83.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">80.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>86.5</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">81.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">70.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>88.2</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">84.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>88.2</strong></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MMMU (val)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">55.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">48.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">47.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">51.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">58.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">74.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">57.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">57.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>76.7</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>75.2</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">72.0</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MMMU-Pro</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">45.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">35.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">33.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">37.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">50.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">67.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">38.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">42.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>69.1</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>70.9</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">63.2</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MM-Vet (v1)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">57.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">44.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">48.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">46.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">53.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">59.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">65.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">44.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">64.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>67.1</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>73.3</strong></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MM-IFEval</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">72.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">54.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">60.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">58.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">62.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">79.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">57.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">61.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>83.0</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>82.0</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">73.2</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MuirBench</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">66.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">61.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">58.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">57.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">65.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>72.8</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">54.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">47.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">71.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">66.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>72.7</u></td>
</tr>
<tr style="border: 0;"><th scope="rowgroup" style="text-align: left; background-color: transparent; padding: 0.55em 0.75em; border: 0; font-weight: 600; padding-top: 1em; padding-bottom: 0.5em;">Perception</th><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; background-color: rgba(108, 79, 224, 0.08);"></td><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; background-color: rgba(108, 79, 224, 0.08);"></td><td colspan="9" aria-hidden="true" style="border: 0; padding: 0.55em 0.75em;"></td></tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">BLINK</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>71.1</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">68.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">61.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">60.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">63.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">69.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">57.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">52.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>70.9</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">68.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">68.9</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">CountBenchQA</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><u>93.0</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">86.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">87.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">86.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">87.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">92.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">81.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">78.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>95.9</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">91.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">90.1</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">HallusionBench</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">65.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">52.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">46.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">53.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">61.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>66.2</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">58.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">56.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>68.9</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">59.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">65.6</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">POPE</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">88.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">86.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>88.9</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>89.2</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">88.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">88.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">88.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">84.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">87.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">85.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>89.2</strong></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">PerceptionBench</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">37.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">28.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">27.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">26.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">29.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">39.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">27.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">28.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>43.5</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>48.8</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">37.7</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">HR-Bench (4K)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><u>82.3</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">71.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">71.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">67.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">76.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>88.1</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">55.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">65.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">77.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">80.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">79.2</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">HR-Bench (8K)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><u>76.2</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">64.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">62.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">61.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">74.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>82.1</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">54.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">57.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">70.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">60.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">75.7</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">ZoomBench (full + crop average)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><u>62.6</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">60.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">61.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">52.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">56.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">61.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">52.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">43.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">59.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">59.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>65.0</strong></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">V*Bench</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><u>86.4</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">80.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">81.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">71.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">85.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>89.5</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">71.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">44.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">69.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">79.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">74.9</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">RealWorldQA</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><u>79.3</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">73.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">72.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">68.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">75.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>81.0</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">67.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">61.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">76.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">72.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">74.4</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">CV-Bench</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>88.8</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">85.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">86.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">82.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">84.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>88.4</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">80.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">77.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">87.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">76.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">82.7</td>
</tr>
<tr style="border: 0;"><th scope="rowgroup" style="text-align: left; background-color: transparent; padding: 0.55em 0.75em; border: 0; font-weight: 600; padding-top: 1em; padding-bottom: 0.5em;">Document, OCR & Chart</th><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; background-color: rgba(108, 79, 224, 0.08);"></td><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; background-color: rgba(108, 79, 224, 0.08);"></td><td colspan="9" aria-hidden="true" style="border: 0; padding: 0.55em 0.75em;"></td></tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">DocVQA (val)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">96.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">94.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">91.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">91.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">95.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>97.1</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">90.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">90.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>97.0</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">94.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">96.2</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">TextVQA (val)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">87.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">85.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>90.4</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">87.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">85.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">88.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">84.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">80.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">88.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">85.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>88.9</u></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">OCRBench v1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><u>86.3</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">82.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">84.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">82.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">83.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">86.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">83.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">71.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">81.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">79.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>87.9</strong></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">OCRBench v2 (En)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">63.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">48.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">48.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">44.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">55.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>65.7</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">50.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">51.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>67.2</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">64.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">55.5</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">ChartQA (test)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>92.7</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">81.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">80.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">88.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">85.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">85.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">86.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">82.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">89.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>90.2</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">88.2</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">InfographicVQA (val)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">86.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">70.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">65.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">72.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">85.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>90.6</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">67.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">71.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">89.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>92.4</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">84.0</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">CharXiv (descriptive, val)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">87.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">65.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">69.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">73.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">84.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">92.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">67.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">85.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>95.8</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>94.3</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">88.2</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">CharXiv (reasoning, val)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">70.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">44.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">38.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">44.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">58.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">68.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">46.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">46.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>77.1</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>73.6</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">69.2</td>
</tr>
<tr style="border: 0;"><th scope="rowgroup" style="text-align: left; background-color: transparent; padding: 0.55em 0.75em; border: 0; font-weight: 600; padding-top: 1em; padding-bottom: 0.5em;">Math & logical reasoning</th><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; background-color: rgba(108, 79, 224, 0.08);"></td><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; background-color: rgba(108, 79, 224, 0.08);"></td><td colspan="9" aria-hidden="true" style="border: 0; padding: 0.55em 0.75em;"></td></tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">LogicVista</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">60.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">30.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">34.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">46.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">54.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">69.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">37.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">48.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>76.3</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>74.7</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">57.0</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MATH-Vision (full)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">51.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">28.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">22.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">30.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">41.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">72.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">33.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">40.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>73.8</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>79.9</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">57.5</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MathVista (mini)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><u>84.2</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">68.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">68.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">71.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">75.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>84.8</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">72.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">62.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">80.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">76.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">77.7</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">We-Math (testmini, strict)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">68.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">20.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">23.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">47.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">59.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>81.0</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">26.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">44.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>78.2</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">70.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">59.1</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">DynaMath (average accuracy)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">79.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">57.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">53.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">63.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">73.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>84.6</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">61.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">63.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>87.6</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>84.6</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">82.2</td>
</tr>
<tr style="border: 0;"><th scope="rowgroup" style="text-align: left; background-color: transparent; padding: 0.55em 0.75em; border: 0; font-weight: 600; padding-top: 1em; padding-bottom: 0.5em;">Visual grounding</th><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; background-color: rgba(108, 79, 224, 0.08);"></td><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; background-color: rgba(108, 79, 224, 0.08);"></td><td colspan="9" aria-hidden="true" style="border: 0; padding: 0.55em 0.75em;"></td></tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">RefCOCO-avg</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>90.5</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">87.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">87.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">86.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">78.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">87.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>88.8</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">68.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">82.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">81.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">81.6</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">RefCOCO-M</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>95.2</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">92.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">94.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">92.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">90.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">93.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>94.6</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">76.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">88.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">89.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">87.6</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">Point-Bench</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>73.8</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">69.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">58.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">16.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">54.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">56.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">47.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">14.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>73.4</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">66.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">51.4</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">RefSpatial-Bench</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">49.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">40.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">32.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">8.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">21.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">30.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">23.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">6.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>51.7</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>52.5</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">33.6</td>
</tr>
<tr style="border: 0;"><th scope="rowgroup" style="text-align: left; background-color: transparent; padding: 0.55em 0.75em; border: 0; font-weight: 600; padding-top: 1em; padding-bottom: 0.5em;">Embodied reasoning</th><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; background-color: rgba(108, 79, 224, 0.08);"></td><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; background-color: rgba(108, 79, 224, 0.08);"></td><td colspan="9" aria-hidden="true" style="border: 0; padding: 0.55em 0.75em;"></td></tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">EmbSpatial-Bench</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>82.9</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">77.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">74.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">71.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">77.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>82.4</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">71.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">67.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">80.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">75.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">75.3</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">ERQA</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">48.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">40.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">39.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">44.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">41.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">52.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">37.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">37.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>59.5</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>56.5</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">50.5</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MindCube (tinybench)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>56.5</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">51.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">45.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">47.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">43.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">52.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">39.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">37.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>54.9</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">45.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">37.5</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">SAT (val + test)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>80.2</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">71.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">57.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">56.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">66.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>80.1</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">59.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">59.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">74.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">71.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">62.8</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">RoboSpatial-Home</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">63.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">51.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">48.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">41.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">47.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>67.4</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">45.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">46.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>66.9</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">63.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">41.4</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">Where2Place</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">44.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">42.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">42.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">6.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">30.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">47.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">24.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">18.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>49.0</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>51.6</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">21.0</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">OpenEQA (episodic memory, video)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">76.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">66.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">49.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">64.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">63.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">72.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">60.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">43.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">56.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>78.5</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>77.5</u></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">VSI-Bench</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><u>63.1</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>63.3</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">26.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">30.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">39.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">50.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">52.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">21.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">31.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">49.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">36.5</td>
</tr>
<tr style="border: 0;"><th scope="rowgroup" style="text-align: left; background-color: transparent; padding: 0.55em 0.75em; border: 0; font-weight: 600; padding-top: 1em; padding-bottom: 0.5em;">GUI understanding</th><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; background-color: rgba(108, 79, 224, 0.08);"></td><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; background-color: rgba(108, 79, 224, 0.08);"></td><td colspan="9" aria-hidden="true" style="border: 0; padding: 0.55em 0.75em;"></td></tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">ScreenSpot-Pro</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><u>55.5</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">49.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">22.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">4.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">38.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">50.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">21.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">1.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">25.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>57.4</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">39.2</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">ScreenSpot-v2 Desktop</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><u>94.6</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>95.5</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">78.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">51.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">75.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">91.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">81.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">52.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">93.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>94.6</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">86.5</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">ScreenSpot-v2 Mobile</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">92.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">91.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">80.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">68.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">82.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>92.4</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">87.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">71.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>93.0</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">88.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">80.0</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">ScreenSpot-v2 Web</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><u>89.9</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">89.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">81.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">56.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">72.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">89.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">82.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">52.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>92.9</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">89.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">78.3</td>
</tr>
<tr style="border: 0;"><th scope="rowgroup" style="text-align: left; background-color: transparent; padding: 0.55em 0.75em; border: 0; font-weight: 600; padding-top: 1em; padding-bottom: 0.5em;">Video</th><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; background-color: rgba(108, 79, 224, 0.08);"></td><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; background-color: rgba(108, 79, 224, 0.08);"></td><td colspan="9" aria-hidden="true" style="border: 0; padding: 0.55em 0.75em;"></td></tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MVBench</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">69.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">59.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">50.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">53.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">64.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>71.3</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>72.3</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">45.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">54.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">68.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">64.5</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">ActivityNet-QA (test)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>71.2</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">59.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">40.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">58.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">59.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">64.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">63.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">47.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">57.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>66.8</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">65.6</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">LVBench</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">41.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">40.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">34.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">39.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">35.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">47.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">42.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">27.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">36.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>58.9</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>58.7</u></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MLVU (dev, M-Avg)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">71.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">63.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">47.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">64.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">68.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">76.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">66.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">45.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">53.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>77.6</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>78.2</strong></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MMVU (val)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">52.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">45.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">38.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">45.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">53.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">67.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">52.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">47.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">65.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>77.6</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>76.3</u></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MotionBench (dev)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><u>64.0</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">56.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">50.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">51.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">56.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">61.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">58.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">41.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">53.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>67.7</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">61.0</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">Video-MME (v1, no subtitles)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">62.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">57.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">44.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">57.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">59.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">71.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">61.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">48.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">62.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>75.7</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>74.0</u></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">Video-MME (v1, subtitles)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">69.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">63.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">43.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">62.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">65.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>78.3</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">63.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">59.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">73.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>81.6</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">77.8</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">Video-MMMU</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">49.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">39.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">22.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">50.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">51.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">69.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">58.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">57.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">72.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>81.1</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>73.9</u></td>
</tr>
<tr style="border: 0;"><th scope="rowgroup" style="text-align: left; background-color: transparent; padding: 0.55em 0.75em; border: 0; font-weight: 600; padding-top: 1em; padding-bottom: 0.5em;">Multilingual</th><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; background-color: rgba(108, 79, 224, 0.08);"></td><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; background-color: rgba(108, 79, 224, 0.08);"></td><td colspan="9" aria-hidden="true" style="border: 0; padding: 0.55em 0.75em;"></td></tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MMMB</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">85.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">80.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">83.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">79.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">81.4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">85.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">81.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">78.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>86.9</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">82.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>85.4</u></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">Multilingual MMBench</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">83.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">72.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">79.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">75.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">75.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">82.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">76.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">68.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>85.4</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">82.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>86.2</strong></td>
</tr>
<tr style="border: 0;"><th scope="rowgroup" style="text-align: left; background-color: transparent; padding: 0.55em 0.75em; border: 0; font-weight: 600; padding-top: 1em; padding-bottom: 0.5em;">Agentic</th><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; background-color: rgba(108, 79, 224, 0.08);"></td><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; background-color: rgba(108, 79, 224, 0.08);"></td><td colspan="9" aria-hidden="true" style="border: 0; padding: 0.55em 0.75em;"></td></tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MM-ToolSandbox (partial credit)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">42.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">32.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">21.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">16.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">15.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">31.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">N/A</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">23.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">43.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>56.1</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>62.4</strong></td>
</tr>
</tbody>
</table>
</div>

</details>

<details>
<summary><small>Evaluation details</small></summary>

<p><small>We evaluated all models with vLLM 0.27.1, using each model's recommended generation parameters when available.</small></p>

<p><small>We used reasoning mode for all models except LFM2.5-VL-3B, which does not support it, and the LFM3-VL-2B no-thinking configuration, for which we disabled thinking. For InternVL3.5, we report the higher score from reasoning and non-reasoning modes on each benchmark. GPT-5.6 Luna and Gemini 3.5 Flash Lite used their default reasoning effort: medium for Luna and minimal for Gemini.</small></p>

<p><small>For models without native video support, we sampled frames at 2 FPS, up to a maximum of 384 frames per video, and provided them to the model as images.</small></p>

<p><small>All scores are normalized to a 0–100 scale. Each category score is the unweighted mean of its benchmark scores, and the Average row is the unweighted mean across all 62 benchmarks.</small></p>

<p><small>We used GPT-6 Luna as a judge for benchmarks that require an LLM judge.</small></p>

<p><small>
<strong>Original score scales:</strong> MME uses a 0–2800 scale; OCRBench, 0–1000; and DocVQA and InfographicVQA, 0–1.<br>
<strong>RefCOCO-avg:</strong> Mean P@1 across eight splits: RefCOCO (val, testA, testB), RefCOCO+ (val, testA, testB), and RefCOCOg (val, test).<br>
<strong>POPE:</strong> F1 over all examples from the adversarial, popular, and random subsets.<br>
<strong>MMMU-Pro:</strong> The multiple-choice variant with 10 answer options per question.
</small></p>

</details>

### Edge inference

LFM3-VL-2B has the highest prefill throughput and the lowest memory use of all compared models on all three devices.

<img src="https://cdn-uploads.huggingface.co/production/uploads/64df8592d27135dd568380b5/ZK7GqqnM_3E4U0AW7Ns_O.png" alt="LFM3-VL-2B edge inference: prefill throughput, decode throughput, and memory on AMD Ryzen AI Max+ 395, Apple M5 Max, and Samsung Galaxy S26 Ultra, compared with LFM2.5-VL-3B, MiniCPM-V 4.7 1B, Qwen3.5-2B, and Gemma 4 E2B." width="1989" height="1999" style="width: 100%; max-width: 995px; height: auto;" />

<details>
<summary><small>Evaluation details</small></summary>

<p><small>All models run in llama.cpp with a Q4_0 GGUF language model and an F16 vision projector (mmproj). Each request has one 512×512 image and 1,024 text tokens, and generates 256 tokens. Prefill is the prompt processing speed and decode is the generation speed, both in tokens per second. Memory is peak use in GB.</small></p>

</details>

### GPU inference

On one NVIDIA B300, LFM3-VL-2B produces more than 12,000 tokens/s at 1,024 concurrent requests, more than any compared model.

<img src="https://cdn-uploads.huggingface.co/production/uploads/64df8592d27135dd568380b5/lXRtpri8b7R9MuwlKtQtt.png" alt="LFM3-VL-2B GPU inference: end-to-end output throughput versus concurrent requests on one NVIDIA B300, compared with Qwen 3.5 2B, MiniCPM-V 4.7 1B, Gemma 4 E2B, and LFM2.5-VL-3B." width="1440" height="749" style="width: 100%; max-width: 1440px; height: auto;" />

<details>
<summary><small>Evaluation details</small></summary>

<p><small>All models run in BF16 on SGLang v0.5.22 with LFM3 support. Each request has one 512×512 image and 1,024 text tokens, and generates at most 256 tokens. Throughput is end-to-end output tokens per second, as the mean of 3 runs.</small></p>

</details>

## Training
<hr style="margin: -0.7em 0 1.2em 0; border: 0; border-top: 1px solid rgba(127, 127, 127, 0.3);" />

<img src="https://cdn-uploads.huggingface.co/production/uploads/64df8592d27135dd568380b5/VRo1ZLQhR_aw0tpC6B707.png" alt="LFM3-VL-2B pre-training: LFM3-1.7B-Base is pre-trained on web and synthetic data (about 15T tokens), then code, math, and science (3T tokens at 4K context), then mid-trained on curated agentic data (3T tokens at 32K context), a 128K extension (500B tokens), and a 256K extension (50B tokens), for 22T tokens in total." width="3344" height="896" style="width: 100%; max-width: 1672px; height: auto;" />

**Pre-training:** LFM3-VL-2B starts from [LFM3-1.7B-Base](https://huggingface.co/LiquidAI/LFM3-1.7B-Base), which is pre-trained in two stages on 22T tokens in total.

- **Main pre-training:** compared with LFM2, the mix adds more scientific papers, repository-level code, math, and a wider range of knowledge sources.
- **Mid-training:** the last 3.5T tokens use curated, higher-quality data with a larger share of agentic traces and tool calls. This stage also extends the context window to 256K tokens.

<img src="https://cdn-uploads.huggingface.co/production/uploads/64df8592d27135dd568380b5/p36YCBS_lG7tinntf-VNB.png" alt="LFM3-VL-2B post-training: LFM3-1.7B-Base and the Liquid vision encoder go through vision mid-training and SFT, then vision RL. MOPD distills the vision RL model and the Mixed RL model from LFM3-1.7B into LFM3-VL-2B." width="2776" height="1376" style="width: 100%; max-width: 1388px; height: auto;" />

**Post-training:** four stages develop visual understanding, reasoning, and tool use.

- **Vision mid-training:** LFM3-1.7B-Base is joined with our new in-house vision encoder, which combines convolution and attention, and trained on image and video data.
- **Supervised fine-tuning (SFT):** a wide mix of instruction following, reasoning, tool calling, agentic traces, grounding, and multimodal perception and understanding.
- **Vision reinforcement learning:** many domains trained at once, to improve reasoning and general intelligence.
- **Multi-domain on-policy distillation (MOPD):** a vision teacher model and the Mixed RL model from LFM3-1.7B are distilled back into a single model.

## Citation
<hr style="margin: -0.7em 0 1.2em 0; border: 0; border-top: 1px solid rgba(127, 127, 127, 0.3);" />

```bibtex
@article{liquidAI2026LFM3,
  author  = {Liquid AI},
  title   = {Introducing LFM3: Every Modality for Specialized Intelligence},
  journal = {Liquid AI Blog},
  year    = {2026},
  note    = {www.liquid.ai/blog/lfm3},
}
```

For questions and feedback, join [Discord](https://discord.com/invite/liquid-ai). For custom deployment and fine-tuning support, [contact Liquid AI](https://www.liquid.ai/connect?utm_source=huggingface&utm_medium=referral&utm_campaign=huggingface).
