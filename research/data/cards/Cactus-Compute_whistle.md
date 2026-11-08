---
library_name: cactus-compute
pipeline_tag: automatic-speech-recognition
license: apache-2.0
language:
  - en
  - de
  - fr
  - es
  - it
  - nl
  - pl
tags:
  - speech-recognition
  - speech-to-text
  - on-device
  - edge
  - quantization
  - webassembly
---

![Cactus Compute - Sub-50mb Super Intelligence For Consumer Devices](https://raw.githubusercontent.com/cactus-compute/cactus/main/assets/banner.svg)

# Whistle

A 16.9 MB speech model for transcription, word timestamps and speech embeddings in seven languages.
See the [Whistle website](https://cactuscompute.com/blog/whistle) for model details, benchmarks and the browser demo.

## Get started

```sh
pip install -U cactus-compute
```

```python
import cactus

print(cactus.transcribe("clip.wav")["text"])
```

Use a 16 kHz WAV file. Install `cactus-compute[mic]` for other sample rates or microphone capture.
The package downloads and caches the engine and weights on first use.
This repository provides `whistle.cact` and `checkpoints/whistle.safetensors`.
[Runtime binaries and supported platforms](https://huggingface.co/Cactus-Compute/cactus) live in the Cactus repository.

## Guides

- [Python API](https://cactuscompute.com/blog/needle-python-docs)
- [Speech guide](https://cactuscompute.com/blog/whistle-best-practices)
- [Fine-tuning](https://cactuscompute.com/blog/finetuning-whistle)
- [Source code](https://github.com/cactus-compute/cactus)
