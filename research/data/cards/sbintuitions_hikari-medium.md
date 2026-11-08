---
license: mit
library_name: transformers
pipeline_tag: automatic-speech-recognition
language:
  - en
  - ja
  - ru
  - de
tags:
  - speech-translation
  - simultaneous-translation
  - streaming-asr
  - whisper
  - s2tt
  - mlx
model_id: sbintuitions/hikari-medium
---

# Hikari-medium

[![GitHub](https://img.shields.io/badge/GitHub-sbintuitions%2Fhikari-181717?logo=github)](https://github.com/sbintuitions/hikari)
[![arXiv](https://img.shields.io/badge/arXiv-2603.11578-b31b1b.svg)](https://arxiv.org/abs/2603.11578)

**Hikari-medium** is a streaming speech-to-text translation and transcription model. It emits text incrementally while the speaker is still talking, without waiting for the utterance to finish.

The model supports simultaneous translation between English and several target languages, as well as streaming English ASR. It can run on either:

- **NVIDIA GPUs** using the PyTorch/CUDA backend
- ![New](https://img.shields.io/badge/NEW-brightgreen) **Apple silicon Macs** using the MLX backend

## Highlights

- 🎧 **Simultaneous speech-to-text translation** — produces target-language text while speech is still in progress.
- 🌐 **Multiple language pairs** — EN→JA, EN→RU, EN→DE, and JA→EN.
- 🗣️ **Streaming ASR** — incremental English transcription.
- ⚡ **Low-latency CUDA inference** — fully causal Whisper encoder with CUDA-graph-captured autoregressive decoding.
- 🍎 **Apple silicon support** — native execution on M-series Macs through MLX.
- 🔄 **One checkpoint, multiple tasks** — the task and target language can be selected at runtime.
- 🖥️ **Browser-based demo** — real-time microphone input through a WebRTC-enabled Gradio client.

## Supported tasks

| Task | Description |
|---|---|
| `transcribe` | Simultaneous English speech-to-text transcription |
| `translate` | Simultaneous speech-to-text translation for EN→JA, EN→DE, EN→RU, and JA→EN |

Tasks, languages, and decoding parameters can be changed at runtime through the Gradio interface.

## Architecture

Hikari is a Whisper-style encoder-decoder model whose encoder has been made **fully causal**. This allows the encoder to process streaming audio chunks without access to future audio.

```text
Browser microphone
        │
      WebRTC
        ▼
Gradio client
        │
    WebSocket
        ▼
Hikari server
        │
        ▼
Causal Whisper Encoder
        │
        ▼
Whisper Decoder
        │
        ▼
Streaming text
```

The server provides two interchangeable inference backends behind the same WebSocket interface:

- **PyTorch/CUDA** for NVIDIA GPUs
- **MLX** for Apple silicon

The training procedure and causal-alignment objective are described in the accompanying paper.

## Quick start

Hikari consists of two processes:

1. A **server** that runs the model.
2. A **client** that provides the browser-based Gradio interface.

Choose the server backend that matches your hardware.

| Hardware | Backend | Expected operation |
|---|---|---|
| NVIDIA GPU | PyTorch/CUDA | Real time; tested on A100 and H100 |
| Apple silicon Mac | MLX | Exact mode is generally slower; approximate refresh mode can approach real time |
| Intel Mac, AMD GPU, or CPU-only machine | Not supported as a model server | The client can still run on CPU |

The real-time factor, or **RTF**, is processing time divided by audio duration. An RTF below 1 means that processing is faster than real time.

### Option A: NVIDIA GPU

The server normally runs on a GPU machine, while the client runs on the local machine.

#### 1. Create an environment

```bash
uv venv .venv --python=3.10
source .venv/bin/activate
```

#### 2. Install the CUDA dependencies and Hikari

On the server machine:

```bash
uv pip install \
    torch==2.8.0 \
    torchcodec==0.7.0 \
    torchaudio==2.8.0 \
    torchvision==0.23.0 \
    --index-url https://download.pytorch.org/whl/cu126

uv pip install \
    "hikari @ git+https://github.com/sbintuitions/hikari"
```

On the client machine:

```bash
uv pip install \
    "hikari @ git+https://github.com/sbintuitions/hikari"
```

#### 3. Start the server

```bash
hikari-server \
    --port 4440 \
    --checkpoint sbintuitions/hikari-medium \
    --device cuda:0
```

The `--checkpoint` argument accepts either a Hugging Face Hub model ID or a local checkpoint path. When given a Hub ID, Hikari downloads the checkpoint automatically.

The CUDA server loads the model and captures CUDA graphs for the encoder and decoder before accepting WebSocket connections.

#### 4. Create an SSH tunnel if the server is remote

```bash
ssh -L 4440:localhost:4440 <GPU_HOST>
```

Then start the client as described in [Start the client](#start-the-client).

### Option B: Apple silicon Mac with MLX

The MLX backend runs the model on the integrated GPU of an Apple silicon Mac. The server and client can run on the same machine, so an SSH tunnel is not required.

#### 1. Create an environment

```bash
uv venv .venv --python=3.10
source .venv/bin/activate
```

#### 2. Install the dependencies and MLX-enabled Hikari

```bash
uv pip install \
    torch==2.8.0 \
    torchaudio==2.8.0

uv pip install \
    "hikari[mlx] @ git+https://github.com/sbintuitions/hikari"
```

On macOS, PyTorch is used only for Silero VAD. Model inference is performed by MLX.

#### 3. Start the server

For exact reference behavior:

```bash
hikari-server \
    --port 4440 \
    --checkpoint sbintuitions/hikari-medium \
    --backend mlx
```

For faster approximate inference, recommended on fanless MacBook Air models:

```bash
hikari-server \
    --port 4440 \
    --checkpoint sbintuitions/hikari-medium \
    --backend mlx \
    --refresh-stride 16
```

#### 4. Configure the client

Start the client, set **Decoder context length** to **100** in the UI, and click **Reset / Apply Settings**.

The default context length of 337, and the `max` setting, are substantially more expensive on a Mac. The `--refresh-stride` setting belongs to the server and is preserved when client-side settings are applied.

The UI displays a `Server in_q` value. If this number continually increases, the server is not keeping up with incoming audio. In that case:

- reduce the decoder context length; or
- enable `--refresh-stride`.

## MLX refresh-stride mode

By default, Hikari re-encodes its complete sliding audio window every 80 ms. This exact behavior is computationally expensive on a laptop GPU.

When the server is started with `--refresh-stride K`, the encoder window advances in blocks of `K` steps:

- The complete window is re-encoded once every `K` steps.
- Between full refreshes, only the newest audio is encoded on top of the cached encoder state.
- The decoder is still recomputed from scratch at every step.
- Decoder KV caching is not currently used.

### Accuracy and performance trade-off

Refresh-stride mode is **approximate**. Cached frames retain the context from the step at which they were computed, and the beginning of the encoder window moves in `K`-step blocks.

A full refresh is triggered automatically when loud speech begins because this changes Whisper's mel normalization. Internal checks found that the logits remained close to those from a fresh recomputation, but validation so far has been limited to transcription on a short English clip.

Users should therefore evaluate the approximate mode on their own audio, target language, and deployment conditions before relying on it.

The default mode without `--refresh-stride` remains the exact reference implementation.

### Choosing a stride

`--refresh-stride 16` is a practical default:

- A smaller value refreshes the full encoder window more frequently. It should stay closer to exact inference, but it is slower.
- A larger value is faster, but allows cached encoder frames to become older.
- Every `K`-th step performs a full refresh and can take approximately 2.5 times longer than an intermediate step, introducing a small amount of latency jitter.
- Smaller decoder contexts reduce compute further.

Only stride values 8 and 16 have been benchmarked by the authors.

## Measured Apple silicon performance

The following measurements were collected on an M4 MacBook Air using English transcription.

| Mode | Decoder context | Initial RTF | RTF after approximately 5 minutes |
|---|---:|---:|---:|
| Exact | 100 | ≈ 2.6 | Not measured |
| `--refresh-stride 16` | 100 | ≈ 0.7 | ≈ 1.0–1.3 |
| `--refresh-stride 16` | 75 | ≈ 0.65 | ≈ 1.0 |

A fanless MacBook Air heats up and throttles under sustained model inference. As a result, real-time operation on this hardware can become borderline during longer sessions even when the initial RTF is comfortably below 1.

Macs with active cooling may have more performance headroom, but this has not yet been measured.

For best results on Apple silicon:

- Turn off **Low Power Mode**. It reduced GPU throughput by approximately 2.5 times in testing on an M4 MacBook Air.
- Keep the machine connected to power and well ventilated.
- Close other GPU-intensive applications.
- Use a decoder context length of 100 or less.
- Benchmark for at least five minutes, since the first minute is not representative of sustained performance.

Translation and transcription use the same model compute. The measurements above were collected using transcription.

To benchmark your own machine:

```bash
python benchmarks/bench_mlx.py \
    --audio some_english.wav \
    --window 100 \
    --stride 16 \
    --seconds 300 \
    --report-every 750
```

The helper script below prints the macOS Low Power Mode state before and after a command:

```bash
benchmarks/run_checked.sh <command>
```

## Start the client

Run the client on your local machine:

```bash
hikari-client \
    --server-port 4440 \
    --app-port 5666 \
    --chunk-ms 80
```

Then open [http://localhost:5666](http://localhost:5666) in a browser.

Due to current HPC security constraints, the client is intended to run locally rather than being hosted on the remote GPU server.

## Development installation

Clone the repository:

```bash
git clone https://github.com/sbintuitions/hikari.git
cd hikari
```

For CUDA development:

```bash
uv venv .venv --python=3.10
source .venv/bin/activate

uv pip install \
    torch==2.8.0 \
    torchcodec==0.7.0 \
    torchaudio==2.8.0 \
    torchvision==0.23.0 \
    --index-url https://download.pytorch.org/whl/cu126

uv pip install -e ".[dev]"
```

For MLX development on Apple silicon:

```bash
uv venv .venv --python=3.10
source .venv/bin/activate

uv pip install \
    torch==2.8.0 \
    torchaudio==2.8.0

uv pip install -e ".[mlx,dev]"
```

The two inference implementations are located in:

- `hikari.server.model_wrapper` for PyTorch/CUDA
- `hikari.server.model_wrapper_mlx` for MLX
- `src/hikari/mlx/` for the MLX model implementation

To compare the MLX implementation with the PyTorch reference:

```bash
pytest tests/
```

These tests require golden reference dumps produced by:

```bash
python benchmarks/make_reference.py
```

Tests that require missing reference dumps skip themselves automatically.

## Requirements

### NVIDIA server

- Python ≥ 3.10
- PyTorch ≥ 2.8.0 with CUDA
- NVIDIA CUDA GPU
- Tested on A100 and H100 GPUs

### Apple silicon server

- Python ≥ 3.10
- macOS on an M-series Mac
- MLX ≥ 0.31, installed through the `mlx` extra
- CPU PyTorch for Silero VAD
- Sufficient unified memory for approximately 1.5 GB of fp16 weights plus working memory

### Client

The client runs on CPU and supports macOS, Linux, and Windows.

The first launch requires internet access to download:

- the Hikari checkpoint;
- the Silero VAD; and
- the Whisper tokenizer.

## Limitations

- The model server does not currently support Intel Macs, AMD GPUs, or CPU-only inference.
- Apple silicon exact mode may be slower than real time, particularly on fanless hardware.
- MLX refresh-stride mode trades exact recomputation for speed and should be evaluated for each deployment.
- Sustained performance on fanless Macs may degrade because of thermal throttling.
- The reported MLX measurements come from an M4 MacBook Air and should not be assumed to represent all Apple silicon devices.
- The MLX approximate mode has so far received only limited validation on a short English transcription sample.
- Streaming output may be revised as additional audio context becomes available.

## Acknowledgements

Hikari is based on OpenAI's [Whisper](https://huggingface.co/openai/whisper-medium) and reuses code components from Kyutai's [Moshi](https://github.com/kyutai-labs/moshi).

## License

Hikari-medium is released under the [MIT License](https://github.com/sbintuitions/hikari/blob/main/LICENSE).

## Citation

If you use Hikari in your work, please cite:

```bibtex
@misc{koshkin2026streamingtranslationtranscriptionspeechtotext,
      title        = {Streaming Translation and Transcription Through Speech-to-Text Causal Alignment},
      author       = {Roman Koshkin and Jeon Haesung and Lianbo Liu and Hao Shi and Mengjie Zhao and Yusuke Fujita and Yui Sudo},
      year         = {2026},
      eprint       = {2603.11578},
      archivePrefix = {arXiv},
      primaryClass = {cs.CL},
      url          = {https://arxiv.org/abs/2603.11578}
}
```

## Links

- [GitHub repository](https://github.com/sbintuitions/hikari)
- [Paper](https://arxiv.org/abs/2603.11578)
- [Whisper-medium](https://huggingface.co/openai/whisper-medium)