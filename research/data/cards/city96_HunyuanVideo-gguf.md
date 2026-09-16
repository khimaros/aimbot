---
base_model: tencent/HunyuanVideo
library_name: gguf
quantized_by: city96
tags:
- text-to-video
license: other
license_name: tencent-hunyuan-community
license_link: LICENSE.md
---
This is a direct GGUF conversion of [tencent/HunyuanVideo](https://huggingface.co/tencent/HunyuanVideo)

**It is intended to be used with the native, built-in ComfyUI HunyuanVideo nodes**

As this is a quantized model not a finetune, all the same restrictions/original license terms still apply.

The model files can be used with the [ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF) custom node.

Place model files in `ComfyUI/models/unet` - see the GitHub readme for further install instructions.

The VAE can be downloaded from [this repository by Kijai](https://huggingface.co/Kijai/HunyuanVideo_comfy/blob/main/hunyuan_video_vae_bf16.safetensors)

Please refer to [this chart](https://github.com/ggerganov/llama.cpp/blob/master/examples/perplexity/README.md#llama-3-8b-scoreboard) for a basic overview of quantization types.
