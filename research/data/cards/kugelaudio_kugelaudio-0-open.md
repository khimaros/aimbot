---
language:
  - en
  - de
  - fr
  - es
  - it
  - pt
  - nl
  - pl
  - ru
  - uk
  - cs
  - ro
  - hu
  - sv
  - da
  - fi
  - no
  - el
  - bg
  - sk
  - hr
  - sr
  - tr
license: mit
tags:
  - text-to-speech
  - tts
  - speech-synthesis
  - audio-generation
  - european-languages
  - diffusion
  - autoregressive
pipeline_tag: text-to-speech
inference: false
model-index:
  - name: kugelaudio-0-open
    results:
      - task:
          type: text-to-speech
        dataset:
          type: custom
          name: YODAS2
        metrics:
          - type: win-rate
            value: 78.0
            name: Human Preference vs ElevenLabs
---

# 🎙️ KugelAudio-0-Open

**Open-source text-to-speech for European languages**
7B parameter model powered by an AR + Diffusion architecture

<p align="center">
  <a href="https://github.com/Kugelaudio/kugelaudio-open"><img src="https://img.shields.io/badge/GitHub-Source_Code-black" alt="GitHub Source Code"></a>
  <a href="https://kugelaudio.com"><img src="https://img.shields.io/badge/🌐-Website-blue" alt="KugelAudio Website"></a>
</p>

<table align="center" style="border-collapse: collapse; border: none;">
  <tr style="border: none;">
    <td style="border: none; padding: 0 20px;">
      <a href="https://kugelaudio.com">
        <img src="https://www.kugelaudio.com/logos/Logo%20Short.svg" alt="KugelAudio" style="height: 60px; width: auto;">
      </a>
    </td>
    <td style="border: none; padding: 0 20px;">
      <a href="https://hpi.de/ki-servicezentrum/">
        <img src="https://docs.sc.hpi.de/attachments/aisc/aisc-logo.png" alt="KI-Servicezentrum Berlin-Brandenburg" style="height: 60px; width: auto;">
      </a>
    </td>
    <td style="border: none; padding: 0 20px;">
      <a href="https://www.bmftr.bund.de">
        <img src="https://hpi.de/fileadmin/_processed_/a/3/csm_BMFTR_de_Web_RGB_gef_durch_cd1f5345bd.jpg" alt="Gefördert durch BMFTR" style="height: 60px; width: auto;">
      </a>
    </td>
  </tr>
</table>

License: MIT Python 3.10+ Hosted API

KugelAudio KI-Servicezentrum Berlin-Brandenburg Gefördert durch BMFTR

---

## Motivation

**Open-source text-to-speech models for European languages are significantly lagging behind.** While English TTS has seen remarkable progress, speakers of German, French, Spanish, Polish, and dozens of other European languages have been underserved by the open-source community.

