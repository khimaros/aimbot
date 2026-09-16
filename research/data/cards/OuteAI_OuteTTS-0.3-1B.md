---
license: cc-by-nc-sa-4.0
pipeline_tag: text-to-speech
library_name: outetts
---
<style>
table {
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 20px;
}
th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: center;
}
.best {
    font-weight: bold;
    text-decoration: underline;
}
.box {
  text-align: center;
  margin: 20px auto;
  padding: 30px;
  box-shadow: 0px 0px 20px 10px rgba(0, 0, 0, 0.05), 0px 1px 3px 10px rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}
.badges {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 10px;
}
.badge {
    text-decoration: none;
    display: inline-block;
    padding: 4px 8px;
    border-radius: 5px;
    color: #fff;
    font-size: 12px;
    font-weight: bold;
    width: 200px;
}
.badge-dark {
    background-color: #000000;
}
.badge-model {
    background-color: #6885ab;
}
.badge-space {
    background-color: #7468ab;
}
</style>

<div class="box">
  <div style="margin-bottom: 20px;">
    <h2 style="margin-bottom: 4px; margin-top: 0px;">Oute <em>A I</em></h2>
    <a href="https://www.outeai.com/" target="_blank" style="margin-right: 10px; font-weight: bold;">🌐 OuteAI.com</a> 
    <a href="https://discord.gg/vyBM87kAmf" target="_blank" style="margin-right: 10px; font-weight: bold;">💬 Join our Discord</a>
    <a href="https://x.com/OuteAI" target="_blank" style="font-weight: bold;">𝕏 @OuteAI</a>
  </div>
  <div class="badges">
    <a href="https://huggingface.co/OuteAI/OuteTTS-0.3-1B" target="_blank" class="badge badge-model">OuteTTS 0.3 1B</a>
    <a href="https://huggingface.co/OuteAI/OuteTTS-0.3-1B-GGUF" target="_blank" class="badge badge-model">OuteTTS 0.3 1B GGUF</a>
    <a href="https://huggingface.co/OuteAI/OuteTTS-0.3-500M" target="_blank" class="badge badge-model">OuteTTS 0.3 500M</a>
    <a href="https://huggingface.co/OuteAI/OuteTTS-0.3-500M-GGUF" target="_blank" class="badge badge-model">OuteTTS 0.3 500M GGUF</a>
    <a href="https://huggingface.co/spaces/OuteAI/OuteTTS-0.3-1B-Demo" target="_blank" class="badge badge-space">OuteTTS 0.3 Demo Space</a>
    <a href="https://github.com/edwko/OuteTTS" target="_blank" class="badge badge-dark">GitHub - OuteTTS</a>
  </div>
</div>

# OuteTTS Version 0.3

OuteTTS version 0.3 introduces multiple model variants tailored for diverse use cases. 
This release significantly enhances the naturalness and coherence of speech synthesis by adding punctuation support, improving the flow and clarity of generated speech.
The following punctuation marks are supported: `'.', '!', '?', ',', '"', '„', '¡', '¿', '…', '...', '。', '！', '？', '，', '؟'`. These are converted into special tokens, for instance, `.` is transformed into `<|period|>`.
Additionally, the models were trained on refined and extended datasets, offering broader linguistic coverage. With this version, two new languages, **German (de)** and **French (fr)**, are supported, bringing the total to six languages: **English (en)**, **Japanese (jp)**, **Korean (ko)**, **Chinese (zh)**, **French (fr)**, and **German (de)**.

OuteTTS is a solution designed to extend any existing large language model (LLM) with text-to-speech (TTS) and speech-to-speech capabilities. By preserving the original architecture, it ensures high compatibility with a broad range of libraries and tools, making it easy to integrate speech functionalities without compromising on flexibility.

Experimental voice control features are also included, though they are in very early stage of development. Due to limited data, these features may produce inconsistent results and might sometimes be ignored by the model.

Special thanks to **Hugging Face** 🤗 for providing the GPU grant that made training this model possible!

## Available Variants

