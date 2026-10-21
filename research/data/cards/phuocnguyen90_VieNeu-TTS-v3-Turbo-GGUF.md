---
language:
- vi
- en
library_name: gguf
tags:
- text-to-speech
- tts
- audio
- vieneu
- audio.cpp
licence: cc-by-nc-4.0
base_model: pnnbao-ump/VieNeu-TTS-v3-Turbo
---

# 🦜 VieNeu-TTS v3 Turbo GGUF (48 kHz)

This repository contains the official GGUF quantized model package for **VieNeu-TTS v3 Turbo (48 kHz)**, fully integrated and supported natively in **[audio.cpp](https://github.com/0xShug0/audio.cpp)** (merged in PR #80).

> **Model Credits & Acknowledgments**: This is a GGUF quantization of the original [VieNeu-TTS-v3-Turbo](https://huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo) model created by **pnnbao-ump**. All credit for the underlying architecture and model training goes to the original authors.

It packs both the compressed Qwen3 talker backbone and the speech tokenizer/decoder weights into a single optimized **163 MB** file, enabling instant load times and ultra-fast, torch-free C++ generation on CPU.

---

## 📊 Performance Benchmarks (CPU)

The following benchmark compares native Python backends (PyTorch CPU, ONNX CPU int8, and ONNX CPU fp32) against the compiled **C++ CPU backend** (using 4 threads, generating **~3.5 seconds of high-fidelity 48 kHz audio**):

| Metric | Native PyTorch CPU | Upstream ONNX CPU (`onnx_int8`) | Upstream ONNX CPU (`onnx_update` / FP32) | C++ CPU (`audio.cpp`) |
| :--- | :---: | :---: | :---: | :---: |
| **Model Load Time** | `9.30 seconds` | `8.93 seconds` | `17.04 seconds` | **`Instant (<0.01s)`** |
| **First Run (Warmup)** | `1.70 seconds` | `1.57 seconds` | `1.40 seconds` | **`0.07 seconds`** |
| **Inference Time (Avg)** | `1.58 seconds` | `1.51 seconds` | `2.80 seconds` | **`0.89 seconds`** |
| **Real-Time Factor (RTF)** | `0.44` | `0.43` | `0.80` | **`0.24`** *(4x faster)* |
| **Combined Load+Warmup** | `11.00 seconds` | `10.50 seconds` | `18.44 seconds` | **`0.08 seconds`** |

---

## 🛠️ Usage

### 1. Build the C++ CLI Runner

Clone the official `audio.cpp` repository and build the target binary:

```bash
# Clone the upstream repository
git clone https://github.com/0xShug0/audio.cpp.git
cd audio.cpp

# Build the executable
chmod +x scripts/build_linux.sh
./scripts/build_linux.sh --backend cpu --target audiocpp_cli
```

### 2. Download the Model File

Download this GGUF model along with its tokenizer configurations using `audio.cpp`'s built-in model manager:

```bash
python tools/model_manager.py install vietneu_tts_v3_turbo
```

Or manually:

```bash
mkdir -p models/VieNeu-TTS-v3-Turbo
cd models/VieNeu-TTS-v3-Turbo

wget https://huggingface.co/phuocnguyen90/VieNeu-TTS-v3-Turbo-GGUF/resolve/main/model.gguf
wget https://huggingface.co/phuocnguyen90/VieNeu-TTS-v3-Turbo-GGUF/resolve/main/config.json
wget https://huggingface.co/phuocnguyen90/VieNeu-TTS-v3-Turbo-GGUF/resolve/main/tokenizer.json
wget https://huggingface.co/phuocnguyen90/VieNeu-TTS-v3-Turbo-GGUF/resolve/main/tokenizer_config.json
wget https://huggingface.co/phuocnguyen90/VieNeu-TTS-v3-Turbo-GGUF/resolve/main/special_tokens_map.json
mkdir -p speech_tokenizer
wget -O speech_tokenizer/config.json https://huggingface.co/phuocnguyen90/VieNeu-TTS-v3-Turbo-GGUF/resolve/main/speech_tokenizer/config.json
```

### 3. Generate Speech

Run inference via the C++ CLI:

```bash
../../build/linux-cpu-release/bin/audiocpp_cli   --task tts   --family vietneu_tts   --model model.gguf   --backend cpu   --voice-ref ../../assets/resources/sample.wav   --reference-text "Some call me nature. Others call me Mother Nature."   --text "sˈin tʃˈaː2w tˈeɜ zˈəːɜj. ɗˈəɪ lˌaː2 bˈaː4n tˈy4 ŋˈiɛ6m."   --out output.wav
```
