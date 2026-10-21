---
license: apache-2.0
base_model: k2-fsa/ZipVoice
library_name: ggml
pipeline_tag: text-to-speech
language:
  - zh
  - en
tags:
  - tts
  - voice-cloning
  - zero-shot
  - gguf
  - ggml
  - flow-matching
---

# ZipVoice-Distill GGUF for audio.cpp

Ready-to-run [GGUF](https://github.com/ggml-io/ggml) packages of
**ZipVoice-Distill** (k2-fsa), a zero-shot voice-cloning TTS with a TTSZipformer
flow-matching backbone and a Vocos 24 kHz vocoder, packaged for the
[audio.cpp](https://github.com/audio-cpp/audio.cpp) engine.

Each file is fully self-contained: flow-matching model + bundled Vocos vocoder +
embedded text-frontend sidecars (`tokens.txt`, `model.json`, zh tables, jieba
dictionaries). Output: 24 kHz mono WAV.

## Files

| File | Precision | Size | Recommended |
|---|---|---:|---|
| `zipvoice-distill-q8_0.gguf` | Q8_0 (weight-only) | 158 MB | ✅ default |
| `zipvoice-distill-orig.gguf` | F32 (original) | 553 MB | bit-exact reference |

**Q8_0 is the recommended download.** Weights are stored as int8 blocks (one
F16 scale per 32 weights); activations stay F32 and the kernels dequantize each
block on the fly — no full-model dequantization at load, no int8 arithmetic.

## Q8_0 vs F32 (Apple M3, Metal, 34 s utterance)

| Metric | F32 | Q8_0 |
|---|---:|---:|
| File size | 553 MB | **158 MB (3.5× smaller)** |
| Runtime memory | 1310 MB | **971 MB (−26%)** |
| RTF (lower is better) | 0.217 | **0.204** |
| Log-mel cosine vs F32 | 1.0000 | **0.9987 (male) / 0.9997 (female)** |
| Velocity field cosine vs PyTorch | 1.0000 | 0.9993 |

Quality is transparent to the ear; 8-step distilled sampling, guidance scale 3,
time shift 0.5. Lower-bit variants (q6_k … q4_0) are deliberately **not**
provided — they trade audible quality for size on this model.

## Usage

### Install with the audio.cpp model manager

```bash
# from an audio.cpp checkout
python3 tools/model_manager_v2.py install zipvoice_distill_q8_0
# → models/ZipVoice-Distill-GGUF/zipvoice-distill-q8_0.gguf
```

### Direct synthesis (CLI)

```bash
audiocpp_cli --task clon --family zipvoice \
    --model models/ZipVoice-Distill-GGUF/zipvoice-distill-q8_0.gguf \
    --voice-ref prompt.wav --reference-text "Reference transcript." \
    --text "你好，这是ZipVoice，支持中文和English两种语言。" --out out.wav
```

`--reference-text` must transcribe `--voice-ref`. Chinese, English and mixed
input are handled by the built-in Emilia frontend (jieba + pypinyin tables +
espeak-ng; the English path needs the espeak-ng dylib shown above). Python API,
server and streaming options are documented in
[`docs/community_models/zipvoice.md`](https://github.com/audio-cpp/audio.cpp/blob/main/docs/community_models/zipvoice.md).

## Provenance & conversion

- Upstream weights: [k2-fsa/ZipVoice](https://huggingface.co/k2-fsa/ZipVoice)
  (`zipvoice_distill`, Apache-2.0)
- Conversion: `tools/community_models/convert_zipvoice.py`
  (torch → safetensors → GGUF with `model.*` / `vocos.*` namespaces)
- Quantization: `audiocpp_gguf --type q8_0` (weight-only, per-block scales)
- Parity: text encoder (per-layer taps), flow decoder, Vocos and full synthesis
  verified against the PyTorch reference; see the zipvoice doc in audio.cpp for
  the full report

## License

Apache-2.0, inherited from the upstream ZipVoice release.
