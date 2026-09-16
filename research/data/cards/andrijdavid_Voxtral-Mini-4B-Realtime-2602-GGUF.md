---
base_model:
- mistralai/Voxtral-Mini-4B-Realtime-2602
---

# Voxtral-Mini-4B-Realtime-2602 (GGUF)

This repository contains GGUF weights for Voxtral Realtime 4B, a high-performance speech recognition (STT) model optimized for low-latency, real-time inference.

These weights are converted from the original [mistralai/Voxtral-Mini-4B-Realtime-2602](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602) model.


Voxtral is designed to process streaming audio with minimal delay, making it ideal for live transcription, voice assistants, and interactive applications.


## Model Details

   - Model Type: Speech Recognition / Transcription
   - Parameters: ~4 Billion
   - Architecture: Hybrid Encoder-Decoder with Log-Mel preprocessing
   - Format: GGUF (optimized for ggml)
   - Sample Rate: 16,000 Hz (Mono)

  
## Inference with voxtral.cpp

  For the fastest inference performance on CPU and GPU, use the voxtral.cpp (https://github.com/andrijdavid/voxtral.cpp) repository. It provides a lightweight C++ implementation based on ggml.


## Getting Started

  1. Clone the repository and build

  ```bash
   git clone https://github.com/andrijdavid/voxtral.cpp
   cd voxtral.cpp
   cmake -B build -DCMAKE_BUILD_TYPE=Release
   cmake --build build -j
  ```

  2. Download a quantized model
  Use the provided script to download your preferred quantization (e.g., Q4_0):

   ```bash
  ./tools/download_model.sh Q4_0
  ```


  4. Run Transcription

     Prepare a 16kHz mono WAV file and run inference:

     
  ```bash
        ./build/voxtral \
        --model models/voxtral/Q4_0.gguf \
        --audio input.wav \
        --threads 8
  ```

 For more advanced usage, including streaming examples and conversion scripts, please visit the voxtral.cpp GitHub repository (https://github.com/andrijdavid/voxtral.cpp).
