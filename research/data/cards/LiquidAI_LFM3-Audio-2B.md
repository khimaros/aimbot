---
library_name: transformers
license: other
license_name: lfm1.0
license_link: LICENSE
pipeline_tag: any-to-any
tags:
- liquid
- lfm3
- audio
- speech
- edge
- conversational
- multilingual
- custom_code
language:
- en
- ar
- da
- de
- el
- fi
- fr
- he
- it
- ja
- ko
- nl
- pl
- pt
- es
- sv
- tr
- zh
---

<div align="center">
  <img
    src="https://huggingface.co/LiquidAI/LFM3-1.7B/resolve/main/assets/liquid-ai-banner.webp"
    alt="Liquid AI"
    style="width: 100%; max-width: 100%; height: auto; display: block; margin: 0;"
  />
  <div align="center" style="display: flex; justify-content: center; align-items: center; gap: 1.25em; margin: 8px 0 1.7rem; padding: 0; line-height: 1.3;">
    <a href="https://console.liquid.ai/dashboard" style="display: inline-flex; align-items: center; gap: 6px;"><img src="https://huggingface.co/LiquidAI/LFM3-1.7B/resolve/main/assets/icons/api.svg" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>API</strong></a>
    <a href="https://playground.liquid.ai/talk" style="display: inline-flex; align-items: center; gap: 6px;"><img src="https://huggingface.co/LiquidAI/LFM3-1.7B/resolve/main/assets/icons/try.svg" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>Try</strong></a>
    <a href="https://docs.liquid.ai/lfm/getting-started/welcome" style="display: inline-flex; align-items: center; gap: 6px;"><img src="https://huggingface.co/LiquidAI/LFM3-1.7B/resolve/main/assets/icons/docs.svg" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>Docs</strong></a>
    <a href="https://www.liquid.ai/blog/lfm3" style="display: inline-flex; align-items: center; gap: 6px;"><img src="https://huggingface.co/LiquidAI/LFM3-1.7B/resolve/main/assets/icons/blog.svg" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>Blog</strong></a>
  </div>
</div>

# LFM3-Audio-2B

LFM3-Audio-2B is a **compact, fully featured audio model that runs locally on laptops and edge devices**. It takes text or audio as input and responds with text, speech, or both.

- **Voice chat:** ask questions aloud and receive streaming replies in text and speech. For text-only responses, the model can reason before answering. Currently supports English only.
- **Multilingual speech:** transcribe, synthesize, and translate speech across 18 languages.
- **Audio understanding and reasoning:** interpret recordings and answer questions about the speech, sounds, and events they contain.
- **Tool calling:** turn spoken requests into tool calls to control apps and devices, with text or speech alongside the calls.

