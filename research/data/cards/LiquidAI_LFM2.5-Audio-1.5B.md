---
language:
- en
tags:
- liquid
- lfm2
- audio
- lfm2-audio
- speech-to-speech
- liquid-audio
license: other
license_name: lfm1.0
license_link: LICENSE
library_name: liquid-audio
pipeline_tag: audio-to-audio
base_model:
- LiquidAI/LFM2-1.2B
---

<center>
<div style="text-align: center;">
  <img 
    src="https://cdn-uploads.huggingface.co/production/uploads/61b8e2ba285851687028d395/2b08LKpev0DNEk6DlnWkY.png" 
    alt="Liquid AI"
    style="width: 100%; max-width: 100%; height: auto; display: inline-block; margin-bottom: 0.5em; margin-top: 0.5em;"
  />
</div>
<div style="display: flex; justify-content: center; gap: 0.5em;">
<a href="https://playground.liquid.ai/"><strong>Try LFM</strong></a> • <a href="https://docs.liquid.ai/lfm/getting-started/welcome"><strong>Docs</strong></a> • <a href="https://leap.liquid.ai/"><strong>LEAP</strong></a> • <a href="https://discord.com/invite/liquid-ai"><strong>Discord</strong></a>
</div>
</center>

<br>

# LFM2.5‑Audio-1.5B

