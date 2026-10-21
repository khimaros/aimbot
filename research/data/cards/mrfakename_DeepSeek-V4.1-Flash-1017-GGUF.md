---
license: mit
base_model: deepseek-ai/DeepSeek-V4.1-Flash-1017
base_model_relation: quantized
pipeline_tag: image-text-to-text
tags:
- gguf
- llama.cpp
- deepseek
---

# DeepSeek-V4.1-Flash-1017 GGUF

GGUF quants of [deepseek-ai/DeepSeek-V4.1-Flash-1017](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017).

| Folder | Size | Files | Notes |
|---|---|---|---|
| `Q8_0` | 473 GiB | 10 | Q8_0 everywhere except the routed experts, which keep their native MXFP4. Closest to the original weights. |
| `Q4_K_M` | 414 GiB | 10 | The routed experts are already about 4-bit, so this saves less than usual. |
| `Q3_K_M` | 323 GiB | 10 | |
| `Q2_K` | 246 GiB | 10 | Smallest usable size. |

These are plain quants with no imatrix. Each folder holds a split GGUF. Point llama.cpp at the `-00001-of-` file and it loads the rest.

## Running

Mainline llama.cpp doesn't support DeepSeek V4.1 yet. These files were made with the branch from [ggml-org/llama.cpp#28696](https://github.com/ggml-org/llama.cpp/pull/28696) at commit `2076412`, and they need that branch or a build that includes it.

```
git clone https://github.com/vcruz305/llama.cpp && cd llama.cpp
git checkout 2076412598e99127ea2554467b2b7530856895d3
cmake -B build && cmake --build build -j
```

The two engram tables are large and read a few rows per token. Keeping them on the CPU works well, for example `-ot "engram_embd.weight=CPU"`. The PR has a tested command line.

Text only for now. The llama.cpp branch can't convert the vision tower yet.

## Acknowledgements

Huge thanks to Hugging Face for generously sponsoring the compute used for this project 🤗

[x.com/realmrfakename](https://x.com/realmrfakename)
