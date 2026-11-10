---
base_model: nace-ai/drex-v2.0
license: other
license_name: nace-ai-open-rail-m
license_link: LICENSE
tags:
- gguf
- decision-model
- system-one
- drex
- moe
---

# Drex v2.0 Q8_0 GGUF

A Q8_0 GGUF of [Drex v2.0](https://huggingface.co/nace-ai/drex-v2.0), a decision model that takes a `state` and named typed questions and returns a probability for every option. The file is 36.9 GB, about half the size of the bf16 weights.

[Drex v2.0](https://huggingface.co/nace-ai/drex-v2.0) · [Drex repository](https://github.com/nace-ai/drex-decision-models) · [llama.cpp fork](https://github.com/nace-ai/llama.cpp) (branch `drex-v2.0`) · [Ollama fork](https://github.com/nace-ai/ollama) (branch `drex-v2.0`)

## Run with llama.cpp

Build the `drex-v2.0` branch of the llama.cpp fork as described on the [model page](https://github.com/nace-ai/drex-decision-models/tree/main/models/drex-v2.0#llamacpp). Then download the GGUF and start the server:

`hf` is the Hugging Face CLI (`pip install -U huggingface_hub`).

```bash
hf download nace-ai/drex-v2.0-Q8_0 drex-v2.0-Q8_0.gguf --local-dir weights/drex-v2.0-Q8_0

llama.cpp/build/bin/llama-server -m weights/drex-v2.0-Q8_0/drex-v2.0-Q8_0.gguf \
  --embedding --pooling none -np 2 -c 32768 -b 16384 -ub 2048 -ngl 28 --port 8000
```

The server answers `POST /v1/systemone`; the request format is in the [repository docs](https://github.com/nace-ai/drex-decision-models/blob/main/docs/request-format.md). On a 48 GB Mac, `-ngl 28` offloads 28 layers to Metal and runs the rest on the CPU; `-ngl 0` runs entirely on the CPU. This command accepts requests up to 16,384 tokens; for larger windows see [Context length](https://github.com/nace-ai/drex-decision-models/blob/main/docs/context-length.md).

## Run with Ollama

Use the Nace fork of Ollama from the model page, with this `Modelfile` next to the GGUF:

```text
FROM ./drex-v2.0-Q8_0.gguf
CAPABILITY decision
PARAMETER num_ctx 16384
PARAMETER num_gpu 28
```

## File

| File | Size | SHA-256 |
|---|---:|---|
| `drex-v2.0-Q8_0.gguf` | 36,907,336,224 bytes | `dc1ab68ed92b66f445b9e084e92b438330d15378cd6f2726a71f0d9529518cfe` |

The GGUF has the `qwen35moe` architecture. It holds 432 Q8_0 tensors and 306 F32 tensors, converted with `--no-mtp`.

## Tested

On an Apple M5 Pro (48 GB unified memory), the Q8_0 GGUF gives the same answers on Metal with `-ngl 28` and on the CPU, with probabilities within 0.03 of each other. Ollama gives the same answers as `llama-server`.

## License

Nace.AI Open RAIL-M license, see [LICENSE](LICENSE).