LFM3-Audio-2B introduces an in-house audio encoder and LiquidCodec audio tokenizer, improving speech quality over LFM2.5-Audio. Find more information about the LFM3 family in [our release blog post](https://www.liquid.ai/blog/lfm3).

## Model details
<hr style="margin: -0.7em 0 1.2em 0; border: 0; border-top: 1px solid rgba(127, 127, 127, 0.3);" />

The [LFM3 family](https://huggingface.co/collections/LiquidAI/lfm3) includes base, text, vision, audio, omni, and decision models.

<table style="width: 100%; display: table; border: 0; border-radius: 0; border-collapse: collapse;">
<thead style="border: 0;">
<tr style="border: 0;">
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Property</th>
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Specification</th>
</tr>
</thead>
<tbody style="border: 0;">
<tr style="border: 0;">
<th scope="row" style="text-align: left; background-color: transparent; font-weight: 400; border: 0; padding: 0.55em 0.75em;"><strong>Parameters</strong></th>
<td style="border: 0; padding: 0.55em 0.75em;">2B total</td>
</tr>
<tr style="border: 0;">
<th scope="row" style="text-align: left; background-color: transparent; font-weight: 400; border: 0; padding: 0.55em 0.75em;"><strong>Architecture</strong></th>
<td style="border: 0; padding: 0.55em 0.75em;">LFM3 backbone, causal audio encoder, and LiquidCodec audio tokenizer</td>
</tr>
<tr style="border: 0;">
<th scope="row" style="text-align: left; background-color: transparent; font-weight: 400; border: 0; padding: 0.55em 0.75em;"><strong>Input</strong></th>
<td style="border: 0; padding: 0.55em 0.75em;">Text or audio; audio encoder operates at 16 kHz</td>
</tr>
<tr style="border: 0;">
<th scope="row" style="text-align: left; background-color: transparent; font-weight: 400; border: 0; padding: 0.55em 0.75em;"><strong>Output</strong></th>
<td style="border: 0; padding: 0.55em 0.75em;">Text, 24 kHz speech, or interleaved text and speech</td>
</tr>
<tr style="border: 0;">
<th scope="row" style="text-align: left; background-color: transparent; font-weight: 400; border: 0; padding: 0.55em 0.75em;"><strong>Context length</strong></th>
<td style="border: 0; padding: 0.55em 0.75em;">32K tokens (input + output)</td>
</tr>
<tr style="border: 0;">
<th scope="row" style="text-align: left; background-color: transparent; font-weight: 400; border: 0; padding: 0.55em 0.75em;"><strong>Streaming</strong></th>
<td style="border: 0; padding: 0.55em 0.75em;">Causal audio encoding, incremental prefill, and streaming speech generation</td>
</tr>
<tr style="border: 0;">
<th scope="row" style="text-align: left; background-color: transparent; font-weight: 400; border: 0; padding: 0.55em 0.75em;"><strong>Speech languages / locales</strong></th>
<td style="border: 0; padding: 0.55em 0.75em;">Arabic, Danish, German, Greek, British English, American English, Finnish, French, Hebrew, Italian, Japanese, Korean, Dutch, Polish, Portuguese, Spanish, Swedish, Turkish, Chinese</td>
</tr>
<tr style="border: 0;">
<th scope="row" style="text-align: left; background-color: transparent; font-weight: 400; border: 0; padding: 0.55em 0.75em;"><strong>License</strong></th>
<td style="border: 0; padding: 0.55em 0.75em;"><a href="LICENSE">LFM Open License v1.0</a></td>
</tr>
</tbody>
</table>

LFM3-Audio-2B is designed for local agents, tool calling, structured outputs, and domain-specific fine-tuning. Use retrieval or search for knowledge-heavy tasks. It is not recommended for agentic coding or complex multi-step reasoning due to its small size.


## Inference
<hr style="margin: -0.7em 0 1.2em 0; border: 0; border-top: 1px solid rgba(127, 127, 127, 0.3);" />

Choose a checkpoint variant for your inference framework and hardware.

<table style="width: 100%; display: table; border: 0; border-radius: 0; border-collapse: collapse;">
<thead style="border: 0;">
<tr style="border: 0;">
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Checkpoint</th>
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Framework</th>
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Description</th>
</tr>
</thead>
<tbody style="border: 0;">
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://huggingface.co/LiquidAI/LFM3-Audio-2B">BF16</a></td>
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://docs.liquid.ai/deployment/gpu-inference/vllm">vLLM</a>, <a href="https://docs.liquid.ai/deployment/gpu-inference/sglang">SGLang</a>, <a href="https://docs.liquid.ai/deployment/gpu-inference/transformers">Transformers</a></td>
<td style="border: 0; padding: 0.55em 0.75em;">BF16 weights for GPU inference.</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://huggingface.co/LiquidAI/LFM3-Audio-2B-GGUF">GGUF</a></td>
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://docs.liquid.ai/deployment/on-device/llama-cpp">llama.cpp</a></td>
<td style="border: 0; padding: 0.55em 0.75em;">Local inference on CPUs and GPUs.</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://huggingface.co/LiquidAI/LFM3-Audio-2B-MLX-4bit">MLX</a></td>
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://docs.liquid.ai/deployment/on-device/mlx">MLX-VLM</a></td>
<td style="border: 0; padding: 0.55em 0.75em;">4-bit quantization for Apple Silicon.</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://huggingface.co/LiquidAI/LFM3-Audio-2B-ONNX">ONNX</a></td>
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://docs.liquid.ai/deployment/on-device/onnx">ONNX Runtime</a></td>
<td style="border: 0; padding: 0.55em 0.75em;">Cross-platform inference with ONNX Runtime.</td>
</tr>
</tbody>
</table>

### Transformers quick start

Install the dependencies, then load the model and processor with the checkpoint's custom code. The codec implementation is included in this repository; the processor loads its weights from `audio_tokenizer/`.

```bash
pip install "transformers>=5.20.2" torch accelerate librosa soundfile
```

Load the model and processor directly from the Hugging Face Hub:

```python
import torch
import soundfile as sf

from transformers import AutoModelForMultimodalLM, AutoProcessor

model_id = "LiquidAI/LFM3-Audio-2B"
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.bfloat16 if device == "cuda" else torch.float32

model = AutoModelForMultimodalLM.from_pretrained(
    model_id, dtype=dtype, device_map=device, trust_remote_code=True
).eval()
processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
codec = processor.audio_tokenizer.to(device=device).eval()
```

**Audio sampling parameters:** use `audio_temperature=1.0`, `audio_top_k=128`, `audio_repetition_penalty=1.1`, and `audio_repetition_window=4096` for speech synthesis and interleaved text and speech. For text-only output, set `suppress_mixed=True` and `suppress_audio_out=True`.

### Usage examples

The examples below reuse the model, codec, and processor loaded above. Replace `audio.wav`, `question.wav`, or `recording.wav` with your own audio files.

<details>
<summary><strong>Speech recognition (ASR)</strong></summary>

To use the model for transcription, use the system prompt `Perform ASR in <language>.`, where `<language>` is the English name of the language.
To let the model infer the language, use `Perform ASR.`.

Below, we transcribe a `.wav` file containing English speech.

```python
conversation = [
    {"role": "system", "content": "Perform ASR in English."},
    {"role": "user", "content": [{"type": "audio", "audio": "audio.wav"}]},
]

inputs = processor.apply_chat_template(
    conversation,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
).to(device)
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=1024,
        suppress_mixed=True,
        suppress_audio_out=True,
        return_dict_in_generate=True,
    )
text = processor.decode(
    outputs.sequences[0, inputs["input_ids"].shape[1]:],
    skip_special_tokens=True,
)
print(text)
```

</details>

<details>
<summary><strong>Live speech recognition (LiveASR)</strong></summary>

LiveASR transcribes speech while it is still being spoken, instead of waiting for the full recording. Use the system prompt `Perform live ASR.`. LiveASR currently supports English only. The model processes audio in chunks of about 0.96 s and writes the text for each chunk as soon as the chunk arrives. `model.transcribe_live()` runs one chunk at a time and returns a state that you pass to the next call.

Below, we simulate a microphone by feeding a `.wav` file in 100 ms pieces.

```python
import librosa

tokenizer = processor.tokenizer
chunk_frames = 8 * model.config.interleaved_n_audio
prompt = tokenizer(
    "<|startoftext|><|im_start|>system\nPerform live ASR.<|im_end|>\n<|im_start|>assistant\n",
    add_special_tokens=False,
    return_tensors="pt",
).input_ids.to(device)
suppress = tokenizer.convert_tokens_to_ids(["<|mixed_end|>", "<|endoftext|>"])
stop = tokenizer.convert_tokens_to_ids(["<|endoftext|>", "<|im_start|>"])
state, feature_cache = None, None
mel = torch.empty((1, processor.feature_extractor.feature_size, 0), device=device)


def transcribe(frames, is_final=False):
    global state
    output = model.transcribe_live(
        frames,
        state,
        input_ids=prompt if state is None else None,
        is_final=is_final,
        max_new_tokens=96 if is_final else 48,
        suppress_token_ids=suppress,
        stop_token_ids=stop,
    )
    state = output.state
    print(tokenizer.decode(output.sequences[0], skip_special_tokens=True), end="", flush=True)


waveform, _ = librosa.load("audio.wav", sr=16_000)
for start in range(0, len(waveform), 1_600):  # 100 ms microphone chunks
    features, feature_cache = processor.feature_extractor.stream(
        waveform[start:start + 1_600], feature_cache
    )
    mel = torch.cat((mel, features.input_features.to(device)), dim=-1)
    while mel.shape[-1] >= chunk_frames:
        transcribe(mel[..., :chunk_frames])
        mel = mel[..., chunk_frames:]

# flush the remaining audio and end the transcript
features, feature_cache = processor.feature_extractor.stream([], feature_cache, is_final=True)
mel = torch.cat((mel, features.input_features.to(device)), dim=-1)
while mel.shape[-1] > chunk_frames:
    transcribe(mel[..., :chunk_frames])
    mel = mel[..., chunk_frames:]
transcribe(mel, is_final=True)
print()
```

For streams longer than 30 seconds, pass `input_ids=prompt` again to start a new text context. The encoder keeps following the audio stream.

</details>

<details>
<summary><strong>Speech synthesis (TTS)</strong></summary>

For speech synthesis, use the system prompt `Perform TTS in <language> using a <gender> voice.`.
Use a language or locale from the model details above and a `female` or `male` voice. Prefill the assistant turn with `<|audio_start|>`.

```python
conversation = [
    {"role": "system", "content": "Perform TTS in American English using a female voice."},
    {"role": "user", "content": "The quick brown fox jumps over the lazy dog"},
    {"role": "assistant", "content": "<|audio_start|>"},
]
inputs = processor.apply_chat_template(
    conversation,
    continue_final_message=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
).to(device)
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        audio_temperature=1.0,
        audio_top_k=128,
        audio_repetition_penalty=1.1,
        audio_repetition_window=4096,
        return_dict_in_generate=True,
    )
    waveform = codec.decode(
        outputs.audio_codes[:1, :, :outputs.audio_lengths[0]]
    ).audio_values[0]  # 24 kHz

sf.write("tts.wav", waveform.float().cpu().numpy(), 24_000)
```

</details>

<details>
<summary><strong>Voice chat: speech and text responses</strong></summary>

In this mode, the model will respond to the user in both speech and text.
The recommended system prompt is `Respond with interleaved text and audio.`.
User input can be either text or audio, and we prefill the assistant turn with a special token `<|mixed_start|>`.

The assistant responds in a conversational style with interleaved text and speech. This example saves the complete response.

```python
conversation = [
    {"role": "system", "content": "Respond with interleaved text and audio."},
    {"role": "user", "content": [{"type": "audio", "audio": "question.wav"}]},
    {"role": "assistant", "content": "<|mixed_start|>"},
]
inputs = processor.apply_chat_template(
    conversation,
    continue_final_message=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
).to(device)
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=1024,
        audio_temperature=1.0,
        audio_top_k=128,
        audio_repetition_penalty=1.1,
        audio_repetition_window=4096,
        return_dict_in_generate=True,
    )

    text = processor.decode(
        outputs.sequences[0, inputs["input_ids"].shape[1]:],
        skip_special_tokens=True,
    )
    waveform = codec.decode(
        outputs.audio_codes[:1, :, :outputs.audio_lengths[0]]
    ).audio_values[0]  # 24 kHz
print(text)
sf.write("reply.wav", waveform.float().cpu().numpy(), 24_000)
```

For streaming applications, `model.generate()` accepts `streamer` for text tokens and `audio_streamer` for speech frames. LiquidCodec supports incremental decoding of those frames.

</details>

<details>
<summary><strong>Speech-to-text chat, with or without reasoning</strong></summary>

For a text-only answer, no specific system prompt is needed. Prefill `<think>` to let the model reason before answering, or `<think></think>` for a direct response.

```python
use_thinking = True
conversation = [
    {"role": "user", "content": [{"type": "audio", "audio": "question.wav"}]},
    {"role": "assistant", "content": "<think>" if use_thinking else "<think></think>"},
]
inputs = processor.apply_chat_template(
    conversation,
    continue_final_message=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
).to(device)
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=1024,
        suppress_mixed=True,
        suppress_audio_out=True,
        return_dict_in_generate=True,
    )
    text = processor.decode(
        outputs.sequences[0, inputs["input_ids"].shape[1]:],
        skip_special_tokens=True,
    )
if use_thinking:
    _, separator, text = text.partition("</think>")
    if not separator:
        raise RuntimeError("Reasoning has not finished; increase max_new_tokens.")
print(text.strip())
```

</details>

<details>
<summary><strong>Audio understanding</strong></summary>

Include the recording and a question in the user turn. Questions can address speech, music, background sounds, or events. No specific system prompt is required; to ground answers in the recording, use `Answer questions about the provided audio clip. Base every answer only on what can be heard.`.

```python
conversation = [
    {
        "role": "system",
        "content": "Answer questions about the provided audio clip. Base every answer only on what can be heard.",
    },
    {
        "role": "user",
        "content": [
            {"type": "audio", "audio": "recording.wav"},
            {"type": "text", "text": "What is happening in this recording?"},
        ],
    },
]
inputs = processor.apply_chat_template(
    conversation,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
).to(device)

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=1024,
        suppress_mixed=True,
        suppress_audio_out=True,
        return_dict_in_generate=True,
    )

print(processor.decode(
    outputs.sequences[0, inputs["input_ids"].shape[1]:],
    skip_special_tokens=True,
))
```

For multiple-choice questions, include the choices in the text part and ask the model to select an answer.

</details>

<details>
<summary><strong>Translation</strong></summary>

Use a system prompt that specifies the source language, target language, and output format:

- **Speech to text:** `Translate the following speech from {source} to {target} in text form.`
- **Text to text:** `Translate the following {source} text into {target}.`

Replace `{source}` and `{target}` with the English names of the source and target languages. Follow the ASR example with the translation prompt; for text input, set the user message's `content` to the text to translate. Translation supports the speech languages listed above; translation to or from English generally works best.

</details>

<details>
<summary><strong>Tool calling from spoken requests</strong></summary>

Pass function schemas through `tools=...` to `apply_chat_template()`. The chat template appends them to the system prompt, one JSON definition per line inside `<tools>…</tools>`. Requests may be spoken or written.

With the system prompt `Respond with function calls, and interleaved text and audio.\n\nList of tools:`, the model either calls tools or answers with interleaved text and speech. Do not prefill the assistant turn: the model chooses whether to start with `<tool_call>` or `<|mixed_start|>`. A tool call looks like this, with multiple calls separated by a blank line:

```
<tool_call>
<function=set_volume>
<parameter=volume>
30
</parameter>
</function>
</tool_call>
```

Values other than strings are written as JSON. Your application parses and runs the calls, then appends the assistant's `tool_calls` (with `arguments` as a dict) and a `tool` message with the results to the conversation. The template wraps the results in `<tool_response>…</tool_response>`. Generate again with the same `tools`: the model either makes more calls or answers.

```python
import json
import re

tools = [{
    "type": "function",
    "function": {
        "name": "set_volume",
        "description": "Set the device speaker volume.",
        "parameters": {
            "type": "object",
            "properties": {
                "volume": {"type": "integer", "description": "Volume from 0 to 100."}
            },
            "required": ["volume"],
        },
    },
}]
functions = {"set_volume": lambda volume: {"volume": volume}}  # your implementations

CALL_RE = re.compile(r"<tool_call>\s*<function=([^>\n]+)>(.*?)</function>\s*</tool_call>", re.DOTALL)
PARAM_RE = re.compile(r"<parameter=([^>\n]+)>\n?(.*?)\n?</parameter>", re.DOTALL)


def parse_tool_calls(text):
    calls = []
    for name, body in CALL_RE.findall(text):
        arguments = {}
        for key, value in PARAM_RE.findall(body):
            try:
                arguments[key] = json.loads(value)
            except json.JSONDecodeError:
                arguments[key] = value  # plain string
        calls.append({"type": "function", "function": {"name": name, "arguments": arguments}})
    return calls


def respond(conversation):
    inputs = processor.apply_chat_template(
        conversation,
        tools=tools,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    ).to(device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=1024,
            audio_temperature=1.0,
            audio_top_k=128,
            audio_repetition_penalty=1.1,
            audio_repetition_window=4096,
            return_dict_in_generate=True,
        )
    text = processor.decode(
        outputs.sequences[0, inputs["input_ids"].shape[1]:],
        skip_special_tokens=True,
    )
    return text, outputs


conversation = [
    {
        "role": "system",
        "content": "Respond with function calls, and interleaved text and audio.\n\nList of tools:",
    },
    {"role": "user", "content": [{"type": "audio", "audio": "question.wav"}]},
]
text, outputs = respond(conversation)
while calls := parse_tool_calls(text):
    results = [functions[c["function"]["name"]](**c["function"]["arguments"]) for c in calls]
    conversation += [
        {"role": "assistant", "tool_calls": calls},
        {"role": "tool", "content": json.dumps(results)},
    ]
    text, outputs = respond(conversation)

print(text)
with torch.no_grad():
    waveform = codec.decode(
        outputs.audio_codes[:1, :, :outputs.audio_lengths[0]]
    ).audio_values[0]  # 24 kHz
sf.write("reply.wav", waveform.float().cpu().numpy(), 24_000)
```

**Text-only answers:** use the system prompt `List of tools:` (keep `tools=`) and pass `suppress_mixed=True, suppress_audio_out=True` to `generate()`. Calls and results are handled the same way.

</details>

## Fine-tuning
<hr style="margin: -0.7em 0 1.2em 0; border: 0; border-top: 1px solid rgba(127, 127, 127, 0.3);" />

LFM3-Audio-2B is designed for **easy customization** for a given domain, task, or application with Hugging Face Transformers.

<table style="width: 100%; display: table; border: 0; border-radius: 0; border-collapse: collapse;">
<thead style="border: 0;">
<tr style="border: 0;">
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Training</th>
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Use case</th>
<th scope="col" style="text-align: center; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Notebook</th>
</tr>
</thead>
<tbody style="border: 0;">
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><strong>SFT</strong></td>
<td style="border: 0; padding: 0.55em 0.75em;">Audio-to-function calling for smart home control</td>
<td style="text-align: center; border: 0; padding: 0.55em 0.75em;"><a href="https://colab.research.google.com/github/Liquid4All/cookbook/blob/main/finetuning/notebooks/lfm3_audio_sft_with_transformers.ipynb" title="SFT with Transformers"><img src="https://colab.research.google.com/assets/colab-badge.svg" width="117" height="20" alt="Open in Colab" style="display: inline-block; width: 117px; height: 20px; margin: 0; vertical-align: middle;" /></a></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><strong>SFT</strong></td>
<td style="border: 0; padding: 0.55em 0.75em;">Text-to-speech (TTS)</td>
<td style="text-align: center; border: 0; padding: 0.55em 0.75em;"><a href="https://colab.research.google.com/github/Liquid4All/cookbook/blob/main/finetuning/notebooks/lfm3_audio_tts_sft_with_transformers.ipynb" title="TTS SFT with Transformers"><img src="https://colab.research.google.com/assets/colab-badge.svg" width="117" height="20" alt="Open in Colab" style="display: inline-block; width: 117px; height: 20px; margin: 0; vertical-align: middle;" /></a></td>
</tr>
</tbody>
</table>

## Performance
<hr style="margin: -0.7em 0 1.2em 0; border: 0; border-top: 1px solid rgba(127, 127, 127, 0.3);" />

### Benchmarks

LFM3-Audio-2B improves over LFM2.5-Audio in speech quality, spoken instruction following, and audio understanding, while supporting multilingual speech and tool calling.

<div role="region" aria-label="Audio model benchmarks" tabindex="0" style="width: 100%; max-width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch;">
<table style="width: 100%; display: table; border: 0; border-radius: 0; border-collapse: collapse; font-size: calc(0.875em - 1pt);">
<thead style="border: 0;">
<tr style="border: 0;">
<th scope="col" style="text-align: left; padding: 0.45em 0.4em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Benchmark</th>
<th scope="col" style="text-align: center; background-color: rgba(108, 79, 224, 0.08); padding: 0.45em 0.4em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);"><strong>LFM3-Audio<br>2B</strong></th>
<th scope="col" style="text-align: center; padding: 0.45em 0.4em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">LFM2.5-Audio<br>1.5B</th>
<th scope="col" style="text-align: center; padding: 0.45em 0.4em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Gemma 4<br>E2B</th>
<th scope="col" style="text-align: center; padding: 0.45em 0.4em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Gemma 4<br>E4B</th>
<th scope="col" style="text-align: center; padding: 0.45em 0.4em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Qwen2.5-Omni<br>3B</th>
<th scope="col" style="text-align: center; padding: 0.45em 0.4em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">NVIDIA Audex<br>2B</th>
<th scope="col" style="text-align: center; padding: 0.45em 0.4em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Voxtral Mini<br>3B</th>
</tr>
</thead>
<tbody style="border: 0;">
<tr style="border: 0;">
<th scope="row" style="text-align: left; background-color: transparent; font-weight: 400; border: 0; padding: 0.45em 0.4em;">Total parameters</th>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.45em 0.4em;">2B</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">1.5B</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">5B</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">8B</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">6B</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">3B</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">5B</td>
</tr>
<tr style="border: 0;">
<th scope="row" style="text-align: left; background-color: transparent; font-weight: 400; border: 0; padding: 0.45em 0.4em;">English ASR<br><small>WER ↓</small></th>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.45em 0.4em;">6.23</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">6.13</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">8.26</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">7.82</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">6.30</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;"><u>5.99</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;"><strong>5.51</strong></td>
</tr>
<tr style="border: 0;">
<th scope="row" style="text-align: left; background-color: transparent; font-weight: 400; border: 0; padding: 0.45em 0.4em;">Multilingual ASR<br><small>WER / CER ↓</small></th>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.45em 0.4em;"><strong>6.03</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">—</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">8.08</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">6.54</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">7.41</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;"><u>6.40</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">7.76</td>
</tr>
<tr style="border: 0;">
<th scope="row" style="text-align: left; background-color: transparent; font-weight: 400; border: 0; padding: 0.45em 0.4em;">English TTS<br><small>UTMOSv2 ↑</small></th>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.45em 0.4em;"><strong>3.83</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">3.22</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">—</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">—</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;"><u>3.42</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">—</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">—</td>
</tr>
<tr style="border: 0;">
<th scope="row" style="text-align: left; background-color: transparent; font-weight: 400; border: 0; padding: 0.45em 0.4em;">VoiceBench ↑</th>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.45em 0.4em;"><strong>73.13</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">55.17</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">63.28</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;"><u>72.90</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">66.37</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">22.55</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">65.78</td>
</tr>
<tr style="border: 0;">
<th scope="row" style="text-align: left; background-color: transparent; font-weight: 400; border: 0; padding: 0.45em 0.4em;">Tool calling<br><small>internal eval ↑</small></th>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.45em 0.4em;"><u>58.50</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">—</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">55.60</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;"><strong>72.40</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">44.30</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">—</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">44.50</td>
</tr>
<tr style="border: 0;">
<th scope="row" style="text-align: left; background-color: transparent; font-weight: 400; border: 0; padding: 0.45em 0.4em;">Audio understanding<br><small>MMAR ↑</small></th>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.45em 0.4em;">50.60</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">25.85</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">44.49</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">49.10</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;"><strong>54.41</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;"><u>53.21</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.45em 0.4em;">50.10</td>
</tr>
</tbody>
</table>
</div>

<details>
<summary><small>Evaluation details</small></summary>

<p><small>
<strong>English ASR</strong>: average word error rate (WER) in percent on the ESB / Open ASR benchmark suite, lower is better.<br>
<strong>Multilingual ASR</strong>: mean error rate in percent on FLEURS across English, Spanish, Portuguese, German, French, Italian, Chinese, Japanese, and Korean, lower is better. WER is used for all languages except Chinese, Japanese, and Korean, which use character error rate (CER).<br>
<strong>English TTS</strong>: UTMOSv2 speech quality score on a 1–5 scale, higher is better.<br>
<strong>VoiceBench</strong>: audio input, text output, percentage score, higher is better.<br>
<strong>Tool calling</strong>: internal evaluation with audio input, percentage score, higher is better.<br>
<strong>Audio understanding</strong>: MMAR, percentage score, higher is better.
</small></p>

<p><small>
Note: Evaluations used audio_temperature=0.4, audio_top_k=0, audio_repetition_penalty=1.2 and audio_repetition_window=64, with greedy text decoding except VoiceBench (do_sample=True, temperature=0.1, top_k=0, repetition_penalty=1.1, text_repetition_window=2048).
</small></p>

</details>

### Streaming performance

The causal encoder processes live microphone input and allows the backbone to prefill while you speak, reducing the wait after you finish. Time to first token can be **as low as 50 ms**.

LiquidCodec converts generated tokens into speech at about **87× real time on a single CPU thread on Apple M4 Max**. It supports streaming decoding so speech can be played as it is generated.

## Architecture
<hr style="margin: -0.7em 0 1.2em 0; border: 0; border-top: 1px solid rgba(127, 127, 127, 0.3);" />

<img src="https://huggingface.co/LiquidAI/LFM3-Audio-2B-Preview/resolve/main/assets/lfm3-audio-architecture.webp" alt="LFM3-Audio-2B architecture: 16 kHz audio input passes through a causal, streaming audio encoder into the LFM3 backbone, and text input enters the backbone directly. The backbone outputs text and tool calls, or speech tokens that LiquidCodec, at 12 tokens per 80 ms, decodes into 24 kHz speech." width="2092" height="572" style="width: 100%; max-width: 2092px; height: auto;" />

**Causal audio encoder:** our LFM-based encoder combines sliding-window attention and short convolution layers to keep memory utilization bounded. Its fully causal design supports live audio input and incremental prefill.

**LiquidCodec:** our in-house audio tokenizer powers multilingual speech generation in both LFM3-Audio and LFM3-Omni. Built on the LFM3 architecture, it represents each **80 ms of speech with 12 discrete tokens** and supports streaming decoding.

**Parallel speech prediction:** multiple audio tokens are predicted iteratively in parallel, replacing the sequential prediction used by previous LFM Audio models. As the backbone generates tokens, the detokenizer progressively turns them into speech faster than real time, keeping conversations responsive.

## Citation
<hr style="margin: -0.7em 0 1.2em 0; border: 0; border-top: 1px solid rgba(127, 127, 127, 0.3);" />

```bibtex
@article{liquidAI2026LFM3,
  author  = {Liquid AI},
  title   = {Introducing LFM3: Every Modality for Specialized Intelligence},
  journal = {Liquid AI Blog},
  year    = {2026},
  note    = {www.liquid.ai/blog/lfm3},
}
```

For questions and feedback, join [Discord](https://discord.com/invite/liquid-ai). For custom deployment and fine-tuning support, [contact Liquid AI](https://www.liquid.ai/connect?utm_source=huggingface&utm_medium=referral&utm_campaign=huggingface).
