---
license: gpl-3.0
language: [en, ne, hi, vi, id, zh, de, fr, es, it, pt, ru, cs, ro, tr, ar, pl]
pipeline_tag: text-to-speech
tags: [text-to-speech, tiny, microcontroller, esp32, wasm, piper, distillation]
library_name: sanotts
---

# sanoTTS — a tiny neural voice that runs anywhere

**Release status: Ready for release.**

***sano*** (सानो) — Nepali for **"small."** A family of tiny neural
text-to-speech voices — **104k to 2.27M parameters** — that run with
**no cloud and no NPU**: real-time on a ~$3 ESP32-S3 (out a GPIO into an
LM386 and a speaker), or live in the browser via WASM.

## heart-nano: a whole English TTS in 201 k parameters

`heart-nano` is our smallest English voice: a 104,215-parameter streaming voice
plus a 96,511-parameter G2P model for words the dictionaries lack, **200,726
parameters from text to 24 kHz audio**, in NumPy on one CPU thread.

| # | Text | Sample |
| --- | --- | --- |
| 1 | Hello! I am heart nano, a whole English voice in about two hundred thousand parameters, small enough to run almost anywhere. | <audio controls src="https://huggingface.co/ampixa/sanoTTS/resolve/main/samples/english-heart-nano-201k-1.mp3"></audio> |
| 2 | The old lighthouse keeper climbed the spiral stairs every evening, lit the lamp, and watched the ships slip quietly past the rocks. | <audio controls src="https://huggingface.co/ampixa/sanoTTS/resolve/main/samples/english-heart-nano-201k-2.mp3"></audio> |
| 3 | Can you believe the train left at 7:05, two minutes early, with 312 passengers on board? | <audio controls src="https://huggingface.co/ampixa/sanoTTS/resolve/main/samples/english-heart-nano-201k-3.mp3"></audio> |
| 4 | Doctor Okonkwo flew from Reykjavik to Ouagadougou on Tuesday, then took the overnight bus to Timbuktu. | <audio controls src="https://huggingface.co/ampixa/sanoTTS/resolve/main/samples/english-heart-nano-201k-4.mp3"></audio> |

