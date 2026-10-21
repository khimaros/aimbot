---
license: apache-2.0
library_name: audiocpp
tags:
- text-to-speech
- tts
- soprano
- audiocpp
---

# Soprano-1.1-80M GGUF

GGUF packages of Soprano-1.1-80M for [audio.cpp](https://github.com/0xShug0/audio.cpp).

**Original model:** [ekwek1/soprano](https://github.com/ekwek1/soprano) — an ultra-lightweight (~80M) English-only TTS model by [@ekwek1](https://github.com/ekwek1).
**Original weights:** [ekwek/Soprano-1.1-80M](https://huggingface.co/ekwek/Soprano-1.1-80M) on Hugging Face.

## Packages

| File | Format | Size |
|---|---|---|
| soprano-1.1-80m-q8_0.gguf | Q8_0 quantized (default) | 88 MB |
| soprano-1.1-80m-bf16.gguf | BF16 | 159 MB |

Install with audio.cpp:
`ash
python3 tools/model_manager_v2.py install soprano_1_1_80m_q8_0
`

## Attribution

This conversion is provided as a community package for use with audio.cpp. All rights to the model and its weights belong to the original authors.
