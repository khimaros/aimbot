---
language:
- en
- zh
- es
- pt
- de
- ja
- ko
- fr
- ru
- it
license: mit
pipeline_tag: automatic-speech-recognition
tags:
- audio.cpp
- gguf
- asr
- streaming
- speaker-attributed-transcription
base_model: microsoft/VibeVoice-ASR-Streaming-1.5B
---

# VibeVoice ASR Streaming 1.5B GGUF for audio.cpp

This repository contains audio.cpp-native GGUF builds of
`microsoft/VibeVoice-ASR-Streaming-1.5B`.

The 1.5B checkpoint runs through the same audio.cpp loader as the 7B with no
code changes: the layer count, hidden size, and head counts are read from the
checkpoint's own `config.json`, and the tensor names are identical.

## Use with audio.cpp

Install the recommended Q8_0 package through the audio.cpp model manager:

```bash
python3 tools/model_manager_v2.py install vibevoice_asr_streaming_1_5b_q8_0
```

Run offline ASR:

```bash
build/debug/bin/audiocpp_cli \
  --task asr \
  --family vibevoice_asr_streaming \
  --model models/VibeVoice-ASR-Streaming-1.5B-GGUF/vibevoice-asr-streaming-1.5b-q8_0.gguf \
  --backend cuda \
  --threads 8 \
  --audio input.wav \
  --text-out transcript.txt \
  --metrics \
  --log
```

Run the server with the model loaded:

```json
{
  "host": "127.0.0.1",
  "port": 8080,
  "backend": "cuda",
  "threads": 8,
  "models": [
    {
      "id": "vibevoice-streaming-1.5b",
      "family": "vibevoice_asr_streaming",
      "path": "models/VibeVoice-ASR-Streaming-1.5B-GGUF/vibevoice-asr-streaming-1.5b-q8_0.gguf",
      "task": "asr",
      "mode": "streaming"
    }
  ]
}
```

Then start the server:

```bash
build/debug/bin/audiocpp_server --config server.json --log
```

For live streaming, send 16 kHz mono signed 16-bit PCM to the live endpoint:

```bash
ffmpeg -hide_banner -loglevel error -i input.wav -f s16le -ac 1 -ar 16000 - \
  | curl -N -X POST \
      -H 'Content-Type: application/octet-stream' \
      -H 'Transfer-Encoding: chunked' \
      -H 'Expect:' \
      -T - \
      'http://127.0.0.1:8080/v1/audio/transcriptions/live?model=vibevoice-streaming-1.5b&sample_rate=16000&channels=1&sample_format=s16le'
```

## Files

| File | Format | Notes |
|---|---|---|
| `vibevoice-asr-streaming-1.5b-bf16.gguf` | BF16 | Highest precision package. |
| `vibevoice-asr-streaming-1.5b-q8_0.gguf` | Q8_0 | Recommended package for audio.cpp. |
| `vibevoice-asr-streaming-1.5b-q4_k.gguf` | Q4_K | Smaller lower-bit package. |

Each GGUF is self-contained and embeds the audio.cpp package spec and required
sidecars.

## Word error rate

Scored over the four LibriSpeech clips in `assets/asr_validation/librispeech/`,
greedy decode, alongside the 7B Q4_K package for reference:

| Package | Size | WER (CUDA) | WER (CPU) |
|---|---:|---:|---:|
| `vibevoice-asr-streaming-7b-q4_k.gguf` | 5.86 GB | 4.35% | 4.35% |
| `vibevoice-asr-streaming-1.5b-bf16.gguf` | 5.64 GB | 4.35% | 4.35% |
| `vibevoice-asr-streaming-1.5b-q8_0.gguf` | 3.34 GB | 5.80% | 4.35% |
| `vibevoice-asr-streaming-1.5b-q4_k.gguf` | 2.12 GB | 7.25% | 5.80% |

Four clips is 69 words, so this separates "works and is in the right class" from
"broken" and nothing finer. The like-for-like comparison is the two Q4_K rows,
where the 7B leads. Do not read the tie between 7B Q4_K and 1.5B BF16 as parity:
different clips happen to sum to the same total.

A WER for a quantized package is only meaningful with its backend. CPU and CUDA
quantize activations differently in upstream ggml, so the quantized rows differ
per backend while BF16, which quantizes no activations, matches exactly.

## Source and license

These GGUF files were converted from the upstream Hugging Face model:

- Upstream repository: https://huggingface.co/microsoft/VibeVoice-ASR-Streaming-1.5B
- Pinned upstream revision: `4262d23d8a539a6530cf64fbd0b1751ef9a30853`
- Upstream license: MIT

The GGUF conversion preserves the upstream MIT license. See the upstream model
card and Microsoft VibeVoice repository for the original model documentation,
usage notes, and any responsible-use guidance.
