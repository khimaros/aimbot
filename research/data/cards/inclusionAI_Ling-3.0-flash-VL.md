---
license: mit
pipeline_tag: image-text-to-text
---
<p align="center">
    <img src="https://mdn.alipayobjects.com/huamei_qa8qxu/afts/img/A*4QxcQrBlTiAAAAAAQXAAAAgAemJ7AQ/original" width="100"/>
</p>
<p align="center">🤗 <a href="https://huggingface.co/inclusionAI">Hugging Face</a>&nbsp;&nbsp; | &nbsp;&nbsp;🤖 <a href="https://modelscope.cn/organization/inclusionAI">ModelScope </a>&nbsp;&nbsp;</p>

# Introduction
We are introducing Ling-3.0-flash-VL, our next-generation native multimodal model. Built upon Ling-3.0-flash, it brings visual information into the complete process of understanding, reasoning, acting, and verification—advancing beyond image and video perception to solving real-world tasks through vision.
With 124B total parameters, only 5.5B activated parameters per token, support for image and video inputs, and a context window of up to 256K tokens, Ling-3.0-flash-VL delivers powerful multimodal reasoning and agentic capabilities with exceptional efficiency.

# Model Overview
Ling-3.0-flash-VL inherits the language, reasoning, and long-context capabilities of Ling-3.0-flash, while extending them with native image and video understanding. The model has 124B total parameters, with only 5.5B parameters activated per token, and supports a context window of up to 256K tokens.

The architecture of Ling-3.0-flash-VL is designed to integrate visual information into real-world reasoning and agentic workflows.

- A ViT visual encoder extracts features from images and videos, while a two-layer MLP projector aligns visual features with text representations for unified multimodal understanding and reasoning;
- VideoRoPE encodes both spatial positions and temporal order, enabling the model to understand visual changes over time and supporting tasks such as event localization, long-video question answering, and video clip editing;
- A 42-layer hybrid backbone alternates KDA and Gated MLA layers at a 5:1 ratio, enabling efficient long-context processing across text, images, videos, and extended agent task histories;
- A sparse MoE architecture maintains a total model capacity of 124B parameters while activating only 5.5B parameters per token, balancing strong multimodal capabilities with inference efficiency.

Overall, these designs make vision more than just an input, integrating it into the complete process of understanding, reasoning, planning, acting, and verification.


