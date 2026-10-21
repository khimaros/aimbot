---
language:
- zh
- en
- de
- es
- fr
- ja
- it
- he
- ko
- ru
- fa
- ar
- pl
- pt
- cs
- da
- sv
- hu
- el
- tr
license: apache-2.0
library_name: transformers
pipeline_tag: text-to-speech
tags:
- text-to-speech
---

# MOSS-TTS Family

<br>

<p align="center">
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://speech-demo.oss-cn-shanghai.aliyuncs.com/moss_tts_demo/tts_readme_imgaes_demo/openmoss_x_mosi" height="50" align="middle" />
</p>



<div align="center">
  <a href="https://github.com/OpenMOSS/MOSS-TTS/tree/main"><img src="https://img.shields.io/badge/Project%20Page-GitHub-blue"></a>
  <a href="https://modelscope.cn/collections/OpenMOSS-Team/MOSS-TTS"><img src="https://img.shields.io/badge/ModelScope-Models-lightgrey?logo=modelscope&amp"></a>
  <a href="https://mosi.cn/#models"><img src="https://img.shields.io/badge/Blog-View-blue?logo=internet-explorer&amp"></a>
  <a href="https://huggingface.co/papers/2602.10934"><img src="https://img.shields.io/badge/Arxiv-2602.10934-red?logo=arxiv&amp"></a>

  <a href="https://studio.mosi.cn"><img src="https://img.shields.io/badge/AIStudio-Try-green?logo=internet-explorer&amp"></a>
  <a href="https://studio.mosi.cn/docs/moss-tts"><img src="https://img.shields.io/badge/API-Docs-00A3FF?logo=fastapi&amp"></a>
  <a href="https://x.com/Open_MOSS"><img src="https://img.shields.io/badge/Twitter-Follow-black?logo=x&amp"></a>
  <a href="https://discord.gg/fvm5TaWjU3"><img src="https://img.shields.io/badge/Discord-Join-5865F2?logo=discord&amp"></a>
</div>

