---
language:
- en
- zh
license: apache-2.0
pipeline_tag: audio-to-audio
---

# MeanVC2: Robust Low-Latency Streaming Zero-Shot Voice Conversion

<div align="center">

[![Paper](https://img.shields.io/badge/arXiv-Paper-b31b1b.svg)](https://arxiv.org/)
[![Github](https://img.shields.io/badge/Github-ASLP--lab/MeanVC2-green)](https://github.com/ASLP-lab/MeanVC2)
[![Demo Page](https://img.shields.io/badge/Demo-Audio%20Samples-green)](https://aslp-lab.github.io/MeanVC2/)

</div>

**MeanVC2** is a robust, low-latency streaming zero-shot voice conversion (VC) system built upon the diffusion-based conditional flow matching (CFM) framework. By introducing **Future-Receptive Chunking (FRC)** and a **Universal Timbre Token Encoder (UTTE)**, MeanVC2 achieves high-fidelity voice conversion with an end-to-end pipeline latency of only **110 ms** while maintaining superior speaker similarity and audio naturalness even with a **40 ms chunk size**.

![img](https://huggingface.co/ASLP-lab/MeanVC2/resolve/main/figs/model.png)

## ✨ Key Features

- **🚀 Ultra-Low Latency Streaming**: 110 ms end-to-end first-packet latency with 40 ms chunk size; full pipeline RTF < 0.633 on single CPU core.
- **⚡ Single-Step Generation**: Mean flows + 1-NFE ODE solving for high-quality mel-spectrogram synthesis.
- **🎯 Zero-Shot Capability**: Convert to any unseen target speaker without re-training, robust under low-quality reference audio.
- **💾 Lightweight**: Only 18M parameters — far smaller than competing streaming VC systems.
- **🔊 High Fidelity**: Future-Receptive Chunking (FRC) with Universal Timbre Token Encoder (UTTE) for pronunciation-aware timbre modeling.

## 📁 Model Checkpoints

This repository hosts all pretrained models for MeanVC2:

### Voice Conversion Models

| File | Description |
|------|-------------|
| `meanvc2_120ms_40ms.safetensors` | 120ms chunk + 40ms future (recommended for quality) |
| `meanvc2_40ms_40ms.safetensors` | 40ms chunk + 40ms future (lower latency) |

### Vocoder (JIT)

| File | Description |
|------|-------------|
| `vocos.pt` | Vocos JIT-traced vocoder |

### ASR Encoder (Fast-U2++ JIT)

| File | Description |
|------|-------------|
| `fastu2pp_80ms.pt` | 80ms chunk JIT model (11-frame window, stride=8) |
| `fastu2pp_160ms.pt` | 160ms chunk JIT model (19-frame window, stride=16) |

## 💻 Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/ASLP-lab/MeanVC2.git
cd MeanVC2

conda create -n meanvc2 python=3.11 -y
conda activate meanvc2

pip install torch==2.5.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
```

### 2. Download Pretrained Models

```bash
python initialization.py --task all
```

Or download selectively:

```bash
python initialization.py --task preprocess   # BN + SpkEmb extraction only
python initialization.py --task train_120ms  # preprocess + 120ms VC + vocoder
python initialization.py --task train_40ms   # preprocess + 40ms VC + vocoder
```

### 3. End-to-End Voice Conversion

No pre-extracted features needed — input two wavs, output converted audio:

```bash
# 120ms+40ms model (recommended for quality)
python src/infer/infer_e2e.py \
    --source-wav /path/to/source.wav \
    --target-wav /path/to/target.wav \
    --ckpt-path ckpts/pretrained_models/meanvc2_120ms_40ms.safetensors \
    --model-config src/config/config_120ms_40ms.json \
    --vocoder-ckpt-path ckpts/vocos/vocos.pt \
    --chunk-size 12 --steps 3 \
    --output-wav output.wav

# 40ms+40ms model (lower latency)
python src/infer/infer_e2e.py \
    --source-wav /path/to/source.wav \
    --target-wav /path/to/target.wav \
    --ckpt-path ckpts/pretrained_models/meanvc2_40ms_40ms.safetensors \
    --model-config src/config/config_40ms_40ms.json \
    --vocoder-ckpt-path ckpts/vocos/vocos.pt \
    --chunk-size 4 --steps 3 \
    --output-wav output.wav
```

### 4. Real-Time Streaming

```bash
cd runtime

# File mode
python run_rt.py --mode file --input in.wav --output out.wav --model 120ms

# Microphone mode
python run_rt.py --mode realtime --model 40ms
```

## 🏗️ Model Architecture

| Component | Description |
|-----------|-------------|
| **Streaming ASR Encoder** | Fast-U2++ (WeNet) extracts bottleneck features (BNFs) from source waveform |
| **Speaker Encoder** | ECAPA-TDNN + WavLM upstream extracts global speaker embedding from reference audio |
| **Universal Timbre Token Encoder (UTTE)** | Transforms speaker embedding into K key-value UTT pairs; BNFs serve as queries in cross-attention for fine-grained, pronunciation-aware timbre cues |
| **DiT-based CFM Decoder** | 4-layer DiT (hidden dim 512, 2 heads) with Future-Receptive Chunking (FRC); trained with mean flows objective for 1-NFE mel-spectrogram generation |
| **Vocoder** | Vocos converts mel-spectrograms to 16 kHz high-fidelity speech waveforms |

**Total parameters**: ~18M

## 📜 License & Disclaimer

MeanVC2 is released under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0). This open-source license allows you to freely use, modify, and distribute the model, as long as you include the appropriate copyright notice and disclaimer.

MeanVC2 is designed for research and legitimate applications in voice conversion technology. Users must obtain proper consent from individuals whose voices are being converted or used as references. We strongly discourage malicious use including impersonation, fraud, or creating misleading audio content. Users are solely responsible for ensuring compliance with ethical standards and legal requirements.

## 📄 Citation

If you find our work helpful, please cite:

```bibtex
@article{ma2026meanvc2,
  title={MeanVC2: Robust Low-Latency Streaming Zero-Shot Voice Conversion},
  author={Ma, Guobin and Xia, Yuxuan and Jiang, Yuepeng and Guo, Dake and Xie, Hanke and Hu, Jingbin and Wang, Yanbo and Xie, Lei and Zhu, Pengcheng},
  journal={arXiv preprint arXiv:2606.09050},
  year={2026}
}
```

## 📧 Contact

For questions or collaborations, please contact: guobin.ma@mail.nwpu.edu.cn

<p align="center">
    <img src="https://huggingface.co/ASLP-lab/MeanVC2/resolve/main/figs/npu@aslp.jpeg" width="500"/>
</p>
