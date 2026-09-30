---
license: apache-2.0
language:
- ja
library_name: nemo
pipeline_tag: automatic-speech-recognition
---
# ASR Model Card: parakeet-ctc-1.1b-ja

## Model Details

- **Model Name**: parakeet-ctc-1.1b-ja
- **Type**: Automatic Speech Recognition (ASR)
- **Language**: Japanese
- **Framework**: NVIDIA NeMo

## Installation

To use this model, you need to install the NeMo toolkit:

```bash
pip install nemo-toolkit==2.0.0rc0 nemo-toolkit[asr]==2.0.0rc0
```

## Usage

Here's a basic example of how to use the model:

```python
import nemo.collections.asr as nemo_asr

# Load the model
nemo_model = nemo_asr.models.ASRModel.restore_from("/path/to/parakeet-ja.nemo")

# Transcribe audio files
audio_files = ["path/to/audio1.wav", "path/to/audio2.wav"]
transcriptions = nemo_model.transcribe(audio_files)

# Print transcriptions
for audio_file, transcription in zip(audio_files, transcriptions):
    print(f"Transcription for {audio_file}: {transcription}")
```

## Limitations

- This model is specifically trained for Japanese language and may not perform well on other languages.
- The accuracy of transcription may vary depending on the audio quality, background noise, and speaker accent.
- The model may struggle with specialized vocabulary or technical terms not encountered during training.

## Performance

The following table compares the performance of the NeMo model (Parakeet-JA) with Whisper v2 large and Whisper v3 large across different Japanese ASR datasets:

| Model          | Dataset                            | WER    | CER    |
|----------------|-----------------------------------|--------|--------|
| Whisper v2 large | japanese-asr/ja_asr.reazonspeech_test | 1.1378 | 0.3472 |
|                | japanese-asr/ja_asr.jsut_basic5000    | 0.8988 | 0.1063 |
|                | japanese-asr/ja_asr.common_voice_8_0  | 1.0314 | 0.1594 |
| Whisper v3 large | japanese-asr/ja_asr.reazonspeech_test | 0.9685 | 0.2107 |
|                | japanese-asr/ja_asr.jsut_basic5000    | 0.9936 | 0.1360 |
|                | japanese-asr/ja_asr.common_voice_8_0  | 1.0178 | 0.1548 |
| NeMo (parakeet-ctc-1.1b-ja) | japanese-asr/ja_asr.reazonspeech_test | 0.7785 | 0.1521 |
|                | japanese-asr/ja_asr.jsut_basic5000    | 0.9462 | 0.1291 |
|                | japanese-asr/ja_asr.common_voice_8_0  | 1.0002 | 0.1290 |

## Ethical Considerations

- Ensure that you have the necessary permissions and comply with local laws when recording and transcribing audio.
- Be aware of potential biases in the model, especially regarding different Japanese dialects or accents.
- Consider the privacy implications of transcribing personal or sensitive conversations.

## Additional Information

For more detailed information on using ASR models with the NeMo toolkit, please refer to the [NeMo ASR documentation](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/asr/intro.html).