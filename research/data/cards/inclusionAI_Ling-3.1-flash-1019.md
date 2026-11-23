---
license: mit
pipeline_tag: text-generation
---
<p align="center">
    <img src="https://mdn.alipayobjects.com/huamei_qa8qxu/afts/img/A*4QxcQrBlTiAAAAAAQXAAAAgAemJ7AQ/original" width="100"/>
</p>
<p align="center">🤗 <a href="https://huggingface.co/inclusionAI">Hugging Face</a>&nbsp;&nbsp; | &nbsp;&nbsp;🤖 <a href="https://modelscope.cn/organization/inclusionAI">ModelScope</a>&nbsp;&nbsp; | &nbsp;&nbsp;🐙 <a href="https://openrouter.ai/inclusionai/ling-3.1-flash">OpenRouter</a>&nbsp;&nbsp;</p>

## Introduction
We introduce **Ling-3.1-flash-1019**, an upgraded version of [Ling-3.1-flash](https://huggingface.co/inclusionAI/Ling-3.1-flash), with **560B** total parameters, **25B** active parameters per token, and a **1M-token context window**. With further post-training optimizations, **Ling-3.1-flash-1019** demonstrates significant improvements in scientific and real-world agentic capabilities. Its **AA-Briefcase** score rises from 1397 to **1524**, while performance on **AutomationBench-AA** increases from 62% to **68%**. The model also makes gains on scientific benchmarks, including **CritPt** (18% → **26%**) and **SciCode** (54% → **57%**). Overall, it scores **44** on the **Artificial Analysis Intelligence Index v4.3.2**, up from 41 for its predecessor. On the updated **Artificial Analysis Intelligence Index v5**, **Ling-3.1-flash-1019** scores **30**. These gains highlight the model's improved capabilities in complex reasoning, multi-step task execution, and agentic workflows across diverse real-world scenarios.
![Ling-3.1-flash-1019-score](https://cdn-uploads.huggingface.co/production/uploads/65d6aba7dee9f442f8ea7ded/HyR08GrR2dKmPC68di84A.png)

## Model Overview
The table and diagram below summarize the model’s specifications and architecture.

| Architecture | Hybrid-linear MoE |
| --- | --- |
| Parameter Scale | Total 560B, Activated 25B |
| Transformer Layers | 63 KDA + 9 Gated MLA (7:1) |
| Number of Dense Layers | 4 |
| Number of Routed Experts | 512 |
| Number of Shared Experts | 1 |
| Number of Activated Experts | 8 |
| Attention Heads | 64 |
| Hidden Size | 4096 |
| Expert Intermediate Size | 1280 |
| Dense Intermediate Size | 10240 |
| Vocabulary Size | 157184 |

![image](https://cdn-uploads.huggingface.co/production/uploads/678143d4ddb1f1ce16daca8e/qwmfVu_K08auI7R_ijbIX.png)

## Quickstart
### SGLang (Recommended)

The day-0 SGLang image includes Ling-3.1-flash support, MTP (NEXTN) speculative decoding, and Hopper decode optimizations:

```bash
docker pull lmsysorg/sglang:dev-ling-3.1-flash
```

#### Run Inference

**Server** (8 × H200, TP8 + EP8):

```bash
docker run --gpus all --network host --ipc=host --rm \
  lmsysorg/sglang:dev-ling-3.1-flash \
  python3 -m sglang.launch_server \
    --model-path inclusionAI/Ling-3.1-flash \
    --tp 8 --ep 8 \
    --speculative-algorithm NEXTN \
    --host 0.0.0.0 --port 30000
```

On 4 × GB300, use `--tp 4 --ep 4` instead. Hopper decode optimizations (optional, ~10% faster batch-1 decode) can be enabled with `SGLANG_ENABLE_FP8_BLOCK_GEMV=1` and `SGLANG_ENABLE_FUSED_KDA_OUTPUT_QUANT=1`.

**Client**

```bash
curl -s http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "Ling-3.1-flash",
       "messages": [{"role": "user", "content": "What is the capital of France?"}],
       "chat_template_kwargs": {"enable_thinking": true},
       "stream": true,
       "temperature": 1.0,
       "top_k": 20,
       "top_p": 0.95}'
```

Verified recipes for H200, GB300, H800, H100, and B200, plus HiCache (Mooncake L3), reasoning on/off, tool calling, and measured accuracy/speed numbers, are in the [SGLang Ling-3.1-flash cookbook](https://docs.sglang.io/cookbook/autoregressive/InclusionAI/Ling-3.1-flash).

### vLLM
#### Environment Preparation
```bash
pip install uv

uv venv ~/my_ling_env

source ~/my_ling_env/bin/activate

git clone -b vllm https://github.com/vllm-project/vllm.git

cd vllm

VLLM_USE_PRECOMPILED=1 uv pip install --editable . --torch-backend=auto
```

#### Run Inference
**Server**

```bash
vllm serve "$MODEL_PATH" \
    --port "$PORT" \
    --trust-remote-code \
    --served-model-name auto \
    --tensor-parallel-size 8 \
    --gpu-memory-utilization 0.85 \
    --enable-prefix-caching \
    --enable-expert-parallel \
    --mamba-cache-mode align \
    --enable-auto-tool-choice \
    --tool-call-parser ling3 \
    --reasoning-parser ling3 \
    --speculative-config '{"method":"mtp","num_speculative_tokens":3}'
```

**Client**  
It is recommended to use the sampling parameters (`temperature=1.0`, `top_p=0.95`, `top_k=20`) and set `enable_thinking` to `true` for better performance.

```bash
curl -s http://${MASTER_IP}:${PORT}/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "auto", 
       "messages": [{"role": "user", "content": "What is the capital of France?"}],
       "chat_template_kwargs": {"enable_thinking": true},
       "stream": true,
       "temperature": 1.0, 
       "top_k": 20,
       "top_p": 0.95}'
```

<!-- TDS-LINKS:START -->
## Training Content Summary

The public training-content summary identifying **Ling-3.1-flash** is available below. Please refer to the document for its covered model versions, training-content scope, summary version, and update date.

- [Training-content summary (PDF)](https://huggingface.co/inclusionAI/AI-Transparency/resolve/main/Ling-3.1_TDS-Summary.pdf)
- [Training-content documentation index](https://huggingface.co/inclusionAI/AI-Transparency)

This summary concerns training-content disclosure; it does not replace the model’s technical documentation, usage terms, or license.
<!-- TDS-LINKS:END -->
