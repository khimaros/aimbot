---
license: mit
language:
  - zh
  - en
base_model: inclusionAI/Ming-3.0-audio-tiny
tags:
  - audio.cpp
  - gguf
  - automatic-speech-recognition
  - text-to-speech
---

# Ming 3.0 Audio Tiny GGUF

Follow or star [audio.cpp](https://github.com/0xShug0/audio.cpp) for the inference
code and integration updates.

### Update 2026-10-23: The model now runs 2x faster with 20% lower peak VRAM on CUDA in fully resident mode! For upstream music example (152.84 s) and meeting example (1,244.64 s), Q4_K resident mode RTF drops from 0.050 to 0.024, while peak VRAM decreases from 14,600 to 11,596 MiB.


GGUF conversion of
[inclusionAI/Ming-3.0-audio-tiny](https://huggingface.co/inclusionAI/Ming-3.0-audio-tiny/tree/25b96e30be3739849bf76c0f48ac11db4a262fb3),
pinned to revision `25b96e30be3739849bf76c0f48ac11db4a262fb3`.
Upstream code: [Ming-3.0-audio-flash](https://github.com/inclusionAI/Ming-3.0-audio-flash).

The single GGUF contains the audio encoder, KDA/MLA MoE Thinker, Talker, audio VAE,
CAMPPlus speaker encoder, tokenizers, and configuration. It supports offline
transcription, audio understanding, named voices, voice cloning, and spoken
responses. Speech output is mono 44.1 kHz.

## Package

| File | Precision |
| --- | --- |
| `ming-3.0-audio-tiny-bf16.gguf` | Original BF16 tensors; expert routers and CAMPPlus in F32 |
| `ming-3.0-audio-tiny-q8_0.gguf` | Q8_0 Thinker expert banks; other tensors retain source precision |
| `ming-3.0-audio-tiny-q4_k.gguf` | Q4_K Thinker expert banks; Q8_0 text output head |

Both quantized packages preserve the audio encoder, Thinker attention and MLP projections,
Talker, VAE and speaker encoder. TTS-only memory usage therefore does not shrink
with Thinker expert quantization.

## Usage

```bash
audiocpp_cli --family ming3_audio --task asr --backend cuda \
  --model ming-3.0-audio-tiny-bf16.gguf --audio recording.wav --log

audiocpp_cli --family ming3_audio --task tts --backend cuda \
  --model ming-3.0-audio-tiny-bf16.gguf \
  --text "The sun warms the earth, and a soft breeze moves through the garden." \
  --request-option voice_id=US_James --request-option language=en \
  --out speech.wav --log

audiocpp_cli --family ming3_audio --task clon --backend cuda \
  --model ming-3.0-audio-tiny-bf16.gguf --voice-ref reference.wav \
  --text "Please leave the lamp beside the window." \
  --request-option language=en --out clone.wav --log
```

Reference audio conditions speaker identity. Add `reference_text` through the
request-option map to also use its acoustic prefix. Use `s2s` with input audio
for a Thinker answer synthesized by the Talker.

Prefer a reference in the target language for more reliable pronunciation.

For lower GPU memory use, add
`--session-option ming3_audio.disk_experts=true`. Expert weights remain in host
memory and are staged into a bounded GPU cache; neural computation stays on the
selected GPU. The default is eight expert slots per layer. Long speech output
uses framework text chunking, controlled by `text_chunk_size` (default 100).
In offload mode, Thinker KV storage grows with actual context use instead of
reserving the entire generation allowance upfront; `max_tokens` is unchanged.

See the [model guide](https://github.com/0xShug0/audio.cpp/blob/main/docs/models/ming3_audio.md)
for controls and conversion instructions. The native frontend uses framework
text chunking, not Python's word/character buffering, and does not run Python's
optional FST text normalizer. Spell out numbers when pronunciation matters.

## Performance

Fresh measurements collected on October 21, 2026, on an RTX 5090 with a Debug
C++17 build. Each Python/audio.cpp pair uses the same input audio or text,
prompt, and reference conditioning. Python uses the official BF16 checkpoint,
PyTorch 2.11.0+cu128, Transformers 5.12.1, and SDPA attention.

RTF is inference time divided by input audio duration for ASR/understanding,
or generated audio duration for TTS; loading and file writing are excluded.
Values average two measured requests after a separate warmup. Peak VRAM is sampled
process usage across each corresponding request sequence, not retained memory.

![Ming 3.0 Audio Tiny performance: warm RTF and peak VRAM for official Python BF16 and audio.cpp.](assets/performance.png)

ASR uses greedy decoding with a 256-token allowance. The complete meeting uses
the same transcription/summary prompt and a 32,768-token allowance on both
implementations, ending naturally. Q4 meeting answers differ from BF16;
these are matched-input performance measurements, not an output-parity claim.

Both TTS cases use the same 1,518-character English text, seed 42, guidance scale 2,
sigma 0.25, and temperature 0. Named-voice TTS uses `voice_id=US_James` without
reference audio; cloning uses the US_James recording and reference transcript.
Both implementations keep their normal chunkers: audio.cpp uses a 100-character
budget; Python uses its own word/character buffering. Timing includes reference
preparation. Long outputs
are 65.4 s for Python and 63.9 s for audio.cpp in the clone case, and 78.1 s
versus 79.7 s for named-voice TTS.

All short-ASR transcripts match Python exactly. For long cloning, Whisper turbo
reports 0% WER for Python versus 0.40% for audio.cpp with the 100-character budget.
The two audio.cpp clone WAVs are byte-identical after an intervening short request.
For named-voice TTS, Whisper medium reports 1.98% WER for Python versus 0% for
audio.cpp; the two audio.cpp named-voice WAVs are also byte-identical.

CPU inference also passes short ASR and TTS functional checks; it is not included
in this CUDA performance comparison.

## License

MIT, following the upstream checkpoint.