On the [Open TTS Leaderboard](https://huggingface.co/spaces/hf-audio/open_tts_leaderboard?streaming-cpu=)
it has the fastest time to first audio in the CPU streaming category: **2.1 ms p50 and 2.8 ms p95**,
with composite WER **0.92 %**, UTMOS **3.88** and RTFx 173. Those numbers are from the maintainers' run of
sanotts 0.5.7 ([PR #69](https://github.com/huggingface/open-tts-leaderboard/pull/69)). These clips are
0.5.8, the same voice with the smaller G2P model; see [below](#heart-nano-smaller-sanotts-058) for how they differ.

```bash
pip install sanotts
sanotts say "Hello from heart nano." --voice heart-nano -o hello.wav
```

![text in → ESP32 → speech out](https://raw.githubusercontent.com/Ampixa/sanoTTS/master/docs/assets/saanotts-mcu-hero.png)

| | |
| --- | --- |
| Parameter range | **104,215 – 2,272,145** |
| Runs real-time on a $3 microcontroller | ESP32-S3, out a GPIO into an LM386 |
| Runs in the browser | WebAssembly, no server |
| Per-voice footprint | **337 KB to 8.7 MB**, zero dependencies (espeak-ng phonemizer included) |
| Live browser demo | **31 voices** across **17 languages** — English, Nepali (नेपाली), Hindi (हिन्दी), Vietnamese (Tiếng Việt), Indonesian (Bahasa), Chinese (中文), German, French, Spanish, Italian, Portuguese, Russian, Czech, Romanian, Turkish, Arabic, and Polish |
| License | open source, **GPL-3.0** |

**Live demo:** [tts.ampixa.com/sanoTTS](https://tts.ampixa.com/sanoTTS) —
**31 voices across 17 languages**, synthesizing your text live in the browser, no server, no upload.

The count is the live demo's voice-picker inventory, including separate model sizes for the same language. **Polish is currently demo-only:** its weights are not yet hosted in this Hugging Face repository. The repository also retains the older Chinese voice for compatibility; the live picker uses its Chinese Xiaoya replacement.

## Download

Both packages stream their weights from **this repo** by default.

```python
import sanotts
sanotts.synthesize("Hello world", voice="heart-nano")  # downloads heartnano-f16/ from here
```

```js
import { SanoTTS } from 'sanotts-web';               // fetches web/voices/ from here
const tts = await SanoTTS.load();
const result = await tts.synthesize('Hello world', { voice: 'heart' });
```

Python needs `sanotts` >= 0.3.0, the browser `sanotts-web` >= 0.3.0. Both fall
back to the GitHub releases or the Pages host if Hugging Face cannot be
reached, so an outage here cannot break an install. Python packages land in
`~/.cache/sanotts/`; set `SANOTTS_VOICE_SOURCE=hf` or `=github` to pin one
host. In the browser, passing `voiceBase` yourself turns the fallback off, so
a self-hosted deployment never quietly reaches back to our servers.

## Samples

Selected samples are embedded below; this is not the full 31-voice demo inventory.
"Package here" links to a voice's Python/C package when available. Browser
bundles for Nepali, Hindi, and Chinese are also hosted here under `web/voices/`.
The older Chinese sample below is retained for compatibility; the live demo
uses [Chinese Xiaoya](https://huggingface.co/ampixa/sanoTTS/tree/main/web/voices/chinese-xiaoya).

The browser collection additionally includes German, French, Spanish, Italian,
Portuguese, Russian, Czech, Romanian, Turkish, Arabic, and the experimental
English Trellis voice. Browse the [browser bundles](https://huggingface.co/ampixa/sanoTTS/tree/main/web/voices)
and try all 31 voices, including demo-only Polish, in the [live demo](https://tts.ampixa.com/sanoTTS).

| Voice | Language | Params | SCOREQ | Package here | Sample |
| --- | --- | ---: | :---: | :---: | --- |
| heart-nano (streaming) | English 🇺🇸 | 104 k voice, 201 k with its G2P | — | [`heartnano-f16/`](https://huggingface.co/ampixa/sanoTTS/tree/main/heartnano-f16) | <audio controls src="https://huggingface.co/ampixa/sanoTTS/resolve/main/samples/english-heart-nano-201k-1.mp3"></audio> |
| heart | English 🇺🇸 | 2.27 M | 3.48 | [`heart/`](https://huggingface.co/ampixa/sanoTTS/tree/main/heart) | <audio controls src="https://huggingface.co/ampixa/sanoTTS/resolve/main/samples/english-heart-1.mp3"></audio> |
| hfc | English 🇺🇸 | 1.83 M | 3.94 | [`hfc-en-1p8m/`](https://huggingface.co/ampixa/sanoTTS/tree/main/hfc-en-1p8m) | <audio controls src="https://huggingface.co/ampixa/sanoTTS/resolve/main/samples/english-hfc-1.mp3"></audio> |
| amy | English 🇺🇸 | 1.46 M | **4.13** | [`amy-en-1p46m/`](https://huggingface.co/ampixa/sanoTTS/tree/main/amy-en-1p46m) | <audio controls src="https://huggingface.co/ampixa/sanoTTS/resolve/main/samples/english-amy-1.mp3"></audio> |
| Indonesian | Bahasa | 1.46 M | — | [`id-newstts-1p46m/`](https://huggingface.co/ampixa/sanoTTS/tree/main/id-newstts-1p46m) | <audio controls src="https://huggingface.co/ampixa/sanoTTS/resolve/main/samples/indonesian-1.mp3"></audio> |
| Vietnamese | Tiếng Việt | 1.46 M | — | [`vi-vais1000-1p46m/`](https://huggingface.co/ampixa/sanoTTS/tree/main/vi-vais1000-1p46m) | <audio controls src="https://huggingface.co/ampixa/sanoTTS/resolve/main/samples/vietnamese-1.mp3"></audio> |
| Nepali | नेपाली | 1.47 M | — | [browser bundle](https://huggingface.co/ampixa/sanoTTS/tree/main/web/voices/nepali) | <audio controls src="https://huggingface.co/ampixa/sanoTTS/resolve/main/samples/nepali-1.mp3"></audio> |
| Hindi | हिन्दी | 1.50 M | — | [browser bundle](https://huggingface.co/ampixa/sanoTTS/tree/main/web/voices/hindi) | <audio controls src="https://huggingface.co/ampixa/sanoTTS/resolve/main/samples/hindi-1.mp3"></audio> |
| Chinese | 中文 | 1.50 M | — | [browser bundle](https://huggingface.co/ampixa/sanoTTS/tree/main/web/voices/chinese) | <audio controls src="https://huggingface.co/ampixa/sanoTTS/resolve/main/samples/chinese-1.mp3"></audio> |

SCOREQ is a no-reference naturalness predictor, higher is better; it is only
reported for the English voices, which share one 24-sentence eval set. The
other languages haven't been scored against a comparable reference yet.

**Size does not order this table, and we are not going to pretend it does.**
`amy` at 1.46M scores higher than `heart` at 2.27M because they come from
different teachers and different architectures, not because one is bigger.
`amy` and the voices above it are the **piperlite** lineage, distilled from a
Piper/VITS teacher at 22.05 kHz. `heart` and `heart-nano` are the newer
**nano** lineage — 24 kHz, mel-100 → ConvNeXt1D → iSTFT, distilled from a
Kokoro teacher through a frozen Vocos — which is the one that quantizes to
int8 and runs on a microcontroller. The two are not interchangeable and the
`sanotts` package picks the right runtime for you.

The `heart` score was re-measured on 2026-09-04; the eval set, checkpoint
hashes, exact commands and all 24 per-clip scores are in
[`evidence/heart-diverse24-remeasure-20260904.json`](https://huggingface.co/ampixa/sanoTTS/blob/main/evidence/heart-diverse24-remeasure-20260904.json).
It was scored on the float32 reference render; `heart` ships as float32 because
its int8 export reached only 0.951 against a 0.98 gate. The same file scores the
first heart-nano (294 k, SCOREQ 2.29), which a streaming 263 k heart-nano
replaced on 2026-11-25 and the 104 k heart-nano on 2026-11-26; neither has a
SCOREQ measurement yet (their UTMOS and WER are below).


## Install & use

| Platform | Install | Then |
| --- | --- | --- |
| Python | `pip install sanotts` | `sanotts say "Hello" --voice heart -o hello.wav` |
| Web (npm) | `npm install sanotts-web` | `const tts = await SanoTTS.load(); await tts.synthesize('Hello', {voice:'heart'})` |
| Web (no build) | copy `dist/` + `voices/` | see [Deploy on your own site](https://github.com/Ampixa/sanoTTS#deploy-on-your-own-site) in the GitHub README |
| Arduino / PlatformIO | zip-install or `lib_deps = https://github.com/Ampixa/sanoTTS.git` | [`arduino/README.md`](https://github.com/Ampixa/sanoTTS/blob/master/arduino/README.md) |
| Hugging Face | this repo | the voice packages above, downloaded for you by `pip install sanotts` |
| Browser | nothing | [tts.ampixa.com/sanoTTS](https://tts.ampixa.com/sanoTTS) |

Pip voices: `heart`, `hfc`, `amy-1p8m`, `amy`, `kristin`, `vi`, `id`,
`amy-1p1m`, `heart-nano` (the streaming 104 k voice with a harmonic-plus-noise decoder; since sanotts 0.5.8 its decoder is stored in float16 and the English G2P model is 96 k, so the whole stack is 201 k; `heart-nano-s` is an alias). Pure numpy inference, no torch, no onnxruntime.

## Streaming and the Open TTS Leaderboard

`sanotts` streams: `Synthesizer.synthesize_stream(text)` yields audio chunk by
chunk, and the chunks join to exactly what `synthesize()` returns, up to
float32 rounding.

```python
from sanotts import Synthesizer
syn = Synthesizer("heart-nano")
for chunk in syn.synthesize_stream("Hello from a 104k-parameter voice."):
    ...  # float32 at syn.sample_rate, ready to play
```

The three English voices were evaluated by the maintainers of the
[Open TTS Leaderboard](https://huggingface.co/spaces/hf-audio/open_tts_leaderboard)
on HF Jobs: heart-nano and heart under sanotts 0.5.7
([PR #69](https://github.com/huggingface/open-tts-leaderboard/pull/69)), amy under 0.5.4
([PR #53](https://github.com/huggingface/open-tts-leaderboard/pull/53)).
Time to first audio is measured on CPU (`cpu-upgrade`, one thread, batch size 1)
over the 497 CV3-Eval English prompts; RTFx is the main eval's throughput, run
on one CPU thread. WER is from Qwen3-ASR over Seed-TTS, CV3-Eval and MiniMax English.

| Voice | Params | TTFA p50 | TTFA p95 | RTFx | WER | UTMOS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **heart-nano** | 104 k | **2.1 ms** | **2.8 ms** | 173 | 0.92 % | 3.88 |
| heart | 2.27 M | 4.3 ms | 6.3 ms | 131 | 0.91 % | 3.26 |
| amy | 1.46 M | 22.7 ms | 36.3 ms | 15 | 1.12 % | 3.99 |

On that board, larger and newer models score higher on UTMOS than these voices
do; what sanoTTS brings is the latency, the throughput and the size. Before PR #69
the heart-nano row was the first, 294 k model (TTFA p50 2.8 ms, p95 5.9 ms, WER 1.16 %,
UTMOS 2.36). Those WER and UTMOS figures are composites over Seed-TTS, CV3-Eval, MiniMax
and ZTTS2-mini English.

### heart-nano, smaller (sanotts 0.5.8)

0.5.8 keeps the 104 k voice and shrinks what ships with it. Folder `heartnano-f16/`:

| | 0.5.7 | 0.5.8 |
| --- | ---: | ---: |
| Voice parameters | 104,215 | 104,215 |
| Voice folder | 518 KB (`heartnano-dsp/`) | **187 KB** (`heartnano-f16/`) |
| English OOV G2P model | 751,551 params, 2.8 MB | **96,511 params, 212 KB** |
| Voice + G2P model | 855,766 | **200,726** |
| Wheel | 6.79 MB | **4.17 MB** |

- The decoder's weights are stored in float16 (computed in float32/64 as before),
  and the folder no longer carries the 0.5.6 neural decoder that 0.5.7 kept only for
  older installs.
- The OOV model only runs for words that are in neither pronunciation dictionary nor
  the table of 618,928 common words precomputed with the 751 k model, which stays in
  front of it: on CV3-Eval that was 38 of 7,274 words. The 96 k model is distilled from
  the 751 k one. It affects every English voice, not only heart-nano.
- Same 200 + 200 held-out Wikipedia sentences as the 0.5.7 selection (plain / with
  brackets, quotes and digits), rendered through the package, Qwen3-ASR WER and
  UTMOS22 strong:

| | held-out WER | heldsym WER | held-out UTMOS | heldsym UTMOS |
| --- | ---: | ---: | ---: | ---: |
| 0.5.7 | 2.75 % | 6.56 % | 3.86 | 3.92 |
| 0.5.8 | 3.07 % | 6.56 % | 3.86 | 3.91 |

  The held-out difference is about 8 of 2,450 words. 19 of the 200 sentences transcribe
  differently, and nearly all of those differences are on rare names and
  transliterations (Totleigh, Purohiths, Ghanashyam). CV3-Eval was not used for any
  0.5.8 choice and has not been re-run.
- TTFA on the same replica as below, three fresh processes each, both versions in the
  same session: 0.5.8 p50 1.59–1.60 ms, p95 1.85 ms, RTFx 190–192; 0.5.7 p50
  1.58–1.59 ms, p95 1.84–1.90 ms, RTFx 188–190. No change.
- Details: [`evidence/heart-nano-201k-20261126.json`](https://huggingface.co/ampixa/sanoTTS/blob/main/evidence/heart-nano-201k-20261126.json).

### heart-nano, streaming (sanotts 0.5.7)

The 0.5.7 `heart-nano` (folder `heartnano-dsp/`; `heart-nano-s` is still accepted
as an alias) has 104,215 parameters. Its front end is the streaming 263 k model's,
unchanged: int8 duration and acoustic models (56,981 parameters) that see only
nearby phonemes, so the first chunk is decoded from the first few words before the
rest of the text has been converted. Its decoder is new: a 47,234-parameter
harmonic-plus-noise decoder that runs in NumPy, distilled from the same Kokoro
af_heart teacher.

On our replica of the leaderboard's TTFA probe (CV3-Eval English, the harness's own
`Voice` loop, numpy 2.5.4, one BLAS thread pinned to one core of an i5-10400, three
fresh processes, cold pass each), and on CV3-Eval English WER (Qwen3-ASR,
leaderboard normaliser) and UTMOS (UTMOS22 strong):

| Voice | TTFA p50 | TTFA p95 | RTFx | CV3 WER | CV3 UTMOS |
| --- | ---: | ---: | ---: | ---: | ---: |
| first heart-nano, 294 k (0.5.5) | 1.61–1.66 ms | 2.93–3.00 ms | 228–231 | 1.57 % | 2.37 |
| heart-nano, 263 k (0.5.6) | 1.32–1.33 ms | 1.59 ms | 230–236 | 1.42 % | 2.52 |
| **heart-nano, 104 k (0.5.7)** | 1.61–1.67 ms | 1.89–2.01 ms | 182–189 | **1.15 %** | **3.88** |

The 104 k voice sounds much better and transcribes slightly better, and it is
slower: about 20 % less throughput and 0.3–0.4 ms more at p95 than the 263 k one,
because the harmonic synthesis costs more than the int8 neural decoder did. The
decoder checkpoint was selected on 400 held-out Wikipedia sentences (UTMOS 3.86 /
3.92), never on CV3; CV3 was run once on the frozen voice. Paired bootstrap against
the 263 k heart-nano on the same 500 CV3 rows: WER −0.27 pp (95% CI −0.50 to
−0.07), UTMOS +1.36 (95% CI +1.33 to +1.39). Details:
[`evidence/heart-nano-dsp-20261126.json`](https://huggingface.co/ampixa/sanoTTS/blob/main/evidence/heart-nano-dsp-20261126.json);
the 263 k release:
[`evidence/heart-nano-s-20261125.json`](https://huggingface.co/ampixa/sanoTTS/blob/main/evidence/heart-nano-s-20261125.json).

`heartnanos/` (the 263 k voice) and `heartnano-dsp/` stay in this repo: sanotts 0.5.6
and 0.5.7 still download them under the name heart-nano.

## How it stacks up

Open small-scale TTS on an honest gate — a diverse 24-sentence set scored
with the **same** no-reference suite (SCOREQ / UTMOS are naturalness
predictors, DNSMOS-SIG is signal quality; higher is better). Parameter
counts are inference-time and exclude the shared external G2P.

| System | Params | SCOREQ | UTMOS | DNS-SIG |
| --- | ---: | :---: | :---: | :---: |
| **sanoTTS (amy)** | **1.46 M** | **4.13** | **4.10** | 3.61 |
| TinyTTS | 1.62 M | 3.94 | 3.65 | **3.62** |
| Inflect Nano | 4.63 M | 3.81 | 3.65 | 3.58 |
| Kitten TTS nano | 15 M | 3.02 | 3.58 | 3.43 |
| _Piper (our teacher)_ | _~15 M_ | _4.71_ | _4.47_ | _3.65_ |
| _Kokoro_ | _82 M_ | _4.89_ | _4.52_ | _3.69_ |

Among the systems in this table, sanoTTS amy is the **smallest** and scores
**highest on naturalness (SCOREQ and UTMOS) below Piper** — beating TinyTTS
while being smaller. This is our own 24-sentence comparison; on the Open TTS
Leaderboard's larger sets, several small models (for example Paradee-8M and
PiVo-1.4M) have higher UTMOS than amy. On DNSMOS-SIG, TinyTTS edges us by 0.01 — no single
metric tells the whole story. It's the only one that runs a full neural
stack on a $3 MCU. The frontier only pulls ahead at Piper, the ~15M teacher
we distilled from, and Kokoro (82M, 56× larger) — a gap we don't claim to
close. Reproduce it with `tools/eval_mos_all.py` + `tools/eval_scorecard.py`
in the GitHub repo.

Shipped-file sizes: sanoTTS amy 2.8 MB fp16 and TinyTTS 3.5 MB fp16, both
verified from the released files; Kokoro's ~330 MB fp32 is its widely cited
public figure.

## How it works

![text → duration → acoustic → decoder → audio](https://raw.githubusercontent.com/Ampixa/sanoTTS/master/docs/assets/saanotts-signal-path.png)

espeak-ng provides phoneme IDs; a duration model predicts timing; an
acoustic model predicts generator latents; a decoder renders audio. The
piperlite voices (amy, kristin, hfc, and the other languages) use a compact
time-domain decoder running in fp32 at 22.05 kHz. The nano voices (heart,
heart-nano) and the 567,008-parameter on-device model use an iSTFT decoder
at 24 kHz, quantized to int8 where it has to fit and run in real time on the
ESP32-S3. Models are distilled from a Piper/VITS or Kokoro teacher — see
[`docs/distillation-recipe.md`](https://github.com/Ampixa/sanoTTS/blob/master/docs/distillation-recipe.md)
in the GitHub repo for the full recipe.

## Deploy

- **ESP32-S3 talking device** — a standalone WiFi dashboard: type text, the
  board phonemizes (on-chip espeak-ng) and speaks. See
  [`mcu/ports/esp32s3/`](https://github.com/Ampixa/sanoTTS/tree/master/mcu/ports/esp32s3).
  Board-by-board measurements are in
  [`BOARDS.md`](https://github.com/Ampixa/sanoTTS/blob/master/BOARDS.md); the
  silicon figures there are for the `en_us_e12nano` lineage, which is a
  sibling of `heart-nano`, not the same weights.
- **Browser** — the full stack in WASM, no server. **[▶ Hear and synthesize
  all 31 voices across 17 languages live](https://tts.ampixa.com/sanoTTS)**; source in
  [`web/`](https://github.com/Ampixa/sanoTTS/tree/master/web).
- **Other MCUs** — which chips can run it and how well:
  [`docs/mcu-classes-and-porting.md`](https://github.com/Ampixa/sanoTTS/blob/master/docs/mcu-classes-and-porting.md).

## Links

- Source, recipes, eval tooling: [github.com/Ampixa/sanoTTS](https://github.com/Ampixa/sanoTTS)
- Live browser demo: [tts.ampixa.com/sanoTTS](https://tts.ampixa.com/sanoTTS)
- npm package: [sanotts-web](https://www.npmjs.com/package/sanotts-web)
- PyPI package: [sanotts](https://pypi.org/project/sanotts/)

## License

GPLv3 — see [`LICENSE`](https://github.com/Ampixa/sanoTTS/blob/master/LICENSE).
The pipeline builds on GPLv3 components (notably
[espeak-ng](https://github.com/espeak-ng/espeak-ng) for G2P, and
[piper](https://github.com/OHF-Voice/piper1-gpl)), so the project as a
whole is GPLv3.

Copyright (C) 2026 Ampixa.

## Files here

Two package layouts, because there are two graphs.

**piperlite** (`amy-en-1p46m/`, `kristin-en-1p4m/`, `hfc-en-1p8m/`,
`amy-en-1p1m/`, `id-newstts-1p46m/`, `vi-vais1000-1p46m/`) — a flat fp16
blob addressed by manifest offsets:

```
manifest.json                 weights.fp16.bin
piper-phoneme-config.json     (+ sibilant-injection calibration where applicable)
```

**nano** (`heart/`, `heartnanos/`, `heartnano-dsp/`, `heartnano-f16/`) — the mel-100 stack, two blobs plus the
generated offset header:

```
meta.json          lineage, per-file sha256, sample rate, vocab
front_*.bin        duration + acoustic
model_*.bin        decoder
nano_q8_meta.h     tensor offsets
```

`heartnanos/` (the 263 k heart-nano of 0.5.6) ships `*_q8.bin` (int8, 311,440 bytes total, header flag
`NANO_LOCAL_FEATURES 1`). `heartnano-dsp/` (heart-nano since 0.5.7) holds the same
`front_q8.bin` plus `dsp_decoder.npz` (the harmonic-plus-noise decoder, float32,
198,632 bytes, sha256 in `meta.json`); its `model_q8.bin` is the 0.5.6 neural decoder,
kept only so sanotts <= 0.5.6 can still load the folder. `heartnano-f16/` (heart-nano
since 0.5.8) holds `front_q8.bin`, the same decoder in float16 (`dsp_decoder.npz`,
104,164 bytes), `nano_q8_meta.h` and `meta.json`, and no `model_*.bin`. `heart/` ships
`*_f32.bin` (float32, 9,137,920 bytes) because its int8 export missed the
fidelity gate. Both layouts are consumed by the `sanotts` Python package and
the portable C runtime.

**`web/voices/`** is a third thing and exists for the browser. The piperlite
voices ship there as `front_f32.bin` + `dec_f32.bin`, a different artifact
from the `weights.fp16.bin` the Python package reads, which is why the same
voice appears twice in this repo under two names. It mirrors `web/` in the
GitHub repo byte for byte and is what `sanotts-web` fetches. The nano voices
are not duplicated: `web/voices/heart/` and `heart/` hold the same blobs.
`web/voices/heartnano-dsp/` is the 104 k heart-nano for the browser
(`heartnano_dsp.js`, float32 decoder); `web/voices/heartnano/` is the first heart-nano
(294 k), kept for older `sanotts-web` versions. Its
top-level `heartnano/` folder was removed on 2026-11-25; sanotts <= 0.5.5 still
downloads it from the GitHub `voices-v2` release, and older revisions of this repo
keep it.

`samples/` holds the audio clips embedded above (mp3, one to four per voice,
plus the on-device `mcu-567k.mp3`), and `evidence/` the eval report behind the
heart scores.
