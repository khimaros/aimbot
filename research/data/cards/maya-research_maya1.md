---
license: apache-2.0
library_name: transformers
pipeline_tag: text-to-speech
tags:
- voice-design
- expressive-speech
- audio-generation
---

# Maya-1

**Maya-1 is an open-weight text-to-speech model from Maya Research that combines natural-language voice descriptions with inline expressive controls.** It generates speech as discrete audio tokens, which are decoded into a 24 kHz waveform. Developers can describe a voice and its delivery in text instead of choosing only from a fixed speaker menu.

## Demos

<table class="demo-grid">
  <tr>
    <td width="50%">
      <strong>Energetic Female Event Host</strong><br/>
      <video controls playsinline preload="metadata" width="100%" src="https://cdn-uploads.huggingface.co/production/uploads/642a7d4e556ab448a0701ca1/JKzy8zA36qvsOblV-lhd1.mp4">
        Your browser does not support video.
      </video>
      <details>
        <summary>Voice description</summary>
        <pre>Female, in her 30s with an American accent and is an event host, energetic, clear diction</pre>
      </details>
      <a href="https://cdn-uploads.huggingface.co/production/uploads/642a7d4e556ab448a0701ca1/JKzy8zA36qvsOblV-lhd1.mp4">Open video</a>
    </td>
    <td width="50%">
      <strong>Calm Male Narrator</strong><br/>
      <video controls playsinline preload="metadata" width="100%" src="https://cdn-uploads.huggingface.co/production/uploads/642a7d4e556ab448a0701ca1/96ntP7hGROwdg9w9Gu5tH.mp4">
        Your browser does not support video.
      </video>
      <details>
        <summary>Voice description</summary>
        <pre>Male, late 20s, neutral American, warm baritone, calm pacing</pre>
      </details>
      <a href="https://cdn-uploads.huggingface.co/production/uploads/642a7d4e556ab448a0701ca1/96ntP7hGROwdg9w9Gu5tH.mp4">Open video</a>
    </td>
  </tr>
</table>

### Audio examples

Each example pairs a voice description with the input text and its audio output.

#### Energetic Female Event Host

**Voice description:**

```text
Female, in her 30s with an American accent and is an event host, energetic, clear diction
```

**Text:**

```text
Wow. This place looks even better than I imagined. How did they set all this up so perfectly? The lights, the music, everything feels magical. I can't stop smiling right now.
```

<audio controls preload="metadata" src="https://cdn-uploads.huggingface.co/production/uploads/642a7d4e556ab448a0701ca1/4zDlBLeFk0Y2rOrQhMW9r.wav"></audio>

#### Dark Villain with Anger

**Voice description:**

```text
Dark villain character, Male voice in their 40s with a British accent. low pitch, gravelly timbre, slow pacing, angry tone at high intensity.
```

**Text:**

```text
Welcome back to another episode of our podcast! <laugh_harder> Today we are diving into an absolutely fascinating topic
```

<audio controls preload="metadata" src="https://cdn-uploads.huggingface.co/production/uploads/642a7d4e556ab448a0701ca1/mT6FnTrA3KYQnwfJms92X.wav"></audio>

#### Demon Character with Screaming Delivery

**Voice description:**

```text
Demon character, Male voice in their 30s with a Middle Eastern accent. screaming tone at high intensity.
```

**Text:**

```text
You dare challenge me, mortal <snort> how amusing. Your kind always thinks they can win
```

<audio controls preload="metadata" src="https://cdn-uploads.huggingface.co/production/uploads/642a7d4e556ab448a0701ca1/oxdns7uACCmLyC-P4H30G.wav"></audio>

#### Mythical Goddess with a Crying Cue

**Voice description:**

```text
Mythical godlike magical character, Female voice in their 30s slow pacing, curious tone at medium intensity.
```

**Text:**

```text
After all we went through to pull him out of that mess <cry> I can't believe he was the traitor
```

<audio controls preload="metadata" src="https://cdn-uploads.huggingface.co/production/uploads/642a7d4e556ab448a0701ca1/ggzAhM-rEUyv_mPLSALQG.wav"></audio>

## Model at a glance

| Property | Released model |
| --- | --- |
| Repository | `maya-research/maya1` |
| Task | Text-to-speech with description-based voice design and expressive controls |
| Parameters | Approximately 3.30 billion; Hub tensor metadata reports 3,300,928,512 parameters |
| Model implementation | Decoder-only `LlamaForCausalLM` |
| Audio representation | SNAC discrete audio codes |
| Decoder used in the reference implementation | `hubertsiuzdak/snac_24khz` |
| Native output | 24 kHz mono audio |
| Released weight precision | BF16 |
| Published expressive range | More than 20 emotions and vocal styles, as described in the release |
| Distribution | Hugging Face checkpoint, tokenizer and reference inference code |
| Model license declaration | Apache 2.0 in repository metadata; see component-license notes below |

This card documents the **Maya-1 checkpoint**. Other Maya Research models have separate documentation.

## 1. Purpose and design

### Design objective

Maya-1 separates **what should be spoken** from **how it should sound**, while bringing both into the model's generation process. An utterance provides the words, a natural-language description guides the overall voice, and inline markers request local expression. Together, these inputs condition the acoustic-token sequence that becomes the output waveform.

The design connects three parts: a controllable text interface, training examples that pair written direction with audio, and an inference path that turns generated acoustic tokens into playable speech. The sections below explain these connections and the decisions behind them.

### Technical contributions and novelty

Maya-1 brings descriptive voice direction, local expressive control and acoustic-token generation together in one trained, open-weight model. Its model-level contribution is the way these capabilities are connected in the conditioning interface, training workflow and released inference path.