## Overview
MOSS‑TTS Family is an open‑source **speech and sound generation model family** from [MOSI.AI](https://mosi.cn/#hero) and the [OpenMOSS team](https://www.open-moss.com/). It is designed for **high‑fidelity**, **high‑expressiveness**, and **complex real‑world scenarios**, covering stable long‑form speech, multi‑speaker dialogue, voice/character design, environmental sound effects, and real‑time streaming TTS.

The model architecture and tokenizer are detailed in the paper [MOSS-Audio-Tokenizer: Scaling Audio Tokenizers for Future Audio Foundation Models](https://huggingface.co/papers/2602.10934).


## Introduction

<p align="center">
  <img src="https://speech-demo.oss-cn-shanghai.aliyuncs.com/moss_tts_demo/tts_readme_imgaes_demo/moss_tts_family_arch.jpeg" width="85%" />
</p>


When a single piece of audio needs to **sound like a real person**, **pronounce every word accurately**, **switch speaking styles across content**, **remain stable over tens of minutes**, and **support dialogue, role‑play, and real‑time interaction**, a single TTS model is often not enough. The **MOSS‑TTS Family** breaks the workflow into five production‑ready models that can be used independently or composed into a complete pipeline.

- **MOSS‑TTS**: MOSS-TTS is the flagship production TTS foundation model, centered on high-fidelity zero-shot voice cloning with controllable long-form synthesis, pronunciation, and multilingual/code-switched speech. It serves as the core engine for scalable narration, dubbing, and voice-driven products.
- **MOSS‑TTSD**: MOSS-TTSD is a production long-form dialogue model for expressive multi-speaker conversational audio at scale. It supports long-duration continuity, turn-taking control, and zero-shot voice cloning from short references for podcasts, audiobooks, commentary, dubbing, and entertainment dialogue.
- **MOSS‑VoiceGenerator**: MOSS-VoiceGenerator is an open-source voice design model that creates speaker timbres directly from free-form text, without reference audio. It unifies timbre design, style control, and content synthesis, and can be used standalone or as a voice-design layer for downstream TTS.
- **MOSS‑SoundEffect**: MOSS-SoundEffect is a high-fidelity text-to-sound model with broad category coverage and controllable duration for real content production. It generates stable audio from prompts across ambience, urban scenes, creatures, human actions, and music-like clips for film, games, interactive media, and data synthesis.
- **MOSS‑TTS‑Realtime**: MOSS-TTS-Realtime is a context-aware, multi-turn streaming TTS model for real-time voice agents. By conditioning on dialogue history across both text and prior user acoustics, it delivers low-latency synthesis with coherent, consistent voice responses across turns.

## Released Models
| Model | Architecture | Size | Model Card | Hugging Face |
|---|---|---:|---|---|
| **MOSS-TTS** | MossTTSDelay | 8B | [moss_tts_model_card.md](https://github.com/OpenMOSS/MOSS-TTS/blob/main/docs/moss_tts_model_card.md) | 🤗 [Huggingface](https://huggingface.co/OpenMOSS-Team/MOSS-TTS) |
|  | MossTTSLocal | 1.7B | [moss_tts_model_card.md](https://github.com/OpenMOSS/MOSS-TTS/blob/main/docs/moss_tts_model_card.md) | 🤗 [Huggingface](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Local-Transformer) |
| **MOSS‑TTSD‑V1.0** | MossTTSDelay | 8B | [moss_ttsd_model_card.md](https://github.com/OpenMOSS/MOSS-TTS/blob/main/docs/moss_ttsd_model_card.md) | 🤗 [Huggingface](https://huggingface.co/OpenMOSS-Team/MOSS-TTSD-v1.0) |
| **MOSS‑VoiceGenerator** | MossTTSDelay | 1.7B | [moss_voice_generator_model_card.md](https://github.com/OpenMOSS/MOSS-TTS/blob/main/docs/moss_voice_generator_model_card.md) | 🤗 [Huggingface](https://huggingface.co/OpenMOSS-Team/MOSS-Voice-Generator) |
| **MOSS‑SoundEffect** | MossTTSDelay | 8B | [moss_sound_effect_model_card.md](https://github.com/OpenMOSS/MOSS-TTS/blob/main/docs/moss_sound_effect_model_card.md) | 🤗 [Huggingface](https://huggingface.co/OpenMOSS-Team/MOSS-SoundEffect) |
| **MOSS‑TTS‑Realtime** | MossTTSRealtime | 1.7B | [moss_tts_realtime_model_card.md](https://github.com/OpenMOSS/MOSS-TTS/blob/main/docs/moss_tts_realtime_model_card.md) | 🤗 [Huggingface](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Realtime) |

## Supported Languages

MOSS-TTS, MOSS-TTSD and MOSS-TTS-Realtime currently supports **20 languages**:

| Language | Code | Flag | Language | Code | Flag | Language | Code | Flag |
|---|---|---|---|---|---|---|---|---|
| Chinese | zh | 🇨🇳 | English | en | 🇺🇸 | German | de | 🇩🇪 |
| Spanish | es | 🇪🇸 | French | fr | 🇫🇷 | Japanese | ja | 🇯🇵 |
| Italian | it | 🇮🇹 | Hebrew | he | 🇮🇱 | Korean | ko | 🇰🇷 |
| Russian | ru | 🇷🇺 | Persian (Farsi) | fa | 🇮🇷 | Arabic | ar | 🇸🇦 |
| Polish | pl | 🇵🇱 | Portuguese | pt | 🇵🇹 | Czech | cs | 🇨🇿 |
| Danish | da | 🇩🇰 | Swedish | sv | 🇸🇪 | Hungarian | hu | 🇭🇺 |
| Greek | el | 🇬🇷 | Turkish | tr | 🇹🇷 |  |  |  |


<br>

# MOSS-TTSD

**MOSS-TTSD** is a long-form spoken dialogue generation model that enables highly expressive multi-party conversational speech synthesis across multiple languages. It supports continuous long-duration generation, flexible multi-speaker dialogue control, and state-of-the-art zero-shot voice cloning with only short reference audio. MOSS-TTSD is designed for real-world long-form content creation, including podcasts, audiobook, sports and esports commentary, dubbing, crosstalk, and entertainment scenarios.


## 1. Overview

### 1.1 TTS Family Positioning
MOSS-TTSD is the Long-Form Dialogue Specialist in our open-source TTS Family. While our foundational models focus on high-fidelity single-speaker synthesis, MOSS-TTSD extends this capability into the realm of complex, multi-party interactions. It is designed to bridge the gap between distinct audio samples and cohesive, continuous conversation.

**Design Goals**
- **Authentic Interaction**: Capturing the natural rhythm, overlaps, and dynamics of human conversation.
- **Sustained Coherence**: Maintaining speaker identity and contextual consistency over extended durations (up to 1 hour).
- **Production Adaptability**: Serving diverse high-end scenarios from rigorous audiobook narration to dynamic sports commentary.

### 1.2 Key Capabilities
MOSS-TTSD transforms static text into living conversations, offering features specifically optimized for multi-speaker environments:

- **Multi-Party Conversational Generation** — Unlike traditional TTS which optimizes for reading, MOSS-TTSD masters the rhythm of conversation. It supports 1 to 5 speakers with flexible control, handling natural turn-taking, overlapping speech patterns, and distinct persona maintenance.

- **Extreme Long-Context Modeling** — Moving beyond short-sentence generation, the model is architected for stability over long durations, supporting up to 60 minutes of coherent audio in a single session without losing speaker identity or prosodic quality.

- **Diverse Scenario Adaptation** — The model is fine-tuned on high-variability scenarios to handle different speaking styles:
  - Conversational Media: AI Podcasts, Interviews.
  - Dynamic Commentary: High-energy Sports/Esports shouting and analysis.
  - Entertainment: Audiobooks (narrator + characters), Dubbing, and Crosstalk (Xiangsheng).

- **Multilingual & Zero-Shot Cloning** — Features state-of-the-art zero-shot voice cloning requiring only short reference audio (3-10s), with robust cross-lingual performance across major languages including Chinese, English, Japanese, and European languages.

### 1.3 Model Architecture

MOSS-TTSD is built on top of **Architecture A: Delay Pattern (MossTTSDelay)** from our MOSS-TTS foundation model — a single Transformer backbone with multi-head parallel prediction using delay scheduling for multi-codebook audio tokens. 
<!-- For full architecture details, see **`moss_tts_delay/moss_tts_delay_architecture.md`**. -->

### 1.4 Released Models

| Model | Architecture | NVQ | Parameters |
|-------|-------------|-----|------------|
| MOSS-TTSD | Architecture A: Delay Pattern (MossTTSDelay) | 16 | 8B |

**Recommended decoding hyperparameters**

| Model | audio_temperature | audio_top_p | audio_top_k | audio_repetition_penalty |
|---|---:|---:|---:|---:|
| **MOSS-TTSD** | 1.1 | 0.9 | 50 | 1.1 |

## 2. Quick Start



### Environment Setup

We recommend a clean, isolated Python environment with **Transformers 5.0.0** to avoid dependency conflicts.

```bash
conda create -n moss-tts python=3.12 -y
conda activate moss-tts
```

Install all required dependencies:

```bash
git clone https://github.com/OpenMOSS/MOSS-TTS.git
cd MOSS-TTS
pip install --extra-index-url https://download.pytorch.org/whl/cu128 -e .
```

#### (Optional) Install FlashAttention 2

For better speed and lower GPU memory usage, you can install FlashAttention 2 if your hardware supports it.

```bash
pip install --extra-index-url https://download.pytorch.org/whl/cu128 -e ".[flash-attn]"
```

If your machine has limited RAM and many CPU cores, you can cap build parallelism:

```bash
MAX_JOBS=4 pip install --extra-index-url https://download.pytorch.org/whl/cu128 -e ".[flash-attn]"
```

Notes:
- Dependencies are managed in `pyproject.toml`, which currently pins `torch==2.9.1+cu128` and `torchaudio==2.9.1+cu128`.
- If FlashAttention 2 fails to build on your machine, you can skip it and use the default attention backend.
- FlashAttention 2 is only available on supported GPUs and is typically used with `torch.float16` or `torch.bfloat16`.


### Basic Usage


MOSS-TTSD uses a **continuation** workflow: provide reference audio for each speaker, their transcripts as a prefix, and the dialogue text to generate. The model continues in each speaker's identity.

```python
from pathlib import Path
import importlib.util
import torch
import torchaudio
from transformers import AutoModel, AutoProcessor
# Disable the broken cuDNN SDPA backend
torch.backends.cuda.enable_cudnn_sdp(False)
# Keep these enabled as fallbacks
torch.backends.cuda.enable_flash_sdp(True)
torch.backends.cuda.enable_mem_efficient_sdp(True)
torch.backends.cuda.enable_math_sdp(True)

pretrained_model_name_or_path = "OpenMOSS-Team/MOSS-TTSD-v1.0"
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.bfloat16 if device == "cuda" else torch.float32

def resolve_attn_implementation() -> str:
    # Prefer FlashAttention 2 when package + device conditions are met.
    if (
        device == "cuda"
        and importlib.util.find_spec("flash_attn") is not None
        and dtype in {torch.float16, torch.bfloat16}
    ):
        major, _ = torch.cuda.get_device_capability()
        if major >= 8:
            return "flash_attention_2"

    # CUDA fallback: use PyTorch SDPA kernels.
    if device == "cuda":
        return "sdpa"

    # CPU fallback.
    return "eager"


attn_implementation = resolve_attn_implementation()
print(f"[INFO] Using attn_implementation={attn_implementation}")

processor = AutoProcessor.from_pretrained(
    pretrained_model_name_or_path,
    trust_remote_code=True,
)
processor.audio_tokenizer = processor.audio_tokenizer.to(device)

model = AutoModel.from_pretrained(
    pretrained_model_name_or_path,
    trust_remote_code=True,
    # If FlashAttention 2 is installed, you can set attn_implementation="flash_attention_2"
    attn_implementation=attn_implementation,
    torch_dtype=dtype,
).to(device)
model.eval()

# --- Inputs ---

# Use audio from ./assets/audio to avoid downloading from the cloud.
prompt_audio_speaker1 = "https://speech-demo.oss-cn-shanghai.aliyuncs.com/moss_tts_demo/tts_readme_demo/reference_02_s1.wav"
prompt_audio_speaker2 = "https://speech-demo.oss-cn-shanghai.aliyuncs.com/moss_tts_demo/tts_readme_demo/reference_02_s2.wav"
prompt_text_speaker1 = "[S1] In short, we embarked on a mission to make America great again for all Americans."
prompt_text_speaker2 = "[S2] NVIDIA reinvented computing for the first time after 60 years. In fact, Erwin at IBM knows quite well that the computer has largely been the same since the 60s."

text_to_generate = "[S1] Listen, let's talk business. China. I'm hearing things. People are saying they're catching up. Fast. What's the real scoop? Their AI—is it a threat? [S2] Well, the pace of innovation there is extraordinary, honestly. They have the researchers, and they have the drive. [S1] Extraordinary? I don't like that. I want us to be extraordinary. Are they winning? [S2] I wouldn't say winning, but their progress is very promising. They are building massive clusters. They're very determined. [S1] Promising. There it is. I hate that word. When China is promising, it means we're losing. It's a disaster, Jensen. A total disaster. "

# --- Load & resample audio ---

target_sr = int(processor.model_config.sampling_rate)
wav1, sr1 = torchaudio.load(prompt_audio_speaker1)
wav2, sr2 = torchaudio.load(prompt_audio_speaker2)

if wav1.shape[0] > 1:
    wav1 = wav1.mean(dim=0, keepdim=True)
if wav2.shape[0] > 1:
    wav2 = wav2.mean(dim=0, keepdim=True)
if sr1 != target_sr:
    wav1 = torchaudio.functional.resample(wav1, sr1, target_sr)
if sr2 != target_sr:
    wav2 = torchaudio.functional.resample(wav2, sr2, target_sr)

# --- Build conversation ---

reference_audio_codes = processor.encode_audios_from_wav([wav1, wav2], sampling_rate=target_sr)
concat_prompt_wav = torch.cat([wav1, wav2], dim=-1)
prompt_audio = processor.encode_audios_from_wav([concat_prompt_wav], sampling_rate=target_sr)[0]

full_text = f"{prompt_text_speaker1} {prompt_text_speaker2} {text_to_generate}"

conversations = [
    [
        processor.build_user_message(
            text=full_text,
            reference=reference_audio_codes,
        ),
        processor.build_assistant_message(
            audio_codes_list=[prompt_audio]
        ),
    ],
]

# --- Inference ---

batch_size = 1

save_dir = Path("inference_root")
save_dir.mkdir(exist_ok=True, parents=True)
sample_idx = 0
with torch.no_grad():
    for start in range(0, len(conversations), batch_size):
        batch_conversations = conversations[start : start + batch_size]
        batch = processor(batch_conversations, mode="continuation")
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)

        outputs = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=2000,
        )

        for message in processor.decode(outputs):
            audio = message.audio_codes_list[0]
            out_path = save_dir / f"sample{sample_idx}.wav"
            sample_idx += 1
            torchaudio.save(out_path, audio.unsqueeze(0), processor.model_config.sampling_rate)

```

### Input Types

**UserMessage**

| Field | Type | Required | Description |
|---|---|---:|---|
| `text` | `str` | Yes | Full dialogue text including speaker tags (`[S1]`, `[S2]`, ...) and prompt transcripts. |
| `reference` | `List` | Yes | Per-speaker reference audio codes from `processor.encode_audios_from_wav()`. |

**AssistantMessage**

| Field | Type | Required | Description |
|---|---|---:|---|
| `audio_codes_list` | `List` | Yes | Concatenated prompt audio codes for all speakers. |

### Generation Hyperparameters

| Parameter | Type | Default | Description |
|---|---|---:|---|
| `max_new_tokens` | `int` | — | Controls total generated audio tokens. **1s ≈ 12.5 tokens**. |
| `audio_temperature` | `float` | 1.1 | Higher values increase variation; lower values stabilize prosody. |
| `audio_top_p` | `float` | 0.9 | Nucleus sampling cutoff. |
| `audio_top_k` | `int` | 50 | Top-K sampling. |
| `audio_repetition_penalty` | `float` | 1.1 | >1.0 discourages repeating patterns. |


## 3. Evaluation
### Objective Evaluation(TTSD-eval)



We introduce a robust evaluation framework leveraging **MMS-FA** for alignment and **wespeaker** for embedding extraction to ensure precise speaker attribution.



- **Method**: Forced-alignment based segmentation + Similarity-based speaker verification.

- **Metrics**: 
  - **Speaker Attribution Accuracy (ACC)**
  - **Speaker Similarity (SIM)**
  - **Word Error Rate (WER)** computed using **Whisper-large-v3**.

- **Dataset**: 100 multi-turn dialogues (CN/EN) spanning 30s–720s. Covers diverse scenarios including Podcasts, TV dubbing, and Crosstalk. Code and data coming soon.  
<br>

| Model | ZH - SIM | ZH - ACC | ZH - WER | EN - SIM | EN - ACC | EN - WER |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Comparison with Open-Source Models** | | | | | | |
| MOSS-TTSD | **0.7949** | **0.9587** | **0.0485** | **0.7326** | **0.9626** | 0.0988 |
| MOSS-TTSD v0.7 | 0.7423 | 0.9391 | 0.0517 | 0.6743 | 0.9266 | 0.1612 |
| Vibevoice 7B | 0.7590 | 0.9222 | 0.0570 | 0.7140 | 0.9554 | **0.0946** |
| Vibevoice 1.5 B | 0.7415 | 0.8798 | 0.0818 | 0.6961 | 0.9353 | 0.1133 |
| FireRedTTS2 | 0.7383 | 0.9022 | 0.0768 | - | - | - |
| Higgs Audio V2 | - | - | - | 0.6860 | 0.9025 | 0.2131 |
| **Comparison with Proprietary Models** | | | | | | |
| Eleven V3 | 0.6970 | 0.9653 | **0.0363** | 0.6730 | 0.9498 | **0.0824** |
| MOSS-TTSD (elevenlabs_voice) | **0.8165** | **0.9736** | 0.0391 | **0.7304** | **0.9565** | 0.1005 |
| | | | | | | |
| gemini-2.5-pro-preview-tts | - | - | - | 0.6786 | 0.9537 | **0.0859** |
| gemini-2.5-flash-preview-tts | - | - | - | 0.7194 | 0.9511 | 0.0871 |
| MOSS-TTSD (gemini_voice) | - | - | - | **0.7893** | **0.9655** | 0.0984 |
| | | | | | | |
| Doubao_Podcast | 0.8034 | 0.9606 | **0.0472** | - | - | - |
| MOSS-TTSD (doubao_voice) | **0.8226** | **0.9630** | 0.0571 | - | - | - |

### Subjective Evaluation
For open-source models, annotators are asked to score each sample pair in terms of speaker attribution accuracy, voice similarity, prosody, and overall quality. Following the methodology of the LMSYS Chatbot Arena, we compute Elo ratings and confidence intervals for each dimension.
<p align="center">
  <img src="https://speech-demo.oss-cn-shanghai.aliyuncs.com/moss_tts_demo/tts_readme_imgaes_demo/moss_ttsd_subjective_evaluation" width="100%" />
</p>

For closed-source models, annotators are only asked to choose the overall preferred one in each pair, and we compute the win rate accordingly.
<p align="center">
  <img src="https://speech-demo.oss-cn-shanghai.aliyuncs.com/moss_tts_demo/tts_readme_imgaes_demo/moss_ttsd_winrate" width="100%" />
</p>

## Citation

If you use this code or result in your paper, please cite our work as:

```bibtex
@misc{gong2026mossaudiotokenizerscalingaudiotokenizers,
      title={MOSS-Audio-Tokenizer: Scaling Audio Tokenizers for Future Audio Foundation Models}, 
      author={Yitian Gong and Kuangwei Chen and Zhaoye Fei and Xiaogui Yang and Ke Chen and Yang Wang and Kexin Huang and Mingshu Chen and Ruixiao Li and Qingyuan Cheng and Shimin Li and Xipeng Qiu},
      year={2026},
      eprint={2602.10934},
      archivePrefix={arXiv},
      primaryClass={cs.SD},
      url={https://arxiv.org/abs/2602.10934}, 
}
```