---
license: mit
language:
- zh
- en
- de
- es
- fr
- ko
- ja
pipeline_tag: text-to-speech
library_name: transformers
tags:
- audio
- text-to-speech
- voice-cloning
- multilingual
- speech-generation
---

<div align="center">
  <img src="./figures/ant-bailing.png" width="60" alt="Ming-3.0-tts Logo" />
  <h1>Ming-3.0-tts-0.5B</h1>
  <p><i>Dense 0.5B multilingual speech synthesis with paralinguistic and free-form control.</i></p>
</div>

<p align="center">
  <span style="white-space: nowrap;"><img src="./figures/icons/github-color.svg" width="18" height="18" alt="" style="display: inline-block; vertical-align: middle; margin: 0;" /> <a href="https://github.com/inclusionAI/Ming-3.0-tts">GitHub</a></span> |
  <span style="white-space: nowrap;"><img src="./figures/icons/technical-report.svg" width="18" height="18" alt="" style="display: inline-block; vertical-align: middle; margin: 0;" /> <a href="https://nomorecoding.github.io/Ming-3.0-tts/">Blog & Demos</a></span> |
  <span style="white-space: nowrap;"><img src="./figures/icons/modelscope-color.svg" width="18" height="18" alt="" style="display: inline-block; vertical-align: middle; margin: 0;" /> <a href="https://modelscope.cn/models/inclusionAI/Ming-3.0-tts-0.5b">ModelScope</a></span>
</p>

This repository contains **Ming-3.0-tts-0.5B**, the dense Ming-3.0-tts checkpoint built on Qwen2.5-0.5B. The checkpoint includes the backbone, DiT head, audio tokenizer, speaker encoder and text tokenizer.

