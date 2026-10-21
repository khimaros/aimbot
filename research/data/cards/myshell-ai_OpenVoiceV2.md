---
license: mit
tags:
- audio
- text-to-speech
- instant-voice-cloning
language:
- en
- zh
inference: false
---

# OpenVoice V2

<a href="https://trendshift.io/repositories/6161" target="_blank"><img src="https://trendshift.io/api/badge/repositories/6161" alt="myshell-ai%2FOpenVoice | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>


In April 2024, we release OpenVoice V2, which includes all features in V1 and has:

1. Better Audio Quality. OpenVoice V2 adopts a different training strategy that delivers better audio quality.

2. Native Multi-lingual Support. English, Spanish, French, Chinese, Japanese and Korean are natively supported in OpenVoice V2.

3. Free Commercial Use. Starting from April 2024, both V2 and V1 are released under MIT License. Free for commercial use.


<video controls autoplay src="https://cdn-uploads.huggingface.co/production/uploads/641de0213239b631552713e4/uCHTHD9OUotgOflqDu3QK.mp4"></video>

### Features
- **Accurate Tone Color Cloning.** OpenVoice can accurately clone the reference tone color and generate speech in multiple languages and accents.
- **Flexible Voice Style Control.** OpenVoice enables granular control over voice styles, such as emotion and accent, as well as other style parameters including rhythm, pauses, and intonation.
- **Zero-shot Cross-lingual Voice Cloning.** Neither of the language of the generated speech nor the language of the reference speech needs to be presented in the massive-speaker multi-lingual training dataset.

### How to Use
Please see [usage](https://github.com/myshell-ai/OpenVoice/blob/main/docs/USAGE.md) for detailed instructions.

# Usage

## Table of Content

- [Quick Use](#quick-use): directly use OpenVoice without installation.
- [Linux Install](#linux-install): for researchers and developers only.
    - [V1](#openvoice-v1)
    - [V2](#openvoice-v2)
- [Install on Other Platforms](#install-on-other-platforms): unofficial installation guide contributed by the community

## Quick Use

The input speech audio of OpenVoice can be in **Any Language**. OpenVoice can clone the voice in that speech audio, and use the voice to speak in multiple languages. For quick use, we recommend you to try the already deployed services:

- [British English](https://app.myshell.ai/widget/vYjqae)
- [American English](https://app.myshell.ai/widget/nEFFJf)
- [Indian English](https://app.myshell.ai/widget/V3iYze)
- [Australian English](https://app.myshell.ai/widget/fM7JVf)
- [Spanish](https://app.myshell.ai/widget/NNFFVz)
- [French](https://app.myshell.ai/widget/z2uyUz)
- [Chinese](https://app.myshell.ai/widget/fU7nUz)
- [Japanese](https://app.myshell.ai/widget/IfIB3u)
- [Korean](https://app.myshell.ai/widget/q6ZjIn)

## Linux Install

This section is only for developers and researchers who are familiar with Linux, Python and PyTorch. Clone this repo, and run

```
conda create -n openvoice python=3.9
conda activate openvoice
git clone git@github.com:myshell-ai/OpenVoice.git
cd OpenVoice
pip install -e .
```

No matter if you are using V1 or V2, the above installation is the same.

### OpenVoice V1

Download the checkpoint from [here](https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_1226.zip) and extract it to the `checkpoints` folder.

**1. Flexible Voice Style Control.**
Please see [`demo_part1.ipynb`](https://github.com/myshell-ai/OpenVoice/blob/main/demo_part1.ipynb) for an example usage of how OpenVoice enables flexible style control over the cloned voice.

**2. Cross-Lingual Voice Cloning.**
Please see [`demo_part2.ipynb`](https://github.com/myshell-ai/OpenVoice/blob/main/demo_part2.ipynb) for an example for languages seen or unseen in the MSML training set.

**3. Gradio Demo.**. We provide a minimalist local gradio demo here. We strongly suggest the users to look into `demo_part1.ipynb`, `demo_part2.ipynb` and the [QnA](QA.md) if they run into issues with the gradio demo. Launch a local gradio demo with `python -m openvoice_app --share`.

### OpenVoice V2

Download the checkpoint from [here](https://myshell-public-repo-hosting.s3.amazonaws.com/openvoice/checkpoints_v2_0417.zip) and extract it to the `checkpoints_v2` folder.

Install [MeloTTS](https://github.com/myshell-ai/MeloTTS):
```
pip install git+https://github.com/myshell-ai/MeloTTS.git
python -m unidic download
```

**Demo Usage.** Please see [`demo_part3.ipynb`](https://github.com/myshell-ai/OpenVoice/blob/main/demo_part3.ipynb) for example usage of OpenVoice V2. Now it natively supports English, Spanish, French, Chinese, Japanese and Korean.


## Install on Other Platforms

This section provides the unofficial installation guides by open-source contributors in the community:

- Windows
  - [Guide](https://github.com/Alienpups/OpenVoice/blob/main/docs/USAGE_WINDOWS.md) by [@Alienpups](https://github.com/Alienpups)
  - You are welcome to contribute if you have a better installation guide. We will list you here.
- Docker
  - [Guide](https://github.com/StevenJSCF/OpenVoice/blob/update-docs/docs/DF_USAGE.md) by [@StevenJSCF](https://github.com/StevenJSCF)
  - You are welcome to contribute if you have a better installation guide. We will list you here.


### Links
- [Github](https://github.com/myshell-ai/OpenVoice)
- [HFDemo](https://huggingface.co/spaces/myshell-ai/OpenVoiceV2)
- [Discord](https://discord.gg/myshell)