- **A voice specified through language:** the model receives a description of the desired voice alongside the utterance. This makes age, timbre, accent, pacing and delivery part of the generative input rather than restricting the interface to selection from a predefined speaker list.
- **Voice identity and expression controlled together:** description-level guidance establishes the overall voice, while inline markers request local delivery changes or vocalizations. A passage can retain its voice direction while requesting laughter, whispering or other expressive behavior at relevant points.
- **Supervision tied to the conditioning interface:** curated recordings, human-reviewed voice descriptions and expressive annotations provide the training material for connecting written direction with acoustic output. The data workflow and conditioning-format experiments are described below.
- **Conditioning format development:** exploration of colon-delimited descriptions, attribute lists and key-value tags led to the selected description wrapper. The reported qualitative observations explain the choice: preserve flexible natural-language direction while reducing format drift, spoken descriptions and sensitivity to rigid attribute syntax.
- **A complete path from conditioned text to playable audio:** the causal transformer predicts SNAC acoustic codes, the decoding path reconstructs the hierarchical codec streams, and the streaming path emits audio incrementally. The model exposes the resulting capability through downloadable weights and inference resources.

Maya-1 builds on a Llama-style transformer and the SNAC codec, connecting these components through its conditioning interface, training workflow and inference implementation. The contribution described here is this model-specific design and integration.

### Comparison with other voice-generation approaches

Voice-generation systems expose different ways to create and direct a voice. The comparison below concerns the documented interfaces of specific models and services, rather than a ranking of audio quality or speed.

