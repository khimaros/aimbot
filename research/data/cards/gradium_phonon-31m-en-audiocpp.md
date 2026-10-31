---
license: apache-2.0
language:
  - en
pipeline_tag: text-to-speech
library_name: gguf
base_model: gradium/phonon-31m-en
base_model_relation: quantized
tags:
  - text-to-speech
  - tts
  - phonon
  - audio.cpp
---

# phonon-31m English for audio.cpp

[phonon-31m-en](https://huggingface.co/gradium/phonon-31m-en) converted for
[audio.cpp](https://github.com/0xShug0/audio.cpp)'s `gradium_phonon` family.
It is the same model; only the file format differs.

> These files need an audio.cpp build with the `gradium_phonon` family, which is not merged
> yet. They do not load in llama.cpp: for llama.cpp, use
> [gradium/phonon-31m-en-llamacpp](https://huggingface.co/gradium/phonon-31m-en-llamacpp).

For the Phonon runtime (command line, Python, browser, iOS, Android), use
[gradium/phonon-31m-en](https://huggingface.co/gradium/phonon-31m-en).

## Files

| File | What it holds |
|---|---|
| `phonon-31m-en-q8_0.gguf` | The model, with its config and tokenizer. The transformer's linear layers are 8-bit; the rest, the Mimi decoder included, keeps the original precision. |
| `default-voice.safetensors` | The default voice, the same file as in [phonon-31m-en](https://huggingface.co/gradium/phonon-31m-en). |

## Quickstart

From an audio.cpp checkout:

```sh
python3 tools/model_manager_v2.py install gradium_phonon_31m_en_q8_0 --models-root models

audiocpp_cli --task tts --family gradium_phonon --model models/phonon-31m-en \
  --backend cpu --text "Hello from Phonon." --out speech.wav
```

`--backend` selects another audio.cpp backend, such as `metal`, and `--mode streaming`
streams the audio.

## Good to know

- **Voices:** without `--voice-id`, the default voice is used. More voices are in
  [gradium/phonon-voices](https://huggingface.co/gradium/phonon-voices): copy one into the
  model folder as `embeddings/<name>.safetensors` and pass `--voice-id <name>`. The model has
  no voice cloning from audio.
- **Text:** audio.cpp sends the text to the tokenizer as written. Write numbers, symbols and
  abbreviations out in words. The Phonon runtime does this for you with `--lang en`.
- **Sampling:** temperature 0.3, the Phonon runtime's default.

## License

[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0), like
[phonon-31m-en](https://huggingface.co/gradium/phonon-31m-en). Phonon builds on
[Pocket TTS](https://github.com/kyutai-labs/pocket-tts) and the Mimi codec, developed by
Kyutai.

[All Phonon models](https://huggingface.co/collections/gradium/phonon) · [Runtime on GitHub](https://github.com/gradium-ai/xn-ptts)
