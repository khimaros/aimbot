---
license: other
license_name: nvidia-open-model-license
license_link: https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license
language:
- ar
- de
- en
- es
- fr
- hi
- it
- ja
- ko
- pt
- vi
- zh
metrics:
- CER
- SSIM
datasets:
- MBZUAI/ClArTTS
- tunis-ai/arabic_speech_corpus
- mrfakename/Emilia-YODAS
- MushanW/GLOBE_V2
- nvidia/hifitts-2
- ai4bharat/Kathbath
- joujiboi/japanese-anime-speech
- OpenSpeechHub/Common-Voice-17-Ja
- amphion/Emilia-Dataset
- seastar105/Emilia-YODAS-KO-filtered
- firstpixel/pt-br_char
- doof-ferb/infore1_25hours
library_name: nemo
tags:
- NeMo
- TTS
- PyTorch
- Speech
- Multilingual-TTS
pipeline_tag: text-to-speech
---

# MagpieTTS Multilingual 357M

<style>
img#model-badge {
  display: inline;
}
</style>

[![Model architecture](https://img.shields.io/badge/model_arch-encoder_decoder_transformer-lightgrey#model-badge)](#model-architecture)
| [![Model size](https://img.shields.io/badge/Params-364M-lightgrey#model-badge)](#model-architecture)
| [![Language](https://img.shields.io/badge/Language-multilingual_(12_langs)-lightgrey#model-badge)](#training-dataset)

🤗 **Hugging Face MagpieTTS Multilingual demo**: [magpie_tts_multilingual_demo](https://huggingface.co/spaces/nvidia/magpie_tts_multilingual_demo)

💻 **NeMo Speech Framework**: [github.com/NVIDIA-NeMo/Speech](https://github.com/NVIDIA-NeMo/Speech)

> [!Note]
> July 21, 2026: MagpieTTS v2607 was released with support for 3 new languages (Arabic, Korean, Portuguese).
>
> For the older checkpoints, refer to below tags:
>
> - Released on March 2026, [v2602](https://huggingface.co/nvidia/magpie_tts_multilingual_357m/tree/v2602).
> - Released on January 2026, [v2512](https://huggingface.co/nvidia/magpie_tts_multilingual_357m/tree/v2512).

## Model Details

- **Developed by:** [NVIDIA](https://www.nvidia.com/)
- **Model type:** Multilingual text-to-speech (encoder–decoder transformer, 364M parameters)
- **Languages:** ar, de, en, es, fr, hi, it, ja, ko, pt, vi, zh
- **License:** [NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license)
- **Version:** v2607 (latest); previous: v2602, v2512
- **Library:** [NeMo Speech](https://github.com/NVIDIA-NeMo/Speech)

### Model Description

MagpieTTS is an end-to-end multilingual neural text-to-speech model that synthesizes speech using 5 English speaker voices — Aria, Jason, Leo, Sofia, and [John Van Stan](https://librivox.org/reader/9017?primary_key=9017&search_category=reader&search_page=1&search_form=get_results&search_order=alpha) — across 12 languages: Arabic (ar), Chinese (zh), English (en), French (fr), German (de), Hindi (hi), Italian (it), Japanese (ja), Korean (ko), Portuguese (pt), Spanish (es), and Vietnamese (vi). The model adopts a transformer encoder–decoder architecture that autoregressively predicts discrete audio codec tokens, using multi-codebook prediction (typically 8 codebooks) with frame stacking (factor = 2) and a local transformer for fine-grained refinement of high-fidelity audio. To improve robustness and controllability, training incorporates attention priors for stable text-to-audio alignment, classifier-free guidance (CFG) for stronger conditioning, and Group Relative Policy Optimization (GRPO) for preference-aligned generation. At inference time, MagpieTTS supports batched synthesis of complete utterances as well as long-form generation of extended text via a sliding-window mechanism; the predicted codec tokens are then decoded into speech waveforms by a frozen pretrained audio codec model ([NanoCodec](https://huggingface.co/nvidia/nemo-nano-codec-22khz-1.89kbps-21.5fps)). This release also removed zero-shot voice-cloning capability for security reasons, and added IPA grapheme-to-phoneme (G2P) support for custom dictionaries and code-switching, and updated G2P support for English-to-Katakana code-switching.

This model is ready for commercial use.

### Key Features

- **Multilingual Support** — Synthesizes natural speech across all 12 supported languages with consistent speaker identity.
- **Expressive Voices** — Multiple voice options with emotional tones and gender variations including 4 proprietary voices and 1 public voice.
- **Text Normalization** — Built-in text normalization for handling numbers, abbreviations, and special characters for all 12 languages.
- **Efficient High-Fidelity Decoding** — A local transformer with frame stacking (factor = 2) performs multi-codebook refinement on stacked frames, improving audio quality while reducing sequence length for faster generation.

### Model Sources

- **Demo:** [magpie_tts_multilingual_demo](https://huggingface.co/spaces/nvidia/magpie_tts_multilingual_demo)
- **Repository:** [NVIDIA NeMo Speech](https://github.com/NVIDIA-NeMo/Speech)
- **Enterprise API:** [MagpieTTS NIM](https://build.nvidia.com/nvidia/magpie-tts-multilingual)
- **Voice-agent examples:** [NVIDIA voice-agent-examples](https://github.com/NVIDIA/voice-agent-examples/tree/riva_voice_agent_example)
- **Nemotron:** [Overview](https://www.nvidia.com/en-us/ai-data-science/foundation-models/nemotron/) · [Developer](https://developer.nvidia.com/nemotron)

## Uses

### Direct Use

MagpieTTS is for developers, researchers, and product teams building multilingual speech applications that need consistent speaker voices across 12 languages. Typical applications include cascade voice agents, audiobook and content narration, accessibility tools, dubbing and localization pipelines, and interactive media. IPA grapheme-to-phoneme (G2P) support for custom dictionaries and code-switching (including English-to-Katakana) also enables mixed-language content and domain-specific pronunciation.

MagpieTTS acts as a dedicated speech-generation layer that plugs into existing AI pipelines without changing upstream language models or downstream audio handling. In cascade voice-agent setups, it converts Large Language Model (LLM) text into natural, real-time speech for user playback. It can also replace or extend existing NVIDIA TTS integrations when multilingual coverage from a single unified model is required.

**Deployment Geography:** Global

### Out-of-Scope Use

This model is not intended for zero-shot voice cloning, languages outside the 12 supported languages, or use cases that bypass the [NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license) terms. See [Technical Limitations & Mitigations](#technical-limitations--mitigations) for additional constraints.

## Model Architecture

**Architecture Type:** Transformer Encoder, Transformer Decoder, Local Transformer, and Feedforward Layers

<img src="magpietts_architecture.png" alt="MagpieTTS Model Architecture" width="600">

*Figure 1: MagpieTTS Model Architecture*

**Network Architecture:**

1. Causal Transformer Encoder with 6 layers, learnable positional encoder of length 2048, and 1 Layer Normalization output layer.
2. Causal Transformer Decoder with 12 layers, learnable positional encoder of length 2048, and 1 Layer Normalization output layer.
3. Local Transformer for multi-codebook refinement, operating on stacked frames with a frame stacking factor of 2 to improve audio quality and reduce sequence length.

**Number of model parameters:** `3.64 x 10^8` (364M parameters)

### Inputs & Outputs

**Input Type(s):** Text<br>
**Input Format:** String<br>
**Input Parameters:** One-Dimensional (1D)<br>
**Other Properties Related to Input:** Text input is UTF-8 encoded; text normalization is required.

**Output Type(s):** Audio<br>
**Output Format:** WAV<br>
**Output Parameters:** One-Dimensional (1D)<br>
**Other Properties Related to Output:** Mono, PCM-encoded 16 bit audio; sampling rate of 22.05 kHz; Audio output with dimensions (B x T), where B is batch size and T is time dimension.

## How to Get Started with the Model

> [!TIP]
> Try the [hosted API](#hosted-api-quickstart), run locally with [NeMo-Speech.cpp](#run-magpietts-locally-with-nemo-speechcpp), or use the [NeMo Speech Framework](#local-inference-with-nemo) for Python inference and training.

### Hosted API Quickstart

<a id="hosted-api-quickstart"></a>

Synthesize speech using the hosted NVIDIA NIM API on [Magpie TTS Multilingual](https://build.nvidia.com/nvidia/magpie-tts-multilingual) — no local GPU, Docker, or checkpoint download required.

**1. Get a free API key:** Open [Magpie TTS Multilingual](https://build.nvidia.com/nvidia/magpie-tts-multilingual) and choose **Get API Key**.

**2. Install the Riva client:**

```bash
pip install nvidia-riva-client
```

**3. Synthesize speech to a WAV file:**

```python
import wave

import riva.client
from riva.client.proto.riva_audio_pb2 import AudioEncoding

auth = riva.client.Auth(
    uri="grpc.nvcf.nvidia.com:443",
    use_ssl=True,
    metadata_args=[
        ["function-id", "877104f7-e885-42b9-8de8-f6e4c6303969"],
        ["authorization", "Bearer nvapi-YOUR_API_KEY"],
    ],
)

service = riva.client.SpeechSynthesisService(auth)

sample_rate_hz = 22050
resp = service.synthesize(
    "Hello from the Magpie multilingual hosted API.",
    "Magpie-Multilingual.EN-US.Sofia",
    "en-US",
    sample_rate_hz=sample_rate_hz,
    encoding=AudioEncoding.LINEAR_PCM,
)

with wave.open("out.wav", "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sample_rate_hz)
    wf.writeframesraw(resp.audio)
```

**Or use the CLI (list voices, then synthesize):**

```bash
git clone https://github.com/nvidia-riva/python-clients.git
export NVIDIA_API_KEY="nvapi-YOUR_API_KEY"

python python-clients/scripts/tts/talk.py \
    --server grpc.nvcf.nvidia.com:443 --use-ssl \
    --metadata function-id "877104f7-e885-42b9-8de8-f6e4c6303969" \
    --metadata authorization "Bearer $NVIDIA_API_KEY" \
    --list-voices

python python-clients/scripts/tts/talk.py \
    --server grpc.nvcf.nvidia.com:443 --use-ssl \
    --metadata function-id "877104f7-e885-42b9-8de8-f6e4c6303969" \
    --metadata authorization "Bearer $NVIDIA_API_KEY" \
    --text "Hello from Magpie." \
    --voice "Magpie-Multilingual.EN-US.Sofia" \
    --language-code en-US \
    --sample-rate-hz 22050 \
    -o out.wav
```

> **Note:** Voice IDs and supported sample rates follow the deployed NIM. Use `--list-voices` against this endpoint, or see the **API Reference** on the [Magpie TTS Multilingual](https://build.nvidia.com/nvidia/magpie-tts-multilingual) page.

### Run MagpieTTS locally with NeMo-Speech.cpp

[NeMo-Speech.cpp](https://github.com/NVIDIA/NeMo-Speech.cpp) provides a
lightweight native C++ runtime for running this model locally. It downloads the
v2607 GGUF, tokenizer assets, and companion NanoCodec decoder automatically.

After [installing NeMo-Speech.cpp](https://github.com/NVIDIA/NeMo-Speech.cpp#installation):

```bash
nemo-speech synthesize "Hello from Magpie Multilingual." \
  --output speech.wav
```

Use `nemo-speech pull magpie` to download the model stack without running
synthesis.

### Python Inference with the NeMo Speech Framework

<a id="local-inference-with-nemo"></a>

To train, fine-tune or perform TTS with this model, you will need to install [NVIDIA NeMo Speech](https://github.com/NVIDIA-NeMo/Speech). We recommend you install it after you've installed latest PyTorch version and Python version ≥ 3.10.12.

```
pip install nemo_toolkit[tts]@main
pip install kaldialign
```

The model is available for use in the [NVIDIA NeMo Speech Framework](https://github.com/NVIDIA-NeMo/Speech), and can be used as a pre-trained checkpoint for inference or for fine-tuning on another dataset.

Two inference paths are available: **Method 1** (single utterance) and **Method 2** (batch inference and evaluation).

#### Method 1 — Single utterance inference

Synthesize one `(text, language)` pair at a time. Text normalization can be applied for all 12 languages.
Load the open-source MagpieTTS checkpoint from Hugging Face and call the model's `do_tts(transcript: str, language: str, apply_TN: bool, use_cfg: bool, speaker_index: int)` method. This returns the generated audio and the length of the audio.

```python
from nemo.collections.tts.models import MagpieTTSModel

speaker_map = {
    "Aria": 0,
    "Jason": 1,
    "John": 2,
    "Leo": 3,
    "Sofia": 4,
}
transcript = "Hello world from NeMo Text to Speech."
language = "en"
speaker = "Sofia"
speaker_idx = speaker_map[speaker]

# Load the latest checkpoint (from the `main` branch).
model = MagpieTTSModel.from_pretrained("nvidia/magpie_tts_multilingual_357m")
audio, audio_len = model.do_tts(transcript, language=language, apply_TN=False, speaker_index=speaker_idx)

# To apply custom phoneme customization in supported languages like English
# Surround the IPA string in a '|' character and add a space token between each IPA character.
ipa_transcript = "Hello world from | ˈ n ɛ m o ʊ | Text to Speech."
audio, audio_len = model.do_tts(ipa_transcript, language=language, apply_TN=False, speaker_index=speaker_idx)
```

<details open>
<summary><strong>Choosing a model version</strong></summary>

`from_pretrained(...)` always loads the latest checkpoint from the `main` branch. To load a specific release instead, download the `.nemo` file for that version tag and restore it with `restore_from(...)`. Available tags: `v2607` (latest, on `main`), `v2602`, and `v2512`.

```python
from huggingface_hub import hf_hub_download
from nemo.collections.tts.models import MagpieTTSModel

# Pin a specific release by its tag (branch, tag, or commit hash).
model_path = hf_hub_download(
    repo_id="nvidia/magpie_tts_multilingual_357m",
    filename="magpie_tts_multilingual_357m.nemo",
    revision="v2602",
)
model = MagpieTTSModel.restore_from(model_path)
```

</details>

#### Method 2 — Batch inference and evaluation

Run batch inference and optional evaluation with `examples/tts/magpietts_inference.py`. The script supports:

- Batch inference from `.nemo` files or `.ckpt` checkpoints
- Optional evaluation with metrics — Character Error Rate (CER), Speaker Similarity (SSIM), and UTMOSv2
- Multiple datasets in a single run

<details open>
<summary><strong>Dataset configuration</strong> (<code>examples/tts/evalset_config.json</code>)</summary>

The script requires a JSON configuration file that defines the metadata for the datasets to process.

**Format**

```json
{
    "dataset_name_1": {
        "manifest_path": "/absolute/path/to/manifest.json",
        "audio_dir": "/",
    },
    "dataset_name_2": {
        "manifest_path": "/path/to/another_manifest.json",
        "audio_dir": "/base/audio/path",
    }
}
```

**Fields**

| Field              | Required | Description                                                                   |
| ------------------ | -------- | ----------------------------------------------------------------------------- |
| `manifest_path`    | Yes      | Absolute path to the NeMo manifest JSON file                                  |
| `audio_dir`        | Yes      | Base directory for audio files. Use `"/"` if manifest contains absolute paths |
| `whisper_language` | No       | Language code for ASR evaluation (default: `"en"`)                            |

**Example**

```json
{
    "libritts_test_clean": {
        "manifest_path": "/data/libritts/test_clean_manifest.json",
        "audio_dir": "/",
        "whisper_language": "en"
    },
    "vctk": {
        "manifest_path": "/data/vctk/manifest.json",
        "audio_dir": "/data/vctk/wav48",
    }
}
```

</details>

<details open>
<summary><strong>Manifest format</strong></summary>

The manifest is a JSON-lines file where each line is a JSON object representing one utterance.

**Minimum required fields**

For **models with fixed speaker context embeddings** (no audio/text conditioning needed):

```json
{
    "audio_filepath": "/path/to/audio.wav",
    "text": "The transcript text.",
    "duration": 3.5
}
```


| Field            | Type   | Description                   |
| ---------------- | ------ | ----------------------------- |
| `audio_filepath` | string | Path to the target audio file |
| `text`           | string | Text transcript to synthesize |
| `duration`       | float  | Audio duration in seconds     |

</details>

<details open>
<summary><strong>Run inference and evaluation</strong></summary>

```bash
# Basic inference (no evaluation)
python examples/tts/magpietts_inference.py \
    --nemo_files "nvidia/magpie_tts_multilingual_357m" \
    --datasets_json_path /path/to/evalset_config.json \
    --out_dir /path/to/output \
    --codecmodel_path "nvidia/nemo-nano-codec-22khz-1.89kbps-21.5fps" \
    --use_cfg \
    --cfg_scale 2.5

# Inference with evaluation
python examples/tts/magpietts_inference.py \
    --nemo_files "nvidia/magpie_tts_multilingual_357m" \
    --datasets_json_path /path/to/evalset_config.json \
    --out_dir /path/to/output \
    --codecmodel_path "nvidia/nemo-nano-codec-22khz-1.89kbps-21.5fps" \
    --run_evaluation \
    --use_cfg \
    --cfg_scale 2.5
```

</details>

<details open>
<summary><strong>Outputs and evaluation metrics</strong></summary>

After running, you'll find:

- Generated audio files in `<out_dir>/<checkpoint_name>/`
- Evaluation metrics in `metrics.json`
- Visualization plots (if evaluation enabled)

When `--run_evaluation` is enabled, the following metrics are computed:


| Metric                  | Description                                                        |
| ----------------------- | ------------------------------------------------------------------ |
| **CER**                 | Character Error Rate (lower is better)                             |
| **WER**                 | Word Error Rate (lower is better)                                  |
| **SSIM (pred-gt)**      | Speaker similarity between predicted and ground truth              |
| **SSIM (pred-context)** | Speaker similarity between predicted and context                   |
| **UTMOSv2**             | Audio quality score (higher is better, requires `utmosv2` package) |
| **RTF**                 | Real-time factor (processing time / audio duration)                |

</details>

## Software & Hardware

**Runtime Engine(s):**

- NVIDIA NeMo Speech Framework 25.11
- NVIDIA Riva 2.24.0

**Acceleration Engine:** Tensor(RT)-LLM, Triton

**Supported Hardware Microarchitecture Compatibility:**

- NVIDIA Ada Lovelace L4
- NVIDIA Ada Lovelace L40
- NVIDIA Ampere A10
- NVIDIA Ampere A30
- NVIDIA Ampere A100
- NVIDIA Hopper H100

**Preferred/Supported Operating System(s):**

- Linux
- Linux 4 Tegra

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA’s hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions.

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment.

## Training and Evaluation Datasets

### Training Dataset

<table>
  <thead>
    <tr><th>Language</th><th>Dataset</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Arabic (UAE, ar-AE)</td>
      <td><a href="https://dataoceanai.com/datasets/asr/uae-arabic-speech-recognition-corpus-corpus-desktop/">UAE Arabic Speech Recognition Corpus (Desktop)</a></td>
    </tr>
    <tr>
      <td>Arabic (MSA, ar-MSA)</td>
      <td>Publicly available internet-scale data (Internal)</td>
    </tr>
    <tr>
      <td rowspan="3">Arabic (Saudi Arabia, ar-SA)</td>
      <td><a href="https://huggingface.co/datasets/MBZUAI/ClArTTS">Classical Arabic Text-to-Speech (ClArTTS)</a></td>
    </tr>
    <tr><td><a href="https://dataoceanai.com/datasets/asr/arabic-saudi-arabia-speech-recognition-corpus-desktop/">Arabic (Saudi Arabia) Speech Recognition Corpus (Desktop)</a></td></tr>
    <tr><td>Publicly available internet-scale data (Internal)</td></tr>
    <tr>
      <td>Arabic (Syrian, ar-SY)</td>
      <td><a href="https://huggingface.co/datasets/tunis-ai/arabic_speech_corpus">Arabic Speech Corpus</a></td>
    </tr>
    <tr>
      <td rowspan="4">Chinese (zh)</td>
      <td><a href="https://www.openslr.org/93/">AISHELL-3</a></td>
    </tr>
    <tr><td><a href="https://huggingface.co/datasets/mrfakename/Emilia-YODAS">Emilia-YODAS Chinese</a></td></tr>
    <tr><td>Publicly available internet-scale data (Internal)</td></tr>
    <tr><td>Riva Speakers (Proprietary)</td></tr>
    <tr>
      <td rowspan="7">English (en)</td>
      <td>David AI (Internal)</td>
    </tr>
    <tr><td><a href="https://huggingface.co/datasets/MushanW/GLOBE_V2">GLOBE-V2</a></td></tr>
    <tr><td><a href="https://www.openslr.org/109">HiFiTTS</a></td></tr>
    <tr><td><a href="https://huggingface.co/datasets/nvidia/hifitts-2">HiFiTTS-2</a></td></tr>
    <tr><td><a href="https://www.openslr.org/60/">LibriTTS</a></td></tr>
    <tr><td>Publicly available internet-scale data (Internal)</td></tr>
    <tr><td>Riva Speakers (Proprietary)</td></tr>
    <tr>
      <td rowspan="2">French (fr)</td>
      <td><a href="https://openslr.org/146/">CML-TTS French</a></td>
    </tr>
    <tr><td>Riva Speakers (Proprietary)</td></tr>
    <tr>
      <td rowspan="2">German (de)</td>
      <td><a href="https://openslr.org/146/">CML-TTS German</a></td>
    </tr>
    <tr><td><a href="https://dataoceanai.com/datasets/asr/german-speech-recognition-corpus-desktop-2">German Speech Recognition Corpus (Desktop)</a></td></tr>
    <tr>
      <td rowspan="3">Hindi (hi)</td>
      <td><a href="https://huggingface.co/datasets/ai4bharat/Kathbath">IndicSUPERB</a></td>
    </tr>
    <tr><td><a href="https://www.openslr.org/104">Multilingual and code-switching ASR Challenge Dataset – sub-task2</a></td></tr>
    <tr><td>Publicly available internet-scale data (Internal)</td></tr>
    <tr>
      <td>Italian (it)</td>
      <td><a href="https://openslr.org/146/">CML-TTS Italian</a></td>
    </tr>
    <tr>
      <td rowspan="4">Japanese (ja)</td>
      <td><a href="https://huggingface.co/datasets/joujiboi/japanese-anime-speech">Japanese Anime Speech Dataset V5</a></td>
    </tr>
    <tr><td><a href="https://huggingface.co/datasets/OpenSpeechHub/Common-Voice-17-Ja">Common Voice Script Speech 17.0 Japanese</a></td></tr>
    <tr><td><a href="https://huggingface.co/datasets/amphion/Emilia-Dataset">Emilia-YODAS Japanese</a></td></tr>
    <tr><td><a href="https://dataoceanai.com/datasets/asr/japanese-conversational-speech-recognition-corpus-mobile/">Japanese Conversational Speech Recognition Corpus (Mobile)</a></td></tr>
    <tr>
      <td>Korean (ko)</td>
      <td><a href="https://huggingface.co/datasets/seastar105/Emilia-YODAS-KO-filtered">Emilia-YODAS Korean</a></td>
    </tr>
    <tr>
      <td rowspan="3">Portuguese (pt)</td>
      <td><a href="https://openslr.org/146/">CML-TTS Portuguese</a></td>
    </tr>
    <tr><td><a href="https://huggingface.co/datasets/firstpixel/pt-br_char">Brazilian Portuguese Merged Speech Dataset</a></td></tr>
    <tr><td><a href="https://github.com/Edresson/TTS-Portuguese-Corpus">TTS-Portuguese Corpus</a></td></tr>
    <tr>
      <td rowspan="3">Spanish (es)</td>
      <td><a href="https://openslr.org/146/">CML-TTS Spanish</a></td>
    </tr>
    <tr><td><a href="https://datasets-dev.vimware.com/">Spanish (Spain) Conversational Smartphone (ESP_ASR003)</a></td></tr>
    <tr><td>Riva Speakers (Proprietary)</td></tr>
    <tr>
      <td rowspan="3">Vietnamese (vi)</td>
      <td>Riva Speakers (Proprietary)</td>
    </tr>
    <tr><td><a href="https://huggingface.co/datasets/doof-ferb/infore1_25hours">InfoRe-1</a></td></tr>
    <tr><td>Publicly available internet-scale data (Internal)</td></tr>
  </tbody>
</table>

**Audio Training Data Size**

- 54,305 Hours

**Properties:**

- Number of data items in training set: `~54.3k` hours
- Data modalities: text and audio
- Nature of the content: Audiobooks, Daily Conversations, podcast interviews, News, Twitter, Youtube
- Languages: 12 languages (Arabic (ar), Chinese (zh), English (en), French (fr), German (de), Hindi (hi), Italian (it), Japanese (ja), Korean (ko), Portuguese (pt), Spanish (es), Vietnamese (vi))
- Sensor Type for Data Collection: Microphones

### Evaluation Dataset

<table>
  <thead>
    <tr><th>Language</th><th>Dataset</th></tr>
  </thead>
  <tbody>
    <tr><td>Arabic (ar)</td><td>Internal</td></tr>
    <tr><td>Chinese (zh)</td><td>Internal</td></tr>
    <tr>
      <td rowspan="2">English (en)</td>
      <td><a href="https://www.openslr.org/60/">LibriTTS test-clean</a></td>
    </tr>
    <tr><td><a href="https://huggingface.co/datasets/MushanW/GLOBE_V2">GLOBE-V2 accent test set</a></td></tr>
    <tr><td>French (fr)</td><td><a href="https://openslr.org/146/">CML-TTS French</a></td></tr>
    <tr><td>German (de)</td><td><a href="https://openslr.org/146/">CML-TTS German</a></td></tr>
    <tr><td>Hindi (hi)</td><td>Internal</td></tr>
    <tr><td>Italian (it)</td><td><a href="https://openslr.org/146/">CML-TTS Italian</a></td></tr>
    <tr><td>Japanese (ja)</td><td>Internal</td></tr>
    <tr><td>Korean (ko)</td><td>Internal</td></tr>
    <tr><td>Portuguese (pt)</td><td><a href="https://openslr.org/146/">CML-TTS Portuguese</a></td></tr>
    <tr><td>Spanish (es)</td><td><a href="https://openslr.org/146/">CML-TTS Spanish</a></td></tr>
    <tr><td>Vietnamese (vi)</td><td>Internal</td></tr>
  </tbody>
</table>

Evaluation data spans all 12 supported languages with the same modalities, content types, and collection method as the training data.

## Evaluation

We report two metrics on per-language held-out test sets:

- **CER** — Character Error Rate (%), lower is better.
- **SSIM** — speaker similarity between prediction and context, higher is better.

<table>
  <thead>
    <tr>
      <th rowspan="2" align="left">Language / dataset</th>
      <th colspan="2" align="center">CER&darr; (%)</th>
      <th colspan="2" align="center">SSIM&uarr; (pred-context)</th>
    </tr>
    <tr>
      <th align="center">v2602</th>
      <th align="center">v2607</th>
      <th align="center">v2602</th>
      <th align="center">v2607</th>
    </tr>
  </thead>
  <tbody>
    <tr><td align="left">Arabic (ar)</td>                   <td align="center">&mdash;</td> <td align="center">1.62</td>      <td align="center">&mdash;</td>  <td align="center">0.806</td>          </tr>
    <tr><td align="left">Chinese (zh)</td>                  <td align="center">&mdash;</td> <td align="center">3.17</td>      <td align="center">&mdash;</td>  <td align="center">0.833</td>          </tr>
    <tr><td align="left">English (en)</td>                  <td align="center">0.34</td>    <td align="center">0.37</td>      <td align="center">0.835</td>    <td align="center">0.822</td>          </tr>
    <tr><td align="left">English (en) <em>accented</em></td><td align="center">&mdash;</td> <td align="center">0.34</td>      <td align="center">&mdash;</td>  <td align="center">0.746</td>          </tr>
    <tr><td align="left">French (fr)</td>                   <td align="center">2.70</td>    <td align="center">1.54</td>      <td align="center">0.703</td>    <td align="center">0.747</td> </tr>
    <tr><td align="left">German (de)</td>                   <td align="center">0.66</td>    <td align="center">0.80</td>      <td align="center">0.626</td>    <td align="center">0.742</td> </tr>
    <tr><td align="left">Hindi (hi)</td>                    <td align="center">&mdash;</td> <td align="center">1.23</td>      <td align="center">&mdash;</td>  <td align="center">0.788</td>          </tr>
    <tr><td align="left">Italian (it)</td>                  <td align="center">&mdash;</td> <td align="center">2.19</td>      <td align="center">&mdash;</td>  <td align="center">0.773</td>          </tr>
    <tr><td align="left">Japanese (ja)</td>                 <td align="center">&mdash;</td> <td align="center">1.40</td>      <td align="center">&mdash;</td>  <td align="center">0.775</td>          </tr>
    <tr><td align="left">Korean (ko)</td>                   <td align="center">&mdash;</td> <td align="center">2.69</td>      <td align="center">&mdash;</td>  <td align="center">0.807</td>          </tr>
    <tr><td align="left">Portuguese (pt)</td>               <td align="center">&mdash;</td> <td align="center">2.91</td>      <td align="center">&mdash;</td>  <td align="center">0.753</td>          </tr>
    <tr><td align="left">Spanish (es)</td>                  <td align="center">1.14</td>    <td align="center">0.60</td>      <td align="center">0.715</td>    <td align="center">0.793</td> </tr>
    <tr><td align="left">Vietnamese (vi)</td>               <td align="center">&mdash;</td> <td align="center">0.59</td>      <td align="center">&mdash;</td>  <td align="center">0.725</td>          </tr>
  </tbody>
</table>

## Technical Limitations & Mitigations

There are two modes of inference, namely, standard and long-form. In standard mode, this model can generate up to 20 seconds of speech at a time in any of the 12 supported languages. In long-form mode, the model performs optimally when the input text contains punctuation and capitalization. The model was trained on a mix of publicly available speech datasets and internally recorded datasets in 12 languages. As a result, it is not suitable for speech generation in any language other than the 12 languages mentioned. We have removed zero-shot capabilities of this model for this release. Text normalization is required.

## Ethical Considerations

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications.  When downloaded or used in accordance with our terms of service, developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.

Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability).

### License / Terms of Use

GOVERNING TERMS: Use of this model is governed by the [NVIDIA Open Model License Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license).

## References

1. Shehzeen Hussain et al., "[Align2speak: Improving TTS for Low Resource Languages via ASR-Guided Online Preference Optimization](https://arxiv.org/abs/2509.21718)", ICASSP, 2026.
2. Roy Fejgin et al., "[Frame-Stacked Local Transformers for Efficient Multi-Codebook Speech Generation](https://arxiv.org/abs/2509.19592)", ICASSP, 2026.
3. Shehzeen Hussain et al., "[Koel-TTS: Enhancing LLM based Speech Generation with Preference Alignment and Classifier Free Guidance](https://arxiv.org/abs/2502.05236)", EMNLP, 2025, ACL.
4. Edresson Casanova et al., "[NanoCodec: Towards High-Quality Ultra Fast Speech LLM Inference](https://arxiv.org/abs/2508.05835)", Interspeech, 2025.
5. Ryan Langman et al., "[HiFiTTS-2: A Large-Scale High Bandwidth Speech Dataset](https://arxiv.org/abs/2506.04152)", Interspeech, 2025.
6. Edresson Casanova et al., "[Low Frame-rate Speech Codec: a Codec Designed for Fast High-quality Speech LLM Training and Inference](https://arxiv.org/abs/2409.12117)", ICASSP, 2025.
7. Paarth Neekhara et al., "[Improving Robustness of LLM-based Speech Synthesis by Learning Monotonic Alignment](https://arxiv.org/abs/2406.17957)", Interspeech, 2024.