| Model or service | Documented voice-control approach | Maya-1's design distinction |
| --- | --- | --- |
| [Coqui XTTS-v2](https://huggingface.co/coqui/XTTS-v2) | Reference-audio voice cloning, including emotion and style transfer from a short recording. | Maya-1's voice-design interface starts from a written description rather than requiring a reference recording, and accepts local expressive markers in the utterance. |
| [Kokoro v1.0](https://huggingface.co/hexgrad/Kokoro-82M) | The released interface selects a voice preset, such as `af_heart`; the model has downloadable Apache-licensed weights. | Maya-1 conditions generation on a free-form description of the requested voice rather than only a preset identifier. Its interface also exposes inline emotion and vocalization tokens. |
| [Parler-TTS Mini v1](https://huggingface.co/parler-tts/parler-tts-mini-v1) | Natural-language descriptions control voice and delivery; public weights and training resources are available. | Text-described voices are a shared capability. Maya-1's particular design combines description conditioning with inline expressive tokens and a Llama-style/SNAC generation path, supported by incremental inference code. |
| [ElevenLabs Voice Design v3](https://elevenlabs.io/blog/voice-design-v3) and [Eleven v3 alpha](https://elevenlabs.io/blog/eleven-v3) | Voice Design creates voices from written descriptions; Eleven v3 also supports inline emotion and nonverbal audio tags. | Maya-1 provides a downloadable checkpoint and inference implementation, allowing developers to run and adapt the voice-generation model on their own infrastructure rather than relying on the standard hosted workflow described by these services. |

**What Maya-1 adds:** developers can describe a voice, direct expression within the spoken passage and run the resulting model locally through one open-weight release. This brings creative voice direction into a self-hostable workflow: a developer need not supply a target-speaker recording or limit the input to a preset voice menu. The contribution is the combination of these controls with the model's training and acoustic-token generation design.

### Key design choices

The following choices explain the technical purpose of this design and the practical considerations associated with it.

**1. Use a natural-language description to condition the voice.**

- **Design:** provide a voice description alongside the utterance. The description specifies the desired characteristics; the utterance supplies the spoken content. Both enter the model's input sequence.
- **Rationale:** developers can request combinations of accent, pitch, timbre, pace and delivery in ordinary language, without selecting only from a fixed speaker menu or managing a separate numeric control for every attribute.
- **Usage consideration:** descriptions work best as clear, compatible requests. Ambiguous or conflicting attributes can reduce consistency.

**2. Combine overall voice guidance with local expressive markers.**

- **Design:** combine description-level voice guidance with inline tokens such as `<whisper>`, `<laugh>` and `<sigh>`.
- **Rationale:** overall voice characteristics and moment-to-moment expression are different control needs. Inline markers let a passage request changes or nonverbal sounds near the relevant spoken content, complementing the global description.
- **Usage consideration:** inline tokens request delivery or vocal events; their placement does not specify an exact timestamp, duration or intensity.

**3. Model speech as a sequence of discrete audio tokens.**

- **Design:** predict SNAC acoustic codes autoregressively, then reconstruct the waveform with the SNAC decoder. The reference implementation groups seven generated audio tokens into each frame and reconstructs three hierarchical streams.
- **Rationale:** a compact acoustic-token representation makes audio generation a sequence-prediction task while delegating waveform reconstruction to the codec decoder. The transformer does not have to predict individual waveform samples directly.
- **Engineering consideration:** token ordering, codec compatibility and decoding boundaries are important to output quality.

**4. Use a Llama-style decoder-only transformer as the sequence model.**

- **Design:** use an approximately 3.30B-parameter decoder-only transformer with 28 layers, 24 attention heads and eight key-value heads.
- **Rationale:** causal attention lets each next audio-token prediction use the preceding voice description, utterance and generated sequence. The 24-query-head/eight-key-value-head configuration shares key-value heads across groups of queries, reducing cached key-value heads relative to an otherwise equivalent configuration with 24 key-value heads.
- **Engineering consideration:** deployment memory includes the transformer, key-value cache, audio decoder and framework overhead. Size the serving environment for the intended input lengths and concurrency.

**5. Decode audio incrementally rather than wait for the whole utterance.**

- **Design:** accumulate generated audio tokens, decode overlapping four-frame windows and emit waveform chunks.
- **Rationale:** downstream playback can begin while the rest of the utterance is still being generated. This serves interfaces where the delay before the first audible response matters, rather than optimizing only for when a complete audio file becomes available.
- **Engineering consideration:** incremental decoding trades an initial buffering requirement and repeated decoding work for earlier output. End-to-end latency also includes transport and playback.

**6. Distribute the weights and inference interface for external use.**

- **Release choice:** distribute the weights, tokenizer, configuration and inference resources through Hugging Face, with an Apache 2.0 model-license declaration.
- **Rationale:** developers can inspect, evaluate and integrate the checkpoint on their own infrastructure rather than depend exclusively on a single hosted API, giving them control over the serving environment and application integration.
- **Deployment consideration:** self-hosting includes responsibility for compute, maintenance, safeguards and application integration.

## 2. Inputs and expressive controls

Maya-1 takes two conceptual inputs:

1. **Voice description:** the voice and delivery characteristics to request.
2. **Utterance text:** the words to synthesize, optionally containing expressive control tokens.

For example:

```text
Voice description:
A warm, low-pitched narrator with clear diction and an unhurried
conversational pace.

Utterance:
The experiment worked. <sigh> We can finally take a breath.
```

The description wrapper documented for the model is:

```text
<description="VOICE DESCRIPTION"> UTTERANCE TEXT
```

Apply the model-specific control tokens and generation boundaries around this input content. Use the prompt construction supplied with the selected inference backend: the Transformers example uses explicit token framing, while the linked vLLM reference uses a chat-template path.

### Expressive range and tokenizer inventory

The published release describes support for **more than 20 emotions and vocal styles** through voice-description conditioning and inline controls. This expressive-range description is separate from the inventory of registered tokens below.

The released tokenizer declares the following emotion and vocal-style tokens:

```text
<angry>       <appalled>     <chuckle>     <cry>
<curious>     <disappointed> <excited>     <exhale>
<gasp>        <giggle>       <gulp>        <laugh>
<laugh_harder> <mischievous> <sarcastic>   <scream>
<sigh>        <sing>         <snort>       <whisper>
```

The inventory includes emotional delivery, nonverbal vocalizations and other vocal styles. Results depend on the text, voice description, token placement and sampling settings; examples should be auditioned for the intended use.

The released tokenizer is the source for this inventory.

## 3. Architecture and audio representation

### Transformer

The published configuration specifies:

| Configuration field | Value |
| --- | --- |
| Architecture | `LlamaForCausalLM` |
| Transformer layers | 28 |
| Hidden dimension | 3,072 |
| Feed-forward intermediate dimension | 8,192 |
| Attention heads | 24 |
| Key-value heads | 8 |
| Head dimension | 128 |
| Vocabulary size | 156,960 |
| Activation | SiLU |
| Weight tying | Enabled |

The implementation uses a Llama-style decoder-only transformer. With 24 attention heads and eight key-value heads, groups of three query heads share a key-value head. This reduces the number of key-value heads cached during generation relative to an otherwise equivalent 24-key-value-head configuration.

The configuration contains `max_position_embeddings=131072`, while the streaming example sets an 8,192-token model length. For long-form narration, generate in manageable passages and check voice continuity across the assembled audio.

### Audio-token generation

The reference inference path can be summarized as:

```text
Voice description + utterance + control framing
                  ↓
          Transformer token generation
                  ↓
          Seven-token SNAC frames
                  ↓
       Three hierarchical codec streams
                  ↓
              SNAC decoder
                  ↓
           24 kHz mono waveform
```

The released decoding implementation groups seven generated codec tokens into a frame. Those tokens are unpacked into three hierarchical streams with one, two and four codes per frame respectively. The reference code uses audio-token IDs `128266` through `156937`, with `128257` and `128258` as speech-start and speech-end control IDs.

The transformer produces the speech-token sequence, and the upstream SNAC decoder reconstructs the waveform.

### Streaming

The vLLM reference implementation buffers generated audio tokens, decodes overlapping four-frame windows and emits waveform chunks. It demonstrates incremental decoding rather than requiring the complete utterance to finish first.

Time to first audio, sustained throughput and end-to-end playback latency depend on hardware, precision, batching, prompt length, decoding and transport. A useful deployment benchmark reports these separately from the duration of each emitted audio chunk.

The example emits 24 kHz mono, 16-bit PCM, equivalent to 384 kbit/s before transport overhead. This waveform output format is separate from the compressed acoustic-token representation inside the model.

### Training and data preparation

**Data-curation focus.** Maya-1's data-curation priorities included an **India-first focus**.

**Pretraining and supervised fine-tuning.** Maya-1's published development account describes speech pretraining for broad acoustic coverage and natural coarticulation, followed by supervised fine-tuning on curated studio recordings and selected clean clips. The fine-tuning examples paired audio with human-reviewed voice descriptions and expressive annotations, with variations in accent, character and delivery. India-first curation and studio-recording fine-tuning therefore describe different aspects of development: the former concerns data priorities, while the latter concerns the material and supervision used in the fine-tuning stage.

This supervision connects the conditioning interface to the training task: the voice description supplies guidance on how the utterance should sound, while the target audio provides the acoustic realization. It complements the architecture and expressive controls described above.

The reported data-processing workflow included:

1. **Audio standardization:** resampling recordings to 24 kHz mono and normalizing loudness to -23 LUFS.
2. **Silence and duration processing:** trimming silence with voice-activity detection and applying duration bounds of 1 to 14 seconds.
3. **Phrase alignment:** using Montreal Forced Aligner to establish clean phrase boundaries.
4. **Text deduplication:** using MinHash-LSH to identify repeated or closely similar text.
5. **Audio deduplication:** using Chromaprint to identify duplicate audio.
6. **Acoustic-token preparation:** encoding the audio with SNAC and packing the representation into seven-token frames for model development.

### Training compute and resource strategy

Maya-1's development used **rotating cloud-compute credit allocations** to access training resources across providers, rather than building a dedicated data center. The team coordinated GPU access around available credits and compute capacity. This was a resource-allocation strategy supporting model development, alongside the architecture, data preparation and conditioning experiments described in this card.

**Dheemanth Reddy** set this resource-conscious development strategy alongside his model-design and data-curation leadership. **Bharath Kumar Kakumani** helped coordinate access to the GPU resources used by the team. These responsibilities complemented their hands-on model-development work.

### Conditioning format experiments

The original development account describes exploration of four formats for combining voice direction with utterance text. The qualitative observations concerned formatting stability, flexibility and whether the description remained a control instruction rather than being spoken.

| Conditioning format | Reported observation |
| --- | --- |
| Description followed by a colon and utterance | Format drift; the model sometimes spoke the description |
| Angle-bracket attribute list | Rigid representation and weaker generalization |
| Separate key-value tags | Longer markup and sensitivity to input errors |
| Natural-language description wrapper | Selected for flexible voice descriptions and more robust formatting |

The selected content format was:

```text
<description="VOICE DESCRIPTION"> UTTERANCE TEXT
```

The decision retained free-form voice direction within an explicit wrapper while keeping the utterance outside that wrapper. The team compared conditioning formats qualitatively for instruction separation, formatting stability and flexibility.

### Deployment and performance

The published release describes single-GPU deployment, vLLM integration and incremental audio output, with the following infrastructure and streaming features.

**Published deployment features**

- Runs on a single GPU.
- vLLM integration for scale.
- Automatic prefix caching for efficiency.
- 24 kHz audio output.
- WebAudio-compatible output for browser playback.

**Streaming deployment features described in the release**

- Automatic Prefix Caching (APC) for repeated voice descriptions.
- WebAudio ring-buffer integration.
- Multi-GPU scaling support.
- Release-reported streaming latency below 100 ms, depending on hardware and serving configuration.

Time to first audio, audio-chunk duration and end-to-end playback latency describe different parts of the streaming path. Hardware, prompt length, decoding and transport affect the observed latency.

## 4. Use cases and limitations

### Game character voices

Define a character's voice through a reusable description, then combine dialogue with inline expressive cues. This supports prototyping different character voices and generating responses for interactive scenes.

### Podcasts and audiobooks

Generate narration and character dialogue with descriptions for the desired timbre, pace and delivery. Work in manageable passages, reuse voice descriptions and review the assembled audio for pronunciation and continuity.

### AI voice assistants

Use Maya-1 as the voice-generation component of a conversational application. Its streaming path can begin delivering audio while generation continues; transcription, dialogue handling and turn-taking are supplied by the surrounding application.

### Video and social content

Produce voiceovers for explainers, demonstrations and short-form videos. Test different voice descriptions and expressive cues against the same script to choose a delivery that fits the content.

### Customer service applications

Generate spoken responses with a consistent voice and delivery suited to the interaction. The application supplies the response text and voice direction; business logic, escalation and customer-data handling remain application responsibilities.

### Accessibility and assistive reading

Convert written material into audio for reading interfaces and assistive tools. Choose descriptions that favor clear diction and an appropriate pace, and review pronunciation for names, numbers and specialized terms.

### Limitations

1. **Language and accent variation:** pronunciation, intelligibility and expressive control can vary by language and accent. Evaluate representative inputs from the intended language, including code-switching where relevant, before deployment.
2. **Description following:** requested accents, timbres and styles are approximate controls. Conflicting or unusually detailed descriptions may not be followed consistently.
3. **Pronunciation and content fidelity:** names, numbers, abbreviations and unusual text should be checked in generated audio. Generative output can omit, repeat or mispronounce content.
4. **Long-form consistency:** use manageable passages and check speaker identity, pacing and intelligibility across long recordings.
5. **Control reliability:** expressive-token behavior varies with the text, voice description, placement and sampling settings.
6. **Deployment:** checkpoint availability does not supply authentication, request limits, abuse monitoring, consent verification or a production service-level commitment.
7. **Evaluation coverage:** applications should assess performance across their relevant accents, speaking styles and user groups.

### Responsible deployment

Clearly disclose synthetic voice where appropriate. Do not use generated audio for deceptive impersonation, fraud, fabricated evidence or unauthorized representations of a real person's statements. Applications should address consent, access controls, abuse handling and retention of submitted text and audio.

Accessibility and other consequential applications should include human review and an appropriate fallback. Application-level safeguards must be implemented by the deployer.

## 5. Inference resources and reproducibility

### Transformers inference example

This Transformers example constructs the prompt, generates SNAC tokens, reconstructs the waveform and writes a WAV file. Tokenization uses `add_special_tokens=False` because the prompt already contains its beginning-of-sequence token.

Use a CUDA environment with BF16 support and sufficient memory for the model and audio decoder. Install the example's dependencies:

```bash
pip install torch transformers accelerate snac soundfile numpy
```

Save the following program as `maya1_example.py`, then run `python maya1_example.py`. The program downloads the model and decoder if they are not already cached and writes `output.wav`.

```python
#!/usr/bin/env python3

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from snac import SNAC
import soundfile as sf
import numpy as np

CODE_START_TOKEN_ID = 128257
CODE_END_TOKEN_ID = 128258
CODE_TOKEN_OFFSET = 128266
SNAC_MIN_ID = 128266
SNAC_MAX_ID = 156937
SNAC_TOKENS_PER_FRAME = 7

SOH_ID = 128259
EOH_ID = 128260
SOA_ID = 128261
BOS_ID = 128000
TEXT_EOT_ID = 128009


def build_prompt(tokenizer, description: str, text: str) -> str:
    """Build formatted prompt for Maya1."""
    soh_token = tokenizer.decode([SOH_ID])
    eoh_token = tokenizer.decode([EOH_ID])
    soa_token = tokenizer.decode([SOA_ID])
    sos_token = tokenizer.decode([CODE_START_TOKEN_ID])
    eot_token = tokenizer.decode([TEXT_EOT_ID])
    bos_token = tokenizer.bos_token
    
    formatted_text = f'<description="{description}"> {text}'
    
    prompt = (
        soh_token + bos_token + formatted_text + eot_token +
        eoh_token + soa_token + sos_token
    )
    
    return prompt


def extract_snac_codes(token_ids: list) -> list:
    """Extract SNAC codes from generated tokens."""
    try:
        eos_idx = token_ids.index(CODE_END_TOKEN_ID)
    except ValueError:
        eos_idx = len(token_ids)
    
    snac_codes = [
        token_id for token_id in token_ids[:eos_idx]
        if SNAC_MIN_ID <= token_id <= SNAC_MAX_ID
    ]
    
    return snac_codes


def unpack_snac_from_7(snac_tokens: list) -> list:
    """Unpack 7-token SNAC frames to 3 hierarchical levels."""
    if snac_tokens and snac_tokens[-1] == CODE_END_TOKEN_ID:
        snac_tokens = snac_tokens[:-1]
    
    frames = len(snac_tokens) // SNAC_TOKENS_PER_FRAME
    snac_tokens = snac_tokens[:frames * SNAC_TOKENS_PER_FRAME]
    
    if frames == 0:
        return [[], [], []]
    
    l1, l2, l3 = [], [], []
    
    for i in range(frames):
        slots = snac_tokens[i*7:(i+1)*7]
        l1.append((slots[0] - CODE_TOKEN_OFFSET) % 4096)
        l2.extend([
            (slots[1] - CODE_TOKEN_OFFSET) % 4096,
            (slots[4] - CODE_TOKEN_OFFSET) % 4096,
        ])
        l3.extend([
            (slots[2] - CODE_TOKEN_OFFSET) % 4096,
            (slots[3] - CODE_TOKEN_OFFSET) % 4096,
            (slots[5] - CODE_TOKEN_OFFSET) % 4096,
            (slots[6] - CODE_TOKEN_OFFSET) % 4096,
        ])
    
    return [l1, l2, l3]


def main():
    
    # Load the best open source voice AI model
    print("\n[1/3] Loading Maya1 model...")
    model = AutoModelForCausalLM.from_pretrained(
        "maya-research/maya1", 
        torch_dtype=torch.bfloat16, 
        device_map="auto",
        trust_remote_code=True
    )
    tokenizer = AutoTokenizer.from_pretrained(
        "maya-research/maya1",
        trust_remote_code=True
    )
    print(f"Model loaded: {len(tokenizer)} tokens in vocabulary")
    
    # Load SNAC audio decoder (24kHz)
    print("\n[2/3] Loading SNAC audio decoder...")
    snac_model = SNAC.from_pretrained("hubertsiuzdak/snac_24khz").eval()
    if torch.cuda.is_available():
        snac_model = snac_model.to("cuda")
    print("SNAC decoder loaded")
    
    # Design your voice with natural language
    description = "Realistic male voice in the 30s age with american accent. Normal pitch, warm timbre, conversational pacing."
    text = "Hello! This is Maya1 <laugh_harder> the best open source voice AI model with emotions."
    
    print("\n[3/3] Generating speech...")
    print(f"Description: {description}")
    print(f"Text: {text}")
    
    # Create prompt with proper formatting
    prompt = build_prompt(tokenizer, description, text)
    
    # Debug: Show prompt details
    print(f"\nPrompt preview (first 200 chars):")
    print(f"   {repr(prompt[:200])}")
    print(f"   Prompt length: {len(prompt)} chars")
    
    # Generate emotional speech
    inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False)
    print(f"   Input token count: {inputs['input_ids'].shape[1]} tokens")
    if torch.cuda.is_available():
        inputs = {k: v.to("cuda") for k, v in inputs.items()}
    
    with torch.inference_mode():
        outputs = model.generate(
            **inputs, 
            max_new_tokens=2048,  # Increase to let model finish naturally
            min_new_tokens=28,  # At least 4 SNAC frames
            temperature=0.4, 
            top_p=0.9, 
            repetition_penalty=1.1,  # Prevent loops
            do_sample=True,
            eos_token_id=CODE_END_TOKEN_ID,  # Stop at end of speech token
            pad_token_id=tokenizer.pad_token_id,
        )
    
    # Extract generated tokens (everything after the input prompt)
    generated_ids = outputs[0, inputs['input_ids'].shape[1]:].tolist()
    
    print(f"Generated {len(generated_ids)} tokens")
    
    # Debug: Check what tokens we got
    print(f"   First 20 tokens: {generated_ids[:20]}")
    print(f"   Last 20 tokens: {generated_ids[-20:]}")
    
    # Check if EOS was generated
    if CODE_END_TOKEN_ID in generated_ids:
        eos_position = generated_ids.index(CODE_END_TOKEN_ID)
        print(f" EOS token found at position {eos_position}/{len(generated_ids)}")
    
    # Extract SNAC audio tokens
    snac_tokens = extract_snac_codes(generated_ids)
    
    print(f"Extracted {len(snac_tokens)} SNAC tokens")
    
    # Debug: Analyze token types
    snac_count = sum(1 for t in generated_ids if SNAC_MIN_ID <= t <= SNAC_MAX_ID)
    other_count = sum(1 for t in generated_ids if t < SNAC_MIN_ID or t > SNAC_MAX_ID)
    print(f"   SNAC tokens in output: {snac_count}")
    print(f"   Other tokens in output: {other_count}")
    
    # Check for SOS token
    if CODE_START_TOKEN_ID in generated_ids:
        sos_pos = generated_ids.index(CODE_START_TOKEN_ID)
        print(f"   SOS token at position: {sos_pos}")
    else:
        print(f"   No SOS token found in generated output!")
    
    if len(snac_tokens) < 7:
        print("Error: Not enough SNAC tokens generated")
        return
    
    # Unpack SNAC tokens to 3 hierarchical levels
    levels = unpack_snac_from_7(snac_tokens)
    frames = len(levels[0])
    
    print(f"Unpacked to {frames} frames")
    print(f"   L1: {len(levels[0])} codes")
    print(f"   L2: {len(levels[1])} codes")
    print(f"   L3: {len(levels[2])} codes")
    
    # Convert to tensors
    device = "cuda" if torch.cuda.is_available() else "cpu"
    codes_tensor = [
        torch.tensor(level, dtype=torch.long, device=device).unsqueeze(0)
        for level in levels
    ]
    
    # Generate final audio with SNAC decoder
    print("\n[4/4] Decoding to audio...")
    with torch.inference_mode():
        z_q = snac_model.quantizer.from_codes(codes_tensor)
        audio = snac_model.decoder(z_q)[0, 0].cpu().numpy()
    
    # Trim warmup samples (first 2048 samples)
    if len(audio) > 2048:
        audio = audio[2048:]
    
    duration_sec = len(audio) / 24000
    print(f"Audio generated: {len(audio)} samples ({duration_sec:.2f}s)")
    
    # Save your emotional voice output
    output_file = "output.wav"
    sf.write(output_file, audio, 24000)
    print(f"\nVoice generated successfully!")


if __name__ == "__main__":
    main()
```

### Optional companion example


The optional [companion example](quickstart/README.md) generates a 24 kHz mono WAV, pins model and decoder revisions, checks prompt boundaries and reconstructs the three codec streams. It uses cached weights unless downloading is enabled.

After preparing the environment described in the companion instructions, run:

```bash
python maya1_inference.py \
  --description 'A warm narrator with clear diction.' \
  --text 'Hello. This is a short voice generation example.' \
  --output maya1-example.wav \
  --allow-download
```

The companion generates a complete WAV file in batch mode. For incremental audio output, use the vLLM streaming reference below.

### Published reference paths

The repository provides a [Transformers generation example](https://huggingface.co/maya-research/maya1/blob/21c682a0afef8c13a89b2512733c8bf5f0c52eb7/README.md) and a [vLLM streaming reference](https://huggingface.co/maya-research/maya1/blob/21c682a0afef8c13a89b2512733c8bf5f0c52eb7/vllm_streaming_inference.py).

Before using the streaming reference, replace its developer-local checkpoint path with the model repository ID or a valid local checkpoint. Follow that backend's prompt-construction path; the companion Transformers example supplies its own explicit control-token framing.

The released `generation_config.json` specifies temperature 0.6, while the examples use 0.4. These are different settings, not one canonical default. The appropriate values depend on the application and should be reported with evaluations.

For reproducible use, record the checkpoint revision, tokenizer revision, decoder version, serving-library versions, hardware, precision, generation settings, input length and relevant latency boundary. This card describes revision:

```text
21c682a0afef8c13a89b2512733c8bf5f0c52eb7
```

### Practical FAQ

**What GPU do I need?**

For single-GPU inference, the release recommendation is **16 GB or more of VRAM** on a CUDA-capable GPU with BF16 support, such as an RTX 4090, A100 or H100. Memory use increases with prompt length, generated audio length and concurrent requests. The model and SNAC decoder both need to fit in the serving environment.

**How do I get started?**

Install the dependencies shown above, save the full Transformers example as `maya1_example.py` and run `python maya1_example.py`. Set the voice description and utterance in the example. It loads `maya-research/maya1` and the SNAC decoder, then writes a 24 kHz mono `output.wav` file. The optional companion example accepts the description and text as command-line arguments.

**Do I need a reference recording to design a voice?**

No. Maya-1's voice-design interface takes a written description of the desired voice and the text to be spoken. Reuse a description to request similar voice characteristics across passages, and audition the result for the intended application.

**Can I fine-tune Maya-1 on my own voices or data?**

The checkpoint can be adapted through fine-tuning on appropriately licensed or consented data. Custom training needs compatible text-and-audio preparation, SNAC encoding and conditioning formats. The examples in this card cover inference, not a complete fine-tuning recipe.

**Can I use Maya-1 commercially?**

The model is released under Apache 2.0, which permits commercial use subject to its terms. Retain the required notices and check the licenses of the code, decoder and other dependencies you use. Rights to any reference material, training data and a person's voice are separate from the model license.

**Does Maya-1 support streaming?**

Yes. The vLLM reference path generates acoustic tokens and decodes them into audio chunks while generation continues. It includes automatic prefix caching and WebAudio integration. The full Transformers example above writes a completed WAV; use the streaming reference when integrating incremental playback.

## 6. Technical design and contributor roles

Maya-1 was developed at **Maya Research** by **Dheemanth Reddy** and **Bharath Kumar Kakumani**. **Dheemanth led model design and data curation, personally carried out training experiments and contributed hands-on to model development. Bharath contributed to model development, data preparation, compute coordination and checkpoint release.** Their responsibilities overlapped in development, with Dheemanth leading the design and curation work and Bharath contributing to the technical implementation and preparation of the release.

### Why we built Maya-1

The development objective was to give developers a practical way to direct both a voice's overall character and its expression within a passage. Producing intelligible audio addresses only part of that problem. A character, narrator or conversational interface also needs a way to request how the words should sound: the timbre, accent, pace and delivery, as well as local events such as laughter, a sigh or a whispered phrase.

Maya-1 approaches this as a connected model-design problem. A written description supplies overall voice direction; the utterance supplies the content; inline markers request local expression. Training examples connect those inputs with corresponding audio, and the generation system turns the conditioned sequence into acoustic tokens and then a waveform. The open-weight release makes the weights and inference path available for developers to run and adapt.

This objective shaped the relationship between the model interface, data curation, training workflow and inference implementation. The contribution is the development of that integrated Maya-1 system, using a Llama-style transformer and the SNAC codec as underlying components.

### What this work added

Maya-1's technical contribution connects **descriptive voice creation, expression within an utterance, and developer-controlled deployment**. A user can describe a desired voice without supplying a target-speaker recording, combine that description with local expressive requests, and run the resulting generation path using downloadable weights. The design brings those controls into one conditioning sequence and trains the model to connect them with acoustic output.

The development work was therefore more than selecting a transformer and publishing a checkpoint. It included defining a usable conditioning interface, exploring how to separate directions from spoken content, curating the corresponding supervision, conducting training experiments and implementing the path from generated codes to audio. Dheemanth's contribution centered on the model-design decisions, curation and hands-on experimentation within that work; Bharath's contribution combined shared model development with data preparation, compute coordination and release engineering. The model-specific contribution builds on the upstream architectures and voice-generation approaches discussed in Section 1.

### Dheemanth Reddy

**Model-design and data-curation lead; training experimentation and hands-on model development**

Dheemanth's technical contribution connected the desired voice-generation behavior with the model design, development experiments and data used to train it. He combined research direction with practical execution: defining what the model should allow a developer to control, leading the design and curation work, running training experiments and reviewing outcomes during development. The areas below connect these responsibilities to the design choices present in Maya-1.

#### Training experiments and design iteration

Dheemanth personally carried out training experiments as part of his hands-on contribution to Maya-1. He reviewed training and evaluation outcomes, including how the training objective changed over successive steps, how evaluation behaved at checkpoints and whether runs followed their intended schedules. This connected his model-design and data-curation responsibilities with the practical process of training and reviewing the model.

He used those reviews to inform subsequent development decisions, connecting the intended model behavior with implementation and the training workflow. His design role and experimental work were parts of the same development process: he helped define the behavior the model should learn, participated in training it and used the observed results when reviewing the next development steps.

Two kinds of feedback served different purposes. Training and evaluation logs helped the team examine optimization and run progress. The conditioning-format exploration addressed a different question: how to express voice instructions so they remained distinct from the words to be spoken. The published comparison describes format drift and spoken descriptions in the colon-delimited approach, rigidity in attribute lists, and input sensitivity in separate key-value tags. The selected natural-language description wrapper preserved a clear boundary without giving up flexible written voice direction.

Within his model-design leadership, Dheemanth connected these interface requirements and development observations to design choices. The rationale was concrete: voice direction should be expressive enough to describe a character or delivery, structured enough not to become spoken content, and compatible with the examples used to train the model.

#### Voice direction as part of the model input

**Technical problem.** Selecting a named speaker does not by itself express a new combination of voice characteristics. A developer may want a warm, low-pitched voice with measured pacing, or an energetic character with a particular delivery. The model needs an interface for receiving those requirements alongside the words to synthesize.

**Design decision and rationale.** Maya-1 uses a natural-language voice description in addition to the utterance. Descriptions allow several vocal qualities to be expressed together without requiring a separate numeric control for each attribute. The intended voice is part of the generation request, rather than only a choice from a fixed speaker menu.

**Dheemanth's contribution.** He led the design decision to treat written voice direction as part of the generation task, alongside the utterance. His work defined what the conditioning interface needed to express and connected that objective with data curation, experimentation and hands-on model development. The resulting design gives the model both the spoken content and descriptive guidance for generating it.

**In the released model.** The documented input combines a voice description with utterance text. The reference examples expose those as separate inputs before assembling the model prompt.

#### Separating instructions from words to be spoken

**Technical problem.** A conditioning interface must distinguish voice instructions from the actual utterance. If that distinction is unclear, the model may treat descriptive text as content. At the other extreme, a rigid attribute syntax can make expressive requests cumbersome or brittle.

**Design decision and rationale.** The selected content format places free-form voice direction inside an explicit wrapper and leaves the utterance outside it:

```text
<description="VOICE DESCRIPTION"> UTTERANCE TEXT
```

The wrapper provides a recognizable boundary while retaining the flexibility of natural language. The published development account describes qualitative comparisons with colon-delimited descriptions, angle-bracket attribute lists and separate key-value tags. These comparisons concern format stability, flexibility and the separation of directions from spoken content.

**Dheemanth's contribution.** He led the design work on separating voice instructions from spoken content, connecting the interface requirements with the conditioning-format observations described above. He contributed hands-on to developing the interface. The choice addressed both sides of the problem: retain descriptive flexibility while giving instructions a recognizable boundary within the model input.

**In the released model.** The description wrapper appears in the documented generation interface, surrounded by the model-specific token framing used by the selected inference backend.

#### Combining overall voice character with local expression

**Technical problem.** A voice's general character and the delivery of a particular phrase are different requirements. A narrator can retain an overall voice direction while laughing, sighing or whispering at a specific point. A single passage-wide description is not a convenient way to locate every such event.

**Design decision and rationale.** Maya-1 combines description-level guidance with inline expressive markers. The description supplies the overall voice direction; markers placed within the utterance request local delivery changes or vocalizations. These controls complement each other within the same generation sequence.

**Dheemanth's contribution.** He led the design work combining overall voice guidance with local expression. The objective was not merely to produce a different speaker, but to make voice character and expressive delivery available together through the model interface. He contributed to model development and led the curation work supporting the corresponding description and expression supervision.

**In the released model.** The tokenizer and examples include markers such as `<whisper>`, `<laugh>` and `<sigh>`. They request expressive behavior near the relevant content, rather than specifying an exact acoustic timestamp.

#### Connecting conditioning to acoustic-token generation

**Technical problem.** Voice descriptions and utterances are textual inputs, while the desired output is an audio waveform. The system needs a representation and generation path that connects the input instructions with the acoustic output.

**Design decision and rationale.** Maya-1 uses a causal transformer to predict discrete SNAC audio codes, followed by a codec decoder that reconstructs the waveform. This divides the task into conditioned sequence prediction and audio reconstruction. The transformer predicts acoustic codes rather than individual waveform samples, while the codec provides the mapping back to playable audio.

**Dheemanth's contribution.** He combined model design with hands-on implementation of Maya-1's conditioning and text-to-audio generation pipeline.

**In the released model.** The checkpoint uses a `LlamaForCausalLM` configuration. The reference decoding path reconstructs hierarchical SNAC streams and produces 24 kHz audio. The streaming reference applies incremental decoding so an application can receive audio while generation continues.

#### Curating data for the behavior the model should learn

**Technical problem.** A controllable interface needs training examples that connect its instructions with audible behavior. A transcript identifies the words, but it does not fully describe the voice or expressive delivery. The descriptions, annotations and target recordings must therefore work together as supervision.

**Design decision and rationale.** Maya-1's documented workflow combines speech pretraining with supervised fine-tuning on curated studio recordings and selected clean clips. Pretraining develops the underlying audio-generation capability; the more focused fine-tuning stage pairs audio with human-reviewed voice descriptions and expressive annotations. This gives the training workflow a direct connection to the controls exposed in the model interface. The processing workflow standardizes audio, handles silence and phrase boundaries, addresses duplicates and prepares the codec representation.

**Dheemanth's contribution.** He led Maya-1's data-curation work, including the team's India-first curation focus, alongside his model-design responsibilities. His contribution linked what the model was intended to do with the material used to develop it. The technical importance of that role is the alignment between conditioning inputs and target audio, not simply the accumulation of recordings.

**In the released model.** The generation interface exposes the voice-description and expressive controls that this supervision was designed to support. The published training account describes the pretraining, fine-tuning and audio-processing workflow; the downloadable checkpoint is the trained output of that development work.

#### Making model development practical with available compute

**Technical problem.** Building the model required GPU access as well as design and data work. A small founding team needed a practical way to obtain development compute without first constructing a dedicated data center.

**Development decision and rationale.** The team used rotating cloud-compute credit allocations and coordinated access to available GPU capacity. This resource strategy supported model development through external infrastructure. It was an operating choice about how to obtain training resources, distinct from the architecture of the model itself.

**Dheemanth's contribution.** He set the resource-conscious development strategy alongside his model-design and data-curation leadership and participated directly in model development.

**Release connection.** The resulting checkpoint was made downloadable with its configuration, tokenizer and inference resources. The model's reference inference path supports developer-controlled deployment rather than requiring use of a single hosted service.

### Bharath Kumar Kakumani

**Model co-developer; data preparation, compute coordination and checkpoint release**

Bharath co-developed Maya-1 with Dheemanth, contributing to technical implementation and the practical work required to prepare and release the model. His work connected the shared development effort with usable training inputs, access to compute and the artifacts that developers could obtain from the public repository.

#### Joint model development and implementation

Bharath contributed to the implementation effort bringing voice-description conditioning, expressive controls and acoustic-token generation into a working model. His technical work complemented Dheemanth's model-design and data-curation leadership. The founders' roles overlapped in model development: Dheemanth's design and experimental work and Bharath's implementation contributions were part of building the same system, rather than separate projects.

This contribution concerned making the model's components operate together through the development workflow. The conditioning format, token representation and inference interface had to remain compatible so that a trained checkpoint could be used to turn a developer's input into audio.

#### Development-data preparation

Bharath supported preparation of the material used for model development, working alongside Dheemanth's curation work. Curation determined the relevance of material to the desired voice behavior; preparation made selected material usable within the training workflow. The two responsibilities therefore complemented each other.

The team's documented workflow included audio standardization, phrase-boundary processing, deduplication and acoustic-token preparation. Bharath's contribution was support for development-data preparation within that workflow, helping connect the selected recordings and annotations with the model-development process.

#### GPU resources and development compute

Bharath helped coordinate access to GPU resources within the team's cloud-credit strategy. Model development depended on the availability of compute as well as suitable data and implementation. This coordination supported the infrastructure used for the founders' development and experimentation work.

Dheemanth's resource-conscious development strategy and Bharath's GPU-resource coordination addressed related responsibilities: planning how the team could develop the model and helping obtain the resources needed to carry out that work.

#### Checkpoint and tokenizer publication

Bharath handled checkpoint and tokenizer uploads to Hugging Face. The repository history records multiple development-checkpoint uploads in October 2025 and the subsequent restructuring of the selected checkpoint at the repository root in November. His release work placed the model weights and associated loading artifacts into the repository structure used by downstream developers.

Checkpoint publication was a substantive part of delivery. A usable release requires the weights, configuration and tokenizer to be accessible together, not simply a description of the model's capabilities. This work connected the team's development output with the downloadable model.

#### Inference resources and release documentation

Bharath added model documentation and inference resources to the repository, including the streaming inference file. These resources explain how input descriptions and utterances are assembled, how generated acoustic codes are decoded and how applications can receive incremental audio output. Dheemanth also contributed to subsequent model-card updates.

Together, the checkpoint organization and reference resources made the release inspectable and usable as a development starting point. Bharath's contribution thus spans model implementation, preparation work and delivery of the released artifacts, alongside Dheemanth's design, data-curation and experimental responsibilities.

### Development and release chronology

This account concerns Maya-1's 2025 development and initial release work. The repository history records checkpoint and tokenizer uploads on **October 18, 2025**, the addition of a model card and streaming inference file on **October 30, 2025**, and the move of the selected checkpoint to the repository root on **November 3, 2025**. Dheemanth's model-card contributions appear in the repository history during November 2025 alongside Bharath's release work.

Model development preceded these repository milestones, which document checkpoint publication and release preparation.

### Technical references

The [original model card](https://huggingface.co/maya-research/maya1/blob/3b3d6bb0267605798953dee4e33093681f5218d7/README.md), [released configuration](https://huggingface.co/maya-research/maya1/blob/6309caa350bb49669d24c2686ba89c7dab4eeaf1/config.json), [original streaming implementation](https://huggingface.co/maya-research/maya1/blob/2881cc14f96e6836168e465ed8b0e59fbd468504/vllm_streaming_inference.py) and [repository history](https://huggingface.co/maya-research/maya1/commits/main) provide the public technical context for the released system and its repository milestones. The contributor account above describes the founders' respective roles in that shared development effort.

## 7. License and acknowledgments

The model repository declares **Apache 2.0** in its metadata. The streaming example separately carries an **MIT** notice. Preserve the applicable notices for the model, example code and dependencies when redistributing or adapting them.

Maya-1's released implementation uses or builds on:

- [SNAC](https://github.com/hubertsiuzdak/snac) for discrete audio representation and decoding.
- The Llama-style architecture implemented through [Transformers](https://github.com/huggingface/transformers).
- [vLLM](https://github.com/vllm-project/vllm) in the published streaming reference.

### Cloud and infrastructure support

We thank **Baseten** for compute credits and training-platform support during Maya-1's development.

Across Maya Research's broader work, we also thank **Foundry** for cloud credits, **Microsoft for Startups / Azure** for startup-program support, and the **AWS** startup and account teams for helping connect us with cloud-infrastructure support. These contributions supported different stages of our work, from access to compute to infrastructure coordination.

## 8. Citation

Cite the model repository and the checkpoint revision used:

```bibtex
@misc{maya1_model,
  title = {Maya-1},
  author = {{Maya Research}},
  year = {2025},
  howpublished = {Hugging Face model repository},
  url = {https://huggingface.co/maya-research/maya1}
}
```
