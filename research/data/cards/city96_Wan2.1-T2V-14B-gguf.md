---
base_model: Wan-AI/Wan2.1-T2V-14B
library_name: gguf
quantized_by: city96
tags:
- text-to-video
license: apache-2.0
---
This is a direct GGUF conversion of [Wan-AI/Wan2.1-T2V-14B](https://huggingface.co/Wan-AI/Wan2.1-T2V-14B)

All quants are created from the FP32 base file, though I only uploaded FP16 due to it exceeding the 50GB max file limit and gguf-split loading not currently being supported in ComfyUI-GGUF.

The model files can be used with the [ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF) custom node.

Place model files in `ComfyUI/models/unet` - see the GitHub readme for further install instructions.

The VAE can be downloaded from [this repository by Kijai](https://huggingface.co/Kijai/WanVideo_comfy/blob/main/Wan2_1_VAE_bf16.safetensors)

Please refer to [this chart](https://github.com/ggerganov/llama.cpp/blob/master/examples/perplexity/README.md#llama-3-8b-scoreboard) for a basic overview of quantization types.
