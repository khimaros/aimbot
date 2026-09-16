---
base_model: black-forest-labs/FLUX.2-dev
library_name: gguf
quantized_by: city96
license: other
license_name: flux-dev-non-commercial-license
license_link: LICENSE.md
tags:
- image-generation
- image-editing
- flux
- diffusion-single-file
pipeline_tag: image-to-image
---

This is a direct GGUF conversion of [black-forest-labs/FLUX.2-dev](https://huggingface.co/black-forest-labs/FLUX.2-dev).

The model files can be used in [ComfyUI](https://github.com/comfyanonymous/ComfyUI/) with the [ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF) custom node. Place the required model(s) in the following folders:

| Type         | Name                                | Location                          | Download         |
| ------------ | ----------------------------------- | --------------------------------- | ---------------- |
| Main Model   | flux2-dev                           | `ComfyUI/models/diffusion_models` | GGUF (this repo) |
| Text Encoder | Mistral-Small-3.2-24B-Instruct-2506 | `ComfyUI/models/text_encoders`    | [Safetensors](https://huggingface.co/Comfy-Org/flux2-dev/tree/main/split_files/text_encoders) / [GGUF](https://huggingface.co/unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF/tree/main) |
| VAE          | flux2 VAE                           | `ComfyUI/models/vae`              | [Safetensors](https://huggingface.co/Comfy-Org/flux2-dev/blob/main/split_files/vae/flux2-vae.safetensors) |

[**Example outputs**](media/flux2dev-image.jpg) - sample size of 1, not strictly representative

![sample](media/flux2dev-image.jpg)

### Notes

> [!NOTE]
> As with Qwen-Image, Q5_K_M, Q4_K_M, Q3_K_M, Q3_K_S and Q2_K have some extra logic as to which blocks to keep in high precision.
> 
> The logic is partially based on guesswork, trial & error, and the graph found in the readme for [Freepik/flux.1-lite-8B](https://huggingface.co/Freepik/flux.1-lite-8B#motivation) (which in turn quotes [this blog by Ostris](https://ostris.com/2024/09/07/skipping-flux-1-dev-blocks/))

*As this is a quantized model not a finetune, all the same restrictions/original license terms still apply.*
