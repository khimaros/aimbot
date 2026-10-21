---
language:
- da
license: cc-by-4.0
library_name: transformers
pipeline_tag: text-to-speech
base_model: syvai/plapre-nano-v2
---

# Plapre 3

Danish multi-task text-to-speech. **v3 is [plapre-nano-v2](https://huggingface.co/syvai/plapre-nano-v2)
further trained with reinforcement learning (GRPO)** to speak more intelligibly: same 335M
`LlamaForCausalLM`, same Kanade 25 Hz codec, same tokenizer, speaker projection and prompt formats.
It is a drop-in replacement for v2.

## What's new in v3

RL with [Edda v0.2](https://huggingface.co/danish-foundation-models/edda-v0.2) as the judge. The model
reads Danish radio-transcript sentences (from DR P1) in voices cut from P1 broadcasts, and is rewarded for
being transcribed correctly, sounding natural, matching the reference voice, keeping the reference
speaker's pace, and stopping cleanly.

Held-out evaluation: 48 sentences (half with numbers, names or long words) × 4 samples, in clone,
speaker-embedding and built-in-voice modes. The data was never used in training. **Røst-Whisper 1.5B was never part of the reward**,
so it measures intelligibility independently of the judge the model was trained against.

| metric | v2 | **v3** |
|---|---|---|
| Edda v0.2 CER ↓ | 3.81 % | **1.67 %** |
| Edda v0.2 WER ↓ | 7.14 % | **4.41 %** |
| [Røst-Whisper 1.5B](https://huggingface.co/CoRal-project/roest-v3-whisper-1.5b) WER ↓ (never optimised) | 7.94 % | **4.93 %** |
| [Røst wav2vec2 315M](https://huggingface.co/CoRal-project/roest-v3-wav2vec2-315m) WER ↓ | 17.2 % | **13.1 %** |
| clips with CER ≤ 2 % ↑ | 63.5 % | **76.0 %** |
| UTMOS (predicted naturalness) ↑ | 3.78 | **4.08** |
| speaker similarity (WavLM-SV) ↑ | 0.936 | **0.944** |
| clean stop rate | 100 % | 100 % |
| mean clip length | 4.63 s | 5.30 s |

v3 speaks about 15 % slower than v2. The pace reward aims for each reference speaker's own rate, so
this brings it closer to the reference voices rather than gaming the recogniser. Use the
**pace** control (`durations=`) if you want v2's tempo.

**Training:** GRPO, 1,275 steps × 64 rollouts (8 prompts × 8 samples), lr 1e-5, KL β = 0.02 to v2,
token-level policy gradient, sampling temperature 0.8. Prompt mix: ⅓ voice-clone, ⅓ speaker-embedding,
⅓ built-in voices; 60 % of sentences weighted toward hard text. Reward per sample:
`−2·CER(Edda) + 0.5·(UTMOS−3.5) + speaker_sim − pace_penalty − 1·[no stop token]`.
The checkpoint was chosen on held-out Edda CER, Røst WER and UTMOS together. Later checkpoints
began to overfit Edda (Edda CER flat while Røst WER rose), so they were not used.

## What it can do

Two **tasks**:

| task | in → out |
|---|---|
| **generate** | text → speech in a chosen voice |
| **edit** | an existing recording + new text → the same recording with words substituted, inserted or deleted; only the masked span is regenerated, the surrounding audio is untouched |

Four **controls** that stack onto generate:

| control | effect |
|---|---|
| **voice-reference (cloning)** | speak in the voice of a reference clip (audio + its transcript) |
| **context** | condition on the previous utterance (text + audio) so tone, energy and tempo continue naturally across turns |
| **pace** | per-word duration targets (40 ms frames) — set the speaking rate, or ramp it within a sentence |
| **pronunciation** | up to 10 (word, reference-audio) pairs that pin how names, loanwords or acronyms are pronounced |

### Combining them

Controls are composable — any subset stacks in one prompt, in this block order:

```
[SPK]  [pronunciation]  [voice-reference]  [context]  <text> BPE  [pace]  <audio> …
```

| combination | what you get |
|---|---|
| clone + pace | a cloned voice at a pace you set |
| clone + pronunciation | a cloned voice that says a name correctly |
| clone + context | a cloned voice continuing a conversation |
| context + pace | a conversational reply at a controlled tempo |
| clone + context + pace + pronunciation | all four at once |
| edit + pronunciation | regenerate a span so the corrected word is pronounced right |

Voice-reference is the only control that swaps the speaker embedding (to the
reference clip's); the others keep the target voice. Edit composes with
pronunciation only. All combinations are trained, not emergent.

## How to use it

The easiest path is the [plapre library](https://github.com/syv-ai/plapre),
which wraps every task and combination:

```python
from plapre import Plapre

tts = Plapre("syvai/plapre-nano-v3")

# plain TTS
tts.speak("Hej, hvordan har du det?", output="out.wav", split_sentences=True)

# clone a voice from any clip
tts.clone("Denne sætning har stemmen aldrig sagt.", reference_wav="voice.wav")

# cloned voice + set pace + pinned pronunciation, in one call
tts.clone(
    "Mette Frederiksen mødte Volodymyr Zelenskyj i København.",
    reference_wav="voice.wav",
    durations=[14, 22, 12, 24, 4, 18],              # one frame count per word
    pronunciations=[("Zelenskyj", "zelenskyj_ref.wav")],
)

# continue a conversation with matching prosody
tts.continue_context("Og det er derfor, vi handler nu.",
                     prev_text="Situationen har ændret sig markant.",
                     prev_wav="previous_line.wav", speaker_wav="voice.wav")

# edit a recording: replace words in place
tts.edit("… ny formulering her …", mask_start=40, mask_end=55,
         original_wav="clip.wav")
```

### Manual inference (transformers)

```python
import numpy as np, torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import hf_hub_download

CKPT = "syvai/plapre-nano-v3"
tok = AutoTokenizer.from_pretrained(CKPT)
m = AutoModelForCausalLM.from_pretrained(CKPT, torch_dtype=torch.float32).eval()
spj = torch.nn.Linear(128, m.config.hidden_size)
spj.load_state_dict(torch.load(hf_hub_download(CKPT, "speaker_proj.pt"), map_location="cpu"))
spj.eval()

g = tok.convert_tokens_to_ids
STOPS = [g("</audio>"), tok.eos_token_id]           # stop on BOTH terminators
pre = [g("<text>")] + tok.encode(text, add_special_tokens=False) + [g("<audio>")]

pe = m.get_input_embeddings()(torch.tensor(pre))
spk = spj(torch.tensor(np.asarray(speaker_embedding), dtype=torch.float32)).unsqueeze(0)
inp = torch.cat([spk, pe], 0).unsqueeze(0)
out = m.generate(inputs_embeds=inp,
                 attention_mask=torch.ones(inp.shape[:2], dtype=torch.long),
                 max_new_tokens=500, do_sample=True, temperature=0.7,
                 top_p=0.95, top_k=50, eos_token_id=STOPS,
                 pad_token_id=tok.eos_token_id)[0].tolist()
audio_base = g("<audio_0>")
content = []
for t in out:
    if audio_base <= t < audio_base + 12800:
        content.append(t - audio_base)
    elif content:
        break
# decode `content` with kanade_tokenizer (frothywater/kanade-25hz-clean) -> 24 kHz wav
```

Control-block prompt formats (reference audio caps, `<dur_j>` ids, edit
masking/splicing) are implemented in
[`plapre/tasks.py`](https://github.com/syv-ai/plapre/blob/main/plapre/tasks.py)
— pure token-layout builders you can read or reuse directly.

### Inference requirements

- **Stop on both terminators**: generated audio ends `</audio>` then `<eos>` —
  pass both ids as stop tokens (the library does this for you).
- **Run in fp32** (the training precision). Lower precision measurably
  increases end-of-utterance artifacts.
- **Use this repo's tokenizer** (vocab 21224).
- **End sentences with terminal punctuation** — append a "." if your text ends
  on a comma or nothing; the stop signal is strongest on sentence-final text.
- **Split long text into sentences** and generate them as a batch; join with
  ~250 ms of silence. Speaking pace follows the voice: reference clips from
  calm speakers yield calm narration.
- If serving with vLLM, use `vllm>=0.15,<0.16` with `enable_prompt_embeds=True`
  — newer stacks measurably degrade generation quality on identical weights.
- Text normalization: collapse whitespace and convert digits to Danish words
  (`num2words`, `lang="da"`) before encoding.

## Model details

| | |
|---|---|
| Architecture | 335M `LlamaForCausalLM` (SmolLM2 layout, hidden 960, 32 layers) + 128→960 speaker projection (`speaker_proj.pt`, unchanged from v2) |
| Audio codec | `frothywater/kanade-25hz-clean` — 25 Hz content codes, 24 kHz output |
| Vocab | 21224 = 8000 Danish BPE + 12800 `<audio_k>` + control tokens + terminators |
| Pre-training (v2) | ~1.5M sentence-aligned Danish speech segments (~2,800 h), 2 epochs, fp32 master weights |
| RL (v3) | GRPO against Edda v0.2 on streamed DR P1 text + voices, 1,275 steps, fp32 weights / bf16 autocast |

## Limitations

- Voice cloning transfers the broad character of a voice (timbre, pace,
  register), not a fine-grained identity — the speaker embedding is one vector
  per recording.
- Trained on a single speech domain; voices far outside it clone less
  faithfully.
- Sampling-based generation can occasionally mis-speak; for user-facing
  products, verify outputs with an ASR pass and resample on mismatch
  (a reference implementation ships with the plapre library's demo server).
- RL trained the **generate** and **voice-reference/clone** paths. Edit, context, pace and
  pronunciation were not in the RL prompt mix. A KL penalty kept the model close to v2, but those
  modes were not re-evaluated.
- Naturalness was measured with UTMOS, an English-trained predictor, not with Danish listeners.