KugelAudio aims to change this. Building on the excellent foundation laid by the [VibeVoice team at Microsoft](https://github.com/microsoft/VibeVoice), we've trained a model specifically focused on European language coverage, using approximately **200,000 hours** of highly pre-processed and enhanced speech data from the [YODAS2 dataset](https://huggingface.co/datasets/espnet/yodas).

## 🏆 Benchmark Results: Outperforming ElevenLabs

**KugelAudio achieves state-of-the-art performance**, beating industry leaders including ElevenLabs in rigorous human preference testing. This breakthrough demonstrates that open-source models can now rival - and surpass - the best commercial TTS systems.

### Human Preference Benchmark (A/B Testing)

We conducted extensive A/B testing with **339 human evaluations** to compare KugelAudio against leading TTS models. Participants listened to a reference voice sample, then compared outputs from two models and selected which sounded more human and closer to the original voice.

### German Language Evaluation

The evaluation specifically focused on **German language samples** with diverse emotional expressions and speaking styles:

* **Neutral Speech**: Standard conversational tones
* **Shouting**: High-intensity, elevated volume speech
* **Singing**: Melodic and rhythmic speech patterns
* **Drunken Voice**: Slurred and irregular speech characteristics

These diverse test cases demonstrate the model's capability to handle a wide range of speaking styles beyond standard narration.

### OpenSkill Ranking Results

| Rank | Model | Score | Record | Win Rate |
|------|-------|-------|--------|----------|
| 🥇 1 | **KugelAudio** | **26** | 71W / 20L / 23T | **78.0%** |
| 🥈 2 | ElevenLabs Multi v2 | 25 | 56W / 34L / 22T | 62.2% |
| 🥉 3 | ElevenLabs v3 | 21 | 64W / 34L / 16T | 65.3% |
| 4 | Cartesia | 21 | 55W / 38L / 19T | 59.1% |
| 5 | VibeVoice | 10 | 30W / 74L / 8T | 28.8% |
| 6 | CosyVoice v3 | 9 | 15W / 91L / 8T | 14.2% |

_Based on 339 evaluations using Bayesian skill-rating system (OpenSkill)_

## Audio Samples

Listen to KugelAudio's diverse voice capabilities across different speaking styles and languages:

### German Voice Samples

| Sample | Description | Audio Player |
|--------|-------------|--------------|
| **Whispering** | Soft whispering voice | <audio controls><source src="https://huggingface.co/kugelaudio/kugelaudio-0-open/resolve/main/samples/258_Lukas_der_Flüsterer.wav" type="audio/wav"></audio> |
| **Female Narrator** | Professional female reader voice | <audio controls><source src="https://huggingface.co/kugelaudio/kugelaudio-0-open/resolve/main/samples/266_Petra_die_Vorleserin.wav" type="audio/wav"></audio> |
| **Angry Voice** | Irritated and frustrated speech | <audio controls><source src="https://huggingface.co/kugelaudio/kugelaudio-0-open/resolve/main/samples/261_Sauerer_Felix.wav" type="audio/wav"></audio> |
| **Radio Announcer** | Professional radio broadcast voice | <audio controls><source src="https://huggingface.co/kugelaudio/kugelaudio-0-open/resolve/main/samples/277_Radio_Lars.wav" type="audio/wav"></audio> |

*All samples are generated using pre-encoded voice embeddings.*

### Training Details

- **Base Model**: [Microsoft VibeVoice](https://github.com/microsoft/VibeVoice)
- **Training Data**: ~200,000 hours from [YODAS2](https://huggingface.co/datasets/espnet/yodas)
- **Hardware**: 8x NVIDIA H100 GPUs
- **Training Duration**: 5 days

### Supported Languages

This model supports the following European languages:

| Language | Code | Flag | Language | Code | Flag | Language | Code | Flag |
|----------|------|------|----------|------|------|----------|------|------|
| English | en | 🇺🇸 | German | de | 🇩🇪 | French | fr | 🇫🇷 |
| Spanish | es | 🇪🇸 | Italian | it | 🇮🇹 | Portuguese | pt | 🇵🇹 |
| Dutch | nl | 🇳🇱 | Polish | pl | 🇵🇱 | Russian | ru | 🇷🇺 |
| Ukrainian | uk | 🇺🇦 | Czech | cs | 🇨🇿 | Romanian | ro | 🇷🇴 |
| Hungarian | hu | 🇭🇺 | Swedish | sv | 🇸🇪 | Danish | da | 🇩🇰 |
| Finnish | fi | 🇫🇮 | Norwegian | no | 🇳🇴 | Greek | el | 🇬🇷 |
| Bulgarian | bg | 🇧🇬 | Slovak | sk | 🇸🇰 | Croatian | hr | 🇭🇷 |
| Serbian | sr | 🇷🇸 | Turkish | tr | 🇹🇷 | | | |

> **📊 Language Coverage Disclaimer**: Quality varies significantly by language. Spanish, French, English, and German have the strongest representation in our training data (~200,000 hours from YODAS2). Other languages may have reduced quality, prosody, or vocabulary coverage depending on their availability in the training dataset.

### Model Specifications

| Property              | Value                                                                       |
| --------------------- | --------------------------------------------------------------------------- |
| **Parameters**        | 7B                                                                          |
| **Architecture**      | AR + Diffusion (Qwen2.5-7B backbone)                                        |
| **Base Model**        | [Microsoft VibeVoice](https://github.com/microsoft/VibeVoice)               |
| **Audio Sample Rate** | 24kHz                                                                       |
| **Audio Format**       | Mono, float32                                                               |
| **VRAM Required**     | \~19GB                                                                      |
| **Training Hardware** | 8x NVIDIA H100                                                              |
| **Training Duration** | 5 days                                                                      |
| **Training Data**     | \~200,000 hours from [YODAS2](https://huggingface.co/datasets/espnet/yodas) |

## Quick Start

### Installation

```bash
# Install with pip
pip install kugelaudio-open

# Or with uv (recommended)
uv pip install kugelaudio-open
```

### Basic Usage

```python
from kugelaudio_open import (
    KugelAudioForConditionalGenerationInference,
    KugelAudioProcessor,
)
import torch

# Load model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = KugelAudioForConditionalGenerationInference.from_pretrained(
    "kugelaudio/kugelaudio-0-open",
    torch_dtype=torch.bfloat16,
).to(device)
model.eval()

processor = KugelAudioProcessor.from_pretrained("kugelaudio/kugelaudio-0-open")

# Strip encoder weights to save VRAM (only decoders needed for inference)
model.model.strip_encoders()

# See available voices
print(processor.get_available_voices())  # ["default", "warm", "clear"]

# Generate speech with a specific voice
inputs = processor(text="Hallo Welt! Das ist KugelAudio.", voice="default", return_tensors="pt")
inputs = {k: v.to(device) if isinstance(v, torch.Tensor) else v for k, v in inputs.items()}

with torch.no_grad():
    outputs = model.generate(**inputs, cfg_scale=3.0)

# Save audio
processor.save_audio(outputs.speech_outputs[0], "output.wav")
```

### Voices

KugelAudio provides pre-encoded voices that can be selected by name. The voices are stored as `.pt` files in the `voices/` folder and are automatically downloaded when needed.

```python
# List available voices
voices = processor.get_available_voices()
print(voices)  # ["default", "warm", "clear"]

# Generate with a specific voice
inputs = processor(text="Hallo, das ist eine warme Stimme!", voice="warm", return_tensors="pt")
inputs = {k: v.to(device) if isinstance(v, torch.Tensor) else v for k, v in inputs.items()}

with torch.no_grad():
    outputs = model.generate(**inputs, cfg_scale=3.0)

processor.save_audio(outputs.speech_outputs[0], "warm_voice_output.wav")
```

> **Note:** Voice cloning from raw audio is not supported in this open-source release. Only the pre-encoded voices listed in `voices/voices.json` are available.

### Generation Parameters

| Parameter        | Default | Description                                                                |
| ---------------- | ------- | -------------------------------------------------------------------------- |
| cfg\_scale       | 3.0     | Classifier-free guidance scale (1.0-10.0). Higher = more adherence to text |
| max\_new\_tokens | 2048    | Maximum number of tokens to generate                                       |
| do\_sample       | False   | Whether to use sampling (vs greedy decoding)                               |
| temperature      | 1.0     | Sampling temperature (if do_sample=True)                                  |

## Architecture

KugelAudio uses a hybrid **Autoregressive + Diffusion** architecture based on Microsoft's VibeVoice:

```
Text Input → Qwen2.5-7B Backbone → Diffusion Head → Acoustic Decoder → Audio Output
                                         ↑
                              Pre-encoded Voice Embedding
```

1. **Text Encoder**: Qwen2.5-7B language model encodes input text
2. **Diffusion Head**: Predicts speech latents using denoising diffusion (20 steps)
3. **Acoustic Decoder**: Hierarchical convolutional decoder converts latents to 24kHz audio

## Audio Watermarking

All audio generated by this model is automatically watermarked using Facebook's AudioSeal. The watermark is:

* **Imperceptible**: No audible difference in audio quality
* **Robust**: Survives compression, resampling, and editing
* **Detectable**: Can verify if audio was generated by KugelAudio

### Verify Watermark

```python
from kugelaudio_open.watermark import AudioWatermark

watermark = AudioWatermark()
result = watermark.detect(audio, sample_rate=24000)

print(f"Watermark detected: {result.detected}")
print(f"Confidence: {result.confidence:.1%}")
```

## Intended Use

### ✅ Appropriate Uses

* **Accessibility**: Text-to-speech for visually impaired users
* **Content Creation**: Podcasts, videos, audiobooks, e-learning
* **Voice Assistants**: Chatbots and virtual assistants
* **Language Learning**: Pronunciation practice and language education
* **Creative Projects**: With proper consent and attribution

### ❌ Prohibited Uses

* Creating deepfakes or misleading content
* Impersonating individuals without explicit consent
* Fraud, deception, or scams
* Harassment or abuse
* Any illegal activities

## Limitations

* **VRAM Requirements**: Requires \~19GB VRAM for inference (less with `strip_encoders()`)
* **Speed**: Approximately 1.0x real-time on modern GPUs
* **Language Quality Variation**: Quality may vary across languages based on training data distribution

## Hosted API

For production use without managing infrastructure, use our hosted API at kugelaudio.com:

* ⚡ **Ultra-low latency**: <100ms end-to-end
* 🌍 **Global edge deployment**
* 🔧 **Zero setup required**
* 📈 **Auto-scaling**

```python
from kugelaudio import KugelAudio

client = KugelAudio(api_key="your_api_key")
audio = client.tts.generate(text="Hello from KugelAudio!", model="kugel-1-turbo")
audio.save("output.wav")
```

## Acknowledgments

This model would not have been possible without the contributions of many individuals and organizations:

* **Microsoft VibeVoice Team**: For the excellent foundation architecture that this model builds upon
* **YODAS2 Dataset**: For providing the large-scale multilingual speech data
* **Qwen Team**: For the powerful language model backbone
* **Facebook AudioSeal**: For the audio watermarking technology

### Special Thanks

* **Carlos Menke**: For his invaluable efforts in gathering the first datasets and extensive work benchmarking the model
* **AI Service Center Berlin-Brandenburg (KI-Servicezentrum)**: For providing the GPU resources (8x H100) that made training this model possible

## Citation

```bibtex
@software{kugelaudio2026,
  title = {KugelAudio: Open-Source Text-to-Speech for European Languages},
  author = {Kratzenstein, Kajo and Menke, Carlos},
  year = {2026},
  institution = {Hasso-Plattner-Institut},
  url = {https://huggingface.co/kugelaudio/kugelaudio-0-open}
}
```

## License

This model is released under the MIT License.

## Author

**Kajo Kratzenstein**  
📧 [kajo@kugelaudio.com](mailto:kajo@kugelaudio.com)  
🌐 [kugelaudio.com](https://kugelaudio.com)

**Carlos Menke**

---

**Funding Notice**

Das zugrunde liegende Vorhaben wurde mit Mitteln des Bundesministeriums für Forschung, Technologie und Raumfahrt unter dem Förderkennzeichen »KI-Servicezentrum Berlin-Brandenburg« 16IS22092 gefördert.

_This project was funded by the German Federal Ministry of Research, Technology and Space under the funding code "AI Service Center Berlin-Brandenburg" 16IS22092._