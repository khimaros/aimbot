---
license: cc-by-nc-sa-4.0
language:
- en
- ar
- zh
- nl
- fr
- de
- it
- ja
- ko
- lt
- ru
- es
- pt
- be
- bn
- ka
- hu
- lv
- fa
- pl
- sw
- ta
- uk
pipeline_tag: text-to-speech
library_name: outetts
---
<div class="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg shadow-sm mb-12">
  <div class="text-center mb-4">
    <h2 class="text-xl font-light text-gray-900 dark:text-white tracking-tight mt-0 mb-0">Oute A I</h2>
    <div class="flex justify-center gap-6 mt-4">
      <a href="https://www.outeai.com/" target="_blank" class="flex items-center gap-1 text-gray-700 dark:text-gray-300 text-m font-medium hover:text-gray-900 dark:hover:text-white transition-colors underline">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
          <path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
        </svg>
        outeai.com
      </a>
      <a href="https://discord.gg/vyBM87kAmf" target="_blank" class="flex items-center gap-1 text-gray-700 dark:text-gray-300 text-m font-medium hover:text-gray-900 dark:hover:text-white transition-colors underline">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
        </svg>
        Discord
      </a>
      <a href="https://x.com/OuteAI" target="_blank" class="flex items-center gap-1 text-gray-700 dark:text-gray-300 text-m font-medium hover:text-gray-900 dark:hover:text-white transition-colors underline">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"></path>
        </svg>
        @OuteAI
      </a>
    </div>
  </div>

  <div class="grid grid-cols-3 sm:grid-cols-3 gap-2">
    <a href="https://huggingface.co/OuteAI/Llama-OuteTTS-1.0-1B" target="_blank" class="bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 text-sm font-medium py-2 px-3 rounded-md text-center hover:bg-gray-100 dark:hover:bg-gray-600 hover:border-gray-300 dark:hover:border-gray-500 border border-transparent transition-all">
      Llama OuteTTS 1.0 1B
    </a>
    <a href="https://huggingface.co/OuteAI/Llama-OuteTTS-1.0-1B-GGUF" target="_blank" class="bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 text-sm font-medium py-2 px-3 rounded-md text-center hover:bg-gray-100 dark:hover:bg-gray-600 hover:border-gray-300 dark:hover:border-gray-500 border border-transparent transition-all">
      Llama OuteTTS 1.0 1B GGUF
    </a>
    <a href="https://github.com/edwko/OuteTTS" target="_blank" class="bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 text-sm font-medium py-2 px-3 rounded-md text-center hover:bg-gray-100 dark:hover:bg-gray-600 hover:border-gray-300 dark:hover:border-gray-500 border border-transparent transition-all">
      GitHub Library
    </a>
  </div>
</div>

