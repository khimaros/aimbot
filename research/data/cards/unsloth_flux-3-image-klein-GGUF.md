---
base_model:
- black-forest-labs/flux-3-image-klein
base_model_relation: quantized
language:
- en
library_name: gguf
license: other
license_name: flux-kommunity-license
license_link: LICENSE.md
pipeline_tag: image-to-image
tags:
- gguf
- unsloth
- text-to-image
- image-editing
- image-to-image
- flux
- flux-3
- black-forest-labs
widget:
- text: 'Macro photograph of a chunky knitted soft sculpture diorama (UD-Q4_K_XL)'
  output:
    url: samples/UD-Q4_K_XL_knitted.png
---

<div>
  <div style="display: flex; gap: 5px; align-items: center; ">
    <a href="https://github.com/unslothai/unsloth/">
      <img src="https://github.com/unslothai/unsloth/raw/main/images/unsloth%20new%20logo.png" width="133">
    </a>
    <a href="https://discord.gg/unsloth">
      <img src="https://github.com/unslothai/unsloth/raw/main/images/Discord%20button.png" width="173">
    </a>
    <a href="https://docs.unsloth.ai/basics/unsloth-dynamic-2.0-ggufs">
      <img src="https://raw.githubusercontent.com/unslothai/unsloth/refs/heads/main/images/documentation%20green%20button.png" width="143">
    </a>
  </div>
</div>

