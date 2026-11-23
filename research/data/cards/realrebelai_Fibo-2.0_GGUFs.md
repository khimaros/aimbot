---
language:
  - en
license: cc-by-nc-4.0
tags:
  - fibo-2.0
  - gguf
  - comfyui
  - image-generation
  - image-editing
  - quantization
  - low-vram
  - rebel-ai
base_model:
  - briaai/Fibo-2.0-dev
  - briaai/Fibo-2.0-edit-turbo
---

<p align="center"> <a href="https://github.com/RealRebelAI"> <img src="https://img.shields.io/badge/GitHub-RealRebelAI-E10600?style=for-the-badge&logo=github&logoColor=E10600&labelColor=0D0D0D" alt="GitHub"> </a> <a href="https://huggingface.co/realrebelai"> <img src="https://img.shields.io/badge/Hugging%20Face-realrebelai-E10600?style=for-the-badge&logo=huggingface&logoColor=E10600&labelColor=0D0D0D" alt="Hugging Face"> </a> <a href="https://www.youtube.com/watch?v=-2wBiPX8eGE"> <img src="https://img.shields.io/badge/YouTube-%40RealRebelAI-E10600?style=for-the-badge&logo=youtube&logoColor=E10600&labelColor=0D0D0D" alt="YouTube"> </a> <a href="https://civitai.com/user/RealRebelAI"> <img src="https://img.shields.io/badge/Civitai-RealRebelAI-E10600?style=for-the-badge&logo=civitai&logoColor=E10600&labelColor=0D0D0D" alt="Civitai"> </a> <a href="https://x.com/realrebelai"> <img src="https://img.shields.io/badge/X-%40realrebelai-E10600?style=for-the-badge&logo=x&logoColor=E10600&labelColor=0D0D0D" alt="X"> </a> </p> 



# Fibo 2.0 GGUFs — Rebel AI

<div class="gallery-scroll" style="display:flex; overflow-x:auto; gap:12px; padding:12px 0; scroll-snap-type:x mandatory; -webkit-overflow-scrolling:touch;">

 <div class="gallery-item" style="flex:0 0 auto; scroll-snap-align:start; width:320px;">
    <img src="https://cdn-uploads.huggingface.co/production/uploads/68761990332d15464ccc8dee/HZbqT2GfIkugHKkpyn7sy.png" alt="example 0" style="width:320px; height:320px; object-fit:cover; border-radius:8px;">
  </div>

<div class="gallery-item" style="flex:0 0 auto; scroll-snap-align:start; width:320px;">
    <img src="https://cdn-uploads.huggingface.co/production/uploads/68761990332d15464ccc8dee/ekv9nHRmPOrbzTXpt0g5o.png" alt="example 0" style="width:320px; height:320px; object-fit:cover; border-radius:8px;">
  </div>

  <div class="gallery-item" style="flex:0 0 auto; scroll-snap-align:start; width:320px;">
    <img src="https://cdn-uploads.huggingface.co/production/uploads/68761990332d15464ccc8dee/EQoZRFvjPHLsCbuMp0VhN.png" alt="example 0" style="width:320px; height:320px; object-fit:cover; border-radius:8px;">
  </div>

   <div class="gallery-item" style="flex:0 0 auto; scroll-snap-align:start; width:320px;">
    <img src="https://cdn-uploads.huggingface.co/production/uploads/68761990332d15464ccc8dee/AXkNYTZ7APHkAQ5HaP3S7.png" alt="example 0" style="width:320px; height:320px; object-fit:cover; border-radius:8px;">
  </div>

  <div class="gallery-item" style="flex:0 0 auto; scroll-snap-align:start; width:320px;">
    <img src="https://cdn-uploads.huggingface.co/production/uploads/68761990332d15464ccc8dee/j0tjOP2bUeLD4BURD3J87.png" alt="example 0" style="width:320px; height:320px; object-fit:cover; border-radius:8px;">
  </div>

</div>







**Low-VRAM GGUF conversions of BRIA AI's Fibo 2.0 Dev and Fibo 2.0 Edit Turbo image models, prepared for ComfyUI.**

This repository provides quantized diffusion-model weights. **The text encoder and VAE are separate downloads.** These are community conversions, not official BRIA AI or Comfy-Org releases.

> **License:** The original Fibo 2.0 model weights are licensed under **CC BY-NC 4.0 (non-commercial use only)**. The quantized weights retain the upstream restrictions. Commercial use requires a separate agreement with BRIA AI.

## Model variants

| Model | Intended use | Notes |
|---|---|---|
| **Fibo 2.0 Dev** | Text-to-image generation and image editing | General-purpose checkpoint; typically requires more sampling steps |
| **Fibo 2.0 Edit Turbo** | Fast image editing | Distilled variant optimized for low-step inference |

