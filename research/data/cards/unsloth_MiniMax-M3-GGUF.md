---
pipeline_tag: image-text-to-text
license: other
license_name: minimax-community
license_link: https://huggingface.co/MiniMaxAI/MiniMax-M3/blob/main/LICENSE
library_name: transformers
tags:
- multimodal
- moe
- agent
- coding
- video
- minimax_m3_vl
base_model:
- MiniMaxAI/MiniMax-M3
---
# Read our How to [Run MiniMax M3 Guide!](https://unsloth.ai/docs/models/minimax-m3)
<div>
  <p style="margin: 0 0 0px 0; margin-top: 0px;">
    <em>See <a href="https://unsloth.ai/docs/basics/unsloth-dynamic-v2.0-gguf">Unsloth Dynamic 2.0 GGUFs</a> for our quantization benchmarks.</em>
  </p>
  <div style="display: flex; gap: 5px; align-items: center; margin-bottom: 0px;">
    <a href="https://github.com/unslothai/unsloth/">
      <img src="https://github.com/unslothai/unsloth/raw/main/images/unsloth%20new%20logo.png" width="133">
    </a>
    <a href="https://discord.gg/unsloth">
      <img src="https://github.com/unslothai/unsloth/raw/main/images/Discord%20button.png" width="173">
    </a>
    <a href="https://unsloth.ai/docs/models/minimax-m3">
      <img src="https://raw.githubusercontent.com/unslothai/unsloth/refs/heads/main/images/documentation%20green%20button.png" width="143">
    </a>
  </div>

  <ul style="margin: 0;">
    <li>EXPERIMENTAL GGUF / support for MiniMax-M3</li>
    <li><b>Jun 12 Update:</b> You can now run MiniMax M3 in Unsloth Studio. See our <a href="https://unsloth.ai/docs/models/minimax-m3#unsloth-studio-guide">Guide</a>.</li>
    <li>Example of MiniMax M3 (5-bit GGUF) running in Unsloth Studio:</li>
  </ul>
</div>
<img width="600" alt="minimax m3 in unsloth studio" src="https://cdn-uploads.huggingface.co/production/uploads/62ecdc18b72a69615d6bd857/4ZRsRdcz9YsSkNDisoxfO.gif" />

<div style="margin: 0;">
<b>EXPERIMENTAL GGUF / support for MiniMax-M3 in llama.cpp:</b>
</div>
</div>

MiniMax-M3 support in llama.cpp is preliminary and not yet in a released build. To run these GGUFs, build llama.cpp from [PR #24523](https://github.com/ggml-org/llama.cpp/pull/24523):

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
git fetch origin pull/24523/head:minimax-m3
git checkout minimax-m3
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release -j --target llama-cli llama-server
```

Then run a quant. The model is large (~428B params), so offload across GPUs with `-ngl 99` or keep the weights in CPU RAM:

```bash
./build/bin/llama-cli -hf unsloth/MiniMax-M3-GGUF:UD-IQ1_M
```

Note: MiniMax Sparse Attention is not supported yet, so inference falls back to dense attention.

---

# MiniMax-M3

**Highlights:**
- **Native Multimodality:** M3 undergoes mixed-modality training from the very first step, enabling deeper semantic fusion across text, image, and video.
- **Context Scaling via Sparse Attention:** M3 introduces MiniMax Sparse Attention (MSA) to improve long context efficiency. M3 delivers 9× prefill and 15× decode speedups compared to M2 at 1M context, reducing per-token compute to 1/20.
- **Coding & Cowork Capability:** M3 achieves frontier-level performance across long-horizon agentic benchmarks, excelling in both coding and cowork.

## Model Details
| | |
| --- | --- |
| Architecture | MoE + MSA (MiniMax Sparse Attention) |
| Total Parameters | ~428B |
| Activated Parameters | ~23B |
| Experts | 128 (4 active per token) |
| Layers | 60 |
| Context Length | 1M tokens |
| Modalities | Text, Image, Video |
| Precision | bfloat16 |
| Transformers | ≥ 4.52.4 (`trust_remote_code=True`) |
| License | [MiniMax Community License](LICENSE) |

## How to Use

- [MiniMax Agent](https://agent.minimax.io/)
- [MiniMax API](https://platform.minimax.io/)

M3 supports two reasoning modes:
- **thinking** — for complex reasoning, agentic tasks, and long-horizon collaboration.
- **non-thinking** — for latency-sensitive scenarios such as chat and code completion.

## Local Deployment

Download the model:

```bash
hf download MiniMaxAI/MiniMax-M3 --local-dir MiniMax-M3
```

You can also get model weights from [ModelScope](https://modelscope.cn/models/MiniMax/MiniMax-M3).

### Inference Parameters

We recommend the following parameters for best performance: `temperature=1.0`, `top_p=0.95`, `top_k=40`. Default system prompt:

```
You are a helpful assistant. Your name is MiniMax-M3 and was built by MiniMax.
```