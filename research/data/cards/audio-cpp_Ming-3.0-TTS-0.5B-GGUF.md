---
license: mit
base_model: inclusionAI/Ming-3.0-tts-0.5B
language:
- zh
- en
- ja
- ko
- de
- fr
- es
pipeline_tag: text-to-speech
tags:
- audio.cpp
- gguf
---

# Ming 3.0 TTS 0.5B GGUF

Star or watch [audio.cpp on GitHub](https://github.com/0xShug0/audio.cpp)
to follow model integration, merged code changes and inference improvements.

GGUF packages of [Ming 3.0 TTS 0.5B](https://huggingface.co/inclusionAI/Ming-3.0-tts-0.5B)
for audio.cpp. Each file contains the Qwen backbone, flow-matching head,
audio VAE, CAMPPlus speaker encoder, configuration, tokenizer and model spec.
Output is mono at 44.1 kHz. No separate codec or Python runtime is required.

audio.cpp family: `ming3_tts`.

Upstream implementation: [inclusionAI/Ming-3.0-tts](https://github.com/inclusionAI/Ming-3.0-tts/tree/e999c39fa676722aaa9ea29b5aa19a90525b271f),
pinned to revision `e999c39fa676722aaa9ea29b5aa19a90525b271f` for the Python comparison.

| Package | Precision |
|---|---|
| `ming-3.0-tts-0.5b-bf16.gguf` | Original checkpoint precision |
| `ming-3.0-tts-0.5b-q8_0.gguf` | Q8_0; BF16 stop head and F32 speaker encoder retained |

## Performance

Measured on an RTX 5090 with eight CPU threads and an audio.cpp Debug C++17
build. Python uses the pinned official BF16 implementation above. Both use
the same text, voice-design instruction and seed. Warm RTF covers a
154-character request, its repeat and a 40-character request; peak memory
covers the complete session, including warmup and a 571-character request.
The long request is excluded from the speed comparison because text chunking
differs between implementations. Lower RTF is better.

| Implementation | Warm RTF | Speed vs Python | Peak VRAM MiB | Peak CPU RSS MiB |
| --- | --- | --- | --- | --- |
| Official Python, BF16 | 0.651-0.675 | 1x | 3,660 | 2,104 |
| audio.cpp, BF16 | 0.173-0.179 | 3.8x | 2,768 | 1,036 |
| audio.cpp, Q8_0 | 0.167-0.175 | 3.9x | 1,924 | 978 |

Speed ratios use mean warm RTF. These are synthesis-speed measurements, not
claims of identical sampled audio.

## Usage

```bash
audiocpp_cli --family ming3_tts --task tts --backend cuda \
  --model ming-3.0-tts-0.5b-bf16.gguf \
  --request-option language=en \
  --text "Good evening. The harbor is quiet tonight." --out speech.wav --log

audiocpp_cli --family ming3_tts --task clon --backend cuda \
  --model ming-3.0-tts-0.5b-bf16.gguf --voice-ref reference.wav \
  --request-option language=en \
  --text "Please leave the lamp beside the window." --out clone.wav --log

audiocpp_cli --family ming3_tts --task vdes --backend cuda \
  --model ming-3.0-tts-0.5b-bf16.gguf \
  --request-option language=en \
  --request-option instruct="A calm adult man with a clear, warm voice." \
  --text "Good evening. The harbor is quiet tonight." --out designed.wav --log
```

Cloning without a transcript uses speaker conditioning. To include the
reference's acoustic prefix, also supply
`--request-option reference_text="Words spoken in the reference."`.

The model supports structured voice, emotion, dialect and speaking-attribute
controls. `speed` is a categorical conditioning control, not waveform
resampling. See the [model guide](https://github.com/0xShug0/audio.cpp/blob/main/docs/models/ming3_tts.md)
for option values and long-form behavior.

The model weights retain their upstream MIT license; see `LICENSE`.
