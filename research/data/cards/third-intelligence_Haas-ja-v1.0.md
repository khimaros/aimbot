---
license: apache-2.0
language:
  - ja
library_name: nemo
pipeline_tag: automatic-speech-recognition
datasets:
  - reazon-research/reazonspeech
  - espnet/yodas
tags:
  - speech
  - audio
  - automatic-speech-recognition
  - japanese
  - TDT
  - FastConformer
  - Conformer
  - KDA
  - NeMo
---

# Haas-ja-v1.0

[![Code: GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/third-intelligence/Haas-ASR)
[![Demo: Hugging Face Space](https://img.shields.io/badge/Demo-Hugging%20Face%20Space-yellow?logo=huggingface)](https://third-intelligence-haas-ja-v1-0.hf.space/longform)
[![Blog](https://img.shields.io/badge/Blog-Third%20Intelligence-green)](https://third-intelligence.com/ja/posts/haas-ja-v1-release)
[![Benchmark: asr-ja-bench](https://img.shields.io/badge/Benchmark-asr--ja--bench-orange)](https://huggingface.co/datasets/third-intelligence/asr-ja-bench)
[![Metrics: jacer](https://img.shields.io/badge/Metrics-jacer-purple)](https://github.com/third-intelligence/jacer)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue)](https://www.apache.org/licenses/LICENSE-2.0)

Haas-ja-v1.0 is a Japanese speech recognition model built to be both fast and
accurate. It is based on NVIDIA's Parakeet-TDT architecture: a FastConformer encoder
and a Token-and-Duration Transducer (TDT) decoder, here with a prediction network
that uses Kimi Delta Attention (KDA). The name is an acronym of *Hear Anything At
Speed* and a nod to Helmut Haas, the acoustician behind the Haas (precedence) effect
used in stereo sound and other audio technology.

At release, Haas-ja-v1.0 sits on the Pareto frontier of speed and accuracy on a
benchmark built from five public Japanese datasets, and is the most accurate of the
open models we evaluated (CER strict 6.12%). Its accuracy is competitive with major
commercial speech-to-text APIs at a small fraction of their cost.

The [blog post](https://third-intelligence.com/ja/posts/haas-ja-v1-release) covers the development in more detail, including a
preliminary experiment comparing prediction networks, the evaluation design and the
full results.

## Model details

Haas-ja-v1.0 follows Parakeet-TDT: a FastConformer encoder and a TDT decoder. TDT
extends RNN-T by also predicting how long each token lasts, so decoding can jump
ahead several encoder frames at a time instead of visiting every frame. Haas-ja-v1.0
replaces the LSTM in Parakeet-TDT's prediction network with Kimi Delta Attention
(KDA), which improves accuracy at almost the same inference speed.

![Haas-ja-v1.0 architecture](assets/architecture.png)

| Property | Value |
|---|---|
| Parameters | 615.8M (encoder 608.9M, prediction network 3.9M, joint network 3.0M) |
| Input | 16 kHz mono audio; 128-bin log-mel spectrogram (25 ms window, 10 ms hop) |
| Encoder | FastConformer, 24 layers, hidden size 1,024, 8 attention heads, 8× subsampling (80 ms per frame), full context |
| Prediction network | Kimi Delta Attention, 2 layers, hidden size 640, 5 heads × 64 |
| Joint network | Hidden size 640; token and duration outputs; durations 0–4 frames |
| Tokenizer | SentencePiece BPE trained on Japanese data, 3,072 tokens, byte fallback |
| Decoding | Greedy, batched |

The full architecture configuration is in [`config.yaml`](config.yaml).

## How to use

Requirements: Linux with an NVIDIA GPU, Python 3.11+ and NeMo 2.7. The prediction
network runs on kernels from
[flash-linear-attention](https://github.com/fla-org/flash-linear-attention), which
needs Triton and CUDA, so CPU and macOS are not supported.

**Try it with the repository**

Clone the [GitHub repository](https://github.com/third-intelligence/Haas-ASR) and
install it with [uv](https://docs.astral.sh/uv/), which installs the exact
dependency versions we tested:

```bash
git clone https://github.com/third-intelligence/Haas-ASR.git
cd Haas-ASR
uv sync
uv run python examples/quickstart.py --model third-intelligence/Haas-ja-v1.0 example.wav
```

**Use it in your own project**

Install the inference package into your environment:

```bash
pip install "haas-asr @ git+https://github.com/third-intelligence/Haas-ASR.git"
```

Then transcribe:

```python
import haas_asr

model = haas_asr.load_model("third-intelligence/Haas-ja-v1.0")
audio = haas_asr.load_audio("example.wav")
output = model.transcribe([audio])
print(output[0].text)
```

`load_model` returns a regular NeMo `ASRModel` and runs it in bfloat16 on a GPU, the
precision used for the evaluation below. `haas_asr.load_audio` reads a WAV, FLAC, MP3
or OGG file, averages stereo to mono and resamples it to 16 kHz, the model's input.

For recordings longer than 30 seconds, use `transcribe_longform`. It splits the audio
at quiet points (detected by volume) and transcribes the pieces in batches:

```python
audio = haas_asr.load_audio("example.flac")
text = haas_asr.transcribe_longform(model, audio, batch_size=64)
```

**Custom vocabulary**

Names and terms the model rarely heard in training can be listed, so that it
recognizes them more often and writes them as you want:

```python
vocabulary = haas_asr.Vocabulary(
    {"Haas": ["ハース"], "Third Intelligence": ["サードインテリジェンス"]}
)
texts = haas_asr.transcribe(model, [audio], vocabulary=vocabulary)  # short clips
text = haas_asr.transcribe_longform(model, audio, vocabulary=vocabulary)
```

Each word maps its written form to its readings, the ways Haas would write it (usually
in kana; several, or none if Haas already writes it as listed). The readings are
boosted while decoding with NeMo's
[GPU phrase boosting](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/asr/asr_customization/word_boosting.html),
and replaced by the written form wherever found. Boosting can also change text where
no listed word was said, so audio without speech is not boosted, and each audio is
also decoded without the words: a change is kept only where it includes a whole listed
word. Both decodes share one encoder pass, so a vocabulary costs about 1.3 times the
time. See the
[repository](https://github.com/third-intelligence/Haas-ASR#custom-vocabulary) for
details.

**Speaker labels**

Combined with NVIDIA's speaker diarization model
[Nemotron-3-Diarization](https://huggingface.co/nvidia/Nemotron-3-Diarization), Haas
produces transcripts with speaker labels. The repository has a
[runnable example](https://github.com/third-intelligence/Haas-ASR#speaker-labels-with-nemotron-3-diarization).

## Training data

The model was trained on about 46,000 hours of audio from public corpora
([ReazonSpeech](https://huggingface.co/datasets/reazon-research/reazonspeech),
[Common Voice 26.0](https://commonvoice.mozilla.org) and
[YODAS](https://huggingface.co/datasets/espnet/yodas)) and internal data. An in-house
filtering pipeline removed low-quality samples. To keep the evaluation fair, the
benchmark data is kept fully separate: none of it, including held-out portions, was
used for training.

## Evaluation

**Benchmark Dataset**

The benchmark, asr-ja-bench v1.1, combines five public datasets chosen to cover a
range of speaking styles and domains (18,318 utterances, 23.38 hours). We checked
samples by hand and corrected or removed those unsuitable for evaluation, such as
silent audio or transcripts that don't match the audio. The per-sample metadata
(source IDs, corrections and removals) is published as
[asr-ja-bench](https://huggingface.co/datasets/third-intelligence/asr-ja-bench), with
a script that rebuilds the benchmark from the original datasets.

The datasets are summarized below.

| Dataset | Content | Utterances | Hours |
|---|---|---:|---:|
| JSUT basic5000 | Read sentences designed to cover the readings of the jōyō kanji | 5,000 | 6.78 |
| JVNV | Emotional speech, with transcribed nonverbal vocalizations | 1,375 | 3.33 |
| TEDxJP-10K | Random segments of the "TEDx talks in Japanese" playlist, with manually corrected subtitles | 9,200 | 8.21 |
| FLEURS | English Wikipedia sentences translated into Japanese and read aloud | 650 | 2.36 |
| SpeechBSD | Business-scene dialogue | 2,093 | 2.70 |

**Metrics**

The same Japanese word can be written in several ways (kanji or Arabic numerals,
different okurigana, kanji or kana), so references and hypotheses are normalized with
the [`jacer`](https://github.com/third-intelligence/jacer)
library before the character error rate (CER) is computed. Three CER variants show
what kind of error was made:

- **CER strict** counts writing a word in kanji where the reference uses kana, or the
  other way round, as an error. This is the primary metric.
- **CER flex** ignores the choice between kanji and kana, but still counts homophone
  errors.
- **CER kana** compares readings, so it only measures whether the sounds were heard
  correctly.

CER is micro-averaged within each dataset, and the overall score weights each dataset
by its audio duration. [`examples/evaluate_asr_ja_bench.py`](https://github.com/third-intelligence/Haas-ASR/blob/main/examples/evaluate_asr_ja_bench.py)
in the repository reproduces the Haas-ja-v1.0 results.

**Results**

In each cell, the top value is CER strict and the bottom values are CER flex / kana
(%, lower is better). Models are sorted by weighted CER strict.

Haas-ja-v1.0 reaches a weighted CER strict of 6.12%, the best of the open models
evaluated. It is competitive with commercial APIs: on par with GPT-Transcribe (6.07%),
while MAI-Transcribe 2, Scribe v2 and Gemini 3.1 Pro remain more accurate.

![CER of each model on the five datasets and RTFx](assets/cer_table.png)

Among open models, Haas-ja-v1.0 is on the Pareto frontier of speed and accuracy. It
runs at almost the same speed as Parakeet (RTFx 3,236 vs. 3,407) while cutting CER
strict by about 1.1 points, and is about 15–17 times faster than Nemotron 3.5
Transcribe and Whisper large-v3, the next most accurate open models.

![CER strict against RTFx / Speed Factor for all models](assets/cer_vs_rtfx.png)

RTFx (seconds of audio transcribed per second) was measured for every open model on
one NVIDIA H200 at batch size 512 (Whisper large-v3 at 256, to fit in memory), and
depends on the hardware and batch size. Nemotron 3.5 Transcribe ran on a vLLM server
with the settings recommended in NVIDIA's model card. For commercial APIs, the Speed
Factor is the audio duration divided by the total response time through OpenRouter.
It includes the network and each provider's own processing, so it is a reference
rather than a like-for-like comparison.

In cost terms, Haas-ja-v1.0 transcribes an hour of audio for about $0.003–0.004:
roughly 1/70–1/100 of GPT-Transcribe (about $0.30), which has similar accuracy, and
about 1/30 of MAI-Transcribe 2 and Scribe v2 (about $0.11), two of the cheapest
commercial APIs.

![CER strict against inference cost per hour of audio](assets/cer_vs_cost.png)

Open-model costs are estimated from the measured H200 time and on-demand H200 prices
in Japan regions (AWS p5en.48xlarge in Tokyo, Azure ND96isr H200 v5 in Japan East),
assuming the GPU is always busy; they exclude the operating costs and margins of
running a service. API costs are what OpenRouter billed during the evaluation.

## Limitations

- **Streaming.** The model is trained for offline transcription, where it sees the whole
  utterance at once. It can still produce live captions by re-transcribing the current
  phrase as audio arrives (see the demo in the repository), but low-latency streaming
  may need further tuning.
- **Non-verbal information.** On its own, the model transcribes what is said, not who
  says it or how: speaker identity, emotion and other non-verbal information are not
  recognized. Speaker labels are possible by combining it with a diarization model (see
  How to use).
- **Output format.** The output style cannot be controlled, for example whether fillers
  are included. The model tends to omit fillers, and its choices of kanji, kana and
  numerals follow its training data. The custom vocabulary can fix the spelling of
  individual words, but not the style as a whole.

## Acknowledgements

Haas-ja-v1.0 stands on the work of many people, and we are grateful to all of them.
It builds on [NVIDIA NeMo](https://github.com/NVIDIA/NeMo) and the
[Parakeet-TDT](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v2) architecture: a
[FastConformer](https://arxiv.org/abs/2305.05084) encoder with a
[Token-and-Duration Transducer](https://arxiv.org/abs/2304.06795) decoder. Its
prediction network uses Kimi Delta Attention from
[Kimi Linear](https://arxiv.org/abs/2510.26692), run on the kernels of
[flash-linear-attention](https://github.com/fla-org/flash-linear-attention), and it was
trained with [Lhotse](https://github.com/lhotse-speech/lhotse). The speaker-label
example uses NVIDIA's
[Nemotron-3-Diarization](https://huggingface.co/nvidia/Nemotron-3-Diarization)
(OpenMDW-1.1). We thank the authors of these projects for making them openly available.

We also thank the creators of [ReazonSpeech](https://huggingface.co/datasets/reazon-research/reazonspeech),
[Common Voice](https://commonvoice.mozilla.org) and
[YODAS](https://huggingface.co/datasets/espnet/yodas), whose openly released speech
made training possible, and the authors of JSUT, JVNV, TEDxJP-10K, FLEURS and
SpeechBSD, whose test sets make up our benchmark.

## License

The model weights and the inference code are released under the
[Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). Third-party
components retain their respective licenses.