> **Inference requires the [Ming-3.0-tts GitHub repository](https://github.com/inclusionAI/Ming-3.0-tts).** This Hugging Face repository is for checkpoint distribution and does not provide a standalone inference setup. Clone the GitHub repository and follow its README for the current dependencies, inference code and usage instructions. The CLI scripts and Python APIs referenced below are provided by the GitHub repository.

## Model Details

| Item | Value |
| --- | --- |
| Architecture | Dense, Qwen2.5-0.5B backbone |
| Parameters | 0.5B |
| Languages | Chinese, English, German, Spanish, French, Korean, Japanese |
| Dialects | Sichuanese, Cantonese |
| Python API | `ming_tts.MingTTS` |
| CLI | `infer.py` |
| Sample rate | 44.1 kHz |

## Capabilities

- Zero-shot voice cloning from a short reference clip
- Voice Design from a natural-language speaker description
- Free-form control of delivery and speaking style
- Built-in Chinese and English voices
- 14 inline tags for breath, cough, sigh, laughter, hesitation, surprise and question/confirmation sounds in Chinese or English
- Explicit emotion, speed, pitch and volume control
- Multilingual synthesis and Sichuanese/Cantonese dialect control

Recommended built-in voices: **UK_George**, **US_Emma**, **灵小柔** and **灵楷**. See the [voice catalog](https://github.com/inclusionAI/Ming-3.0-tts/blob/main/cookbooks/instruction_en.md#built-in-premium-voices) for the full list and voice descriptions. Use the exact `ip` values shown.

<p align="center">
  <img src="./figures/ming_3.0_tts.png" width="760" alt="Ming-3.0-tts architecture" />
</p>

## Quick Start

### Installation

```bash
git clone https://github.com/inclusionAI/Ming-3.0-tts.git
cd Ming-3.0-tts
pip install -r requirements.txt
```

Tested on NVIDIA H800-80GB and H20-96G with CUDA 12.4. `flash-attn` is optional; inference falls back to PyTorch SDPA.

Numbers, dates, units and symbols are normalized with FST grammars. Install `pynini`, or pass `--no_text_normalization` to skip text normalization:

```bash
conda install -c conda-forge pynini==2.1.6
```

### Download

```bash
pip install "huggingface_hub[cli]"
hf download inclusionAI/Ming-3.0-tts-0.5B --local-dir Ming-3.0-tts-0.5b
```

### CLI Inference

```bash
python infer.py \
  --model_path inclusionAI/Ming-3.0-tts-0.5B \
  --task TTS \
  --language_id Chinese \
  --text "傍晚的风从山口吹过来，远处的云慢慢染成了金色。" \
  --prompt_wav_path data/wavs/10002287-00000094.wav \
  --prompt_text "在此奉劝大家别乱打美白针。" \
  --use_spk_emb \
  --output output/tts.wav
```

### Python API

```python
from ming_tts import MingTTS

model = MingTTS("inclusionAI/Ming-3.0-tts-0.5B")
model.synthesize(
    task="TTS",
    language_id="Chinese",             # English for English text
    text="傍晚的风从山口吹过来，远处的云慢慢染成了金色。",
    prompt_wav_path="data/wavs/10002287-00000094.wav",
    prompt_text="在此奉劝大家别乱打美白针。",
    use_spk_emb=True,
    output_path="output/tts.wav",
)
```

Supported tasks are `TTS`, `FREEFORM`, `VOICE_DESIGN`, `MULTILINGUAL`, `BASIC`, `EMOTION`, `DIALECT` and `IP`. See the [task cookbook](https://github.com/inclusionAI/Ming-3.0-tts/blob/main/cookbooks/instructions.md) for controls and examples.

`MULTILINGUAL` requires `language_id` for German, Spanish, French, Korean or Japanese; `DIALECT` takes no language ID. Freeform uses its own task and cannot be combined with voice design, a built-in voice, emotion, dialect or attribute controls. With a reference clip it follows that voice; without a reference, the instruction can choose the voice.

### Verify the Checkpoint

```bash
python tools/preflight.py --model_path /path/to/Ming-3.0-tts-0.5b
```

## Performance

Benchmark comparisons from the [project README](https://github.com/inclusionAI/Ming-3.0-tts#performance).

**Bold** and <u>underline</u> mark the best and second-best values among the listed open-source models; ties share a mark. Seed-TTS and NVbench-GT are unranked reference rows.

### Zero-shot TTS (Seed-TTS testset)

<table style="border-collapse: collapse; border-top: 1.5px solid black; border-bottom: 1.5px solid black; margin: 16px 0;">
  <thead>
    <tr><th rowspan="2" style="padding: 6px 12px; border: none; border-bottom: 1px solid black;">Model</th><th colspan="2" style="padding: 6px 12px; border: none; border-bottom: 1px solid black;">seed-tts-eval-zh</th><th colspan="2" style="padding: 6px 12px; border: none; border-bottom: 1px solid black;">seed-tts-eval-en</th></tr>
    <tr><th style="padding: 6px 12px; border: none; border-bottom: 1px solid black;">WER ↓</th><th style="padding: 6px 12px; border: none; border-bottom: 1px solid black;">SIM ↑</th><th style="padding: 6px 12px; border: none; border-bottom: 1px solid black;">WER ↓</th><th style="padding: 6px 12px; border: none; border-bottom: 1px solid black;">SIM ↑</th></tr>
  </thead>
  <tbody>
    <tr><td style="padding: 5px 12px; border: none; color: rgb(119, 119, 119);"><i>Seed-TTS</i></td><td align="center" style="padding: 5px 12px; border: none; color: rgb(119, 119, 119);">1.110%</td><td align="center" style="padding: 5px 12px; border: none; color: rgb(119, 119, 119);">0.796</td><td align="center" style="padding: 5px 12px; border: none; color: rgb(119, 119, 119);">2.240%</td><td align="center" style="padding: 5px 12px; border: none; color: rgb(119, 119, 119);">0.762</td></tr>
    <tr><td style="padding: 5px 12px; border: none;">GLM-TTS</td><td align="center" style="padding: 5px 12px; border: none;">1.030%</td><td align="center" style="padding: 5px 12px; border: none;">0.761</td><td align="center" style="padding: 5px 12px; border: none;">2.230%</td><td align="center" style="padding: 5px 12px; border: none;">0.672</td></tr>
    <tr><td style="padding: 5px 12px; border: none;">Qwen3-TTS</td><td align="center" style="padding: 5px 12px; border: none;">1.070%</td><td align="center" style="padding: 5px 12px; border: none;">—</td><td align="center" style="padding: 5px 12px; border: none;">1.390%</td><td align="center" style="padding: 5px 12px; border: none;">—</td></tr>
    <tr><td style="padding: 5px 12px; border: none;">Qwen3-TTS-12Hz-0.6B-Base</td><td align="center" style="padding: 5px 12px; border: none;">0.920%</td><td align="center" style="padding: 5px 12px; border: none;">—</td><td align="center" style="padding: 5px 12px; border: none;"><u>1.320%</u></td><td align="center" style="padding: 5px 12px; border: none;">—</td></tr>
    <tr><td style="padding: 5px 12px; border: none;">Qwen3-TTS-12Hz-1.7B-Base</td><td align="center" style="padding: 5px 12px; border: none;"><u>0.770%</u></td><td align="center" style="padding: 5px 12px; border: none;">—</td><td align="center" style="padding: 5px 12px; border: none;"><b>1.240%</b></td><td align="center" style="padding: 5px 12px; border: none;">—</td></tr>
    <tr><td style="padding: 5px 12px; border: none;">CosyVoice3-0.5B</td><td align="center" style="padding: 5px 12px; border: none;">1.160%</td><td align="center" style="padding: 5px 12px; border: none;"><u>0.780</u></td><td align="center" style="padding: 5px 12px; border: none;">2.020%</td><td align="center" style="padding: 5px 12px; border: none;"><u>0.718</u></td></tr>
    <tr><td style="padding: 5px 12px; border: none;">CosyVoice3-1.5B</td><td align="center" style="padding: 5px 12px; border: none;"><b>0.710%</b></td><td align="center" style="padding: 5px 12px; border: none;">0.775</td><td align="center" style="padding: 5px 12px; border: none;">1.450%</td><td align="center" style="padding: 5px 12px; border: none;">0.695</td></tr>
    <tr><td style="padding: 5px 12px; border: none;">F5-TTS</td><td align="center" style="padding: 5px 12px; border: none;">1.560%</td><td align="center" style="padding: 5px 12px; border: none;">0.741</td><td align="center" style="padding: 5px 12px; border: none;">1.830%</td><td align="center" style="padding: 5px 12px; border: none;">0.647</td></tr>
    <tr><td style="padding: 5px 12px; border: none; border-top: 1px solid black;"><b>Ming-3.0-tts-0.5b</b></td><td align="center" style="padding: 5px 12px; border: none; border-top: 1px solid black;">0.800%</td><td align="center" style="padding: 5px 12px; border: none; border-top: 1px solid black;">0.758</td><td align="center" style="padding: 5px 12px; border: none; border-top: 1px solid black;">1.584%</td><td align="center" style="padding: 5px 12px; border: none; border-top: 1px solid black;">0.691</td></tr>
    <tr><td style="padding: 5px 12px; border: none;"><b>Ming-3.0-tts-tiny</b></td><td align="center" style="padding: 5px 12px; border: none;">0.820%</td><td align="center" style="padding: 5px 12px; border: none;"><b>0.781</b></td><td align="center" style="padding: 5px 12px; border: none;">1.666%</td><td align="center" style="padding: 5px 12px; border: none;"><b>0.728</b></td></tr>
  </tbody>
</table>

### Multilingual (MiniMax test set, selected languages)

Evaluated on the German, Spanish, French, Korean, and Japanese subsets of [MiniMaxAI/TTS-Multilingual-Test-Set](https://huggingface.co/datasets/MiniMaxAI/TTS-Multilingual-Test-Set).

<table style="border-collapse: collapse; border-top: 1.5px solid black; border-bottom: 1.5px solid black; margin: 16px 0;">
  <thead>
    <tr><th rowspan="2" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Model</th><th colspan="2" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">German</th><th colspan="2" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Spanish</th><th colspan="2" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">French</th><th colspan="2" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Korean</th><th colspan="2" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Japanese</th></tr>
    <tr><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">WER ↓</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">SIM ↑</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">WER ↓</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">SIM ↑</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">WER ↓</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">SIM ↑</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">CER ↓</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">SIM ↑</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">CER ↓</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">SIM ↑</th></tr>
  </thead>
  <tbody>
    <tr><td style="padding: 5px 10px; border: none;">dots.tts</td><td align="center" style="padding: 5px 10px; border: none;">0.452%</td><td align="center" style="padding: 5px 10px; border: none;"><u>0.798</u></td><td align="center" style="padding: 5px 10px; border: none;">2.593%</td><td align="center" style="padding: 5px 10px; border: none;"><u>0.839</u></td><td align="center" style="padding: 5px 10px; border: none;">19.878%</td><td align="center" style="padding: 5px 10px; border: none;"><u>0.789</u></td><td align="center" style="padding: 5px 10px; border: none;">4.837%</td><td align="center" style="padding: 5px 10px; border: none;"><u>0.853</u></td><td align="center" style="padding: 5px 10px; border: none;">5.134%</td><td align="center" style="padding: 5px 10px; border: none;"><b>0.838</b></td></tr>
    <tr><td style="padding: 5px 10px; border: none;">VoxCPM2</td><td align="center" style="padding: 5px 10px; border: none;">0.963%</td><td align="center" style="padding: 5px 10px; border: none;">0.790</td><td align="center" style="padding: 5px 10px; border: none;">1.324%</td><td align="center" style="padding: 5px 10px; border: none;">0.836</td><td align="center" style="padding: 5px 10px; border: none;"><b>3.380%</b></td><td align="center" style="padding: 5px 10px; border: none;">0.761</td><td align="center" style="padding: 5px 10px; border: none;">3.547%</td><td align="center" style="padding: 5px 10px; border: none;">0.839</td><td align="center" style="padding: 5px 10px; border: none;">4.358%</td><td align="center" style="padding: 5px 10px; border: none;"><u>0.825</u></td></tr>
    <tr><td style="padding: 5px 10px; border: none;">Fish Audio S2</td><td align="center" style="padding: 5px 10px; border: none;">1.045%</td><td align="center" style="padding: 5px 10px; border: none;">0.714</td><td align="center" style="padding: 5px 10px; border: none;">1.216%</td><td align="center" style="padding: 5px 10px; border: none;">0.748</td><td align="center" style="padding: 5px 10px; border: none;">3.636%</td><td align="center" style="padding: 5px 10px; border: none;">0.698</td><td align="center" style="padding: 5px 10px; border: none;"><u>1.675%</u></td><td align="center" style="padding: 5px 10px; border: none;">0.761</td><td align="center" style="padding: 5px 10px; border: none;"><u>3.427%</u></td><td align="center" style="padding: 5px 10px; border: none;">0.755</td></tr>
    <tr><td style="padding: 5px 10px; border: none;">FireRedTTS3</td><td align="center" style="padding: 5px 10px; border: none;"><u>0.348%</u></td><td align="center" style="padding: 5px 10px; border: none;"><b>0.825</b></td><td align="center" style="padding: 5px 10px; border: none;"><u>1.086%</u></td><td align="center" style="padding: 5px 10px; border: none;"><b>0.868</b></td><td align="center" style="padding: 5px 10px; border: none;">4.366%</td><td align="center" style="padding: 5px 10px; border: none;"><b>0.807</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>1.644%</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>0.864</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>3.418%</b></td><td align="center" style="padding: 5px 10px; border: none;"><u>0.825</u></td></tr>
    <tr><td style="padding: 5px 10px; border: none; border-top: 1px solid black;"><b>Ming-3.0-tts-0.5b</b></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">0.365%</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">0.753</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">1.099%</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">0.763</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">4.264%</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">0.675</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">1.728%</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">0.793</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">3.765%</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">0.765</td></tr>
    <tr><td style="padding: 5px 10px; border: none;"><b>Ming-3.0-tts-tiny</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>0.325%</b></td><td align="center" style="padding: 5px 10px; border: none;">0.791</td><td align="center" style="padding: 5px 10px; border: none;"><b>0.971%</b></td><td align="center" style="padding: 5px 10px; border: none;">0.797</td><td align="center" style="padding: 5px 10px; border: none;"><u>3.470%</u></td><td align="center" style="padding: 5px 10px; border: none;">0.733</td><td align="center" style="padding: 5px 10px; border: none;">6.000%</td><td align="center" style="padding: 5px 10px; border: none;">0.797</td><td align="center" style="padding: 5px 10px; border: none;"><u>3.427%</u></td><td align="center" style="padding: 5px 10px; border: none;">0.780</td></tr>
  </tbody>
</table>

<p><small>Each open-source model was evaluated using its recommended inference settings under a unified ASR-based WER/CER evaluation protocol.</small></p>

### Paralinguistic Control (NVBench)

<table style="border-collapse: collapse; border-top: 1.5px solid black; border-bottom: 1.5px solid black; margin: 16px 0;">
  <thead>
    <tr><th rowspan="3" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">Model</th><th colspan="6" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">Single</th><th colspan="6" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">Multi</th></tr>
    <tr><th colspan="3" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">Chinese</th><th colspan="3" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">English</th><th colspan="3" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">Chinese</th><th colspan="3" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">English</th></tr>
    <tr><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">CER</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">PCER</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">OCER</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">CER</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">PCER</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">OCER</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">CER</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">PCER</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">OCER</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">CER</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">PCER</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">OCER</th></tr>
  </thead>
  <tbody>
    <tr><td style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);"><i>NVbench-GT</i></td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">3.86</td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">9.38</td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">4.07</td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">6.73</td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">8.31</td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">6.90</td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">3.79</td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">23.71</td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">5.07</td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">7.26</td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">21.41</td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">8.62</td></tr>
    <tr><td style="padding: 5px 8px; border: none;">Orpheus-TTS</td><td align="center" style="padding: 5px 8px; border: none;">11.36</td><td align="center" style="padding: 5px 8px; border: none;">88.77</td><td align="center" style="padding: 5px 8px; border: none;">13.91</td><td align="center" style="padding: 5px 8px; border: none;">9.03</td><td align="center" style="padding: 5px 8px; border: none;">71.92</td><td align="center" style="padding: 5px 8px; border: none;">10.63</td><td align="center" style="padding: 5px 8px; border: none;">19.83</td><td align="center" style="padding: 5px 8px; border: none;">84.85</td><td align="center" style="padding: 5px 8px; border: none;">24.38</td><td align="center" style="padding: 5px 8px; border: none;">8.68</td><td align="center" style="padding: 5px 8px; border: none;">71.46</td><td align="center" style="padding: 5px 8px; border: none;">11.89</td></tr>
    <tr><td style="padding: 5px 8px; border: none;">SMIIP-NV-CV2</td><td align="center" style="padding: 5px 8px; border: none;">8.80</td><td align="center" style="padding: 5px 8px; border: none;">75.64</td><td align="center" style="padding: 5px 8px; border: none;">11.34</td><td align="center" style="padding: 5px 8px; border: none;">17.92</td><td align="center" style="padding: 5px 8px; border: none;">56.80</td><td align="center" style="padding: 5px 8px; border: none;">19.47</td><td align="center" style="padding: 5px 8px; border: none;">10.66</td><td align="center" style="padding: 5px 8px; border: none;">77.20</td><td align="center" style="padding: 5px 8px; border: none;">14.79</td><td align="center" style="padding: 5px 8px; border: none;">20.93</td><td align="center" style="padding: 5px 8px; border: none;">54.49</td><td align="center" style="padding: 5px 8px; border: none;">23.87</td></tr>
    <tr><td style="padding: 5px 8px; border: none;">Emilia-NV-CV2</td><td align="center" style="padding: 5px 8px; border: none;">5.05</td><td align="center" style="padding: 5px 8px; border: none;">40.00</td><td align="center" style="padding: 5px 8px; border: none;">6.64</td><td align="center" style="padding: 5px 8px; border: none;">12.50</td><td align="center" style="padding: 5px 8px; border: none;">55.30</td><td align="center" style="padding: 5px 8px; border: none;">13.21</td><td align="center" style="padding: 5px 8px; border: none;">5.54</td><td align="center" style="padding: 5px 8px; border: none;">48.74</td><td align="center" style="padding: 5px 8px; border: none;">8.09</td><td align="center" style="padding: 5px 8px; border: none;">11.71</td><td align="center" style="padding: 5px 8px; border: none;">60.28</td><td align="center" style="padding: 5px 8px; border: none;">14.63</td></tr>
    <tr><td style="padding: 5px 8px; border: none;">CosyVoice3</td><td align="center" style="padding: 5px 8px; border: none;">3.85</td><td align="center" style="padding: 5px 8px; border: none;">57.69</td><td align="center" style="padding: 5px 8px; border: none;">5.86</td><td align="center" style="padding: 5px 8px; border: none;">7.87</td><td align="center" style="padding: 5px 8px; border: none;">62.75</td><td align="center" style="padding: 5px 8px; border: none;">9.06</td><td align="center" style="padding: 5px 8px; border: none;">4.75</td><td align="center" style="padding: 5px 8px; border: none;">61.94</td><td align="center" style="padding: 5px 8px; border: none;">8.26</td><td align="center" style="padding: 5px 8px; border: none;"><u>6.39</u></td><td align="center" style="padding: 5px 8px; border: none;">57.84</td><td align="center" style="padding: 5px 8px; border: none;">10.69</td></tr>
    <tr><td style="padding: 5px 8px; border: none;">NV-FlexiVoice</td><td align="center" style="padding: 5px 8px; border: none;">6.98</td><td align="center" style="padding: 5px 8px; border: none;">31.08</td><td align="center" style="padding: 5px 8px; border: none;">8.15</td><td align="center" style="padding: 5px 8px; border: none;">11.88</td><td align="center" style="padding: 5px 8px; border: none;">50.43</td><td align="center" style="padding: 5px 8px; border: none;">13.21</td><td align="center" style="padding: 5px 8px; border: none;">8.20</td><td align="center" style="padding: 5px 8px; border: none;">39.37</td><td align="center" style="padding: 5px 8px; border: none;">10.39</td><td align="center" style="padding: 5px 8px; border: none;">9.60</td><td align="center" style="padding: 5px 8px; border: none;">51.32</td><td align="center" style="padding: 5px 8px; border: none;">13.76</td></tr>
    <tr><td style="padding: 5px 8px; border: none;">NV-CV3</td><td align="center" style="padding: 5px 8px; border: none;">3.80</td><td align="center" style="padding: 5px 8px; border: none;">27.69</td><td align="center" style="padding: 5px 8px; border: none;"><u>4.90</u></td><td align="center" style="padding: 5px 8px; border: none;">8.33</td><td align="center" style="padding: 5px 8px; border: none;">46.13</td><td align="center" style="padding: 5px 8px; border: none;">9.44</td><td align="center" style="padding: 5px 8px; border: none;"><b>3.44</b></td><td align="center" style="padding: 5px 8px; border: none;"><b>30.04</b></td><td align="center" style="padding: 5px 8px; border: none;"><b>4.84</b></td><td align="center" style="padding: 5px 8px; border: none;">6.70</td><td align="center" style="padding: 5px 8px; border: none;"><u>47.13</u></td><td align="center" style="padding: 5px 8px; border: none;"><u>10.10</u></td></tr>
    <tr><td style="padding: 5px 8px; border: none; border-top: 1px solid black;"><b>Ming-3.0-tts-0.5b</b></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><b>2.70</b></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><u>22.80</u></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><b>3.20</b></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><u>7.60</u></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><u>37.00</u></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><u>8.90</u></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><u>3.50</u></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;">36.60</td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;">8.10</td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;">7.90</td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;">47.30</td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;">10.40</td></tr>
    <tr><td style="padding: 5px 8px; border: none;"><b>Ming-3.0-tts-tiny</b></td><td align="center" style="padding: 5px 8px; border: none;"><u>2.80</u></td><td align="center" style="padding: 5px 8px; border: none;"><b>17.23</b></td><td align="center" style="padding: 5px 8px; border: none;"><b>3.20</b></td><td align="center" style="padding: 5px 8px; border: none;"><b>5.86</b></td><td align="center" style="padding: 5px 8px; border: none;"><b>32.95</b></td><td align="center" style="padding: 5px 8px; border: none;"><b>7.05</b></td><td align="center" style="padding: 5px 8px; border: none;">4.49</td><td align="center" style="padding: 5px 8px; border: none;"><u>32.88</u></td><td align="center" style="padding: 5px 8px; border: none;"><u>5.81</u></td><td align="center" style="padding: 5px 8px; border: none;"><b>5.12</b></td><td align="center" style="padding: 5px 8px; border: none;"><b>46.13</b></td><td align="center" style="padding: 5px 8px; border: none;"><b>7.68</b></td></tr>
  </tbody>
</table>

### Dialect Control

<table style="border-collapse: collapse; border-top: 1.5px solid black; border-bottom: 1.5px solid black; margin: 16px 0;">
  <thead>
    <tr><th rowspan="2" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">Model</th><th colspan="3" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">WSC-Eval-TTS-easy</th><th colspan="3" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">WSC-Eval-TTS-hard</th><th colspan="3" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">WSYue-TTS-eval-Base</th><th colspan="3" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">WSYue-TTS-eval-Coverage</th></tr>
    <tr><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">CER ↓</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">SIM ↑</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">ACC ↑</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">CER ↓</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">SIM ↑</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">ACC ↑</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">CER ↓</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">SIM ↑</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">ACC ↑</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">CER ↓</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">SIM ↑</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">ACC ↑</th></tr>
  </thead>
  <tbody>
    <tr><td style="padding: 5px 8px; border: none;">Qwen3-TTS</td><td align="center" style="padding: 5px 8px; border: none;">4.13%</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">7.35%</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td></tr>
    <tr><td style="padding: 5px 8px; border: none;">CosyVoice3-0.5B</td><td align="center" style="padding: 5px 8px; border: none;">3.17%</td><td align="center" style="padding: 5px 8px; border: none;">0.696</td><td align="center" style="padding: 5px 8px; border: none;">76.05%</td><td align="center" style="padding: 5px 8px; border: none;">4.07%</td><td align="center" style="padding: 5px 8px; border: none;"><u>0.723</u></td><td align="center" style="padding: 5px 8px; border: none;">81.41%</td><td align="center" style="padding: 5px 8px; border: none;">8.36%</td><td align="center" style="padding: 5px 8px; border: none;">0.611</td><td align="center" style="padding: 5px 8px; border: none;">91.70%</td><td align="center" style="padding: 5px 8px; border: none;">8.95%</td><td align="center" style="padding: 5px 8px; border: none;">0.658</td><td align="center" style="padding: 5px 8px; border: none;"><b>95.80%</b></td></tr>
    <tr><td style="padding: 5px 8px; border: none;">CosyVoice3-1.5B + DiffRO-EMO</td><td align="center" style="padding: 5px 8px; border: none;">7.14%</td><td align="center" style="padding: 5px 8px; border: none;">0.703</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">9.06%</td><td align="center" style="padding: 5px 8px; border: none;">0.601</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">14.38%</td><td align="center" style="padding: 5px 8px; border: none;"><u>0.812</u></td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">13.74%</td><td align="center" style="padding: 5px 8px; border: none;"><u>0.826</u></td><td align="center" style="padding: 5px 8px; border: none;">—</td></tr>
    <tr><td style="padding: 5px 8px; border: none;">CosyVoice2-WSC</td><td align="center" style="padding: 5px 8px; border: none;">4.28%</td><td align="center" style="padding: 5px 8px; border: none;"><u>0.728</u></td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">8.87%</td><td align="center" style="padding: 5px 8px; border: none;">0.626</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td></tr>
    <tr><td style="padding: 5px 8px; border: none;">CosyVoice2-WSC-SFT</td><td align="center" style="padding: 5px 8px; border: none;">4.08%</td><td align="center" style="padding: 5px 8px; border: none;"><b>0.788</b></td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">7.22%</td><td align="center" style="padding: 5px 8px; border: none;">0.680</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td></tr>
    <tr><td style="padding: 5px 8px; border: none;">CosyVoice2-Yue</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">10.33%</td><td align="center" style="padding: 5px 8px; border: none;"><b>0.821</b></td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">9.49%</td><td align="center" style="padding: 5px 8px; border: none;"><b>0.834</b></td><td align="center" style="padding: 5px 8px; border: none;">—</td></tr>
    <tr><td style="padding: 5px 8px; border: none;">Sparks-TTS</td><td align="center" style="padding: 5px 8px; border: none;">10.83%</td><td align="center" style="padding: 5px 8px; border: none;">0.677</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">12.52%</td><td align="center" style="padding: 5px 8px; border: none;">0.545</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">27.79%</td><td align="center" style="padding: 5px 8px; border: none;">0.762</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">24.25%</td><td align="center" style="padding: 5px 8px; border: none;">0.781</td><td align="center" style="padding: 5px 8px; border: none;">—</td></tr>
    <tr><td style="padding: 5px 8px; border: none; border-top: 1px solid black;"><b>Ming-3.0-tts-0.5b</b></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><b>2.27%</b></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;">0.689</td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><u>80.68%</u></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><u>3.35%</u></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;">0.691</td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><u>87.64%</u></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><b>6.15%</b></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;">0.586</td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><b>98.00%</b></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><b>8.15%</b></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;">0.622</td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><u>95.27%</u></td></tr>
    <tr><td style="padding: 5px 8px; border: none;"><b>Ming-3.0-tts-tiny</b></td><td align="center" style="padding: 5px 8px; border: none;"><u>2.53%</u></td><td align="center" style="padding: 5px 8px; border: none;">0.721</td><td align="center" style="padding: 5px 8px; border: none;"><b>86.09%</b></td><td align="center" style="padding: 5px 8px; border: none;"><b>3.11%</b></td><td align="center" style="padding: 5px 8px; border: none;"><b>0.738</b></td><td align="center" style="padding: 5px 8px; border: none;"><b>88.94%</b></td><td align="center" style="padding: 5px 8px; border: none;"><u>7.40%</u></td><td align="center" style="padding: 5px 8px; border: none;">0.605</td><td align="center" style="padding: 5px 8px; border: none;"><u>92.90%</u></td><td align="center" style="padding: 5px 8px; border: none;"><u>8.67%</u></td><td align="center" style="padding: 5px 8px; border: none;">0.653</td><td align="center" style="padding: 5px 8px; border: none;">95.16%</td></tr>
  </tbody>
</table>

### Emotion Control (CV3)

<table style="border-collapse: collapse; border-top: 1.5px solid black; border-bottom: 1.5px solid black; margin: 16px 0;">
  <thead>
    <tr><th rowspan="2" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Model</th><th rowspan="2" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Average</th><th colspan="3" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Text-Related</th><th colspan="3" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Text-Unrelated</th></tr>
    <tr><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Happy</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Sad</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Angry</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Happy</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Sad</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Angry</th></tr>
  </thead>
  <tbody>
    <tr><td style="padding: 5px 10px; border: none;">CosyVoice3-0.5B</td><td align="center" style="padding: 5px 10px; border: none;">66.33%</td><td align="center" style="padding: 5px 10px; border: none;">92%</td><td align="center" style="padding: 5px 10px; border: none;">70%</td><td align="center" style="padding: 5px 10px; border: none;">72%</td><td align="center" style="padding: 5px 10px; border: none;">64%</td><td align="center" style="padding: 5px 10px; border: none;">42%</td><td align="center" style="padding: 5px 10px; border: none;">58%</td></tr>
    <tr><td style="padding: 5px 10px; border: none;">CosyVoice3-1.5B</td><td align="center" style="padding: 5px 10px; border: none;">63.00%</td><td align="center" style="padding: 5px 10px; border: none;">86%</td><td align="center" style="padding: 5px 10px; border: none;">64%</td><td align="center" style="padding: 5px 10px; border: none;">72%</td><td align="center" style="padding: 5px 10px; border: none;">64%</td><td align="center" style="padding: 5px 10px; border: none;">44%</td><td align="center" style="padding: 5px 10px; border: none;">48%</td></tr>
    <tr><td style="padding: 5px 10px; border: none;">CosyVoice3-1.5B + DiffRO-EMO</td><td align="center" style="padding: 5px 10px; border: none;"><b>77.67%</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>98%</b></td><td align="center" style="padding: 5px 10px; border: none;">68%</td><td align="center" style="padding: 5px 10px; border: none;">84%</td><td align="center" style="padding: 5px 10px; border: none;"><b>98%</b></td><td align="center" style="padding: 5px 10px; border: none;"><u>50%</u></td><td align="center" style="padding: 5px 10px; border: none;">68%</td></tr>
    <tr><td style="padding: 5px 10px; border: none;">F5-TTS</td><td align="center" style="padding: 5px 10px; border: none;">64.67%</td><td align="center" style="padding: 5px 10px; border: none;">92%</td><td align="center" style="padding: 5px 10px; border: none;">52%</td><td align="center" style="padding: 5px 10px; border: none;">72%</td><td align="center" style="padding: 5px 10px; border: none;"><u>80%</u></td><td align="center" style="padding: 5px 10px; border: none;">28%</td><td align="center" style="padding: 5px 10px; border: none;">64%</td></tr>
    <tr><td style="padding: 5px 10px; border: none;">Sparks-TTS</td><td align="center" style="padding: 5px 10px; border: none;">55.33%</td><td align="center" style="padding: 5px 10px; border: none;">80%</td><td align="center" style="padding: 5px 10px; border: none;">56%</td><td align="center" style="padding: 5px 10px; border: none;">50%</td><td align="center" style="padding: 5px 10px; border: none;">50%</td><td align="center" style="padding: 5px 10px; border: none;"><b>60%</b></td><td align="center" style="padding: 5px 10px; border: none;">36%</td></tr>
    <tr><td style="padding: 5px 10px; border: none; border-top: 1px solid black;"><b>Ming-3.0-tts-0.5b</b></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">72.33%</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>96%</u></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>76%</u></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><b>94%</b></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">52%</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">36%</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><b>80%</b></td></tr>
    <tr><td style="padding: 5px 10px; border: none;"><b>Ming-3.0-tts-tiny</b></td><td align="center" style="padding: 5px 10px; border: none;"><u>74.00%</u></td><td align="center" style="padding: 5px 10px; border: none;"><b>98%</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>82%</b></td><td align="center" style="padding: 5px 10px; border: none;"><u>90%</u></td><td align="center" style="padding: 5px 10px; border: none;">60%</td><td align="center" style="padding: 5px 10px; border: none;">36%</td><td align="center" style="padding: 5px 10px; border: none;"><u>78%</u></td></tr>
  </tbody>
</table>

### Emotion Control (CV3N, hard emotion control)

<table style="border-collapse: collapse; border-top: 1.5px solid black; border-bottom: 1.5px solid black; margin: 16px 0;">
  <thead>
    <tr><th rowspan="2" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Model</th><th rowspan="2" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Average</th><th colspan="3" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Text-Related</th><th colspan="3" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Text-Unrelated</th></tr>
    <tr><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Happy</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Sad</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Angry</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Happy</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Sad</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Angry</th></tr>
  </thead>
  <tbody>
    <tr><td style="padding: 5px 10px; border: none;">CosyVoice3-0.5B</td><td align="center" style="padding: 5px 10px; border: none;"><b>40.00%</b></td><td align="center" style="padding: 5px 10px; border: none;"><u>68%</u></td><td align="center" style="padding: 5px 10px; border: none;">30%</td><td align="center" style="padding: 5px 10px; border: none;"><b>78%</b></td><td align="center" style="padding: 5px 10px; border: none;"><u>14%</u></td><td align="center" style="padding: 5px 10px; border: none;"><u>4%</u></td><td align="center" style="padding: 5px 10px; border: none;"><b>46%</b></td></tr>
    <tr><td style="padding: 5px 10px; border: none; border-top: 1px solid black;"><b>Ming-3.0-tts-0.5b</b></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>37.33%</u></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><b>70%</b></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>36%</u></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>70%</u></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>14%</u></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>4%</u></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>30%</u></td></tr>
    <tr><td style="padding: 5px 10px; border: none;"><b>Ming-3.0-tts-tiny</b></td><td align="center" style="padding: 5px 10px; border: none;">30.67%</td><td align="center" style="padding: 5px 10px; border: none;">60%</td><td align="center" style="padding: 5px 10px; border: none;"><b>40%</b></td><td align="center" style="padding: 5px 10px; border: none;">44%</td><td align="center" style="padding: 5px 10px; border: none;"><b>18%</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>10%</b></td><td align="center" style="padding: 5px 10px; border: none;">12%</td></tr>
  </tbody>
</table>

### Voice Design (InstructTTSEval-ZH)

<table style="border-collapse: collapse; border-top: 1.5px solid black; border-bottom: 1.5px solid black; margin: 16px 0;">
  <thead>
    <tr><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Model</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Average</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">APS</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">DSD</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">RP</th></tr>
  </thead>
  <tbody>
    <tr><td style="padding: 5px 10px; border: none;">Qwen3-TTS</td><td align="center" style="padding: 5px 10px; border: none;"><b>77.13%</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>85.20%</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>81.10%</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>65.10%</b></td></tr>
    <tr><td style="padding: 5px 10px; border: none;">Mimo-Audio-7B-Instruct</td><td align="center" style="padding: 5px 10px; border: none;">70.50%</td><td align="center" style="padding: 5px 10px; border: none;">75.70%</td><td align="center" style="padding: 5px 10px; border: none;">74.30%</td><td align="center" style="padding: 5px 10px; border: none;"><u>61.50%</u></td></tr>
    <tr><td style="padding: 5px 10px; border: none;">VoiceSculptor</td><td align="center" style="padding: 5px 10px; border: none;">67.30%</td><td align="center" style="padding: 5px 10px; border: none;">75.70%</td><td align="center" style="padding: 5px 10px; border: none;">64.70%</td><td align="center" style="padding: 5px 10px; border: none;"><u>61.50%</u></td></tr>
    <tr><td style="padding: 5px 10px; border: none;">VoxInstruct</td><td align="center" style="padding: 5px 10px; border: none;">47.47%</td><td align="center" style="padding: 5px 10px; border: none;">47.50%</td><td align="center" style="padding: 5px 10px; border: none;">52.30%</td><td align="center" style="padding: 5px 10px; border: none;">42.60%</td></tr>
    <tr><td style="padding: 5px 10px; border: none; border-top: 1px solid black;"><b>Ming-3.0-tts-0.5b</b></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">72.29%</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">78.54%</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">77.28%</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">61.06%</td></tr>
    <tr><td style="padding: 5px 10px; border: none;"><b>Ming-3.0-tts-tiny</b></td><td align="center" style="padding: 5px 10px; border: none;"><u>75.37%</u></td><td align="center" style="padding: 5px 10px; border: none;"><u>85.10%</u></td><td align="center" style="padding: 5px 10px; border: none;"><u>79.90%</u></td><td align="center" style="padding: 5px 10px; border: none;">61.10%</td></tr>
  </tbody>
</table>

### Basic Attribute Control

<table style="border-collapse: collapse; border-top: 1.5px solid black; border-bottom: 1.5px solid black; margin: 16px 0;">
  <thead>
    <tr><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Model</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Speed</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Volume</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Pitch</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Average</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">WER ↓</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">SIM ↑</th></tr>
  </thead>
  <tbody>
    <tr><td style="padding: 5px 10px; border: none;">CosyVoice3-0.5B</td><td align="center" style="padding: 5px 10px; border: none;"><b>100.00%</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>97.67%</b></td><td align="center" style="padding: 5px 10px; border: none;">65.33%</td><td align="center" style="padding: 5px 10px; border: none;">87.67%</td><td align="center" style="padding: 5px 10px; border: none;">1.210%</td><td align="center" style="padding: 5px 10px; border: none;">0.580</td></tr>
    <tr><td style="padding: 5px 10px; border: none; border-top: 1px solid black;"><b>Ming-3.0-tts-0.5b</b></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>99.00%</u></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>95.00%</u></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><b>86.00%</b></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><b>93.30%</b></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>0.317%</u></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>0.712</u></td></tr>
    <tr><td style="padding: 5px 10px; border: none;"><b>Ming-3.0-tts-tiny</b></td><td align="center" style="padding: 5px 10px; border: none;">93.00%</td><td align="center" style="padding: 5px 10px; border: none;">93.00%</td><td align="center" style="padding: 5px 10px; border: none;"><u>78.70%</u></td><td align="center" style="padding: 5px 10px; border: none;"><u>88.23%</u></td><td align="center" style="padding: 5px 10px; border: none;"><b>0.274%</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>0.742</b></td></tr>
  </tbody>
</table>

## Limitations

- Speaker similarity is weaker than content accuracy; French SIM is the clearest multilingual gap.
- NVBench Multi trails Single; stability with several paralinguistic events in one sentence is still improving.
- Emotion control is harder when the words carry no emotional signal.
- Pitch is less accurate than speed and volume, and open-ended Voice Design does not yet match the strongest evaluated system.

## Usage Disclaimer

- Voice cloning and built-in character voices are provided for research and legitimate creative use. Do not use them to impersonate a real person without consent, to deceive, or for any illegal purpose.
- Label synthetic speech as synthetic where it could be mistaken for a real recording.
- The authors accept no liability for misuse. If you find abuse of this project, please report it to us.

## Acknowledgements

- [Qwen2.5](https://github.com/QwenLM/Qwen2.5) for the backbone
- [CAM++](https://modelscope.cn/models/iic/speech_campplus_sv_zh-cn_16k-common) for speaker embedding extraction
- [Ming-omni-tts](https://github.com/inclusionAI/Ming-omni-tts), the previous generation, whose audio tokenizer this release builds on

## License

Released under the [MIT license](https://github.com/inclusionAI/Ming-3.0-tts/blob/main/LICENSE).