![ling-3.0-flash-vl-0910](https://cdn-uploads.huggingface.co/production/uploads/6666ca359f5a0b3229238a1a/IL2eS4KUbKLYCWcoFC-Bq.png)

# Evaluation
Ling-3.0-flash-VL achieves a score of **42** on the Artificial Analysis Intelligence Index v4.1.1, improving by 4 points over Ling-3.0-flash’s score of 38. The results show that extending the model with visual capabilities further improves its overall intelligence performance.


![ling-3.0-flash-vl-aa](https://cdn-uploads.huggingface.co/production/uploads/6666ca359f5a0b3229238a1a/5gqrYjboQ8j7sTWjd1A_q.png)

Across multimodal benchmarks, Ling-3.0-flash-VL demonstrates three distinct capability dimensions:

- **Understand: Comprehending complex visual information.** The model can handle object counting, complex layouts, charts, and document content.
- **Reason: Reasoning and verification with visual evidence.** The model can use visual information for calculation, multi-step reasoning, and external information verification.
- **Act: Interacting with interfaces and completing tasks.** The model can understand web and software interfaces, then translate visual information into sequences of actions.

![ling-3.0-flash-vl-benchmark](https://cdn-uploads.huggingface.co/production/uploads/6666ca359f5a0b3229238a1a/w-V0gtCa3qy0un6vuz-sj.png)

> + Thinking mode is enabled by default. Unless otherwise specified, the default parameters for Ling-3.0-flash-VL are as follows: `temperature=0.6`, `top_p=0.95`, `top_k=20`.
> + Terminal-Bench 2.1: Evaluated under the Artificial Analysis (AA) protocol using the default Terminus 2 harness, a unified 2-hour timeout, the provided JSON parser in preserve-thinking mode, and 3 runs per task (mean). Decoding uses temperature=1.0, max_new_tokens=32K, with a 256K context window.

# Quickstart
## SGLang
The hardware- and recipe-specific launch matrix (BF16/FP8 × Low-Latency / High-Throughput), with a live command generator and verified configurations, lives in the SGLang cookbook:

**Cookbook:** https://docs.sglang.io/cookbook/autoregressive/InclusionAI/Ling-3.0-flash-VL


### Install SGLang

```bash
docker pull lmsysorg/sglang:dev-Ling-3.0-flash-VL
```

### Run Inference
Recommended recipe with 256K context (YaRN), on 4× 141GB-class GPUs (H20-3e / H200) or 4-GPU Blackwell nodes (B300 / GB300):

```bash
docker run --rm --gpus all --ipc=host --shm-size 32g \
  -p 30000:30000 \
  -e HF_TOKEN=<your-hf-token> \
  lmsysorg/sglang:dev-Ling-3.0-flash-VL \
  env SGLANG_ALLOW_OVERWRITE_LONGER_CONTEXT_LEN=1 \
  python3 -m sglang.launch_server \
    --model-path inclusionAI/Ling-3.0-flash-VL \
    --tp 4 \
    --context-length 262144 \
    --json-model-override-args '{"rope_scaling":{"rope_type":"yarn","factor":2.0,"rope_theta":6000000,"partial_rotary_factor":0.5,"original_max_position_embeddings":131072}}' \
    --trust-remote-code \
    --reasoning-parser auto \
    --tool-call-parser auto \
    --host 0.0.0.0 \
    --port 30000
```

On 80GB cards (H100 / H800), scale out to `--tp 8`. The reasoning and tool-call parsers resolve automatically to `ling3` from the chat template; you can also set them explicitly with `--reasoning-parser ling3 --tool-call-parser ling3`.

**Client**

Thinking is enabled by default by the chat template; disable it per request with `"chat_template_kwargs": {"enable_thinking": false}`. Recommended sampling: `temperature=1.0`, `top_p=0.95`, `top_k=20` (per `generation_config.json`).

```bash
curl -s http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "inclusionAI/Ling-3.0-flash-VL",
       "messages": [{"role": "user", "content": [
         {"type": "image_url", "image_url": {"url": "https://example.com/image.png"}},
         {"type": "text", "text": "Describe this image in one sentence."}
       ]}],
       "stream": true,
       "temperature": 1.0, "top_k": 20, "top_p": 0.95
     }'
```
Video input uses `{"type": "video_url", "video_url": {"url": "..."}}` in the same message shape. For MMMU-Pro / `bench_serving` reproduction commands and per-hardware recipes, see the cookbook page linked above.

## vLLM
### Environment Preparation

```bash
pip install uv

uv venv ~/my_ling_env

source ~/my_ling_env/bin/activate

git clone https://github.com/inclusionAI/vllm-ling-v3.git

cd vllm-ling-v3

VLLM_USE_PRECOMPILED=1 uv pip install --editable . --torch-backend=auto
```

### Run Inference

**Server**

```bash
vllm serve "$MODEL_PATH" \
    --port "$PORT" \
    --trust-remote-code \
    --served-model-name auto \
    --tensor-parallel-size 4 \
    --gpu-memory-utilization 0.85 \
    --enable-prefix-caching \
    --mamba-cache-mode align \
    --enable-auto-tool-choice \
    --tool-call-parser ling3 \
    --reasoning-parser ling3
```

**Client**

Thinking is enabled by default by the chat template; disable it per request with `"chat_template_kwargs": {"enable_thinking": false}`. Recommended sampling: `temperature=1.0`, `top_p=0.95`, `top_k=20` (per `generation_config.json`).

```bash
curl -s http://${MASTER_IP}:${PORT}/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "auto", -d '{"model": "inclusionAI/Ling-3.0-flash-VL",
       "messages": [{"role": "user", "content": [
         {"type": "image_url", "image_url": {"url": "https://example.com/image.png"}},
         {"type": "text", "text": "Describe this image in one sentence."}
       ]}],
       "stream": true,
       "temperature": 1.0, "top_k": 20, "top_p": 0.95
     }'
```
Video input uses `{"type": "video_url", "video_url": {"url": "..."}}` in the same message shape. For MMMU-Pro / `bench_serving` reproduction commands and per-hardware recipes, see the cookbook page linked above.


<!-- TDS-LINKS:START -->
## Training content summary

The public training-content summary identifying **Ling-3.0-flash-VL** is available below. Please refer to the document for its covered model versions, training-content scope, summary version, and update date.

- [Training-content summary (PDF)](https://huggingface.co/inclusionAI/AI-Transparency/resolve/main/Ling-3.0-VL_TDS-Summary.pdf)
- [Training-content documentation index](https://huggingface.co/inclusionAI/AI-Transparency)

This summary concerns training-content disclosure; it does not replace the model’s technical documentation, usage terms, or license.
<!-- TDS-LINKS:END -->

