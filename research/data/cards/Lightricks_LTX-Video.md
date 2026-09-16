---
tags:
- ltx-video
- image-to-video
pinned: true
language:
- en
license: other
library_name: diffusers
---

# LTX-Video Model Card
This model card focuses on the model associated with the LTX-Video model, codebase available [here](https://github.com/Lightricks/LTX-Video).

LTX-Video is the first DiT-based video generation model capable of generating high-quality videos in real-time. It produces 30 FPS videos at a 1216×704 resolution faster than they can be watched. Trained on a large-scale dataset of diverse videos, the model generates high-resolution videos with realistic and varied content.

<img src="./media/trailer.gif" alt="trailer" width="512">

### Image-to-video examples
| | | |
|:---:|:---:|:---:|
| ![example1](./media/ltx-video_i2v_example_00001.gif) | ![example2](./media/ltx-video_i2v_example_00002.gif) | ![example3](./media/ltx-video_i2v_example_00003.gif) |
| ![example4](./media/ltx-video_i2v_example_00004.gif) | ![example5](./media/ltx-video_i2v_example_00005.gif) |  ![example6](./media/ltx-video_i2v_example_00006.gif) |
| ![example7](./media/ltx-video_i2v_example_00007.gif) |  ![example8](./media/ltx-video_i2v_example_00008.gif) | ![example9](./media/ltx-video_i2v_example_00009.gif) |

# Models & Workflows

| Name                                                                                                                                   | Notes                                                                                                         | inference.py config                                                                                                              | ComfyUI workflow (Recommended)                                                                                                                                |
|----------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ltxv-13b-0.9.8-dev                                                                                                                     | Highest quality, requires more VRAM                                                                           | [ltxv-13b-0.9.8-dev.yaml](https://github.com/Lightricks/LTX-Video/blob/main/configs/ltxv-13b-0.9.8-dev.yaml)                     | [ltxv-13b-i2v-base.json](https://github.com/Lightricks/ComfyUI-LTXVideo/blob/master/example_workflows/ltxv-13b-i2v-base.json)                                 |
| [ltxv-13b-0.9.8-mix](https://app.ltx.studio/motion-workspace?videoModel=ltxv-13b)                                                      | Mix ltxv-13b-dev and ltxv-13b-distilled in the same multi-scale rendering workflow for balanced speed-quality | N/A                                                                                                                              | [ltxv-13b-i2v-mixed-multiscale.json](https://github.com/Lightricks/ComfyUI-LTXVideo/blob/master/example_workflows/ltxv-13b-i2v-mixed-multiscale.json)         |
| [ltxv-13b-0.9.8-distilled](https://app.ltx.studio/motion-workspace?videoModel=ltxv)                                                    | Faster, less VRAM usage, slight quality reduction compared to 13b. Ideal for rapid iterations                 | [ltxv-13b-0.9.8-distilled.yaml](https://github.com/Lightricks/LTX-Video/blob/main/configs/ltxv-13b-0.9.8-dev.yaml)               | [ltxv-13b-dist-i2v-base.json](https://github.com/Lightricks/ComfyUI-LTXVideo/blob/master/example_workflows/13b-distilled/ltxv-13b-dist-i2v-base.json)         |
| ltxv-2b-0.9.8-distilled                                                                                                                | Smaller model, slight quality reduction compared to 13b distilled. Ideal for light VRAM usage                 | [ltxv-2b-0.9.8-distilled.yaml](https://github.com/Lightricks/LTX-Video/blob/main/configs/ltxv-2b-0.9.8-dev.yaml)                 | N/A                                                                                                                                                           |
| ltxv-13b-0.9.8-fp8                                                                                                                     | Quantized version of ltxv-13b                                                                                 | [ltxv-13b-0.9.8-dev-fp8.yaml](https://github.com/Lightricks/LTX-Video/blob/main/configs/ltxv-13b-0.9.8-dev-fp8.yaml)             | [ltxv-13b-i2v-base-fp8.json](https://github.com/Lightricks/ComfyUI-LTXVideo/blob/master/example_workflows/ltxv-13b-i2v-base-fp8.json)                         |
| ltxv-13b-0.9.8-distilled-fp8                                                                                                           | Quantized version of ltxv-13b-distilled                                                                       | [ltxv-13b-0.9.8-distilled-fp8.yaml](https://github.com/Lightricks/LTX-Video/blob/main/configs/ltxv-13b-0.9.8-distilled-fp8.yaml) | [ltxv-13b-dist-i2v-base-fp8.json](https://github.com/Lightricks/ComfyUI-LTXVideo/blob/master/example_workflows/13b-distilled/ltxv-13b-dist-i2v-base-fp8.json) |
| ltxv-2b-0.9.8-distilled-fp8                                                                                                            | Quantized version of ltxv-2b-distilled                                                                        | [ltxv-2b-0.9.8-distilled-fp8.yaml](https://github.com/Lightricks/LTX-Video/blob/main/configs/ltxv-2b-0.9.8-distilled-fp8.yaml)   | N/A                                                                                                                                                           |
| ltxv-2b-0.9.6                                                                                                                          | Good quality, lower VRAM requirement than ltxv-13b                                                            | [ltxv-2b-0.9.6-dev.yaml](https://github.com/Lightricks/LTX-Video/blob/main/configs/ltxv-2b-0.9.6-dev.yaml)                       | [ltxvideo-i2v.json](https://github.com/Lightricks/ComfyUI-LTXVideo/blob/master/example_workflows/low_level/ltxvideo-i2v.json)                                 |
| ltxv-2b-0.9.6-distilled                                                                                                                | 15× faster, real-time capable, fewer steps needed, no STG/CFG required                                        | [ltxv-2b-0.9.6-distilled.yaml](https://github.com/Lightricks/LTX-Video/blob/main/configs/ltxv-2b-0.9.6-distilled.yaml)           | [ltxvideo-i2v-distilled.json](https://github.com/Lightricks/ComfyUI-LTXVideo/blob/master/example_workflows/low_level/ltxvideo-i2v-distilled.json)             |


## Model Details
- **Developed by:** Lightricks
- **Model type:** Diffusion-based image-to-video generation model
- **Language(s):** English


## Usage

### Direct use
You can use the model for purposes under the license:
- 2B version 0.9: [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/ltx-video-2b-v0.9.license.txt)
- 2B version 0.9.1 [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/ltx-video-2b-v0.9.1.license.txt)
- 2B version 0.9.5 [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/ltx-video-2b-v0.9.5.license.txt)
- 2B version 0.9.6-dev [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt)
- 2B version 0.9.6-distilled [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt)
- 13B version 0.9.7-dev [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt)
- 13B version 0.9.7-dev-fp8 [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt)
- 13B version 0.9.7-distilled [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt)
- 13B version 0.9.7-distilled-fp8 [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt)
- 13B version 0.9.7-distilled-lora128 [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt)
- 13B version 0.9.7-ICLoRA Depth [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt)
- 13B version 0.9.7-ICLoRA Pose [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt)
- 13B version 0.9.7-ICLoRA Canny [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt)
- Temporal upscaler version 0.9.7 [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt)
- Spatial upscaler version 0.9.7 [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt)
- 13B version 0.9.8-dev [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt)
- 13B version 0.9.8-dev-fp8 [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt)
- 13B version 0.9.8-distilled [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt)
- 13B version 0.9.8-distilled-fp8 [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt)
- 2B version 0.9.8-distilled [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt)
- 2B version 0.9.8-distilled-fp8 [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt)
- 13B version 0.9.8-ICLoRA detailer [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt)
- Temporal upscaler version 0.9.8 [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt)
- Spatial upscaler version 0.9.8 [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt)

### General tips:
* The model works on resolutions that are divisible by 32 and number of frames that are divisible by 8 + 1 (e.g. 257). In case the resolution or number of frames are not divisible by 32 or 8 + 1, the input will be padded with -1 and then cropped to the desired resolution and number of frames.
* The model works best on resolutions under 720 x 1280 and number of frames below 257.
* Prompts should be in English. The more elaborate the better. Good prompt looks like `The turquoise waves crash against the dark, jagged rocks of the shore, sending white foam spraying into the air. The scene is dominated by the stark contrast between the bright blue water and the dark, almost black rocks. The water is a clear, turquoise color, and the waves are capped with white foam. The rocks are dark and jagged, and they are covered in patches of green moss. The shore is lined with lush green vegetation, including trees and bushes. In the background, there are rolling hills covered in dense forest. The sky is cloudy, and the light is dim.`

### Online demo
The model is accessible right away via the following links:
- [LTX-Studio image-to-video (13B-mix)](https://app.ltx.studio/motion-workspace?videoModel=ltxv-13b)
- [LTX-Studio image-to-video (13B distilled)](https://app.ltx.studio/motion-workspace?videoModel=ltxv)
- [Fal.ai image-to-video (13B full)](https://fal.ai/models/fal-ai/ltx-video-13b-dev/image-to-video)
- [Fal.ai image-to-video (13B distilled)](https://fal.ai/models/fal-ai/ltx-video-13b-distilled/image-to-video)
- [Replicate image-to-video](https://replicate.com/lightricks/ltx-video)

### ComfyUI
To use our model with ComfyUI, please follow the instructions at a dedicated [ComfyUI repo](https://github.com/Lightricks/ComfyUI-LTXVideo/).

### Run locally

#### Installation

The codebase was tested with Python 3.10.5, CUDA version 12.2, and supports PyTorch >= 2.1.2.

```bash
git clone https://github.com/Lightricks/LTX-Video.git
cd LTX-Video

# create env
python -m venv env
source env/bin/activate
python -m pip install -e .\[inference-script\]
```

#### Inference

To use our model, please follow the inference code in [inference.py](https://github.com/Lightricks/LTX-Video/blob/main/inference.py):


#### For image-to-video generation:

```bash
python inference.py --prompt "PROMPT" --input_image_path IMAGE_PATH --height HEIGHT --width WIDTH --num_frames NUM_FRAMES --seed SEED --pipeline_config configs/ltxv-13b-0.9.8-distilled.yaml
```

#### For video generation with multiple conditions:

You can now generate a video conditioned on a set of images and/or short video segments.
Simply provide a list of paths to the images or video segments you want to condition on, along with their target frame numbers in the generated video. You can also specify the conditioning strength for each item (default: 1.0).

```bash
python inference.py --prompt "PROMPT" --conditioning_media_paths IMAGE_OR_VIDEO_PATH_1 IMAGE_OR_VIDEO_PATH_2 --conditioning_start_frames TARGET_FRAME_1 TARGET_FRAME_2 --height HEIGHT --width WIDTH --num_frames NUM_FRAMES --seed SEED --pipeline_config configs/ltxv-13b-0.9.8-distilled.yaml
```

### Diffusers 🧨

LTX Video is compatible with the [Diffusers Python library](https://huggingface.co/docs/diffusers/main/en/index) for image-to-video generation.

Make sure you install `diffusers` before trying out the examples below.

```bash
pip install -U git+https://github.com/huggingface/diffusers
```

Now, you can run the examples below (note that the upsampling stage is optional but reccomeneded):


### For image-to-video:

```py
import torch
from diffusers import LTXConditionPipeline, LTXLatentUpsamplePipeline
from diffusers.pipelines.ltx.pipeline_ltx_condition import LTXVideoCondition
from diffusers.utils import export_to_video, load_image, load_video

pipe = LTXConditionPipeline.from_pretrained("Lightricks/LTX-Video-0.9.8-dev", torch_dtype=torch.bfloat16)
pipe_upsample = LTXLatentUpsamplePipeline.from_pretrained("Lightricks/ltxv-spatial-upscaler-0.9.8", vae=pipe.vae, torch_dtype=torch.bfloat16)
pipe.to("cuda")
pipe_upsample.to("cuda")
pipe.vae.enable_tiling()

def round_to_nearest_resolution_acceptable_by_vae(height, width):
    height = height - (height % pipe.vae_spatial_compression_ratio)
    width = width - (width % pipe.vae_spatial_compression_ratio)
    return height, width

image = load_image("https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/penguin.png")
video = load_video(export_to_video([image])) # compress the image using video compression as the model was trained on videos
condition1 = LTXVideoCondition(video=video, frame_index=0)

prompt = "A cute little penguin takes out a book and starts reading it"
negative_prompt = "worst quality, inconsistent motion, blurry, jittery, distorted"
expected_height, expected_width = 480, 832
downscale_factor = 2 / 3
num_frames = 96

# Part 1. Generate video at smaller resolution
downscaled_height, downscaled_width = int(expected_height * downscale_factor), int(expected_width * downscale_factor)
downscaled_height, downscaled_width = round_to_nearest_resolution_acceptable_by_vae(downscaled_height, downscaled_width)
latents = pipe(
    conditions=[condition1],
    prompt=prompt,
    negative_prompt=negative_prompt,
    width=downscaled_width,
    height=downscaled_height,
    num_frames=num_frames,
    num_inference_steps=30,
    generator=torch.Generator().manual_seed(0),
    output_type="latent",
).frames

# Part 2. Upscale generated video using latent upsampler with fewer inference steps
# The available latent upsampler upscales the height/width by 2x
upscaled_height, upscaled_width = downscaled_height * 2, downscaled_width * 2
upscaled_latents = pipe_upsample(
    latents=latents,
    output_type="latent"
).frames

# Part 3. Denoise the upscaled video with few steps to improve texture (optional, but recommended)
video = pipe(
    conditions=[condition1],
    prompt=prompt,
    negative_prompt=negative_prompt,
    width=upscaled_width,
    height=upscaled_height,
    num_frames=num_frames,
    denoise_strength=0.4,  # Effectively, 4 inference steps out of 10
    num_inference_steps=10,
    latents=upscaled_latents,
    decode_timestep=0.05,
    image_cond_noise_scale=0.025,
    generator=torch.Generator().manual_seed(0),
    output_type="pil",
).frames[0]

# Part 4. Downscale the video to the expected resolution
video = [frame.resize((expected_width, expected_height)) for frame in video]

export_to_video(video, "output.mp4", fps=24)
```


### For video-to-video: 

```py
import torch
from diffusers import LTXConditionPipeline, LTXLatentUpsamplePipeline
from diffusers.pipelines.ltx.pipeline_ltx_condition import LTXVideoCondition
from diffusers.utils import export_to_video, load_video

pipe = LTXConditionPipeline.from_pretrained("Lightricks/LTX-Video-0.9.8-dev", torch_dtype=torch.bfloat16)
pipe_upsample = LTXLatentUpsamplePipeline.from_pretrained("Lightricks/ltxv-spatial-upscaler-0.9.8", vae=pipe.vae, torch_dtype=torch.bfloat16)
pipe.to("cuda")
pipe_upsample.to("cuda")
pipe.vae.enable_tiling()

def round_to_nearest_resolution_acceptable_by_vae(height, width):
    height = height - (height % pipe.vae_spatial_compression_ratio)
    width = width - (width % pipe.vae_spatial_compression_ratio)
    return height, width

video = load_video(
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/cosmos/cosmos-video2world-input-vid.mp4"
)[:21]  # Use only the first 21 frames as conditioning
condition1 = LTXVideoCondition(video=video, frame_index=0)

prompt = "The video depicts a winding mountain road covered in snow, with a single vehicle traveling along it. The road is flanked by steep, rocky cliffs and sparse vegetation. The landscape is characterized by rugged terrain and a river visible in the distance. The scene captures the solitude and beauty of a winter drive through a mountainous region."
negative_prompt = "worst quality, inconsistent motion, blurry, jittery, distorted"
expected_height, expected_width = 768, 1152
downscale_factor = 2 / 3
num_frames = 161

# Part 1. Generate video at smaller resolution
downscaled_height, downscaled_width = int(expected_height * downscale_factor), int(expected_width * downscale_factor)
downscaled_height, downscaled_width = round_to_nearest_resolution_acceptable_by_vae(downscaled_height, downscaled_width)
latents = pipe(
    conditions=[condition1],
    prompt=prompt,
    negative_prompt=negative_prompt,
    width=downscaled_width,
    height=downscaled_height,
    num_frames=num_frames,
    num_inference_steps=30,
    generator=torch.Generator().manual_seed(0),
    output_type="latent",
).frames

# Part 2. Upscale generated video using latent upsampler with fewer inference steps
# The available latent upsampler upscales the height/width by 2x
upscaled_height, upscaled_width = downscaled_height * 2, downscaled_width * 2
upscaled_latents = pipe_upsample(
    latents=latents,
    output_type="latent"
).frames

# Part 3. Denoise the upscaled video with few steps to improve texture (optional, but recommended)
video = pipe(
    conditions=[condition1],
    prompt=prompt,
    negative_prompt=negative_prompt,
    width=upscaled_width,
    height=upscaled_height,
    num_frames=num_frames,
    denoise_strength=0.4,  # Effectively, 4 inference steps out of 10
    num_inference_steps=10,
    latents=upscaled_latents,
    decode_timestep=0.05,
    image_cond_noise_scale=0.025,
    generator=torch.Generator().manual_seed(0),
    output_type="pil",
).frames[0]

# Part 4. Downscale the video to the expected resolution
video = [frame.resize((expected_width, expected_height)) for frame in video]

export_to_video(video, "output.mp4", fps=24)
```

To learn more, check out the [official documentation](https://huggingface.co/docs/diffusers/main/en/api/pipelines/ltx_video). 

Diffusers also supports directly loading from the original LTX checkpoints using the `from_single_file()` method. Check out [this section](https://huggingface.co/docs/diffusers/main/en/api/pipelines/ltx_video#loading-single-files) to learn more.

## Limitations
- This model is not intended or able to provide factual information.
- As a statistical model this checkpoint might amplify existing societal biases.
- The model may fail to generate videos that matches the prompts perfectly.
- Prompt following is heavily influenced by the prompting-style.