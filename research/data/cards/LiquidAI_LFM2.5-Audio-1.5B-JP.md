---
language:
- ja
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
- LiquidAI/LFM2.5-Audio-1.5B
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
  <a href="https://playground.liquid.ai/chat">
<a href="https://playground.liquid.ai/"><strong>Try LFM</strong></a> • <a href="https://docs.liquid.ai/lfm"><strong>Documentation</strong></a> • <a href="https://leap.liquid.ai/"><strong>LEAP</strong></a></a>
</div>
</center>

<br>

# 🇯🇵 LFM2.5-Audio-1.5B-JP

<div align="center">
  <video controls style="width:100%; max-width:100%;">
    <source
      src="https://huggingface.co/LiquidAI/LFM2.5-Audio-1.5B-JP/resolve/main/demo.mp4"
      type="video/mp4">
  </video>

  <img
    src="https://cdn-uploads.huggingface.co/production/uploads/64618cf05dba83471db2be9b/sACh7Oein9RdmldNqR-2E.png"
    alt="Liquid AI"
    width="70%"
  />
</div>

LFM2.5-Audio-1.5B-JP is [Liquid AI](https://www.liquid.ai/)'s first Japanese capable audio model and the first Japanese speech-to-speech model at this lightweight scale built from the foundations of [LFM2.5-Audio-1.5B.](https://huggingface.co/LiquidAI/LFM2.5-Audio-1.5B)

LFM2.5-Audio-1.5B-JP is an end-to-end multimodal speech and text language model, and as such does not require separate ASR and TTS components.
Designed with low latency and real time conversation in mind, at only 1.5 billion parameters LFM2.5-Audio-JP enables seamless Japanese conversational interaction, achieving capabilities on par with much larger models. 
Our model consists of a pretrained LFM2.5 model as its multimodal backbone, along with a FastConformer based audio encoder to handle continuous audio inputs, and an RQ-transformer generating discrete tokens coupled with a lightweight audio detokenizer for audio output.

LFM2.5-Audio-JP supports two distinct generation routines, each suitable for a set of tasks.
Interleaved generation enables real-time speech-to-speech conversational chatbot capabilities, where audio generation latency is key.
Sequential generation is suited for non-conversational tasks such as ASR or TTS, and allows the model to switch generated modality on the fly.


LFM2.5-Audio-1.5B-JPは、[Liquid AI](https://www.liquid.ai/)初となる日本語対応の音声モデルであり、[LFM2.5-Audio-1.5B](https://huggingface.co/LiquidAI/LFM2.5-Audio-1.5B)の基盤から構築された、この軽量な規模においては初となる日本語のSpeech-to-Speechモデルです。

LFM2.5-Audio-1.5B-JPは、エンドツーエンドのマルチモーダルな音声・テキスト言語モデルであり、そのため独立したASR（自動音声認識）やTTS（音声合成）のコンポーネントを必要としません。低遅延とリアルタイムな会話を念頭に設計されたLFM2.5-Audio-JPは、わずか15億（1.5B）パラメータでありながら、シームレスな日本語の対話インタラクションを可能にし、より大規模なモデルに匹敵する能力を実現しています。
当社のモデルは、マルチモーダルのバックボーン（基盤）として事前学習済みのLFM2.5モデルで構成されており、それに加えて、連続的な音声入力を処理するFastConformerベースの音声エンコーダー、離散トークンを生成するRQ-transformer、そして音声出力用の軽量な音声デトークナイザーが組み合わされています。

LFM2.5-Audio-JPは、それぞれ異なるタスクに適した2つの生成ルーティン（方式）をサポートしています。「インターリーブド（交互）生成」は、音声生成の遅延（レイテンシー）が重要となる、リアルタイムの音声対話チャットボット機能を可能にします。「シーケンシャル（逐次）生成」は、ASRやTTSなどの非対話的なタスクに適しており、モデルが生成するモダリティ（音声かテキストか）をその場で動的に切り替えることができます。

## 📈 Performance

### VoiceBench<sup>1</sup> (Audio Input)

<div align="center">
  <img 
    src="https://cdn-uploads.huggingface.co/production/uploads/64618cf05dba83471db2be9b/FXitmLQHhxAzGzQB_8UPe.png" 
    alt="Liquid AI" 
    style="width: 100%; max-width: 100%; height: auto; display: inline-block; margin-bottom: 0.5em; margin-top: 0.5em;"
  />
  <div style="display: flex; justify-content: center; gap: 0.5em;">
  </div>
</div>

We use GPT-4o as an LLM-as-a-judge and report the highest score assigned to each sample. Elyza and spoken_Elyza are scored on a 0–5 scale, while M-ifeval is scored on a 0–1 scale. Average performance was computed after rescaling all benchmark scores to a 0–5 scale.


| Model                | Size |     Elyza | spoken_Elyza |  M-ifeval |
| -------------------- | ---: | --------: | -----------: | --------: |
| LFM2.5-Audio-1.5B-JP | 1.5B |     2.272 |    **2.118** |     0.143 |
| Qwen2.5-Omni-3B      | 5.5B | **2.365** |        2.094 |     0.137 |
| LLM-jp-Moshi-v1      | 7.7B |     1.000 |        1.023 |     0.110 |
| J-Moshi              | 7.7B |     1.034 |        1.012 | **0.151** |


*<sup>1</sup> Dataset is derived from [sbintuitions/voicebench-ja](https://huggingface.co/datasets/sbintuitions/voicebench-ja).*

### ASR<sup>2</sup>

We evaluated character error rate (CER) on three ASR datasets.

| Model | CommonVoice 8 (Japanese test set.) | JSUT Basic 5000 | ReazonSpeech (held-out test set) |
|---|---:|---:|---:|
| LFM2.5-Audio-1.5B-JP | **4.42** | 8.07 | 24.24 |
| reazon-research/reazonspeech-nemo-v2 | 9.1 | 7.4 | **11.2** |
| japanese-asr/distil-whisper-large-v3-ja-reazonspeech-all | 9.2 | 8.4 | 11.6 |
| japanese-asr/distil-whisper-large-v3-ja-reazonspeech-large | 9.4 | 8.5 | 12.2 |
| japanese-asr/distil-whisper-large-v3-ja-reazonspeech-medium | 10.9 | 11.3 | 14.8 |
| japanese-asr/distil-whisper-large-v3-ja-reazonspeech-small | 30.2 | 39 | 40.7 |
| japanese-asr/distil-whisper-large-v3-ja-reazonspeech-tiny | 94.8 | 96.3 | 96.7 |
| openai/whisper-large-v3 | 8.5 | **7.1** | 14.9 |
| openai/whisper-large-v2 | 9.7 | 8.2 | 28.1 |
| openai/whisper-large | 10 | 8.9 | 34.1 |
| openai/whisper-medium | 11.5 | 10 | 33.2 |
| openai/whisper-base | 28.6 | 24.9 | 70.4 |
| openai/whisper-small | 15.1 | 14.2 | 41.5 |
| openai/whisper-tiny | 53.7 | 36.5 | 137.9 |

*<sup>2</sup> Results are derived from [japanese-asr](https://huggingface.co/japanese-asr).*

## 📄 Model details

| Property | |
|---|---:|
| **Parameters (LM only)** | 1.2B |
| **Audio encoder** | FastConformer (115M, [canary-180m-flash](https://huggingface.co/nvidia/canary-180m-flash)) |
| **Backbone layers** | hybrid conv+attention |
| **Audio tokenizer** | [Mimi](https://huggingface.co/kyutai/mimi), using 8 codebooks |
| **Context** | 32,768 tokens |
| **Vocab size** | 65,536 (text) / 2049*8 (audio) |
| **Precision** | bfloat16 |
| **License** | LFM Open License v1.0 |

**Supported languages:** Japanese

## 🏃 How to run LFM2.5-Audio-JP

Install the `liquid-audio` package via `pip`
```bash
pip install liquid-audio
pip install "liquid-audio [demo]" # optional, to install demo dependencies
pip install flash-attn --no-build-isolation  # optional, to use flash attention 2. Will fallback to torch SDPA if not installed
```

## Multi-turn, multi-modal chat

The `liquid-audio` library provides a lower lever interface to the model and generation routines, ideal for custom usecases.
We demonstrate this with a simple multi-turn chat, where the first turn is given as audio, and the second turn is given as text.

For multi-turn chat with text and audio output, we use interleaved generation. The system prompt should be set to `Respond with interleaved text and audio.`. Here we use audio as the first user turn, and text as the second one.
```python
import torch
import soundfile as sf
from liquid_audio import LFM2AudioModel, LFM2AudioProcessor, ChatState, LFMModality

# Load models
HF_REPO = "LiquidAI/LFM2.5-Audio-1.5B-JP"

processor = LFM2AudioProcessor.from_pretrained(HF_REPO).eval()
model = LFM2AudioModel.from_pretrained(HF_REPO).eval()

# Set up inputs for the model
chat = ChatState(processor)

chat.new_turn("system")
chat.add_text("Respond with interleaved text and audio.")
chat.end_turn()

chat.new_turn("user")
wav, sampling_rate = sf.read("assets/question_jp.wav", dtype="float32")
wav = torch.from_numpy(wav).unsqueeze(0)
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

# output: こんにちは。私はリキッドリリーと申します。質問に答えたり、アドバイスを提供したりするためのAIボイスアシスタントです。リアルタイムでさまざまな言語タスクをお手伝いするよう設計されています。

# Detokenize audio, removing the last "end-of-audio" codes
# Mimi returns audio at 24kHz
audio_codes = torch.stack(audio_out[:-1], 1).unsqueeze(0)
waveform = processor.decode(audio_codes)
sf.write("answer_jp1.wav", waveform.cpu()[0], 24_000)

# Append newly generated tokens to chat history
chat.append(
    text = torch.stack(text_out, 1),
    audio_out = torch.stack(audio_out, 1),
    modality_flag = torch.tensor(modality_out),
)
chat.end_turn()

# Start new turn
chat.new_turn("user")
chat.add_text("富士山の高さは何メートルですか。")
chat.end_turn()

chat.new_turn("assistant")

# Generate second turn text and audio tokens.
audio_out: list[torch.Tensor] = []
for t in model.generate_interleaved(**chat, max_new_tokens=512, audio_temperature=1.0, audio_top_k=4):
    if t.numel() == 1:
        print(processor.text.decode(t), end="", flush=True)
    else:
        audio_out.append(t)

# output: 富士山の高さは約3,776メートルです。

# Detokenize second turn audio, removing the last "end-of-audio" codes
audio_codes = torch.stack(audio_out[:-1], 1).unsqueeze(0)
waveform = processor.decode(audio_codes)
sf.write("answer_jp2.wav", waveform.cpu()[0], 24_000)
```

### ASR

For ASR, we use sequential generation, with the fixed system prompt `Perform ASR in japanese.`.

```python
import torch
import soundfile as sf
from liquid_audio import LFM2AudioModel, LFM2AudioProcessor, ChatState, LFMModality

# Load models
HF_REPO = "LiquidAI/LFM2.5-Audio-1.5B-JP"

processor = LFM2AudioProcessor.from_pretrained(HF_REPO).eval()
model = LFM2AudioModel.from_pretrained(HF_REPO).eval()

# Set up inputs for the model
chat = ChatState(processor)

chat.new_turn("system")
chat.add_text("Perform ASR in japanese.")
chat.end_turn()

chat.new_turn("user")
wav, sampling_rate = sf.read("assets/asr_jp.wav", dtype="float32")
wav = torch.from_numpy(wav).unsqueeze(0)
chat.add_audio(wav, sampling_rate)
chat.end_turn()

chat.new_turn("assistant")

# Generate text
for t in model.generate_sequential(**chat, max_new_tokens=512):
    if t.numel() == 1:
        print(processor.text.decode(t), end="", flush=True)

# Output: この度は弊社の確認不足により多大なご迷惑をおかけしましたことを深くお詫び申し上げます。今後はこのようなことが二度と起こらないよう社内のチェック体制を徹底してまいります。
```

### TTS

For TTS, we also use sequential generation, with the fixed system prompt `Perform TTS in japanese.`.

```python
import torch
import soundfile as sf
from liquid_audio import LFM2AudioModel, LFM2AudioProcessor, ChatState, LFMModality

# Load models
HF_REPO = "LiquidAI/LFM2.5-Audio-1.5B-JP"

processor = LFM2AudioProcessor.from_pretrained(HF_REPO).eval()
model = LFM2AudioModel.from_pretrained(HF_REPO).eval()

# Set up inputs for the model
chat = ChatState(processor)

chat.new_turn("system")
chat.add_text("Perform TTS in japanese.")
chat.end_turn()

chat.new_turn("user")
chat.add_text("先週ご相談いただいた新しいプロジェクトの件ですが、社内で検討した結果、ぜひ前向きに進めさせていただきたいと考えております。つきましては、具体的なスケジュールについて一度お打ち合わせの機会をいただけますでしょうか。")
chat.end_turn()

chat.new_turn("assistant")

# Generate text
audio_out: list[torch.Tensor] = []
for t in model.generate_sequential(**chat, max_new_tokens=512, audio_temperature = 0.8, audio_top_k=64):
    if t.numel() > 1:
        audio_out.append(t)

# Detokenize audio
audio_codes = torch.stack(audio_out[:-1], 1).unsqueeze(0)
waveform = processor.decode(audio_codes)
sf.write("tts_jp.wav", waveform.cpu()[0], 24_000)
```

## Output Samples

### Multi-turn, multi-modal chat

<table>
<tr><th>User</th><th>Assistant</th></tr>
<tr>
<td><audio controls controlsList="nodownload" src="https://cdn-uploads.huggingface.co/production/uploads/694763a9050e80d123d7e6c7/TSCN9qI0WieUtJzpiHxhW.wav"></audio></td>
<td><audio controls controlsList="nodownload" src="https://cdn-uploads.huggingface.co/production/uploads/694763a9050e80d123d7e6c7/QJp46oX-XCHS7mwchPI22.wav"></audio></td>
</tr>
<tr>
<td><audio controls controlsList="nodownload" src="https://cdn-uploads.huggingface.co/production/uploads/694763a9050e80d123d7e6c7/UnbZWQLr5j64QqTweXRj8.wav"></audio></td>
<td><audio controls controlsList="nodownload" src="https://cdn-uploads.huggingface.co/production/uploads/694763a9050e80d123d7e6c7/QgkiEwj0iNAqals2VYyhx.wav"></audio></td>
</tr>
<tr>
<td><audio controls controlsList="nodownload" src="https://cdn-uploads.huggingface.co/production/uploads/694763a9050e80d123d7e6c7/5U784EgBePJOmRt6PIS_v.wav"></audio></td>
<td><audio controls controlsList="nodownload" src="https://cdn-uploads.huggingface.co/production/uploads/694763a9050e80d123d7e6c7/jaNtOqXvIPp_2uuY4ZrlN.wav"></audio></td>
</tr>
<tr>
<td><audio controls controlsList="nodownload" src="https://cdn-uploads.huggingface.co/production/uploads/694763a9050e80d123d7e6c7/k-lAqnshXAz-B8sbPBPqu.wav"></audio></td>
<td><audio controls controlsList="nodownload" src="https://cdn-uploads.huggingface.co/production/uploads/694763a9050e80d123d7e6c7/rD2HxytqnchdcVWy3MjVz.wav"></audio></td>
</tr>
<tr>
<td><audio controls controlsList="nodownload" src="https://cdn-uploads.huggingface.co/production/uploads/694763a9050e80d123d7e6c7/gjUdJjNtbGbP8iqYkNCq5.wav"></audio></td>
<td><audio controls controlsList="nodownload" src="https://cdn-uploads.huggingface.co/production/uploads/694763a9050e80d123d7e6c7/mRcjc275iDB9fVirKH5SQ.wav"></audio></td>
</tr>
</table>

### ASR

<table>
<tr><th width="320">Input</th><th width="480">Output</th></tr>
<tr>
<td><audio controls controlsList="nodownload" src="https://cdn-uploads.huggingface.co/production/uploads/694763a9050e80d123d7e6c7/a5p89s0RopjhbqMmWvsc8.wav"></audio></td>
<td>本日はお忙しい中貴重なお時間をいただき誠にありがとうございました。皆様からいただいた貴重なご意見を元に次回の会議までに提案内容をさらにブラッシュアップしてまいります。</td>
</tr>
<tr>
<td><audio controls controlsList="nodownload" src="https://cdn-uploads.huggingface.co/production/uploads/694763a9050e80d123d7e6c7/EbAU4tY5RqRbzsORqjc5n.wav"></audio></td>
<td>先週ご相談いただいた新しいプロジェクトの件ですが、社内で検討した結果、ぜひ前向きに進めさせていただきたいと考えております。つきましては、具体的なスケジュールについて一度お打ち合わせの機会をいただけますでしょうか。</td></tr>
<tr>
<td><audio controls controlsList="nodownload" src="https://cdn-uploads.huggingface.co/production/uploads/694763a9050e80d123d7e6c7/Ed6epCBr-6y_R2vxD4d_l.wav"></audio></td>
<td>お世話になっております。先ほどお送りいたしました企画書につきまして、一部データの修正を行いましたので、最新版を添付にて再送いたします。お手数をおかけしますが、ご確認のほどよろしくお願いいたします。</td>
</tr>
<tr>
<td><audio controls controlsList="nodownload" src="https://cdn-uploads.huggingface.co/production/uploads/694763a9050e80d123d7e6c7/iRtbhRuaR4THl8Q67dFBH.wav"></audio></td>
<td>昨日は突然のスケジュール変更にもかかわらず迅速にご対応いただき本当に助かりました。おかげさまで無事に期限内に資料を提出することができました。心より感謝申し上げます。</td>
</tr>
<tr>
<td><audio controls controlsList="nodownload" src="https://cdn-uploads.huggingface.co/production/uploads/694763a9050e80d123d7e6c7/QTLP3M_wFRLgtthzOAZ7q.wav"></audio></td>
<td>この度は弊社の確認不足により多大なご迷惑をおかけしましたことを深くお詫び申し上げます。今後はこのようなことが二度と起こらないよう社内のチェック体制を徹底してまいります。</td>
</tr>
</table>

### TTS

<table>
<tr><th width="480">Input</th><th width="320">Output</th></tr>
<tr>
<td>本日はお忙しい中貴重なお時間をいただき誠にありがとうございました。皆様からいただいた貴重なご意見を元に次回の会議までに提案内容をさらにブラッシュアップしてまいります。</td>
<td><audio controls controlsList="nodownload" src="https://cdn-uploads.huggingface.co/production/uploads/694763a9050e80d123d7e6c7/MjI5yPmSz8nETrLupPYzh.wav"></audio></td>
</tr>
<tr>
<td>先週ご相談いただいた新しいプロジェクトの件ですが、社内で検討した結果、ぜひ前向きに進めさせていただきたいと考えております。つきましては、具体的なスケジュールについて一度お打ち合わせの機会をいただけますでしょうか。</td>
<td><audio controls controlsList="nodownload" src="https://cdn-uploads.huggingface.co/production/uploads/694763a9050e80d123d7e6c7/OrzL8BdnP8bKRBXwXdYJx.wav"></audio></td>
</tr>
<tr>
<td>お世話になっております。先ほどお送りいたしました企画書につきまして、一部データの修正を行いましたので、最新版を添付にて再送いたします。お手数をおかけしますが、ご確認のほどよろしくお願いいたします。</td>
<td><audio controls controlsList="nodownload" src="https://cdn-uploads.huggingface.co/production/uploads/694763a9050e80d123d7e6c7/lgmulNCb2nIi5qXGhVJZ_.wav"></audio></td>
</tr>
<tr>
<td>昨日は突然のスケジュール変更にもかかわらず迅速にご対応いただき本当に助かりました。おかげさまで無事に期限内に資料を提出することができました。心より感謝申し上げます。</td>
<td><audio controls controlsList="nodownload" src="https://cdn-uploads.huggingface.co/production/uploads/694763a9050e80d123d7e6c7/qkGqWEzqNFmmnbbukinxd.wav"></audio></td>
</tr>
<tr>
<td>この度は弊社の確認不足により多大なご迷惑をおかけしましたことを深くお詫び申し上げます。今後はこのようなことが二度と起こらないよう社内のチェック体制を徹底してまいります。</td>
<td><audio controls controlsList="nodownload" src="https://cdn-uploads.huggingface.co/production/uploads/694763a9050e80d123d7e6c7/QToKR9RSgMZ80n8cfKm87.wav"></audio></td>
</tr>
</table>

## Finetuning

To finetune on your own data, make use of the `ChatMessage` interface. This requires you to:

1. map your raw dataset rows into `list[ChatMessage]`
2. use the [`LFM2AudioChatMapper`](src/liquid_audio/data/mapper.py) to create a preprocessed dataset
3. train a model from the preprocessed dataset with `LFM2DataLoader`

To finetune our Japanese model on your own data in interleaved generation mode, instantiate the `LFM2AudioChatMapper` class with `interleaved_text_tokens=6` and `interleaved_audio_tokens=9`. These values reflect the predefined Japanese interleaving ratio of 6 text tokens to 9 audio tokens, based on tokenization statistics.

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