> [!IMPORTANT]
> **Important Sampling Considerations**  
> 
> When using OuteTTS version 1.0, it is crucial to use the settings specified in the [Sampling Configuration](#sampling-configuration) section.
> The **repetition penalty implementation** is particularly important - this model requires penalization applied to a **64-token recent window**,
> rather than across the entire context window. Penalizing the entire context will cause the model to produce **broken or low-quality output**.
> 
> To address this limitation, all necessary samplers and patches for all backends are set up automatically in the **outetts** library.
> If using a custom implementation, ensure you correctly implement these requirements.

# OuteTTS Version 1.0

This update brings significant improvements in speech synthesis and voice cloning—delivering a more powerful, accurate, and user-friendly experience in a compact size.

## What's New

### 1. Prompt Revamp & Dependency Removal
- **Automatic Word Alignment:** The model now performs word alignment internally. Simply input raw text—no pre-processing required—and the model handles the rest, streamlining your workflow. For optimal results, use normalized, readable text without newlines (light normalization is applied automatically in outetts library).
- **Native Multilingual Text Support:** Direct support for native text across multiple languages eliminates the need for romanization.
- **Enhanced Metadata Integration:** The updated prompt system incorporates additional metadata (time, energy, spectral centroid, pitch) at both global and word levels, improving speaker flow and synthesis quality.
- **Special Tokens for Audio Codebooks:** New tokens for c1 (codebook 1) and c2 (codebook 2).

### 2. New Audio Encoder Model
- **DAC Encoder:** Integrates a DAC audio encoder from [ibm-research/DAC.speech.v1.0](https://huggingface.co/ibm-research/DAC.speech.v1.0), utilizing two codebooks for high quality audio reconstruction.
- **Performance Trade-off:** Improved audio fidelity increases the token generation rate from 75 to 150 tokens per second. This trade-off prioritizes quality, especially for multilingual applications.

### 3. Voice Cloning
- **One-Shot Voice Cloning:** To achieve one-shot cloning, the model typically requires only around **10 seconds** of reference audio to produce an accurate voice representation.
- **Improved Accuracy:** Enhanced by the new encoder and additional training metadata, voice cloning is now more natural and precise.

### 4. Auto Text Alignment & Numerical Support
- **Automatic Text Alignment:** Aligns raw text at the word level, even for languages without clear boundaries (e.g., Japanese, Chinese), using insights from pre-processed training data.
- **Direct Numerical Input:** Built-in multilingual numerical support allows direct use of numbers in prompts—no textual conversion needed. (The model typically chooses the dominant language present. Mixing languages in a single prompt may lead to mistakes.)

### 5. Multilingual Capabilities

- **Supported Languages:** OuteTTS offers varying proficiency levels across languages, based on training data exposure.

- **High Training Data Languages:** These languages feature extensive training: **English, Arabic, Chinese, Dutch, French, German, Italian, Japanese, Korean, Lithuanian, Russian, Spanish**

- **Moderate Training Data Languages:** These languages received moderate training, offering good performance with occasional limitations: **Portuguese, Belarusian, Bengali, Georgian, Hungarian, Latvian, Persian/Farsi, Polish, Swahili, Tamil, Ukrainian**

- **Beyond Supported Languages:** The model can generate speech in untrained languages with varying success. Experiment with unlisted languages, though results may not be optimal.

## Video Showcase

<video width="1280" height="720" controls style="box-shadow: 0px 0px 20px 10px rgba(0, 0, 0, 0.05), 0px 1px 3px 10px rgba(255, 255, 255, 0.05);">
  <source src="https://huggingface.co/OuteAI/Llama-OuteTTS-1.0-1B-GGUF/resolve/main/media/showcase.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>

## Quick Start Guide

Getting started with **OuteTTS** is simple:

### Installation

🔗 [Installation instructions](https://github.com/edwko/OuteTTS?tab=readme-ov-file#installation)

### Basic Usage
```python
import outetts

# Initialize the interface
interface = outetts.Interface(
    config=outetts.ModelConfig.auto_config(
        model=outetts.Models.VERSION_1_0_SIZE_1B,
        # For llama.cpp backend
        backend=outetts.Backend.LLAMACPP,
        quantization=outetts.LlamaCppQuantization.FP16
        # For transformers backend
        # backend=outetts.Backend.HF,
    )
)

# Load the default speaker profile
speaker = interface.load_default_speaker("EN-FEMALE-1-NEUTRAL")

# Or create your own speaker profiles in seconds and reuse them instantly
# speaker = interface.create_speaker("path/to/audio.wav")
# interface.save_speaker(speaker, "speaker.json")
# speaker = interface.load_speaker("speaker.json")

# Generate speech
output = interface.generate(
    config=outetts.GenerationConfig(
        text="Hello, how are you doing?",
        generation_type=outetts.GenerationType.CHUNKED,
        speaker=speaker,
        sampler_config=outetts.SamplerConfig(
            temperature=0.4
        ),
    )
)

# Save to file
output.save("output.wav")
```

### More Configuration Options
For advanced settings and customization, visit the official repository:  
🔗 [interface_usage.md](https://github.com/edwko/OuteTTS/blob/main/docs/interface_usage.md)

## Usage Recommendations

### Speaker Reference
The model is designed to be used with a speaker reference. Without one, it generates random vocal characteristics, often leading to lower-quality outputs. 
The model inherits the referenced speaker's emotion, style, and accent. 
When transcribing to other languages with the same speaker, you may observe the model retaining the original accent. 

### Multilingual Application
It is recommended to create a speaker profile in the language you intend to use. This helps achieve the best results in that specific language, including tone, accent, and linguistic features.

While the model supports cross-lingual speech, it still relies on the reference speaker. If the speaker has a distinct accent—such as British English—other languages may carry that accent as well.

### Optimal Audio Length
- **Best Performance:** Generate audio around **42 seconds** in a single run (approximately 8,192 tokens). It is recomended not to near the limits of this windows when generating. Usually, the best results are up to 7,000 tokens.
- **Context Reduction with Speaker Reference:** If the speaker reference is 10 seconds long, the effective context is reduced to approximately 32 seconds.

### Temperature Setting Recommendations
Testing shows that a temperature of **0.4** is an ideal starting point for accuracy (with the sampling settings below). However, some voice references may benefit from higher temperatures for enhanced expressiveness or slightly lower temperatures for more precise voice replication.

### Verifying Speaker Encoding
If the cloned voice quality is subpar, check the encoded speaker sample. 

```python
interface.decode_and_save_speaker(speaker=your_speaker, path="speaker.wav")
```

The DAC audio reconstruction model is lossy, and samples with clipping, excessive loudness, or unusual vocal features may introduce encoding issues that impact output quality.

### Sampling Configuration
For optimal results with this TTS model, use the following sampling settings.

| Parameter         | Value    |
|-------------------|----------|
| Temperature       | 0.4      |
| Repetition Penalty| 1.1      |
| **Repetition Range**  | **64**       |
| Top-k             | 40       |
| Top-p             | 0.9      |
| Min-p             | 0.05     |

## Model Specifications

- **Training Data:** Trained on **~60k hours of audio** 
- **Context Length:** Supports a maximum context window of **8,192 tokens**

### Training Parameters  

#### **Pre-Training**  
- **Optimizer:** AdamW  
- **Batch Size:** 1 million tokens  
- **Max Learning Rate:** 3e-4
- **Min Learning Rate:** 3e-5
- **Context Length:** 8192

#### **Fine-Tuning**  
- **Optimizer:** AdamW    
- **Max Learning Rate:** 1e-5
- **Min Learning Rate:** 5e-6
- **Data:** 10,000 diverse, high-quality examples 

## License Information

- **Initial Llama3.2 Components:** [Llama 3.2 Community License Agreement ](https://huggingface.co/meta-llama/Llama-3.2-1B/blob/main/LICENSE.txt)
- **Our Continued Pre-Training, Fine-Tuning, and Additional Components:** [CC-BY-NC-SA-4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Acknowledgments

- Big thanks to **Hugging Face** for their continued resource support through their grant program!
- Audio encoding and decoding utilize [ibm-research/DAC.speech.v1.0](https://huggingface.co/ibm-research/DAC.speech.v1.0)
- OuteTTS is built with [Llama3.2-1B](https://huggingface.co/meta-llama/Llama-3.2-1B) as the base model, with continued pre-training and fine-tuning.

### Ethical Use Guidelines
This text-to-speech model is intended for legitimate applications that enhance accessibility, creativity, and communication; 
prohibited uses include impersonation without consent, creation of deliberately misleading content, 
generation of harmful or harassing material, distribution of synthetic audio without proper disclosure, 
voice cloning without permission, and any uses that violate applicable laws, regulations, or copyrights.