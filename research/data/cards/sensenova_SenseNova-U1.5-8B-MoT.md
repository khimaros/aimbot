---
license: apache-2.0
language:
- en
- zh
library_name: transformers
tags:
- native multimodal
- image-generation
- image-editing
- any-to-any
---

# SenseNova-U1.5-8B-MoT

<p align="center">
  <strong>English</strong> | <a href="./README_CN.md">简体中文</a>
</p>

<p align="center">
  <a href="https://github.com/OpenSenseNova/SenseNova-U1"><img src="https://img.shields.io/badge/GitHub-SenseNova--U1-181717?logo=github" alt="GitHub"></a>
  <a href="https://huggingface.co/collections/sensenova/sensenova-u15"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20HuggingFace-U1.5-yellow" alt="SenseNova-U1.5 on Hugging Face"></a>
  <a href="https://huggingface.co/blog/sensenova/neo-unify"><img src="https://img.shields.io/badge/Architecture-NEO--unify-2459B8" alt="NEO-unify"></a>
  <a href="https://modelscope.cn/models/SenseNova/SenseNova-U1.5-8B-MoT"><img src="https://img.shields.io/badge/%F0%9F%A4%96%20ModelScope-模型-purple" alt="ModelScope-模型"></a>
  <a href="https://unify.light-ai.top/"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20SenseNova_U-Demo-Green" alt="SenseNova-U Demo"></a>
  <a href="https://github.com/OpenSenseNova/SenseNova-U1/blob/refs/heads/feat/u1.5/LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License"></a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/OpenSenseNova/SenseNova-U1/refs/heads/feat/u1.5/docs/assets/teaserU1.5.png" alt="SenseNova-U1.5 native unified multimodal architecture" width="100%">
</p>

## Overview

