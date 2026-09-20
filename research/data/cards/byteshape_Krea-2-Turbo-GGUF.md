---
library_name: gguf
license: other
license_name: krea-2-community-license
license_link: https://www.krea.ai/krea-2-licensing
pipeline_tag: text-to-image
base_model:
- krea/Krea-2-Turbo
base_model_relation: quantized
tags:
- krea
- krea-2
- text-to-image
- image-generation
- gguf
- comfyui
- byteshape
---

# Krea-2-Turbo GGUF (ShapeLearn Quantized)

This is a GGUF-quantized version of the **Krea-2-Turbo** diffusion transformer, produced with **ByteShape's ShapeLearn**, which learns the optimal datatype per tensor to maintain high quality even at very low bitlengths.

Five sizes are available, from **14.31 GB (8.93 bpw)** down to **6.26 GB (3.91 bpw)**. All variants generate high-quality images.

These files run in **[ComfyUI](https://github.com/Comfy-Org/ComfyUI)** via the [ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF) extension.

Krea-2-Turbo is **step-distilled**: 8 steps, no classifier-free guidance. A 1024 x 1024 image takes about **6 seconds** on an RTX 5090. See [Sampling Parameters](#sampling-parameters) before you run anything, because these settings differ sharply from a normal diffusion model.

> Looking for more speed? We also publish a **vLLM-Omni** build of the same model with optimized Humming kernels, about **1.6x faster** per step. See [byteshape/Krea-2-Turbo-Humming](https://huggingface.co/byteshape/Krea-2-Turbo-Humming).

If you have questions or want to share feedback, reach us on [Reddit](https://www.reddit.com/r/ByteShape/).

## A Note on Speed

Unlike the decoding stage of an LLM, diffusion inference is **not** heavily constrained by memory bandwidth. Compressing the model therefore does not necessarily make image generation faster. Quantization here buys you **VRAM headroom**, not throughput. Backend optimization is what moves the needle.

GGUF supports the widest range of platforms and hardware, but the current backend kernels are not highly optimized for these layers. Measured on an NVIDIA RTX 5090 at 1024 x 1024, 8 steps, everything resident on the GPU:

| Backend | Time per step (RTX 5090) | Time for 8 steps | End-to-end |
|---|---|---|---|
| **GGUF** (this repo) | \~0.67 s | \~5.4 s | \~5.9 s |
| [vLLM-Omni](https://huggingface.co/byteshape/Krea-2-Turbo-Humming) | \~0.41 s | \~3.3 s | \~4.0 s |

Both rows are the same ByteShape recipe (the 4.93 bpw GGUF and the 5.06 bpw Humming transformer) with a BF16 text encoder.

Speed is nearly flat across bit-widths: the dequantization kernels, not the weight bytes, set the pace. Pick a size by VRAM.

## What Do the Sizes Look Like?

![One prompt rendered by BF16 and all five GGUF sizes, with a matching close-up crop of the dot-matrix board under each variant](img/collage.jpg)

Judge for yourself: the [blog post](https://byteshape.com/blogs/Krea-2-Turbo/) walks through the full set, and the [interactive comparison explorer](https://byteshape.com/blogs/Krea-2-Turbo/comparison/) lets you A/B any two variants across 24 curated prompts at full resolution, with a slider, zoom, and a curator note for each prompt. If you read the outputs differently, tell us on [Reddit](https://www.reddit.com/r/ByteShape/).

## Available Models

The sizes below are for the **diffusion model only**. In ComfyUI you also load a text encoder (\~5.2 GB with the fp8 encoder) and the VAE (\~0.25 GB). ComfyUI offloads whatever does not fit to system RAM, so smaller cards still work; they just run slower.

| Model ID | Bits/Weight | Model Size | Download |
|---|---|---|---|
| GGUF-1 | 3.91 | 6.26 GB | [Krea-2-Turbo-Q3_K_M-3.91bpw.gguf](https://huggingface.co/byteshape/Krea-2-Turbo-GGUF/blob/main/Krea-2-Turbo-Q3_K_M-3.91bpw.gguf) |
| GGUF-2 | 4.27 | 6.84 GB | [Krea-2-Turbo-Q4_K_S-4.27bpw.gguf](https://huggingface.co/byteshape/Krea-2-Turbo-GGUF/blob/main/Krea-2-Turbo-Q4_K_S-4.27bpw.gguf) |
| GGUF-3 | 4.93 | 7.90 GB | [Krea-2-Turbo-Q4_K_M-4.93bpw.gguf](https://huggingface.co/byteshape/Krea-2-Turbo-GGUF/blob/main/Krea-2-Turbo-Q4_K_M-4.93bpw.gguf) |
| GGUF-4 | 7.29 | 11.69 GB | [Krea-2-Turbo-Q6_K-7.29bpw.gguf](https://huggingface.co/byteshape/Krea-2-Turbo-GGUF/blob/main/Krea-2-Turbo-Q6_K-7.29bpw.gguf) |
| GGUF-5 | 8.93 | 14.31 GB | [Krea-2-Turbo-Q8_0-8.93bpw.gguf](https://huggingface.co/byteshape/Krea-2-Turbo-GGUF/blob/main/Krea-2-Turbo-Q8_0-8.93bpw.gguf) |

The `Qx_K` label names the nearest uniform k-quant tier; these are mixed-precision files, not uniform quants.

**Selection rule:** take the largest model that comfortably fits your VRAM alongside the text encoder. Since compression does not speed up diffusion, there is little reason to go smaller than your card allows.

## Sampling Parameters

Krea-2-Turbo is a **step-distilled** flow-matching model. It needs far fewer steps than a standard diffusion model and it must run **without** classifier-free guidance. Using ordinary Qwen-Image or SDXL settings here produces bad images.

| Parameter | Value | Notes |
|---|---|---|
| Steps | **8** | Krea-2-**Raw** needs ~52; these settings are for Turbo only. |
| CFG / guidance | **off** | ComfyUI `cfg=1.0` · diffusers `guidance_scale=0.0`. The negative branch is never evaluated. |
| Sampler | `euler` | What the workflow in this repo uses. |
| Scheduler | `simple` | Flow-matching model. |
| Flow shift | **1.15** | Applied automatically by ComfyUI; you do not set it by hand. |
| Denoise | 1.0 | |
| Resolution | **2048 x 2048 recommended**, 1024 x 1024 also fine | The model samples visibly nicer images at 2K; see [Resolution](#resolution). A BF16 DiT on a 32 GB card is tight at 2048². |
| Negative prompt | zeroed | The workflow wires `ConditioningZeroOut`; the content is irrelevant at cfg 1.0. |

### Resolution

**Run this model at 2048 x 2048 if you can.** Krea-2-Turbo resolves noticeably more real detail at 2K than at 1K: fur and hair separate into individual strands, bark and foliage keep their texture instead of dissolving into soft blobs, and fine features like whiskers survive. At 1024 x 1024 the same prompt and seed give a good but distinctly softer image. The workflow shipped here is set to 2048 x 2048 for that reason.

Krea's own reference command for the Turbo checkpoint runs at this size too (`--steps 8 --cfg 0.0 --mu 1.15 --width 2048 --height 2048`).

It is not free. 2K is 4x the pixels and costs substantially more time per step, so drop back to 1024 x 1024 while you iterate on prompts, then re-run the keeper at 2K.

## Quick Start (ComfyUI)

### 1. Set up the environment

You need **ComfyUI v0.25 or newer**, which detects Krea 2 natively. Create a Python environment, install ComfyUI, and add the ComfyUI-GGUF extension:

```bash
conda create -y -n comfy python=3.13
conda activate comfy

git clone https://github.com/Comfy-Org/ComfyUI.git
cd ComfyUI
pip install -r requirements.txt

cd custom_nodes
git clone https://github.com/city96/ComfyUI-GGUF
cd ComfyUI-GGUF
pip install -r requirements.txt
```

Return to the root of the ComfyUI repository before downloading the models.

### 2. Download the models

Krea-2-Turbo needs three separate components: the **main diffusion model** (this repo), a **VAE**, and a **text encoder**.

#### Main diffusion model

Pick a quantization from the table above and download it into `models/unet`:

```bash
curl -L -C - -o models/unet/Krea-2-Turbo-Q4_K_M-4.93bpw.gguf \
  https://huggingface.co/byteshape/Krea-2-Turbo-GGUF/resolve/main/Krea-2-Turbo-Q4_K_M-4.93bpw.gguf
```

#### VAE

A small model that decodes images from latent space into pixel space. Krea 2 uses the Qwen-Image VAE:

```bash
curl -L -C - -o models/vae/qwen_image_vae.safetensors \
  https://huggingface.co/Comfy-Org/Krea-2/resolve/main/vae/qwen_image_vae.safetensors
```

#### Text encoder

Krea 2 conditions on **Qwen3-VL-4B**, consuming 12 stacked hidden layers rather than a single output.

We did not quantize the text encoder ourselves: several good packagings already exist and it contributes little to overall inference time. Choose **one** of the following.

**Recommended: fp8 scaled (5.24 GB).** The lighter option, and what the workflow in this repo expects:

```bash
curl -L -C - -o models/text_encoders/qwen3vl_4b_fp8_scaled.safetensors \
  https://huggingface.co/Comfy-Org/Krea-2/resolve/main/text_encoders/qwen3vl_4b_fp8_scaled.safetensors
```

*Alternative (BF16, 8.88 GB)*, a little more fidelity for ~3.6 GB more memory:

```bash
curl -L -C - -o models/text_encoders/qwen3vl_4b_bf16.safetensors \
  https://huggingface.co/Comfy-Org/Krea-2/resolve/main/text_encoders/qwen3vl_4b_bf16.safetensors
```

### 3. Run ComfyUI

From the root of the ComfyUI repository:

```bash
python main.py
```

Once it starts, open a browser and go to **http://127.0.0.1:8188** to reach the ComfyUI interface. If ComfyUI runs on a different machine, use that machine's address instead of `127.0.0.1`.

### 4. Load the example workflow

**Use the workflow shipped in this repo: [`krea2-turbo-gguf-workflow.json`](krea2-turbo-gguf-workflow.json).** Drag it onto the ComfyUI canvas, pick your `.gguf` in the **Unet Loader (GGUF)** node, and hit Run. Ten nodes, no subgraph, nothing else to download.

It is exactly the documented configuration: `UnetLoaderGGUF`, `CLIPLoader` with `type=krea2` and your Qwen3-VL-4B encoder, `VAELoader` with `qwen_image_vae.safetensors`, `EmptyLatentImage` at **2048 x 2048**, the negative branch through `ConditioningZeroOut`, and a `KSampler` at **8 steps, cfg 1.0, euler, simple, denoise 1.0**.

It ships at 2K because that is where this model looks best; see [Resolution](#resolution). Lower the `EmptyLatentImage` to 1024 x 1024 if you want faster iterations.

### A note on the architecture tag

These GGUFs carry `general.architecture=qwen_image` **deliberately**. Stock ComfyUI-GGUF has no `krea2` entry in its allowlist, while ComfyUI core detects Krea 2 from the tensor names regardless. Changing the tag would break loading, not fix it.

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `unet_name` / `lora_name_1` "not available", or a "Missing Models" prompt | Load [`krea2-turbo-gguf-workflow.json`](krea2-turbo-gguf-workflow.json) instead of ComfyUI's built-in Krea 2 template. |
| Loader rejects the file / unknown architecture | ComfyUI-GGUF is missing or out of date, or ComfyUI is older than v0.25. Both are required for Krea 2. |
| Washed-out, over-smoothed, or scrambled images | CFG is on. Set `cfg=1.0` in the KSampler. |
| Blurry, unfinished-looking images | Too few steps, or Raw settings applied to Turbo. Use 8 steps with the `simple` scheduler. |
| Out of memory | Pick a smaller bit-width or use the fp8 text encoder. ComfyUI offloads to system RAM automatically. |

## License

Krea 2 Community License. Read it at [krea.ai/krea-2-licensing](https://www.krea.ai/krea-2-licensing) ([PDF](https://cdn.jsdelivr.net/gh/krea-ai/krea-2@db3984fbc6e13b34c0064990fc2d95ac64d00058/assets/hf_samples/LICENSE.pdf)), also bundled here as `LICENSE.pdf`. Use is additionally subject to Krea's [Acceptable Use Policy](https://www.krea.ai/krea-2-use-policy). Quantized weights inherit the base model's terms.

These weights are a **quantized** version of [krea/Krea-2-Turbo](https://huggingface.co/krea/Krea-2-Turbo), modified by quantizing the diffusion transformer with ByteShape's ShapeLearn. They are not an official Krea product and are not endorsed by Krea.

> Krea 2 is licensed under the Krea 2 Community License Agreement. For more information, visit https://krea.ai/krea-2-licensing.
