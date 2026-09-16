---
base_model: stabilityai/stable-diffusion-3.5-large
library_name: gguf
quantized_by: city96
tags:
- text-to-image
- image-generation
- stable-diffusion
language:
- en
license: other
license_name: stabilityai-ai-community
license_link: LICENSE.md
---

This is a direct GGUF conversion of [stabilityai/stable-diffusion-3.5-large](https://huggingface.co/stabilityai/stable-diffusion-3.5-large/tree/main)

As this is a quantized model not a finetune, all the same restrictions/original license terms still apply.

The model files can be used with the [ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF) custom node.

Place model files in `ComfyUI/models/unet` - see the GitHub readme for further install instructions.

Please refer to [this chart](https://github.com/ggerganov/llama.cpp/blob/master/examples/perplexity/README.md#llama-3-8b-scoreboard) for a basic overview of quantization types.
