---
license: apache-2.0
base_model: Audio8/Audio8-TTS-Preview-0.6b
library_name: audio.cpp
pipeline_tag: text-to-speech
tags:
- tts
- voice-cloning
- gguf
- audio.cpp
- arktts
- q8_0
language:
- yue
- zh
- en
- nl
- fr
- de
- it
- ja
- ko
- pl
- es
---

# Audio8-TTS-Preview-0.6b-GGUF

GGUF conversion of **[Audio8/Audio8-TTS-Preview-0.6b](https://huggingface.co/Audio8/Audio8-TTS-Preview-0.6b)** for [audio.cpp](https://github.com/0xShug0/audio.cpp). No new training.

**Original checkpoint:** 0.6B DualAR — Slow 24×896 (14 heads, 2 KV), Fast 4×896, 10×4096 codebooks, 44.1 kHz codec (2048 samples/frame), 2048 context. Languages: yue/zh/nl/en/fr/de/it/ja/ko/pl/es/auto. See original model card for details and evaluation.

## File

| File | Tensors | Precision | Size |
|------|---------|-----------|------|
| `audio8-tts-preview-0.6b-q8_0.gguf` | 681 (226 AR + 455 codec) | q8_0 | ~1.4 GiB |

Both embed `config.json`, `tokenizer.json`, `tokenizer_config.json` and `model_specs/audio8_tts.json`. `q8_0` is the recommended default.

## Conversion

* **Source:** `model.safetensors` + `codec.safetensors` from `Audio8/Audio8-TTS-Preview-0.6b`
* **Tool:** [`convert_audio8_tts.py`](https://github.com/jasonchen31/audio.cpp/blob/dev-audio8_tts/tools/community_models/convert_audio8_tts.py) + `audiocpp_gguf` (`--family audio8_tts --model-spec model_specs/audio8_tts.json --type q8_0/bf16`)
* **Change:** storage type/quantization only (q8_0). No architecture or training changes.

```bash
python tools/community_models/convert_audio8_tts.py \
  --model-dir /path/to/Audio8-TTS-Preview-0.6b \
  --converter build/bin/audiocpp_gguf \
  --type q8_0
```

## Usage (audio.cpp)

```bash
# offline TTS
audiocpp_cli --task tts --family audio8_tts \
  --model audio8-tts-preview-0.6b-q8_0.gguf \
  --text "The quick brown fox jumps over the lazy dog." --out out.wav

# streaming + voice cloning
audiocpp_cli --task tts --mode streaming --family audio8_tts \
  --model audio8-tts-preview-0.6b-q8_0.gguf \
  --text "Hello world" --voice-ref ref.wav --reference-text "transcript of ref.wav" --out out.wav

# server (OpenAI-compatible)
audiocpp_server --config server.json
# POST /v1/audio/speech {"model":"audio8-tts","input":"...","stream":true,"stream_format":"sse","response_format":"pcm"}
```

Params: `max_tokens` (default 1024), `temperature` 0.7, `top_p` 0.9, `top_k` 50, `seed`.

## License and Attribution

**License:** [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0) — same as upstream.

> Upstream: *Code and model weights are released under the Apache License 2.0. See [NOTICE](https://github.com/Audio8-AI/Audio8_TTS/blob/main/NOTICE).*

This repository is a Derivative Work (GGUF format conversion) under Apache-2.0 §1.

* Copyright retained by Audio8 — see upstream `LICENSE`/`NOTICE` (includes DualAR attribution to Fish Audio).
* This distribution includes Apache-2.0 `LICENSE`.
* Not affiliated or endorsed by Audio8.

## Acknowledgements

Audio8 for `Audio8-TTS-Preview-0.6b` (Apache-2.0) and Fish Audio for DualAR architecture.

## Limitations

Preview checkpoint; noisy/long/mismatched reference clips reduce stability. Obtain consent before cloning a voice and disclose synthetic audio.

