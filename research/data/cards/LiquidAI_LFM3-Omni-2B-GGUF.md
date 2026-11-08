---
library_name: gguf
license: other
license_name: lfm1.0
license_link: LICENSE
pipeline_tag: any-to-any
tags:
- liquid
- lfm3
- lfm3-omni
- omni
- audio
- vision
- gguf
- llama.cpp
language:
- en
- ar
- zh
- fr
- de
- it
- ja
- ko
- pt
- es
- vi
- th
- id
- hi
- ru
- pl
- da
- el
- fi
- he
- nl
- sv
- tr
base_model: LiquidAI/LFM3-Omni-2B
---


<div align="center">
  <img
    src="https://huggingface.co/LiquidAI/LFM3-1.7B/resolve/main/assets/liquid-ai-banner.webp"
    alt="Liquid AI"
    style="width: 100%; max-width: 100%; height: auto; display: block; margin: 0;"
  />
  <div align="center" style="display: flex; justify-content: center; align-items: center; gap: 1.25em; margin: 8px 0 1.7rem; padding: 0; line-height: 1.3;">
    <a href="https://console.liquid.ai/dashboard" style="display: inline-flex; align-items: center; gap: 6px;"><img src="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2216%22 height=%2216%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke-width=%222.2%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22%3E%3Cstyle%3Epath%7Bstroke:%23000%7D%40media (prefers-color-scheme:dark)%7Bpath%7Bstroke:%23d1d5dc%7D%7D%3C/style%3E%3Cpath d=%22m8 6-6 6 6 6m8-12 6 6-6 6m-2-14-4 16%22/%3E%3C/svg%3E" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>API</strong></a>
    <a href="https://playground.liquid.ai/" style="display: inline-flex; align-items: center; gap: 6px;"><img src="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2216%22 height=%2216%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke-width=%222.2%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22%3E%3Cstyle%3Epath%7Bstroke:%23000%7D%40media (prefers-color-scheme:dark)%7Bpath%7Bstroke:%23d1d5dc%7D%7D%3C/style%3E%3Cpath transform=%22translate(3 0)%22 d=%22M8 5.5v13L19 12 8 5.5Z%22/%3E%3C/svg%3E" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>Try</strong></a>
    <a href="https://docs.liquid.ai/lfm/getting-started/welcome" style="display: inline-flex; align-items: center; gap: 6px;"><img src="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2216%22 height=%2216%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke-width=%222.2%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22%3E%3Cstyle%3Epath%7Bstroke:%23000%7D%40media (prefers-color-scheme:dark)%7Bpath%7Bstroke:%23d1d5dc%7D%7D%3C/style%3E%3Cpath d=%22M12 6c-3-2-6-2.5-10-2v15c4-.5 7 0 10 2m0-15c3-2 6-2.5 10-2v15c-4-.5-7 0-10 2V6Z%22/%3E%3C/svg%3E" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>Docs</strong></a>
    <a href="https://www.liquid.ai/blog/lfm3" style="display: inline-flex; align-items: center; gap: 6px;"><img src="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2216%22 height=%2216%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke-width=%222.2%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22%3E%3Cstyle%3Epath%7Bstroke:%23000%7D%40media (prefers-color-scheme:dark)%7Bpath%7Bstroke:%23d1d5dc%7D%7D%3C/style%3E%3Cpath transform=%22translate(1 0)%22 d=%22m16 3 5 5L8 21H3v-5L16 3Zm-3 3 5 5%22/%3E%3C/svg%3E" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>Blog</strong></a>
  </div>
</div>


# LFM3-Omni-2B-GGUF

GGUF version of [LFM3-Omni-2B](https://huggingface.co/LiquidAI/LFM3-Omni-2B) for local inference on CPUs and GPUs.

LFM3-Omni-2B is an omni-modal model that understands text, images, video and audio, and answers in text and speech. It is built for on-device use.

Find architecture and usage details in the [original model card](https://huggingface.co/LiquidAI/LFM3-Omni-2B).

## How to run LFM3-Omni-2B
<hr style="margin: -0.7em 0 1.2em 0; border: 0; border-top: 1px solid rgba(127, 127, 127, 0.3);" />

Recommended sampling: greedy decoding (temperature 0) for text output. For speech output, audio temperature 0.4 and audio repetition penalty 1.2.

- [Llama.app](https://llama.app) (**Use this model > Llama** in the menu), for macOS and Windows: image, audio and video input. Requires llama.cpp version [v0.8.0](https://github.com/ggml-org/llama.cpp/releases/tag/v0.8.0) or newer.
- [LM Studio](https://lmstudio.ai) (**Use this model > LM Studio** in the menu), for macOS, Windows and Linux: image input. Requires LM Studio with llama.cpp engine 2.65.1 or newer.
- [Ollama](https://ollama.com) (`ollama run lfm3-omni`), for macOS: image and audio input. Requires Ollama version [v0.40.12](https://github.com/ollama/ollama/releases/tag/v0.40.12) or newer.

## Use with llama.cpp
<hr style="margin: -0.7em 0 1.2em 0; border: 0; border-top: 1px solid rgba(127, 127, 127, 0.3);" />

> [!NOTE]
> Supported in [llama.cpp](https://github.com/ggml-org/llama.cpp) [b11960](https://github.com/ggml-org/llama.cpp/releases/tag/b11960) ([v0.8.0](https://github.com/ggml-org/llama.cpp/releases/tag/v0.8.0)) and newer, including real-time voice conversations (with tool calls) on the `/v1/realtime` WebSocket API of `llama serve`.

Add a quantization tag to pick a file. With `-hf`, llama.cpp also downloads the vision and audio projector.

LFM3-Omni-2B is a non-reasoning model: with `llama serve`, use `--reasoning off`. Start a web chat UI and an OpenAI-compatible API at `http://localhost:8080`:

```bash
llama serve -hf LiquidAI/LFM3-Omni-2B-GGUF:Q4_K_M --reasoning off --temp 0 --port 8080
```

To ask one question from the command line, use `llama cli`.

Speech recognition: use the system prompt `Perform ASR in <language>.`

```bash
llama cli -hf LiquidAI/LFM3-Omni-2B-GGUF:Q4_K_M \
  --audio speech.wav -sys "Perform ASR in English." -p "<__media__>" --temp 0
```

Image understanding:

```bash
llama cli -hf LiquidAI/LFM3-Omni-2B-GGUF:Q4_K_M \
  --image photo.png -p "Describe this image." --temp 0
```

Video understanding: the model sees the frames and hears the soundtrack of the video, use the system prompt `Answer questions about the video using what you see and hear.` Video input needs `ffmpeg` in `PATH`.

```bash
curl -sL -o reading.mp4 https://huggingface.co/datasets/raushan-testing-hf/videos-test/resolve/4cba700bd771f44d72b549253da025c32e944d42/sample_demo_1.mp4  # a child reading a book

llama cli -hf LiquidAI/LFM3-Omni-2B-GGUF:Q4_K_M \
  --video reading.mp4 -sys "Answer questions about the video using what you see and hear." \
  -p "What happens here, and what can you hear?" --temp 0
```

Speech synthesis: `--tts-lang` takes a language code (default `en`) and `--tts-voice` is `female` (default) or `male`. The audio sampling parameters of the original model card are stored in the GGUF.

```bash
llama-tts -m LFM3-Omni-2B-Q4_K_M.gguf -mm mmproj-LFM3-Omni-2B-Q8_0.gguf \
  -p "Hello world" -o out.wav
```

More options in the [llama.cpp guide](https://docs.liquid.ai/deployment/on-device/llama-cpp).