Download the GGUF file and quantization level you want from the **[Files tab](https://huggingface.co/realrebelai/Fibo-2.0_GGUFs/tree/main)**. Smaller quantizations reduce disk and model-weight memory use, but may affect quality. Actual VRAM usage depends on the encoder, VAE, resolution, offloading, and workflow.

## Requirements

- An up-to-date **[ComfyUI](https://github.com/Comfy-Org/ComfyUI)** installation with native Fibo 2.0 support.
- **[ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF)**, with a loader version compatible with these GGUF files.
- **Qwen3-VL-4B text encoder** (the INT8 ConvRot release is a lower-memory option).
- **FLUX.2 VAE** (`flux2-vae.safetensors`).

**Note:** GGUF loading is dependent on your installed ComfyUI-GGUF version and the Fibo 2.0 model architecture. If a GGUF fails to load, test the equivalent official safetensors model with the same workflow to isolate loader compatibility. A successful GGUF conversion alone does not guarantee runtime compatibility.

## Installation

Put your chosen GGUF into `ComfyUI/models/unet/` (the default ComfyUI-GGUF model folder), or another folder configured for your GGUF loader. Put the encoder and VAE in their standard folders:

```text
ComfyUI/
└── models/
    ├── unet/
    │   └── <your-fibo2-model>.gguf
    ├── text_encoders/
    │   └── qwen3vl_4b_int8_convrot.safetensors
    └── vae/
        └── flux2-vae.safetensors
```

**Download required components** from the official [Comfy-Org/Fibo-2.0](https://huggingface.co/Comfy-Org/Fibo-2.0) repository:

- [Qwen3-VL-4B INT8 ConvRot encoder](https://huggingface.co/Comfy-Org/Fibo-2.0/blob/main/text_encoders/qwen3vl_4b_int8_convrot.safetensors)
- [FLUX.2 VAE](https://huggingface.co/Comfy-Org/Fibo-2.0/blob/main/vae/flux2-vae.safetensors)

For Windows users with the modern Hugging Face `hf` CLI, these commands place the files in the correct directories when run from the `ComfyUI/models` folder:

```bat
hf download Comfy-Org/Fibo-2.0 text_encoders/qwen3vl_4b_int8_convrot.safetensors --local-dir .
hf download Comfy-Org/Fibo-2.0 vae/flux2-vae.safetensors --local-dir .
```

## Using in ComfyUI

1. Open a **Fibo 2.0-compatible** text-to-image or image-edit workflow.
2. Replace the standard diffusion model loader with **Unet Loader (GGUF)** (or the equivalent node from your installed ComfyUI-GGUF version).
3. Select your downloaded Fibo 2.0 GGUF.
4. Load `qwen3vl_4b_int8_convrot.safetensors` using the Fibo 2.0-compatible text encoder configuration, and load `flux2-vae.safetensors` as the VAE.
5. Keep the remaining Fibo-specific conditioning and sampling nodes from the compatible workflow.

**Starting points (not universal presets):**

| Checkpoint | Steps | CFG | Suggested first test |
|---|---:|---:|---|
| Dev | ~30–50 | ~5 | Text-to-image at 1024×1024 |
| Edit Turbo | ~4 | ~1 | Single-image editing |

Results depend on the workflow, sampler, scheduler, and model implementation. Start from a workflow known to work with Fibo 2.0, rather than reusing a FLUX or Qwen workflow unchanged.

For example workflows, see the [Fibo 2.0 ComfyUI workflows](https://comfyui.nomadoor.net/en/basic-workflows/fibo-2/) and the [official Comfy-Org model card](https://huggingface.co/Comfy-Org/Fibo-2.0).

## Quantization approach

The source Dev and Edit Turbo checkpoints share the same audited tensor layout:

- **634 BF16 tensors** per source checkpoint
- **44 main transformer blocks**
- Fused QKV and feed-forward projections in the main transformer
- Separate cross-attention, noise-refiner, and Perceiver components

These conversions use **selective GGUF quantization** of the main transformer matrices. The conversion strategy preserves sensitive auxiliary components—such as adaptive normalization, cross-attention, noise-refiner, Perceiver, embeddings, and output heads—at higher precision to prioritize quality. Quantization settings and file sizes vary by uploaded variant.

**Quality notice:** Quantization is lossy. The original BF16 weights are the reference for fidelity. Verify outputs against the original checkpoint before drawing conclusions about image quality or speed.

## Credits and licensing

- **Original model:** [BRIA AI — Fibo 2.0](https://huggingface.co/briaai)
- **ComfyUI model packaging and required components:** [Comfy-Org/Fibo-2.0](https://huggingface.co/Comfy-Org/Fibo-2.0)
- **GGUF loader:** [city96/ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF)
- **GGUF conversions / repository maintenance:** [Rebel AI (@realrebelai)](https://huggingface.co/realrebelai)

**Original model license:** [Creative Commons Attribution–NonCommercial 4.0 International](https://creativecommons.org/licenses/by-nc/4.0/). Attribution is required; commercial use is not permitted under this license. For commercial licensing, contact [BRIA AI](https://platform.bria.ai/licensing/pricing?model=fibo-2).

---

*Unofficial community quantization project. Not affiliated with or endorsed by BRIA AI or Comfy-Org.*
