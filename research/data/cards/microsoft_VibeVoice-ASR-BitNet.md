---
language:
- en
- zh
- fr
- it
- ko
- pt
- vi
license: mit
pipeline_tag: automatic-speech-recognition
tags:
- ASR
- quantization
- cpu-inference
- gguf
- bitnet
- multilingual
library_name: ggml
---

## VibeVoice-ASR-BitNet

[![GitHub](https://img.shields.io/badge/GitHub-Repo-black?logo=github)](https://github.com/microsoft/VibeASR.cpp)
[![Technical Report](https://img.shields.io/badge/arXiv-2607.21075-b31b1b?logo=arxiv)](https://arxiv.org/abs/2607.21075)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**VibeVoice-ASR-BitNet** is a compressed variant of [VibeVoice-ASR](https://huggingface.co/microsoft/VibeVoice-ASR) optimized for **real-time inference on edge CPUs** — no GPU required. Through heterogeneous quantization, the model is compressed from 4.62 GB to **1.58 GB** while achieving **1.6–2.3× faster** inference than Whisper.cpp with real-time capability (RTF < 1) on as few as 3 CPU threads.

➡️ **Code:** [microsoft/VibeASR.cpp](https://github.com/microsoft/VibeASR.cpp)<br>
➡️ **Report:** [VibeVoice-ASR-BitNet Technical Report](https://arxiv.org/abs/2607.21075)<br>
➡️ **Base Model:** [microsoft/VibeVoice-ASR](https://huggingface.co/microsoft/VibeVoice-ASR)<br>

<p align="center">
  <img src="figures/report_overview.png" width="90%"/>
</p>

---

## 🔥 Key Features

- **⚡ Real-time on CPU** — RTF < 1 with 3+ threads on commodity x86 (AVX2) and ARM (NEON) hardware
- **📦 Compact** — 1.58 GB total (2.9× compression from FP16), fits in edge device memory
- **🌍 Multilingual** — English, Chinese, French, Italian, Korean, Portuguese, Vietnamese, and more
- **🔧 Custom SIMD Kernels** — Fused operators within the ggml framework for both ARM and x86 platforms

---

## Quantization Strategy

<div align="center">

| Component | FP16 | Quantized | Method | Compression |
|:-:|:-:|:-:|:-:|:-:|
| VAE Tokenizer | 1.31 GB | 0.65 GB | I8\_S | 2.0× |
| LM Decoder | 3.32 GB | 0.92 GB | I2\_S + Q6\_K | 3.6× |
| **Total** | **4.62 GB** | **1.58 GB** | — | **2.9×** |

</div>

---

## Evaluation

### Inference Speed

<div align="center">

| Threads | 1 | 2 | 3 | 4 | 6 | 8 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| RTF | 1.98 | 1.08 | **0.77** | **0.63** | **0.49** | **0.42** |
| vs. Whisper.cpp | 2.28× | 2.12× | 1.86× | 1.86× | 1.71× | 1.55× |

</div>

> Benchmarked on AMD EPYC 7V13 (AVX2+FMA) with 20s audio. **Bold** = RTF < 1 (real-time).

### Accuracy (WER%)

<div align="center">

| Benchmark | VibeVoice-ASR-7B | VibeVoice-ASR-BitNet | Parakeet | Whisper | SenseVoice | FunASR |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| MLC-EN | 7.82 | **8.25** | 8.40 | 13.57 | 12.39 | 11.36 |
| MLC-FR | 16.03 | 17.41 | — | — | — | — |
| MLC-IT | 15.67 | 17.23 | — | — | — | — |
| MLC-KO | 9.83 | 11.15 | — | — | — | — |
| MLC-PT | 22.41 | 24.87 | — | — | — | — |
| MLC-VI | 20.15 | 22.38 | — | — | — | — |
| AISHELL4 | 19.83 | 27.45 | — | — | 22.52 | **20.41** |
| AMI-ihm | 17.42 | **21.36** | 21.92 | 27.07 | 30.81 | 32.07 |
| AMI-sdm | 24.18 | **25.87** | 26.33 | 36.92 | 48.11 | 40.17 |
| AliMeeting | 36.21 | 40.58 | — | — | **38.75** | 39.27 |
| Fleurs-en | 4.73 | 5.21 | 4.09 | **3.99** | 6.84 | 4.93 |
| Fleurs-zh | 7.92 | 8.35 | — | — | **5.56** | 7.00 |
| Libri-clean | 2.17 | 2.41 | **1.49** | 1.98 | 2.78 | 1.58 |
| Libri-other | 5.84 | 6.27 | **3.13** | 3.60 | 6.81 | 4.01 |
| VoxPopuli | 4.92 | **5.18** | 5.26 | 7.19 | 8.63 | 6.46 |

</div>

---

## Model Files

<div align="center">

| File | Size | Description |
|:-:|:-:|:-:|
| `vibeasr-vae-encoder-i8_s.gguf` | 0.65 GB | VAE tokenizer, I8\_S quantized (ready to use) |
| `vibeasr-lm-i2_s-embed-q6_k.gguf` | 0.92 GB | LM decoder, I2\_S quantized (ready to use) |
| `model-*.safetensors` | 10.7 GB | Original SafeTensors (for conversion) |

</div>

---

## License

This project is licensed under the MIT License.

## Contact

This project was conducted by members of Microsoft Research. If you have suggestions, questions, or observe unexpected behavior, please contact us at VibeVoice@microsoft.com.
