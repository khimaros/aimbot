---
frameworks:
- ""
language:
- zh
license: apache-2.0
tags:
- speech
- asr
tasks: []
---

# Dolphin-CN-Dialect

[Paper](https://arxiv.org/abs/2605.08961)
[Github](https://github.com/DataoceanAI/Dolphin)
[Huggingface](https://huggingface.co/DataoceanAI)
[Modelscope](https://www.modelscope.cn/organization/DataoceanAI)

# Repository Notice

This model is officially maintained by **Dataocean AI**.

To ensure compatibility with existing user code and download links, we keep two official repositories for the same model:

- Original / legacy repository: DataoceanAI
- Organization / enterprise repository: DataoceanAI1

Both repositories are maintained by the same team and contain the same model files.  
DataoceanAI1 is the newly created enterprise organization account, while DataoceanAI is kept to avoid breaking existing user download scripts and links.

Please do not regard either repository as an unofficial copy or unauthorized redistribution.

**Dolphin-CN-Dialect** is a multi-dialect ASR model developed by Dataocean AI and Tsinghua University, with a strong focus on Chinese dialect recognition and real-world deployment scenarios. Compared with the previous Dolphin series, Dolphin-CN-Dialect introduces significant improvements in tokenizer design, dialect-balanced training, streaming capability, hotword biasing, and deployment efficiency.

The model supports Mandarin Chinese and 22 Chinese dialects, while also maintaining multilingual ASR capability inherited from Dolphin. Dolphin-CN-Dialect supports both streaming and non-streaming inference, enabling practical deployment in latency-sensitive applications such as real-time transcription and industrial speech recognition systems.


## Approach

Dolphin-CN-Dialect is built upon the Dolphin architecture and follows a joint CTC-Attention framework with:

* Encoder: E-Branchformer
* Decoder: Transformer Decoder
* Training Objective: Joint CTC + Attention loss

Compared to Dolphin, Dolphin-CN-Dialect introduces several important improvements:

* Temperature-based data sampling for balancing standard Mandarin and low-resource dialects
* Redesigned tokenizer with:
    * character-level modeling for Chinese
    * BPE-based subword modeling for English
    * extensible dialect tokens
* Streaming ASR support
* Hotword-biased decoding, including:
    * encoder-level contextual biasing
    * prompt-based decoder biasing

Experimental results show that Dolphin-CN-Dialect achieves:

* 38% improvement in dialect recognition accuracy
* 16.3% relative CER reduction over Dolphin
* Competitive performance with recent large-scale ASR systems while maintaining a smaller model size

![Dolphin-CN-Dialect 特色海报](Dolphin-CN-Dialect.png)


See details in the [Paper](https://arxiv.org/abs/2605.08961).


## Setup

Dolphin-CN-Dialect requires FFmpeg to convert audio files into WAV format. Please install FFmpeg first if it is not already installed on your system.

```shell
# Ubuntu / Debian
sudo apt update && sudo apt install ffmpeg
# MacOS
brew install ffmpeg
# Windows
choco install ffmpeg
```

Install Dolphin with pip:

```shell
pip install -U dolphin
```

Alternatively, install from source:

```shell
pip install git+https://github.com/DataoceanAI/Dolphin.git
```

## Available Models

Currently, Dolphin-CN-Dialect provides multiple model sizes optimized for different deployment scenarios.

|  Model  | Parameters  | Hotwords |
|:------:|:----------:|:----------:|
|  base.cn  |    0.1 B   | ❌ |
|  base.cn.streaming  |    0.1 B   |❌  |
| small.cn  |   0.4 B      | Encoder-biased Hotwords |
| small.cn.streaming  |   0.4 B      | Encoder-biased Hotwords |
| small.cn.prompt |   0.4 B      | Prompt-based Hotwords |


## Hotword Biasing

Dolphin-CN-Dialect supports two hotword biasing approaches.

**Encoder-Level Contextual Biasing**

* Supports both streaming and non-streaming models
* Integrates contextual embeddings into encoder representations
* Efficient adaptation without retraining the full model

**Prompt-Based Hotword Biasing**

* Designed for non-streaming models
* Injects hotwords directly into decoder prompts
* Particularly effective for long-tail and rare phrases

Experimental results show significant reductions in hotword error rates while maintaining strong overall ASR performance.



## Supported Languages and Dialects

Dolphin-CN-Dialect primarily focuses on:

* Mandarin Chinese
* 22 Chinese dialects
* Regional accented Mandarin

Supported dialects include:

* Sichuan
* Wu
* Minnan
* Shanghai
* Gansu
* Guangdong
* Wenzhou
* Hunan
* Anhui
* Henan
* Fujian
* Hebei
* Liaoning
* Shaanxi
* Tianjin
* and more

For the complete language and dialect list, see [languages.md](./languages.md).

## Supported Devices

| Device Type | Support Status |
|:-------------:|:----------------:|
|**CUDA**|✅Supported|
|**MPS (Apple)**|✅Supported|
|**CPU**|✅Supported|


## Usage

### Command-line usage

```shell
dolphin audio.wav

# Download model and specify the model path
dolphin audio.wav --model small.cn --model_dir /data/models/dolphin/

# Specify language and region
dolphin audio.wav --model small.cn --model_dir /data/models/dolphin/ --lang_sym "zh" --region_sym "CN"

# Specify the hotwords file with Encoder-biased method
dolphin audio.wav --model small.cn --model_dir /data/models/dolphin/ --hotword_list_path hotwords.txt --use_deep_biasing true

# Using prompt-based model
dolphin audio.wav --model small.cn.prompt --model_dir /data/models/dolphin/ --hotword_list_path hotwords.txt --use_prompt_hotword true --use_two_stage_filter true

```

### Python usage

```python
import dolphin
from dolphin import transcribe

model_name = 'small.cn'
model = dolphin.load_model(model_name, device="cuda")

result = transcribe(model, 'audio.wav')
print(result.text)

# Specify language
result = transcribe(model, 'audio.wav', lang_sym="zh")
print(result.text)

# Specify language and region and encoder-biased hotwords
result = transcribe(model, 'audio.wav', lang_sym="zh", region_sym="CN", hotwords=['诺香丹青牌科研胶囊'], use_deep_biasing=True, use_two_stage_filter=True)
print(result.text)

## prompt-based hotwords

model_name = 'small.cn.prompt'
model = dolphin.load_model(model_name, device="cuda")

result = transcribe(model, 'audio.wav', hotwords=['诺香丹青牌科研胶囊'], use_prompt_hotword=True, use_two_stage_filter=True, decoding_method='attention')

print(result.text)

```


## License

Dolphin-CN-Dialect is released under the Apache 2.0 License￼.