This is a GGUF quantized version of [FLUX 3 Image Klein](https://huggingface.co/black-forest-labs/flux-3-image-klein) by Black Forest Labs, the 5.6B image transformer (16-step distilled checkpoint) for text to image and image editing. <br>
unsloth/flux-3-image-klein-GGUF uses [Unsloth Dynamic 2.0](https://docs.unsloth.ai/basics/unsloth-dynamic-2.0-ggufs) methodology: the `UD-` files are mixed precision, with every layer's type chosen from a measured sensitivity scan, and they beat the uniform files at the same size.
- Loads in diffusers through `Flux3Transformer2DModel.from_single_file(..., quantization_config=GGUFQuantizationConfig(...))`. Also loads in [Unsloth Desktop](https://github.com/unslothai/unsloth/).
- Tensor names follow the original Black Forest Labs checkpoint layout. The text encoder (Qwen3-VL-4B-Instruct) and the VAE are unchanged; take them from [black-forest-labs/flux-3-image-klein](https://huggingface.co/black-forest-labs/flux-3-image-klein).

**Recommended:** `UD-Q4_K_XL` (3.93 GB) for most GPUs: LPIPS 0.038 against 0.060 for `Q4_K_M`. For output closest to bf16 use `Q8_0`; on small cards use `UD-Q2_K_XL` (2.62 GB).

## Samples

The same prompt, seed and noise through each file:

<img src="samples/compare_church.png" width="800">

<img src="samples/compare_knitted.png" width="800">

## Files and accuracy

LPIPS (alex, lower is better) and SSIM against the bf16 transformer, same prompt, seed, noise and text encoder, 16 steps, over 19 renders: 8 held-out prompts at 1024x1024 plus 11 text-to-image and editing cases (single and multi-reference). A repeated bf16 render scores 0, so the numbers measure only the quantization.

| File | Size | Bits per weight | LPIPS vs bf16 (mean) | LPIPS vs bf16 (max) | SSIM vs bf16 |
|---|---|---|---|---|---|
| `flux-3-image-klein-UD-Q2_K_XL.gguf` | 2.62 GB | 3.78 | 0.152 | 0.317 | 0.800 |
| `flux-3-image-klein-Q3_K_M.gguf` | 3.01 GB | 4.34 | 0.126 | 0.268 | 0.827 |
| `flux-3-image-klein-UD-Q3_K_XL.gguf` | 3.28 GB | 4.73 | 0.087 | 0.266 | 0.879 |
| `flux-3-image-klein-Q4_K_M.gguf` | 3.67 GB | 5.29 | 0.060 | 0.233 | 0.910 |
| `flux-3-image-klein-UD-Q4_K_XL.gguf` | 3.93 GB | 5.67 | 0.038 | 0.139 | 0.940 |
| `flux-3-image-klein-Q5_K_M.gguf` | 4.22 GB | 6.08 | 0.032 | 0.144 | 0.951 |
| `flux-3-image-klein-UD-Q5_K_XL.gguf` | 4.48 GB | 6.46 | 0.020 | 0.083 | 0.966 |
| `flux-3-image-klein-Q6_K.gguf` | 4.80 GB | 6.92 | 0.017 | 0.057 | 0.970 |
| `flux-3-image-klein-Q8_0.gguf` | 6.09 GB | 8.78 | 0.006 | 0.034 | 0.989 |
| `flux-3-image-klein-BF16.gguf` | 11.10 GB | 16.0 | 0.000 | 0.000 | 1.000 |

---

# FLUX 3 Image Klein

![Launch gallery](https://huggingface.co/black-forest-labs/flux-3-image-klein/resolve/main/launch-gallery.jpg)

![Teaser](https://huggingface.co/black-forest-labs/flux-3-image-klein/resolve/main/teaser.jpg)

FLUX 3 Image Klein is a 5.6B open weights model for text-to-image generation and image editing. It takes a prompt and up to 10 reference images and returns one image. Text-to-image, single-reference edits and multi-reference compositions run through the same model, with Qwen3-VL-4B-Instruct as the text encoder.

The 5.6B parameter label refers to the image transformer; the text encoder is separate.

This repository holds the distilled checkpoint for generation and image editing. For fine-tuning, LoRA training and research, use [FLUX 3 Image Klein Base](https://huggingface.co/black-forest-labs/flux-3-image-klein-base).

Inference code, prompt upsampling and the bounding box format: [black-forest-labs/flux-3-image-klein](https://github.com/black-forest-labs/flux-3-image-klein) on GitHub.

This repository includes the BF16 transformer and [FP8](https://huggingface.co/black-forest-labs/flux-3-image-klein/tree/main/variants/fp8r) and [NVFP4](https://huggingface.co/black-forest-labs/flux-3-image-klein/tree/main/variants/nvfp4) variants, together with the Qwen3-VL-4B-Instruct text encoder and image autoencoder.

| Checkpoint | Format | Steps | Guidance | Built for |
| --- | --- | --- | --- | --- |
| [Klein Base](https://huggingface.co/black-forest-labs/flux-3-image-klein-base) | undistilled, bfloat16 | 50 | 3.5 | fine-tuning, LoRA training, research |
| [Klein](https://huggingface.co/black-forest-labs/flux-3-image-klein) | distilled, bfloat16 | 16 | none | generation and editing, self-hosting; the checkpoint behind the BFL API |

## Key Features

1. Text-to-image, single-reference editing and multi-reference generation in one model.
2. Bounding boxes in the prompt. Place elements with boxes on a 0 to 1000 grid, then recolor, move, replace or remove them through the prompt. Boxes guide placement and scale; they do not constrain pixels to a hard mask.
3. Text rendering within generated images.
4. Released under the [FLUX Kommunity License](LICENSE.md). The license permits non-commercial use and provides a commercial-output exception for Qualifying Users, subject to its terms. See [License](#license) below.

## Download

Download the root BF16 distilled package, including its text encoder and image autoencoder, without downloading the quantized variants:

```python
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="black-forest-labs/flux-3-image-klein",
    local_dir="weights/flux-3-image-klein",
    allow_patterns=[
        "model.safetensors", "config.json", "manifest.json",
        "ae.safetensors", "text_encoder/*",
        "README.md", "LICENSE.md", "NOTICE.md",
    ],
)
```

To download a quantized distilled transformer instead, replace the three root transformer patterns (`model.safetensors`, `config.json`, and `manifest.json`) with `variants/fp8r/*` or `variants/nvfp4/*`. Keep `ae.safetensors` and `text_encoder/*` for the other components.

These files contain the model package, not a complete inference application. Use an inference implementation that supports flow-map sampling and this checkpoint format. Quantized packages need a loader that supports their format; their file size is not a measure of total GPU memory use.

## Using with reference code

The distilled checkpoint is served on the [BFL API](https://bfl.ai) as FLUX 3 Image Klein. The reference inference code is [black-forest-labs/flux-3-image-klein](https://github.com/black-forest-labs/flux-3-image-klein).

From the reference implementation checkout, install the package and download the two components the CLI loads besides this checkpoint. The CLI reads its weights from `weights/` (set `WEIGHTS_DIR` for another root), where the download above puts this repository.

```bash
pip install -e .

# safety classifier, always loaded
hf download Falconsai/nsfw_image_detection --local-dir weights/nsfw-classifier
# prompt upsampler (18.8 GB), rewrites the prompt first; skip it and add --no-pup to send prompts as typed
hf download black-forest-labs/flux-3-image-klein-pup --local-dir weights/pup

# text-to-image
python scripts/cli.py "A wide-angle photograph of a lone American bison in a misty geothermal landscape, half hidden by white steam, a slate-blue stream and evergreens fading into the mist behind. Muted, cool palette, soft overcast light." \
  --model distilled --out bison.png

# image editing; repeat --image for multiple references
python scripts/cli.py "The same lone American bison in the same misty geothermal landscape, now at night under a full moon: the steam lit from behind, cool blue light, deep shadows, stars above the evergreens." \
  --model distilled --image bison.png --out bison_night.png
```

## Using with Diffusers

FLUX 3 Image Klein uses a modular pipeline. Pass `prompt` for text-to-image generation, or pass `image` with a prompt for editing. `image` can be one image or a list of reference images.

```shell
pip install git+https://github.com/huggingface/diffusers.git
```

```python
import torch
from diffusers import ModularPipeline

pipe = ModularPipeline.from_pretrained("black-forest-labs/flux-3-image-klein")
pipe.load_components(dtype=torch.bfloat16)
pipe.to("cuda")

image = pipe(
    prompt="A wide-angle photograph of a lone American bison in a misty geothermal landscape, half hidden by white steam, a slate-blue stream and evergreens fading into the mist behind. Muted, cool palette, soft overcast light.",
    generator=torch.Generator().manual_seed(0),
    output="images",
)[0]
image.save("bison.png")

night = pipe(
    prompt="The same lone American bison in the same misty geothermal landscape, now at night under a full moon: the steam lit from behind, cool blue light, deep shadows, stars above the evergreens.",
    image=image,
    generator=torch.Generator().manual_seed(0),
    output="images",
)[0]
night.save("bison_night.png")
```

### Prompt upsampling

The reference CLI runs a prompt upsampler before every generation: it turns a short request, together with the reference images when editing, into the full scene caption the model wants. With Diffusers it is a separate model, [black-forest-labs/flux-3-image-klein-pup](https://huggingface.co/black-forest-labs/flux-3-image-klein-pup). Run it with Transformers and pass its output to the pipeline above as `prompt`:

```python
import json

from huggingface_hub import hf_hub_download
from transformers import AutoProcessor, Qwen3_5ForConditionalGeneration

pup_id = "black-forest-labs/flux-3-image-klein-pup"
processor = AutoProcessor.from_pretrained(pup_id)
upsampler = Qwen3_5ForConditionalGeneration.from_pretrained(pup_id, dtype=torch.bfloat16, device_map="auto").eval()
system_prompts = json.load(open(hf_hub_download(pup_id, "system_prompts.json")))


def upsample(prompt, images=()):
    if images:
        text = (
            "Reference images follow in order (the first image, the second image, ...).\n"
            f"User request: {prompt}\nOutput the caption."
        )
        content = [{"type": "image", "image": image} for image in images] + [{"type": "text", "text": text}]
        messages = [{"role": "system", "content": system_prompts["i2i"]}, {"role": "user", "content": content}]
    else:
        messages = [{"role": "system", "content": system_prompts["t2i"]}, {"role": "user", "content": prompt}]
    inputs = processor.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=True, return_dict=True, return_tensors="pt", enable_thinking=False
    ).to(upsampler.device)
    with torch.no_grad():
        output = upsampler.generate(**inputs, max_new_tokens=3584, do_sample=False)
    return processor.decode(output[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()


image = pipe(prompt=upsample("A bison in a misty geothermal landscape"), output="images")[0]
```

For an edit, pass the same reference images to both: `pipe(prompt=upsample(instruction, [image]), image=image, ...)`. The upsampler also writes the layout captions from a list of boxes; see its model card.

## Prompting
The caption controls composition; reference images anchor content, they do not lock structure.
- Write full scene captions: framing, subject, background, lighting. A short prompt gives generic output, and a one-line edit instruction ("make it blue") reframes the shot. The [prompt upsampler](#prompt-upsampling) writes the caption from a short request.
- For edits, describe the target image as a complete caption of the reference with the edit folded in, or let the [prompt upsampler](#prompt-upsampling) write it from the instruction and the references. For style, describe the attributes (palette, stroke, texture) rather than naming an artwork.
- For layout, append a JSON list of elements to the caption. Each box is `[top, left, bottom, right]` on a 0 to 1000 grid; tag the element in the caption with `<id>`:
```text
Minimalist graphic illustration featuring a black silhouette of a person <silhouette_1> centered against a solid, vibrant chartreuse background <background_1>. The figure is captured in a dynamic, mid-stride running pose, facing toward the left side of the frame. [{"id": "background_1", "bbox": [0, 0, 1000, 1000], "desc": "A flat field of neon yellow-green with a subtle paper texture and fine, organic grain."}, {"id": "silhouette_1", "bbox": [150, 150, 850, 850], "desc": "A black silhouette of a person in motion, made of dense stippled ink."}]
```
For edits by box, refer to the n-th reference as `<ref_image_n>` and give each element `from`, `src_bbox` and `tgt_bbox`; a `null` target removes it. The full format with worked examples: [Bounding boxes](https://docs.bfl.ai/flux_3/flux3_image_bounding_boxes).


## Limitations

- This model is not intended or able to provide factual information.
- While the model can output text, text rendered may be inaccurate or subject to distortion.
- As a statistical model, this checkpoint may represent or amplify biases observed in the training data.
- The model may fail to generate output that matches the prompts.
- Prompt following is heavily influenced by the prompting style. Short prompts produce generic output.
- Boxes set placement and scale, not a hard mask: an element can extend past its box, and small requested elements may not appear. Edits can change content outside the requested region.

## Hardware

Peak GPU memory with the [reference code](https://github.com/black-forest-labs/flux-3-image-klein), B200, 1024x1024, prompt upsampler off: 31 GB in BF16, 26 GB in FP8, 25 GB in NVFP4. The prompt upsampler adds about 28 GB on an 80 GB GPU.

## Out-of-scope use

See Section 4 of the [FLUX Kommunity License](LICENSE.md) for the full restrictions. They include military purposes; surveillance, including related research and development; biometric processing; unlawful, unsafe, fraudulent, defamatory, or abusive activity; generating unlawful content, including child sexual abuse material or non-consensual intimate images; violating third-party rights, including rights of publicity or digital replica rights; and using the model, its Derivatives, or its Outputs to improve another AI model that performs a function similar to a FLUX Model or Derivative.

The license also covers export controls and sanctions. Its commercial-use exception is not blanket permission for commercial fine-tuning or distribution. Consult the full license for the terms that apply to each use.

Nothing contained in this model card should be interpreted as or deemed a restriction or modification to the license the model is released under.

## Responsible AI Development

Black Forest Labs is committed to responsible model development and deployment. Prior to releasing FLUX 3 Image Klein, we evaluated and mitigated a number of risks, including child sexual abuse material (CSAM) and nonconsensual intimate imagery (NCII). For detailed information about our mitigations, evaluation processes, content provenance features, and policies, please see our post: [Capable, Open, and Safe: Combating AI Misuse](https://bfl.ai/blog/capable-open-and-safe-combating-ai-misuse). 
To report safety concerns, contact [safety@blackforestlabs.ai](mailto:safety@blackforestlabs.ai).

## License

This model is released under the [FLUX Kommunity License v.1.0](LICENSE.md): non-commercial use, plus commercial output generation by Qualifying Users with less than US$5M in gross annualized revenue, including affiliates, subject to the license terms. For other uses, see [commercial licensing](https://bfl.ai/licensing).

The Qwen3-VL-4B-Instruct text encoder is under [Apache-2.0](https://huggingface.co/black-forest-labs/flux-3-image-klein/blob/main/text_encoder/LICENSE).

## Trademarks and IP

Use of Black Forest Labs and FLUX trademarks requires prior written permission, except for required attribution or necessary descriptive references. Use must not cause confusion or imply sponsorship or endorsement. Third-party trademarks remain subject to their owners' policies.

## Citation

If you use FLUX 3 Image in your work, please cite:

```bibtex
@misc{bfl2026flux3image,
  author       = {{Black Forest Labs}},
  title        = {{FLUX} 3 Image Klein},
  year         = {2026},
  url          = {https://bfl.ai/blog/flux-3-image-klein},
}