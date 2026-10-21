---
language:
  - en
license: other
license_name: ltx-2-community
license_link: https://huggingface.co/ResembleAI/Dramabox/blob/main/LICENSE
pipeline_tag: text-to-speech
tags:
  - tts
  - voice-cloning
  - audio-generation
  - diffusion-transformer
  - flow-matching
  - ltx-2
library_name: ltx-audio-tts
base_model: Lightricks/LTX-2.3
base_model_relation: finetune
---

<p align="center">
  <a href="https://www.resemble.ai/learn/models/dramabox">
    <img src="https://huggingface.co/ResembleAI/Dramabox/resolve/main/assets/Dramabox.png" alt="DramaBox" width="720"/>
  </a>
</p>

# Dramabox — Expressive TTS with Voice Cloning

[![Discord](https://img.shields.io/discord/1377773249798344776?label=join%20discord&logo=discord&style=flat)](https://discord.gg/rJq9cRJBJ6)

> **Built on [LTX-2](https://github.com/Lightricks/LTX-2) by Lightricks.**
> Dramabox is **Resemble AI's** expressive TTS, trained on top of the LTX-2.3 audio branch under the LTX-2 Community License. Huge thanks to the Lightricks team for open-sourcing the base.

*Made with ♥️ by* <a href="https://www.resemble.ai/learn/models/dramabox" target="_blank"><img width="100" alt="resemble-logo-horizontal" src="https://github.com/user-attachments/assets/35cf756b-3506-4943-9c72-c05ddfa4e525" /></a>

Dramabox is a prompt-driven TTS where **the prompt itself controls everything** — speaker identity, emotion, delivery, laughs, sighs, breaths, pauses, transitions. An optional 10-second voice reference clones the target timbre. It is an IC-LoRA fine-tune of the **LTX-2.3 3.3B audio-only** model (Diffusion Transformer + flow matching), conditioned on Gemma 3 12B text embeddings.

| | |
|---|---|
| 🤗 Model | [`ResembleAI/Dramabox`](https://huggingface.co/ResembleAI/Dramabox) |
| 🎭 Demo Space | [`ResembleAI/Dramabox`](https://huggingface.co/spaces/ResembleAI/Dramabox) (ZeroGPU) |
| 💻 Code | [`resemble-ai/DramaBox`](https://github.com/resemble-ai/DramaBox) |
| 🏗️ Base model | [`Lightricks/LTX-2.3`](https://huggingface.co/Lightricks/LTX-2.3) |
| 📜 License | LTX-2 Community License — see [LICENSE](https://huggingface.co/ResembleAI/Dramabox/blob/main/LICENSE) |

## Quick start

### Python (warm server — recommended, ~2.5 s / generation)

```python
from src.inference_server import TTSServer

server = TTSServer(device="cuda")              # downloads weights on first run

server.generate_to_file(
    prompt='A woman speaks warmly, "Hello, how are you today?" '
           'She laughs, "Hahaha, it is so good to see you!"',
    output="output.wav",
    voice_ref="reference.wav",                  # optional, 10+ seconds of target voice
    cfg_scale=2.5,
    stg_scale=1.5,
    duration_multiplier=1.1,
    seed=42,
)
```

### CLI

```bash
python src/inference.py \
    --prompt 'A woman speaks warmly, "Hello, how are you today?"' \
    --voice-sample reference.wav \
    --output output.wav \
    --cfg-scale 2.5 --stg-scale 1.5
```

## Inference parameters

| Parameter | Default | What it does |
|---|---|---|
| `prompt` | — | The scene description. Dialogue inside `"double quotes"`, stage directions outside. See "Prompt format" below. |
| `voice_ref` (`--voice-sample`) | `None` | Optional 10+ s audio clip whose timbre the model clones. Without it, the model picks a voice that fits the description. |
| `cfg_scale` | 2.5 | Classifier-free guidance — how strictly the output follows the prompt. Lower = more natural, higher = more text-faithful but more dramatic. Auto-rescaled internally to prevent clipping at high cfg (see *Auto rescale* below). |
| `stg_scale` | 1.5 | Skip-token guidance — applied through the perturbed transformer block path (block 29). Increases expressive emphasis without saturating like cfg. |
| `duration_multiplier` (`--duration-multiplier`) | 1.1 | Multiplier on the auto-estimated speech length (10 % breathing-room headroom). Only used when `gen_duration` (or `--gen-duration`) is 0. |
| `gen_duration` (`--gen-duration`, "Target duration" slider) | 0 (auto) | Explicit output duration in seconds. Set to 20–60 s for music or long scenes. Overrides the prompt-based estimate when > 0. |
| `ref_duration` (`--ref-duration`, "Reference duration" slider) | 10.0 | How many seconds of the voice reference the model conditions on (3–30 s). Longer ref → richer timbre capture, shorter ref → faster encode. |
| `seed` | 42 | Reproducibility. |
| `rescale_scale` (`--rescale-scale`) | `"auto"` | Latent-side CFG std-rescale. The default is a cfg-aware schedule (0 below cfg=2, ramping to 1.0 by cfg=10) that keeps the output peak below 0 dBFS at every cfg. Pass any float in [0, 1] to override or 0 to disable. |
| `watermark` (`--no-watermark` to disable) | `True` | Apply [Resemble Perth](https://github.com/resemble-ai/Perth) imperceptible neural watermark to the output. Survives MP3/AAC, common edits; ≈ 100 % detection accuracy. |

## Prompt format

```
<speaker description>, "<dialogue>" <action direction> "<more dialogue>"
```

**Inside double quotes** — the model speaks these literally:
- Dialogue: `"Hello, how are you?"`
- Phonetic vocalisations (one word, no separators): `"Hahaha"`, `"Hehehe"`, `"Mmmmm"`, `"Ugh"`, `"Argh"`, `"Hmm"`

**Outside quotes** — stage directions interpreted as performance cues, never spoken:
- `She sighs deeply.` · `He clears his throat.` · `A long pause.` · `Her voice cracks.` · `He gulps nervously.`

**Avoid inside quotes** (the model will speak the word literally): `Sigh`, `Gasp`, `Cough`, `Ahem`, `Pfft`.

## Sample outputs

### Regal Queen — Cold Fury to Venomous Whisper

> A regal woman speaks with cold fury in a measured, low voice. She sighs deeply, "I have told you a thousand times, and yet here we are again." Her voice sharpens with rising anger, "Do you honestly think I enjoy repeating myself?! Do you?!" She lets out a cold, mocking laugh, "Hahaha, how utterly pathetic you are." She drops to a venomous whisper, leaning close, "Now get out of my sight before I do something we will both regret."

**Reference**
<audio controls src="https://storage.googleapis.com/resemble-sampletables/Apr16/efqN7-b6HWE/ltx-tts-eval/expressive/refs/01_queen_sighs_rage.wav"></audio>

**Generated**
<audio controls src="https://storage.googleapis.com/resemble-sampletables/Apr16/efqN7-b6HWE/ltx-tts-eval/expressive/generated/01_queen_sighs_rage.wav"></audio>

### Catgirl — Uncontrollable Giggling

> A playful girl speaks in a bright, singsong voice, already mid-giggle, "Hehehe, oh my gosh you should see your face right now, it is priceless!" She gasps for air between giggles, "Oh my, hehe, oh my, I cannot stop laughing!" She tries to compose herself with a long sigh, "Ahhhhh okay okay okay, I will stop, I promise I will stop." She leans in and whispers conspiratorially, "But seriously though, between you and me," then immediately loses it again, "Haha, no I, hehehe, I just cannot! You are way too funny, haha!" She snorts mid-laugh, "Pfft, oh no no no, that was so embarrassing, pretend you did not hear that!"

**Reference**
<audio controls src="https://storage.googleapis.com/resemble-sampletables/Apr16/efqN7-b6HWE/ltx-tts-eval/expressive/refs/04_catgirl_giggles_snort.wav"></audio>

**Generated**
<audio controls src="https://storage.googleapis.com/resemble-sampletables/Apr16/efqN7-b6HWE/ltx-tts-eval/expressive/generated/04_catgirl_giggles_snort.wav"></audio>

### Villain — Sinister Laugh

> A deep-voiced villain speaks with theatrical menace, chuckling softly at first, "Heh heh heh, ha ha ha ha ha! Oh, forgive me, forgive me." He catches his breath with a sinister grin, He clears his throat. "It is just SO amusing when they struggle, is it not?" His voice drips with contempt, "I expected more from you, truly I did. How disappointing." He leans in close and whispers with vicious intensity, "But fear not, my dear. The REAL entertainment has only just begun." He chuckles one last time, "Heh heh heh."

**Reference**
<audio controls src="https://storage.googleapis.com/resemble-sampletables/Apr16/efqN7-b6HWE/ltx-tts-eval/expressive/refs/09_villain_sinister_laugh.wav"></audio>

**Generated**
<audio controls src="https://storage.googleapis.com/resemble-sampletables/Apr16/efqN7-b6HWE/ltx-tts-eval/expressive/generated/09_villain_sinister_laugh.wav"></audio>

### Talk Show Host — Wheezing Laughter

> A talk show host speaks with animated enthusiasm. He gasps with exaggerated shock, "No! You did NOT just say that, tell me you did not just say that!" He bursts into uncontrollable laughter, "HAHAHA! Oh my god, oh my god!" He wheezes, barely getting words out, "I cannot, I literally cannot breathe right now!" He wipes his eyes, sniffling, "Oh that is so good, that is really genuinely good." He sighs happily, "Ahhh okay okay, let me compose myself, I am a professional." He takes one breath then immediately cracks up again, "Pfft hehehe, no I absolutely cannot, I am so sorry everybody!" He claps, "Folks, THIS, this right here, is why I love my job!"

**Reference**
<audio controls src="https://storage.googleapis.com/resemble-sampletables/Apr16/efqN7-b6HWE/ltx-tts-eval/expressive/refs/13_conan_wheezing_laughter.mp3"></audio>

**Generated**
<audio controls src="https://storage.googleapis.com/resemble-sampletables/Apr16/efqN7-b6HWE/ltx-tts-eval/expressive/generated/13_conan_wheezing_laughter.wav"></audio>

### Football Commentator — Martin Tyler

> Martin Tyler, a calm, authoritative English football commentator with a smooth, measured delivery, building tension gradually with precise timing and understated drama. "And here he comes… into the kitchen… opens the fridge…" he says evenly as a faint murmur of an imaginary crowd begins to rise. "You sense a moment here… the options are there…" his voice steady, observational. "Milk… eggs… leftovers… he considers them…" a slight pause, the crowd beginning to anticipate. "No… he moves past them…" a hint of intrigue enters his tone. "Now this is interesting…" The crowd grows, a low hum building behind the moment. "He's taking his time… weighing every option…" he continues calmly. A sudden hush falls. "Wait a moment… he's reaching…" The pause stretches—then— "He's got the juice!" his voice lifts, controlled but clearly excited. For a split second, silence—then the crowd detonates. "And listen to that! The place has absolutely erupted!" he says as roaring cheers, shouting, and thunderous applause fill the air. "They're on their feet—what a reaction to a moment of pure decision-making!" his voice rises just slightly above the chaos. The roar continues, echoing and relentless. "Extraordinary scenes… simply extraordinary…" he adds, letting the sound carry the moment. "And in the end… it's the juice that wins it…" he concludes as the crowd slowly begins to fade, still buzzing.

**Reference**
<audio controls src="https://storage.googleapis.com/resemble-sampletables/Apr24/mLbkPu2Qzwo/refs/002_ltx_tts_8ng372ra.wav"></audio>

**Generated**
<audio controls src="https://storage.googleapis.com/resemble-sampletables/Apr24/mLbkPu2Qzwo/generated/002_ltx_tts_8ng372ra.wav"></audio>

### Backstreet Boys — Pop Harmony

> Backstreet Boys, a polished late-90s boy band with five smooth, harmonizing male voices, blending in rich, emotional layers with clean pop production. "Step by step… out the door… new day… ready for more…" they sing in soft, synchronized harmony. One voice steps forward with a warm, heartfelt lead. "Keys in my hand… got my plan… heading out right on time…" The others swell behind him with lush backing vocals. "Don't be late… gotta move…" and then "city's calling my name…" Their voices rise together, smooth and uplifting. "Tell me why… every morning feels the same…" they sing with nostalgic warmth. Harmonies tighten with polished precision. "But I know… I'm on my way again…" and then "Coffee in my hand…" A brief pause, softer now. "I'm ready to go…" The full group returns in a bright, unified chorus. "We'll make it our way…" they sing with confident energy. "Through the rush, through the noise, we keep moving strong, yeah!" they finish with smooth, layered harmony and feel-good momentum.

**Reference**
<audio controls src="https://storage.googleapis.com/resemble-sampletables/Apr24/mLbkPu2Qzwo/refs/004_00_ltx_tts_ttop_woi.wav"></audio>

**Generated**
<audio controls src="https://storage.googleapis.com/resemble-sampletables/Apr24/mLbkPu2Qzwo/generated/004_00_ltx_tts_ttop_woi.wav"></audio>

## Files

| File | Size | Contents |
|---|---|---|
| `dramabox-dit-v1.safetensors` | 6.6 GB | Audio-only DiT (LoRA already merged into base) |
| `dramabox-audio-components.safetensors` | 1.9 GB | Audio embeddings connector + audio text projection + audio VAE + vocoder |
| [`unsloth/gemma-3-12b-it-bnb-4bit`](https://huggingface.co/unsloth/gemma-3-12b-it-bnb-4bit) | ~8 GB | Text encoder (auto-downloaded on first run) |

**VRAM**: ~24 GB peak, warm server. **Speed**: ~2.5 s / generation on H100 once warm.

## Watermarking

Every output of `inference.py` and `TTSServer.generate_to_file` is automatically watermarked with [Resemble Perth](https://github.com/resemble-ai/Perth) — an imperceptible neural watermark that survives MP3 compression, audio editing, and common manipulations while maintaining nearly 100 % detection accuracy.

```python
import perth, librosa
wav, sr = librosa.load("output.wav", sr=None, mono=True)
detector = perth.PerthImplicitWatermarker()
print(detector.get_watermark(wav, sample_rate=sr))   # ≈ 1.0 for our outputs
```

Pass `--no-watermark` (CLI) or `watermark=False` (Python) to disable for debugging.

## License & acknowledgement

Dramabox is a Resemble AI fine-tune of [LTX-2](https://github.com/Lightricks/LTX-2). Distributed under the LTX-2 Community License Agreement — see [LICENSE](https://huggingface.co/ResembleAI/Dramabox/blob/main/LICENSE). Thanks again to Lightricks for releasing the base model.