LFM2.5-Audio-1.5B is [Liquid AI](https://www.liquid.ai/)'s updated end-to-end audio foundation model.
Key improvements include a custom, LFM based audio detokenizer, `llama.cpp` compatible GGUFs for CPU inference, and better ASR and TTS performance.

LFM2.5-Audio is an end-to-end multimodal speech and text language model, and as such does not require separate ASR and TTS components.
Designed with low latency and real time conversation in mind, at only 1.5 billion parameters LFM2.5-Audio enables seamless conversational interaction, achieving capabilities on par with much larger models.
Our model consists of a pretrained LFM2.5 model as its multimodal backbone, along with a FastConformer based audio encoder to handle continuous audio inputs, and an RQ-transformer generating discrete tokens coupled with a lightweight audio detokenizer for audio output.

LFM2.5-Audio supports two distinct generation routines, each suitable for a set of tasks.
Interleaved generation enables real-time speech-to-speech conversational chatbot capabilities, where audio generation latency is key.
Sequential generation is suited for non-conversational tasks such as ASR or TTS, and allows the model to switch generated modality on the fly. 

## 📄 Model details

| Property | |
|---|---:|
| **Parameters (LM only)** | 1.2B |
| **Audio encoder** | FastConformer (115M, [canary-180m-flash](https://huggingface.co/nvidia/canary-180m-flash)) |
| **Backbone layers** | hybrid conv+attention |
| **Audio detokenizer** | [Mimi](https://huggingface.co/kyutai/mimi)-compatible, using 8 codebooks |
| **Context** | 32,768 tokens |
| **Vocab size** | 65,536 (text) / 2049*8 (audio) |
| **Precision** | bfloat16 |
| **License** | LFM Open License v1.0 |

**Supported languages:** English

## 🏃 How to run LFM2.5-Audio
Install the `liquid-audio` package via `pip`
```bash
pip install liquid-audio
pip install "liquid-audio [demo]" # optional, to install demo dependencies
pip install flash-attn --no-build-isolation  # optional, to use flash attention 2. Will fallback to torch SDPA if not installed
```

## Gradio demo
The simplest way to get started is by running the Gradio demo interface. After installation, run the command
```
liquid-audio-demo
```
This will start a webserver on port 7860. The interface can then be accessed via the URL http://localhost:7860/.

## Multi-turn, multi-modal chat
The `liquid-audio` library provides a lower lever interface to the model and generation routines, ideal for custom usecases.
We demonstrate this with a simple multi-turn chat, where the first turn is given as audio, and the second turn is given as text.

For multi-turn chat with text and audio output, we use interleaved generation. The system prompt should be set to `Respond with interleaved text and audio.`. Here we use audio as the first user turn, and text as the second one.
```python
import torch
import torchaudio
from liquid_audio import LFM2AudioModel, LFM2AudioProcessor, ChatState, LFMModality

# Load models
HF_REPO = "LiquidAI/LFM2.5-Audio-1.5B"

processor = LFM2AudioProcessor.from_pretrained(HF_REPO).eval()
model = LFM2AudioModel.from_pretrained(HF_REPO).eval()

# Set up inputs for the model
chat = ChatState(processor)

chat.new_turn("system")
chat.add_text("Respond with interleaved text and audio.")
chat.end_turn()

chat.new_turn("user")
wav, sampling_rate = torchaudio.load("assets/question.wav")
chat.add_audio(wav, sampling_rate)
chat.end_turn()

chat.new_turn("assistant")

# Generate text and audio tokens.
text_out: list[torch.Tensor] = []
audio_out: list[torch.Tensor] = []
modality_out: list[LFMModality] = []
for t in model.generate_interleaved(**chat, max_new_tokens=512, audio_temperature=1.0, audio_top_k=4):
    if t.numel() == 1:
        print(processor.text.decode(t), end="", flush=True)
        text_out.append(t)
        modality_out.append(LFMModality.TEXT)
    else:
        audio_out.append(t)
        modality_out.append(LFMModality.AUDIO_OUT)

# output: Sure! How about "Handcrafted Woodworking, Precision Made for You"? Another option could be "Quality Woodworking, Quality Results." If you want something more personal, you might try "Your Woodworking Needs, Our Expertise."

# Detokenize audio, removing the last "end-of-audio" codes
# Mimi returns audio at 24kHz
audio_codes = torch.stack(audio_out[:-1], 1).unsqueeze(0)
waveform = processor.decode(audio_codes)
torchaudio.save("answer1.wav", waveform.cpu(), 24_000)

# Append newly generated tokens to chat history
chat.append(
    text = torch.stack(text_out, 1),
    audio_out = torch.stack(audio_out, 1),
    modality_flag = torch.tensor(modality_out),
)
chat.end_turn()

# Start new turn
chat.new_turn("user")
chat.add_text("My business specialized in chairs, can you give me something related to that?")
chat.end_turn()

chat.new_turn("assistant")

# Generate second turn text and audio tokens.
audio_out: list[torch.Tensor] = []
for t in model.generate_interleaved(**chat, max_new_tokens=512, audio_temperature=1.0, audio_top_k=4):
    if t.numel() == 1:
        print(processor.text.decode(t), end="", flush=True)
    else:
        audio_out.append(t)

# output: Sure thing! How about “Comfortable Chairs, Crafted with Care” or “Elegant Seats, Handcrafted for You”? Let me know if you’d like a few more options.

# Detokenize second turn audio, removing the last "end-of-audio" codes
audio_codes = torch.stack(audio_out[:-1], 1).unsqueeze(0)
waveform = processor.decode(audio_codes)
torchaudio.save("answer2.wav", waveform.cpu(), 24_000)
```

### ASR, TTS, additional information
Please visit the `liquid-audio` [package repository](https://github.com/Liquid4All/liquid-audio) for additional examples and sample audio snippets.

## 📈 Performance

### VoiceBench (audio input)

Higher is better. AlpacaEval, CommonEval and WildVoice are scored out of 5.

| Model           | Components & Size | AlpacaEval | CommonEval | WildVoice | SD-QA | MMSU  | OBQA  | BBH   | IFEval | ADVBench | Overall |
| --------------- | ----------------- | ---------- | ---------- | --------- | ----- | ----- | ----- | ----- | ------ | -------- | ------- |
| LFM2.5-Audio-1.5B | 1.5B parameters | 3.76       | 3.53       | 3.15      | 30.92 | 33.04 | 44.40 | 49.54 | 28.48  | 99.04    | 54.92   |
| LFM2-Audio-1.5B | 1.5B parameters   | 3.71       | 3.49       | 3.17      | 30.56 | 31.95 | 44.40 | 30.54 | 31.23  | 97.31    | 52.77   |
| Moshi           | 7B parameters     | 2.01       | 1.60       | 1.30      | 15.64 | 24.04 | 25.93 | 47.40 | 10.12  | 44.23    | 29.51   |
| Qwen2.5-Omni-3B | 5B parameters     | 3.72       | 3.51       | 3.42      | 44.94 | 55.29 | 76.26 | 61.30 | 32.90  | 88.46    | 63.57   |
| Mini-Omni2      | 0.6B parameters   | 2.32       | 2.18       | 1.79      | 9.31  | 24.27 | 26.59 | 46.40 | 11.56  | 57.50    | 33.49   |

### ASR

Word Error Rate (WER), lower is better.

| Model                | Components & Size | Audio output  | Open | WER average |  AMI   | Earnings22 | GigaSpeech | LibriSpeech-clean | LibriSpeech-other | SPGISpeech | TED-LIUM | VoxPopuli |
| -------------------- | ----------------- | ------------- | ---- | ----------- | ------ | ---------- | ---------- | ----------------- | ----------------- | ---------- | -------- | --------- |
| LFM2.5-Audio-1.5B    | 1.5B parameters   | Yes           | Yes  | 7.53        | 15.63  | 14.56      | 10.47      | 1.95              | 4.30              | 2.76       | 3.47     | 7.13      |
| LFM2-Audio-1.5B      | 1.5B parameters   | Yes           | Yes  | 9.38        | 15.36  | 19.75      | 10.63      | 2.03              | 4.39              | 4.17       | 3.56     | 9.93      |
| Qwen2.5-Omni-3B      | 5B parameters     | Yes           | Yes  | 7.90        | 15.05  | 14.81      | 11.76      | 2.14              | 4.52              | 3.24       | 5.08     | 5.60      |
| Whisper-large-V3     | 1.5B parameters   | No — ASR only | Yes  | 7.44        | 15.95  | 11.29      | 10.02      | 2.01              | 3.91              | 2.94       | 3.86     | 9.54      |


## 📬 Contact

- Got questions or want to connect? [Join our Discord community](https://discord.com/invite/liquid-ai)
- If you are interested in custom solutions with edge deployment, please contact [our sales team](https://www.liquid.ai/contact).

## License
The code in this the package repository and associated weights are licensed under the [LFM Open License v1.0](LICENSE).

The code for the audio encoder is based on [Nvidia NeMo](https://github.com/NVIDIA-NeMo/NeMo/tree/main), licensed under [Apache 2.0](https://github.com/NVIDIA-NeMo/NeMo/blob/294ddff187f68c055d87ffe9400e65975b38693d/LICENSE), and the [canary-180m-flash](https://huggingface.co/nvidia/canary-180m-flash) checkpoint, licensed under [CC-BY 4.0](https://huggingface.co/datasets/choosealicense/licenses/blob/main/markdown/cc-by-4.0.md). To simplify dependency resolution, we also ship the Python code of [Kyutai Mimi](https://github.com/kyutai-labs/moshi), licensed under the [MIT License](https://github.com/kyutai-labs/moshi/blob/aee53fc0fc0119e4d7343e5ea4dd6ddafd7f09c4/LICENSE-MIT).
We also redistribute weights for [Kyutai Mimi](https://huggingface.co/kyutai/moshiko-pytorch-bf16), licensed under [CC-BY-4.0](https://huggingface.co/datasets/choosealicense/licenses/blob/main/markdown/cc-by-4.0.md).

## Citation

```
@article{liquidai2025lfm2,
 title={LFM2 Technical Report},
 author={Liquid AI},
 journal={arXiv preprint arXiv:2511.23404},
 year={2025}
}
```