### OuteTTS-0.3-500M
- **Base**: Qwen2.5-0.5B (Apache-2.0)
- **TTS Model License**: CC-BY-SA-4.0
- **Training**: 10,000 hours of speech audio (~4 billion tokens)
- **Supported Languages**: en, jp, ko (small dataset), zh, fr, de

### OuteTTS-0.3-1B
- **Base**: OLMo-1B (Apache-2.0)
- **TTS Model License**: CC-BY-NC-SA-4.0 _(Incorporates the Emilia dataset, for improved quality)_
- **Training**: 20,000 hours of speech audio (~8 billion tokens)
- **Supported Languages**: en, jp, ko, zh, fr, de

## Showcase Video
<video width="1280" height="720" controls style="box-shadow: 0px 0px 20px 10px rgba(0, 0, 0, 0.05), 0px 1px 3px 10px rgba(255, 255, 255, 0.05);">
  <source src="https://huggingface.co/OuteAI/OuteTTS-0.3-1B-GGUF/resolve/main/generation_preview.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>

---

## Installation

Install the OuteTTS package via pip:

```bash
pip install outetts --upgrade
```

## Usage

### Quick Start: Full Basic Example

```python
import outetts

# Configure the model
model_config = outetts.HFModelConfig_v2(
    model_path="OuteAI/OuteTTS-0.3-1B",
    tokenizer_path="OuteAI/OuteTTS-0.3-1B"
)
# Initialize the interface
interface = outetts.InterfaceHF(model_version="0.3", cfg=model_config)

# You can create a speaker profile for voice cloning, which is compatible across all backends.
# speaker = interface.create_speaker(audio_path="path/to/audio/file.wav")
# interface.save_speaker(speaker, "speaker.json")
# speaker = interface.load_speaker("speaker.json")

# Print available default speakers
interface.print_default_speakers()
# Load a default speaker
speaker = interface.load_default_speaker(name="en_male_1")

# Generate speech
gen_cfg = outetts.GenerationConfig(
    text="Speech synthesis is the artificial production of human speech.",
    temperature=0.4,
    repetition_penalty=1.1,
    max_length=4096,
    speaker=speaker,
)
output = interface.generate(config=gen_cfg)

# Save the generated speech to a file
output.save("output.wav")
```
### Additional Usage Examples

> [!IMPORTANT]
> For additional usage examples and recommendations, visit the: [GitHub repository](https://github.com/edwko/OuteTTS?tab=readme-ov-file#usage).

### Generation Performance

> [!IMPORTANT]
> The model performs best with 30-second generation batches. This window is reduced based on the length of your speaker samples. For example, if the speaker reference sample is 10 seconds, the effective window becomes approximately 20 seconds. I am currently working on adding batched generation capabilities to the library, along with further improvements that are not yet implemented.

---

## Dataset Attribution

The OuteTTS-0.3-1B training data incorporates various publicly available speech datasets. Below is a summary of the key data sources:

- **Emilia Dataset**: CC-BY-NC 4.0
- **Mozilla Common Voice**: CC-0
- **MLCommons People's Speech Dataset (selected portions)**: CC-BY 4.0
- **Noisy Speech Database (Edinburgh DataShare)**: CC BY 4.0
- **Multilingual LibriSpeech (MLS)**: CC BY 4.0
- **CSTR VCTK Corpus (Edinburgh DataShare)**: CC BY 4.0
- **THCHS-30 (Open Speech and Language Resources)**: Apache-2.0
- **Zeroth-Korean (Open Speech and Language Resources)**: CC BY 4.0
- **Aishell (Open Speech and Language Resources)**: Apache-2.0
- **Other permissively licensed datasets**

## Credits & References

Special acknowledgment to the open-source community and researchers for their valuable contributions.

- [WavTokenizer GitHub](https://github.com/jishengpeng/WavTokenizer) | [WavTokenizer HF](https://huggingface.co/novateur/WavTokenizer-large-speech-75token)
- [CTC Forced Alignment](https://pytorch.org/audio/stable/tutorials/ctc_forced_alignment_api_tutorial.html)
- [Qwen-2.5-0.5B](https://huggingface.co/Qwen/Qwen2.5-0.5B)
- [OLMo-1B](https://huggingface.co/allenai/OLMo-1B-hf)