**SenseNova-U1.5-8B-MoT** is our latest native unified multimodal checkpoint for more accurate, consistent, reliable, and aesthetically compelling visual creation. Built on [NEO-unify](https://huggingface.co/blog/sensenova/neo-unify), it strengthens the patchify layers, data quality and distribution, task formulation, prompt enhancement, and post-training pipeline.

The official release focuses on six user-visible improvements:

- **Higher-quality image generation:** improved composition and color harmony, with more realistic material rendering, natural lighting, stronger visual fidelity, and finer local details.
- **Better text rendering and infographic generation:** more legible Chinese and English text, with clearer information hierarchy in posters, infographics, brand assets, and other text-dense designs.
- **More efficient native 4K generation:** more coherent global structure, color harmony, and stable high-resolution output with improved generation efficiency.
- **More reliable native image editing:** stronger preservation of subject identity and unedited content across local, text, multi-reference, insertion, and replacement edits.
- **Stronger complex-instruction following:** more consistent execution of object counts, spatial relationships, layouts, styles, and multiple constraints within a single request.
- **More precise visual control:** more accurate region- and object-level control through bounding boxes, visual markers, and single- or multi-image references.

## Showcases

<p align="center">
  <img src="https://raw.githubusercontent.com/OpenSenseNova/SenseNova-U1/refs/heads/feat/u1.5/docs/assets/u1.5_teaser2.webp" alt="SenseNova-U1.5 generation and editing showcases" width="100%">
</p>

## Key Benchmarks

<p align="center">
  <img src="https://raw.githubusercontent.com/OpenSenseNova/SenseNova-U1/refs/heads/feat/u1.5/docs/assets/benchmarks/u1.5_radial.webp" alt="SenseNova-U1.5 benchmark overview" width="100%">
</p>

<details>
<summary>View detailed benchmark results</summary>

<p align="center">
  <img src="https://raw.githubusercontent.com/OpenSenseNova/SenseNova-U1/refs/heads/feat/u1.5/docs/assets/benchmarks/u1.5_combined.webp" alt="SenseNova-U1.5 detailed benchmark results" width="100%">
</p>

</details>

## Quick Start

The reference inference implementation is available in the [SenseNova-U1 GitHub repository](https://github.com/OpenSenseNova/SenseNova-U1/tree/refs/heads/feat/u1.5).

### Installation

```bash
git clone https://github.com/OpenSenseNova/SenseNova-U1.git
cd SenseNova-U1
uv sync
source .venv/bin/activate
```

The upstream environment uses Python 3.11, PyTorch 2.8, and CUDA 12.8. For other CUDA versions and optional FlashAttention configurations, see the [installation guide](https://github.com/OpenSenseNova/SenseNova-U1/blob/refs/heads/feat/u1.5/docs/installation.md).

### Text-to-Image

```bash
python examples/t2i/inference.py \
  --model_path sensenova/SenseNova-U1.5-8B-MoT \
  --prompt "A cinematic mountain lake at sunrise, realistic photography." \
  --width 2048 --height 2048 \
  --device_map auto \
  --output output.png
```

### Image Editing

```bash
python examples/editing/inference.py \
  --model_path sensenova/SenseNova-U1.5-8B-MoT \
  --image input.png \
  --prompt "Change the jacket to cobalt blue. Preserve the face, pose, background, lighting, and framing." \
  --output edited.png
```

See the [inference examples](https://github.com/OpenSenseNova/SenseNova-U1/blob/refs/heads/feat/u1.5/examples/README.md) for more options, supported resolutions, and batch processing.

## Best Practices

Direct natural-language prompts work well for clear tasks with few constraints. For complex generation or editing, use prompt enhancement when additional planning is needed and explicitly specify what should remain unchanged.

See the **[SenseNova-U1.5 Cookbook](https://github.com/OpenSenseNova/SenseNova-U1/blob/refs/heads/feat/u1.5/docs/u1.5_best_practices.md)** for setup instructions and optional Image PE, Caption-to-Prompt, and Editing PE recipes.

## 🌐 Use with SenseNova-Studio

The fastest way to experience SenseNova-U1.5 is through **[SenseNova-Studio](https://unify.light-ai.top/)** — a 🆓 free online playground where you can try the model directly in your browser, no installation or GPU required.

## Ongoing Improvements

The official release improves upon the Preview, though challenges remain in:

- **Over-emphasized details or colors:** some prompts may produce excessive high-frequency detail or oversaturated colors, which can often be mitigated by lowering `cfg_scale`.
- **Dense text errors:** dense, lengthy, small, or mixed Chinese-English text may contain errors.
- **Constrained layouts:** exact counts, alignment, or hierarchy may be imperfect in highly constrained layouts.
- **Unstable human details:** small faces, hands, limbs, and fine-grained object structures may remain unstable.
- **Complex editing drift:** broad, multi-turn, or multi-reference edits may drift, especially when many regions must be preserved simultaneously.

## Models

| Model | Stage | HF Weights |
| :---- | :---- | :--------- |
| **SenseNova-U1.5-8B-MoT** | RL | [🤗 Model](https://huggingface.co/sensenova/SenseNova-U1.5-8B-MoT) |
| SenseNova-U1.5-8B-MoT-SFT | Supervised fine-tuning | [🤗 Model](https://huggingface.co/sensenova/SenseNova-U1.5-8B-MoT-SFT) |

## 🌐 Join the Community!

Join our growing community to share feedback, get support, and stay updated on the latest SenseNova-U1 developments — we'd love to hear from you!

<div align="center">
<table>
  <tr>
    <td align="center"><b><a href="https://discord.com/invite/BuTXPHmQub">Discord</a></b></td>
    <td align="center"><b>Feishu Group</b></td>
  </tr>
  <tr>
    <td align="center"><a href="https://discord.com/invite/BuTXPHmQub"><img src="https://raw.githubusercontent.com/OpenSenseNova/SenseNova-U1/main/docs/assets/discord_qr.webp" width="160"/></a></td>
    <td align="center"><img src="https://raw.githubusercontent.com/OpenSenseNova/SenseNova-U1/main/docs/assets/feishu.png" width="160"/></td>
  </tr>
</table>
</div>


## Citation

If this project is helpful for your research, please consider starring the repository and citing:

```bibtex
@misc{sensenova2026neounify,
  title        = {NEO-unify: Building Native Multimodal Unified Models End to End},
  author       = {SenseNova},
  journal      = {Hugging Face blog},
  url          = {https://huggingface.co/blog/sensenova/neo-unify},
  year         = {2026}
}

@article{sensenova2026sensenovau1,
  title        = {SenseNova-U1: Unifying Multimodal Understanding and Generation with NEO-unify Architecture},
  author       = {Diao, Haiwen and Wu, Penghao and Deng, Hanming and Wang, Jiahao and Bai, Shihao and Wu, Silei and Fan, Weichen and Ye, Wenjie and Tong, Wenwen and Fan, Xiangyu and others},
  journal      = {arXiv preprint arXiv:2605.12500},
  year         = {2026}
}

@article{sensenova2026sensenovau1.5,
  title        = {SenseNova-U1. 5: Towards Native Unified Visual Intelligence},
  author       = {Diao, Haiwen and Wang, Jiahao and Ding, Chenjing and Deng, Hanming and Chen, Jiangnan and Zhang, Ruixi and Wang, Ruohui and Tong, Wenwen and Fan, Xiangyu and Wang, Yubo and others},
  journal      = {arXiv preprint arXiv:2609.11929},
  year         = {2026}
}
```

## License

This model is released under the [Apache 2.0 License](https://github.com/OpenSenseNova/SenseNova-U1/blob/refs/heads/feat/u1.5/LICENSE).
