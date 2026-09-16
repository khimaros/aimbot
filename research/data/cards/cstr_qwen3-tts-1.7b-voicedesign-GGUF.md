---
license: apache-2.0
language:
  - zh
  - en
  - ja
  - ko
  - de
  - fr
  - ru
  - pt
  - es
  - it
pipeline_tag: text-to-speech
tags:
  - audio
  - tts
  - voice-design
  - instruct-tts
  - ggml
  - gguf
  - crispasr
  - qwen3-tts
library_name: ggml
base_model: Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign
---

# Qwen3-TTS 12Hz 1.7B VoiceDesign — GGUF (CrispASR)

GGUF / ggml conversions of [`Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign`](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign) for use with the `qwen3-tts` backend in **[CrispStrobe/CrispASR](https://github.com/CrispStrobe/CrispASR)**.

VoiceDesign is the instruct-tuned variant of Qwen3-TTS-12Hz-1.7B. Instead of cloning a reference WAV (Base) or picking from a fixed speaker table (CustomVoice), VoiceDesign generates speech in a voice **described by a natural-language instruction** — no reference audio, no preset speaker.

```bash
crispasr ... \
    --instruct "A young female voice with a slight British accent, energetic, slightly fast paced" \
    --tts "Hello, I am an excited engineer."
```

This repo contains the **talker / code-predictor** model only. It must be used together with the separate tokenizer / codec GGUF from [`cstr/qwen3-tts-tokenizer-12hz-GGUF`](https://huggingface.co/cstr/qwen3-tts-tokenizer-12hz-GGUF). The model has no speaker-encoder branch — the instruct text is embedded directly into the talker prefill.

VoiceDesign is **1.7B-only**: there is no 0.6B-VoiceDesign weight release upstream.

## Files

File | Size | Notes
--- | --- | ---
`qwen3-tts-12hz-1.7b-voicedesign-f16.gguf` | 3.6 GB | F16 reference baseline
`qwen3-tts-12hz-1.7b-voicedesign-q8_0.gguf` | 1.9 GB | Q8_0, recommended quantised talker

## Quick Start

Build CrispASR:

```bash
git clone https://github.com/CrispStrobe/CrispASR
cd CrispASR
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j$(nproc) --target crispasr
```

Download the talker + tokenizer:

```bash
huggingface-cli download cstr/qwen3-tts-1.7b-voicedesign-GGUF \
    qwen3-tts-12hz-1.7b-voicedesign-q8_0.gguf --local-dir .

huggingface-cli download cstr/qwen3-tts-tokenizer-12hz-GGUF \
    qwen3-tts-tokenizer-12hz.gguf --local-dir .
```

Synthesise with a natural-language voice description:

```bash
./build/bin/crispasr \
    --backend qwen3-tts-1.7b-voicedesign \
    -m qwen3-tts-12hz-1.7b-voicedesign-q8_0.gguf \
    --codec-model qwen3-tts-tokenizer-12hz.gguf \
    --instruct "A young female voice with a slight British accent, energetic, slightly fast paced" \
    --tts "Hello, I am an excited engineer." \
    --tts-output hello.wav
```

Or let CrispASR pull both files for you on first run:

```bash
./build/bin/crispasr \
    --backend qwen3-tts-1.7b-voicedesign -m auto \
    --instruct "warm, calm middle-aged male narrator" \
    --tts "The story begins on a quiet Tuesday morning." \
    --tts-output story.wav
```

Notes:
- `--instruct` is **required** for VoiceDesign models. Passing `--voice` instead is a CLI error with a hint.
- The instruct text is wrapped as `<|im_start|>user\n{instruct}<|im_end|>\n` and prepended to the talker prefill; the codec bridge omits the speaker frame entirely (the model has no fixed speaker embedding).

## Quantisation Notes

- `qwen3-tts-12hz-1.7b-voicedesign-f16.gguf`
  - reference baseline (3.6 GB)
- `qwen3-tts-12hz-1.7b-voicedesign-q8_0.gguf`
  - recommended quantised deployment (1.9 GB)
  - ASR-roundtrips word-exact on the English smoke prompt in current CrispASR testing
    (`"Hello, I am an excited engineer."` → parakeet-v3 → `"Hello! I am an excited engineer!"`)

Lower-bit talker quants (`q6_k`, `q5_k`, `q4_k`) can still load but are not numerically faithful to the F16 reference and should be treated as experimental.

The companion tokenizer / codec should stay at F16.

## How this was made

1. The upstream HF safetensors checkpoint was converted to GGUF F16 by [`models/convert-qwen3-tts-to-gguf.py`](https://github.com/CrispStrobe/CrispASR/blob/main/models/convert-qwen3-tts-to-gguf.py). The converter sets `qwen3tts.tts_model_type = "voice_design"` from the upstream `config.json`, which the runtime keys off to switch into the VoiceDesign prefill path.
2. Quantised variants are produced with CrispASR's GGUF quantiser.
3. Inference is implemented in [`src/qwen3_tts.cpp`](https://github.com/CrispStrobe/CrispASR/blob/main/src/qwen3_tts.cpp); the VoiceDesign-specific prefill builder (`build_voicedesign_prefill_embeds`) mirrors `Qwen3TTSForConditionalGeneration.generate` for `speaker_embed=None + instruct_ids` (modeling_qwen3_tts.py L2076–L2233).

## Reference implementation

Architecture and behaviour were checked against the official Qwen release:

- upstream model card: [`Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign`](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign)
- upstream repository: [`QwenLM/Qwen3-TTS`](https://github.com/QwenLM/Qwen3-TTS)

The CrispASR runtime is a clean C++ / ggml re-implementation for this repo's backend stack.

## Related

- Base sibling (voice cloning from reference WAV): [`cstr/qwen3-tts-1.7b-base-GGUF`](https://huggingface.co/cstr/qwen3-tts-1.7b-base-GGUF)
- Smaller sibling (Base, 0.6B): [`cstr/qwen3-tts-0.6b-base-GGUF`](https://huggingface.co/cstr/qwen3-tts-0.6b-base-GGUF)
- Fixed-speaker sibling (CustomVoice, 0.6B): [`cstr/qwen3-tts-0.6b-customvoice-GGUF`](https://huggingface.co/cstr/qwen3-tts-0.6b-customvoice-GGUF)
- Companion tokenizer / codec GGUF: [`cstr/qwen3-tts-tokenizer-12hz-GGUF`](https://huggingface.co/cstr/qwen3-tts-tokenizer-12hz-GGUF)
- Upstream VoiceDesign model: [`Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign`](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign)
- C++ runtime: [`CrispStrobe/CrispASR`](https://github.com/CrispStrobe/CrispASR)

## License

Apache-2.0, inherited from the base model.

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign) — published by `Qwen`.
- **Upstream licence:** `apache-2.0`. This repository redistributes under the same terms; it grants no rights the upstream licence does not.
- **What was done here:** format conversion and/or quantisation only (GGUF/GGML). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository. No training-content summary was found on the upstream model card at the time of writing; that documentation gap is upstream's and is not filled here.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
