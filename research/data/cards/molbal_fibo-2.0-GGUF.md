---
license: cc-by-nc-4.0
base_model:
  - briaai/Fibo-2.0-dev
  - briaai/Fibo-2.0-edit-turbo
base_model_relation: quantized
pipeline_tag: text-to-image
tags:
  - gguf
  - comfyui
  - image-to-image
  - image-editing
---

# Fibo 2.0 GGUF

This repository contains GGUF quantizations of Fibo 2.0 Dev and Fibo 2.0 Edit Turbo. The Dev variant supports text-to-image and image editing. Edit Turbo is distilled for four-step image editing and is not intended for text-to-image.

Both variants use the Fibo 2.0 architecture. Dev uses 50 steps and CFG 5 for text-to-image. Edit Turbo uses 4 steps and CFG 1 for image editing.

## Example outputs

### Fibo 2.0 Dev

![Fibo 2.0 Dev text-to-image example](example-output.webp)

### Fibo 2.0 Edit Turbo

![Fibo 2.0 Edit Turbo image-to-image example](example-edit-output.webp)

The edit workflow uses the included `fibo2-test-input.png`. Copy it to `ComfyUI/input/`, or replace it with your own image in the workflow's Load Image node.

## Quantizations

File sizes are shown in GiB. Standard GGUF files use common GGML formats. Q8_CR uses the custom ConvRot layout and requires `comfyui-gguf-reboot`.

| Variant | Quant | Format | Size | File |
| --- | --- | --- | ---: | --- |
| Dev | Q8_0 | Standard GGUF | 8.29 GiB | [fibo2-dev-Q8_0.gguf](https://huggingface.co/molbal/fibo-2.0-GGUF/blob/main/fibo2-dev-Q8_0.gguf) |
| Dev | Q6_K | Standard GGUF | 6.48 GiB | [fibo2-dev-Q6_K.gguf](https://huggingface.co/molbal/fibo-2.0-GGUF/blob/main/fibo2-dev-Q6_K.gguf) |
| Dev | Q4_K_M | Standard GGUF | 5.16 GiB | [fibo2-dev-Q4_K_M.gguf](https://huggingface.co/molbal/fibo-2.0-GGUF/blob/main/fibo2-dev-Q4_K_M.gguf) |
| Dev | Q8_CR | Proprietary, `comfyui-gguf-reboot` | 7.83 GiB | [fibo2-dev_Q8_CR.gguf](https://huggingface.co/molbal/fibo-2.0-GGUF/blob/main/fibo2-dev_Q8_CR.gguf) |
| Edit Turbo | Q8_0 | Standard GGUF | 8.29 GiB | [fibo2-edit-turbo-Q8_0.gguf](https://huggingface.co/molbal/fibo-2.0-GGUF/blob/main/fibo2-edit-turbo-Q8_0.gguf) |
| Edit Turbo | Q6_K | Standard GGUF | 6.48 GiB | [fibo2-edit-turbo-Q6_K.gguf](https://huggingface.co/molbal/fibo-2.0-GGUF/blob/main/fibo2-edit-turbo-Q6_K.gguf) |
| Edit Turbo | Q4_K_M | Standard GGUF | 5.16 GiB | [fibo2-edit-turbo-Q4_K_M.gguf](https://huggingface.co/molbal/fibo-2.0-GGUF/blob/main/fibo2-edit-turbo-Q4_K_M.gguf) |
| Edit Turbo | Q8_CR | Proprietary, `comfyui-gguf-reboot` | 7.83 GiB | [fibo2-edit-turbo_Q8_CR.gguf](https://huggingface.co/molbal/fibo-2.0-GGUF/blob/main/fibo2-edit-turbo_Q8_CR.gguf) |

## ComfyUI setup

Fibo2 requires ComfyUI core commit [`87ed5a066d9c4660ef42100fd01a888da6994856`](https://github.com/comfyanonymous/ComfyUI/commit/87ed5a066d9c4660ef42100fd01a888da6994856) or newer, plus [comfyui-gguf-reboot](https://registry.comfy.org/publishers/molbal/nodes/comfyui-gguf-reboot). Load the GGUF with `UnetLoaderGGUFDynamicVRAM` from `models/diffusion_models/`.

Download the [Qwen3-VL 4B Int8 ConvRot text encoder](https://huggingface.co/Comfy-Org/Fibo-2.0/resolve/main/text_encoders/qwen3vl_4b_int8_convrot.safetensors) and place it at `ComfyUI/models/text_encoders/qwen3vl_4b_int8_convrot.safetensors`.

Download the [FLUX.2 VAE](https://huggingface.co/Comfy-Org/Fibo-2.0/resolve/main/vae/flux2-vae.safetensors) and save it as `ComfyUI/models/vae/fibo2-flux2-vae.safetensors` so it does not replace another FLUX.2 VAE.

### Workflows

- [Dev text-to-image workflow](workflows/fibo2-dev-t2i-gguf.json)
- [Edit Turbo image-to-image workflow](workflows/fibo2-edit-turbo-gguf.json)

## License and attribution

Fibo 2.0 Dev and Edit Turbo are released under CC BY-NC 4.0. Commercial use requires a separate agreement with Bria. See the [Dev model card](https://huggingface.co/briaai/Fibo-2.0-dev) and [Edit Turbo model card](https://huggingface.co/briaai/Fibo-2.0-edit-turbo) for the complete terms and model details.
