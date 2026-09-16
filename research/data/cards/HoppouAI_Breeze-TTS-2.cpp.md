---
base_model: BreezeBlue/Breeze-TTS-2
language:
  - en
  - zh
library_name: gguf
license: other
license_name: breezeblue-research-and-non-commercial
license_link: https://huggingface.co/BreezeBlue/Breeze-TTS-2
pipeline_tag: text-to-speech
tags:
  - text-to-speech
  - tts
  - gguf
  - ggml
  - vulkan
  - voice-cloning
  - voice-conversion
---

# Breeze-TTS-2 GGUF

GGUF conversions of [BreezeBlue/Breeze-TTS-2](https://huggingface.co/BreezeBlue/Breeze-TTS-2) for
[**Breeze-TTS-2.cpp**](https://github.com/HoppouAI/Breeze-TTS-2.cpp), a C++ reimplementation running on
ggml with a Vulkan backend, so it works on NVIDIA, AMD and Intel GPUs and falls back to CPU.

Bilingual English and Mandarin, 24 kHz, around 1.2x realtime at Q8_0 on an RTX 3060.

These files will not load in llama.cpp. They need the Breeze-TTS-2.cpp runtime, which implements all
four stages of the model: the T5Gemma2 text encoder, the Qwen3 backbone, the 15 step depth decoder and
the vocoder.

## Files

| File | Size | Notes |
| --- | --- | --- |
| `breeze-tts-2-f16.gguf` | 5.9 GB | Reference quality, unquantized |
| `breeze-tts-2-q8_0.gguf` | 3.3 GB | **Recommended.** No audible loss against F16 |
| `breeze-tts-2-q6_k.gguf` | 2.9 GB | |
| `breeze-tts-2-q4_k.gguf` | 2.4 GB | Smallest safe choice, holds up well |
| `breeze-tts-2-q8_0-dd4.gguf` | 3.2 GB | Experimental, Q8_0 base with a Q4_K depth decoder |
| `breeze-tts-2-q8_0-dd2.gguf` | 3.1 GB | Experimental, Q8_0 base with a Q2_K depth decoder |
| `breeze-tts-2-q4_k-dd2.gguf` | 2.3 GB | Experimental, Q4_K base with a Q2_K depth decoder |

Approximate VRAM is about 1 GB above the file size.

### About the `-dd` variants

Everything except the `-dd` files keeps the depth decoder at higher precision than the rest of the
model. The `-dd` variants quantize it too, which is why they are smaller.

The depth decoder runs **15 sequential steps for every single frame of audio**, so on hardware where
that is the bottleneck rather than memory bandwidth, shrinking it can speed generation up noticeably.
That is the reason these exist and it is worth benchmarking on your own card.

The tradeoff is that depth codes feed back into the backbone every frame, so quantization error
compounds as generation continues. Output holds up early and then drifts progressively muffled and
thin past **roughly 45 seconds of continuous generation**. Short lines and dialogue are fine. Long
narration is not, and the failure is gradual rather than obvious, so it is easy to miss on quick tests.

Treat them as experimental. If in doubt, use `q8_0` or `q4_k`.

## Usage

```bash
git clone --recursive https://github.com/HoppouAI/Breeze-TTS-2.cpp
cd Breeze-TTS-2.cpp
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
```

```bash
# invent a voice from a description
build/breeze-cli breeze-tts-2-q8_0.gguf \
  --text "Welcome aboard. Your journey begins now." \
  --instruction "A warm, thoughtful young woman with a clear, calm delivery." \
  --output design.wav

# clone a voice from a clip
build/breeze-cli breeze-tts-2-q8_0.gguf \
  --text "It is good to hear your voice again." \
  --ref-audio ref_voice.wav --ref-text "The harbour lights came on one by one as the evening tide began to turn." \
  --output clone.wav
```

Or run the server, which has a web UI built in plus HTTP and WebSocket streaming:

```bash
build/breeze-server breeze-tts-2-q8_0.gguf --host 127.0.0.1 --port 8080 --webui
```

`ref_voice.wav` in this repo is a sample reference clip. Its transcript is
"The harbour lights came on one by one as the evening tide began to turn."

## Vocal events

Inline tags in round brackets produce non speech sounds: `(laugh)`, `(sigh)`, `(cough)`,
`(clears throat)`, and `[笑]` or `[叹气]` in Chinese. The vocabulary is free form rather than a fixed
token list, so descriptive tags like `(nervous chuckle)` often work.

They usually need `--cfg-scale 2` to `3` to actually fire. At the default of 1.0 the model treats a tag
as a suggestion and tends to read straight past anything outside the common set.

## Voice conversion

The runtime can also respeak an existing recording in a different voice, keeping the original timing,
phrasing and emphasis while changing only the speaker. This is not part of the upstream model, it falls
out of how the codec separates semantic content from acoustic detail.

It is experimental. Pitch is regenerated rather than copied, so a converted vocal is re-sung in the
target voice's own register instead of at the source's. Whether a tune survives varies clip to clip,
and `keep_acoustic 1` or `2` copies the lowest acoustic codebooks from the source to pull more of the
original contour through. Judge it by ear, and leave `keep_acoustic` at 0 for ordinary speech.

## Conversion

Produced with `scripts/convert_hf_to_gguf.py` and `breeze-quantize` from the repo. The source download
must include the `audio_tokenizer/` directory, which holds the vocoder that the model actually uses at
inference time.

## License

Weights are governed by the **BreezeBlue Research and Non-Commercial License** from the
[original model](https://huggingface.co/BreezeBlue/Breeze-TTS-2). Converting to GGUF does not change
that. The Breeze-TTS-2.cpp source code is Apache 2.0.

You are responsible for complying with the weight license and for obtaining consent for any reference
audio or voices you use.
