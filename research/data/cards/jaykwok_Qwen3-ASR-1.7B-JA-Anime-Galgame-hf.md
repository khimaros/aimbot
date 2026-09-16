---
license: apache-2.0
pipeline_tag: automatic-speech-recognition
library_name: transformers
base_model: Qwen/Qwen3-ASR-1.7B-hf
language:
- ja
tags:
- qwen3-asr
- automatic-speech-recognition
- japanese
- transformers-native
- forced-alignment
- ctc
---

# Qwen3-ASR-1.7B-JA-Anime-Galgame-hf

This is a Transformers-native `-hf` layout conversion of
[`jaykwok/Qwen3-ASR-1.7B-JA-Anime-Galgame`](https://huggingface.co/jaykwok/Qwen3-ASR-1.7B-JA-Anime-Galgame),
which was fine-tuned from the non-`-hf` Qwen3-ASR checkpoint.

The repository also ships three optional **CTC alignment heads** trained on
this model's audio encoder. They are not part of the ASR model and are not
loaded by
`AutoModelForMultimodalLM`; see [CTC Alignment Heads](#ctc-alignment-heads)
below.

## Difference From The Non-`-hf` Repository

The source repository is intended for the `qwen-asr` wrapper / original Qwen3-ASR
layout. This repository is intended for native Hugging Face Transformers loading.

The conversion keeps the fine-tuned weights unchanged and only rewrites the
repository layout to match [`Qwen/Qwen3-ASR-1.7B-hf`](https://huggingface.co/Qwen/Qwen3-ASR-1.7B-hf):

- config / processor / tokenizer files come from the official `-hf` template.
- safetensors keys are rewritten as:
  - `thinker.audio_tower.* -> model.audio_tower.*`
  - `thinker.audio_tower.proj1.* -> model.multi_modal_projector.linear_1.*`
  - `thinker.audio_tower.proj2.* -> model.multi_modal_projector.linear_2.*`
  - `thinker.model.* -> model.language_model.*`
- tensor count after conversion: `707`.
- converted tensor bytes: `4076104960`.

## Requirements

Requires the stable `transformers >= 5.13.0` release for native Qwen3-ASR support:

```bash
pip install "transformers>=5.13.0"
```

With uv:

```bash
uv pip install "transformers>=5.13.0"
```

## Usage

```python
from transformers import AutoModelForMultimodalLM, AutoProcessor

model_id = "jaykwok/Qwen3-ASR-1.7B-JA-Anime-Galgame-hf"

processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForMultimodalLM.from_pretrained(
    model_id,
    torch_dtype="auto",
    device_map="auto",
)

inputs = processor.apply_transcription_request(
    audio="path/to/audio.wav",
    language="Japanese",
).to(model.device, model.dtype)

output_ids = model.generate(**inputs, max_new_tokens=256)
generated_ids = output_ids[:, inputs["input_ids"].shape[1]:]
text = processor.decode(generated_ids, return_format="transcription_only")[0]
print(text)
```

## CTC Alignment Heads

The original general-purpose head remains available under its original name.
Each JAV/non-semantic-vocalisation head is a separate file, not an in-place
replacement:

| | JAV vocalisation v3 | JAV vocalisation v2 | Original general head |
|---|---|---|---|
| File | `ctc_aligner_jav_vocalisation_v3.pt` | `ctc_aligner_jav_vocalisation_v2.pt` | `ctc_aligner.pt` |
| Schema | `asr_ctc_alignment_head_v2` | `asr_ctc_alignment_head_v1` | `asr_ctc_alignment_head_v1` |
| Intended use | As v2, plus telling moaning apart from silence and from speech per frame | JAV or other Japanese audio with frequent non-semantic vocalisation | General anime / galgame alignment and reproducing existing results |
| Training domains | Galgame + anime SFW + anime NSFW/JAV | Galgame + anime SFW + anime NSFW/JAV | Galgame with sparse word-timestamp supervision |
| Vocabulary | Acoustic characters only (`acoustic_only=True`); punctuation has zero acoustic width | Acoustic characters only (`acoustic_only=True`); punctuation has zero acoustic width | Character vocabulary including punctuation |
| Vocalisation treatment | As v2, and a second output head labels each frame `silence` / `vocalisation` / `speech` | Vocalisation-stripped targets and blank-only examples teach non-semantic vocalisation as blank | No JAV-specific stripped-target pass |
| Output classes | 2,603 (+ 3 frame classes) | 2,603 | 2,328 |
| Parameters | 3,982,894 | 3,981,355 | 3,840,280 |

Choose a JAV variant when non-semantic moans are being transcribed as words or
when punctuation classes fragment otherwise continuous blank runs; choose v3 over
v2 when a consumer wants to know *what kind* of sound filled a stretch rather
than only that no character was evidenced there. Choose the original head for its
original domain or when exact compatibility with existing timelines matters.

All three heads are encoder-specific and all three preserve all audio: blank runs
are used to choose chunk boundaries, never to delete samples. The frame classes
in v3 carry the same restriction. They are a description of a stretch of audio,
not a licence to discard it.

### What the heads do

ASR gives you text and a segment window. It does not tell you *when inside that
window* each character was spoken, so a subtitle writer has to spread the text
across the window in proportion to character count and hope. This head replaces
that guess with a measurement.

It is a small CTC classifier over the **frozen** audio encoder of this model.
It brings no acoustic model of its own — that is the point. General-purpose
Japanese forced aligners are not adapted to this domain, so pairing one with a
domain-fine-tuned ASR makes the aligner the bottleneck. Sitting on the encoder
that was already fine-tuned means the domain adaptation is paid for once, and
only a 3.8 M-parameter head has to be learned.

**It is encoder-specific.** It is trained against the features *this* fine-tune's
encoder produces and will not transfer to `Qwen/Qwen3-ASR-1.7B-hf` or to another
fine-tune. That is why it ships here, next to the encoder it belongs to, rather
than in the application that consumes it.

| | |
|---|---|
The architecture below is shared. The concrete dimensions in this table describe
the original `ctc_aligner.pt`; the variant table above gives the fields that
differ for `ctc_aligner_jav_vocalisation_v2.pt`.

| | |
|---|---|
| File | `ctc_aligner.pt` (14.7 MB, `torch.save` payload, `weights_only=False`) |
| Schema | `asr_ctc_alignment_head_v1` |
| Input | `(B, T, 2048)` encoder hidden states, 13 fps (76.9 ms per frame) |
| Output | `(B, T*2, 2328)` log-probabilities, **38.5 ms** resolution |
| Parameters | 3,840,280 |
| Vocabulary | 2,328 = 2,326 characters + blank (index 0) + `<unk>` (index 1) |
| Targets | Japanese **characters**, NFKC-folded, whitespace stripped |

Two design choices differ from the obvious ones:

- **Characters, not kana or phonemes.** Kana needs g2p (`pyopenjtalk`), which
  adds a dependency and, worse, a reading-error source on kanji. Characters need
  neither, and the density works out better: the training corpus runs 4.67
  chars/s against a 13 fps encoder, i.e. ~2.8 frames per character, where kana
  would be nearer 2.
- **The encoder is upsampled before the classifier.** It adds no information,
  but CTC cannot emit more tokens than it has frames, and timestamp resolution
  is bounded by frame duration — 76.9 ms natively. A ×2 transposed convolution
  is cheap and buys back both.

### Readings of the same tensor

The head is run once per audio chunk; the resulting log-probabilities are read
two different ways (three, for v3).

1. **Character timestamps.** CTC forced alignment (Viterbi over the standard
   blank-interleaved target lattice) of the *known* transcript against the
   log-probs yields a start/end frame per character. This is what gives subtitle
   cues real in-segment timing and real word gaps to split lines at.
2. **Blank runs.** A stretch the head covers entirely with blank is a stretch
   with no character evidence in it — read straight off the argmax, with no
   tuned threshold and no free parameter beyond a minimum run length. These are
   the natural pause locations, useful for choosing where to cut long audio into
   chunks.

Reading (2) is a gate on *cut points only*. Deciding that a stretch is silence
and therefore deleting the audio would make a false blank unrecoverable; using
it to choose where to cut leaves every sample in the stream either way.

3. **Frame classes (`ctc_aligner_jav_vocalisation_v3.pt` only).** A second linear
   layer over the same 512-dimensional trunk emits three log-probabilities per
   output frame, in the fixed order `("silence", "vocalisation", "speech")`. This
   is what separates the two things a blank run conflates: a stretch with no
   character evidence may be a pause or may be a moan, and the CTC vocabulary is
   the same either way because the JAV variants are trained to call moaning
   blank. Reading (3) says which.

   It shares the trunk deliberately. Alignment and vocalisation detection are the
   same acoustic question asked twice, and the 1,539 extra parameters are the
   whole cost of asking it the second way.

   `payload["frame_classes"]` names the classes in output order. Check it rather
   than assuming the tuple above: the order is positional, and a consumer that
   hard-codes it will silently swap two classes if it is ever changed.

### Loading a variant

The payload is self-contained: architecture hyper-parameters, vocabulary and
weights all travel in the same file.

```python
import torch
from huggingface_hub import hf_hub_download

filename = "ctc_aligner_jav_vocalisation_v3.pt"  # JAV, with frame classes
# filename = "ctc_aligner_jav_vocalisation_v2.pt"  # JAV, CTC only
# filename = "ctc_aligner.pt"                      # original general head

path = hf_hub_download(
    repo_id="jaykwok/Qwen3-ASR-1.7B-JA-Anime-Galgame-hf",
    filename=filename,
)
payload = torch.load(path, map_location="cpu", weights_only=False)

payload["schema"]      # "asr_ctc_alignment_head_v2" for v3, "..._v1" otherwise
payload["input_dim"]   # 2048
payload["hidden_dim"]  # 512
payload["upsample"]    # 2
payload["blocks"]      # 4
payload["vocab"]       # {"schema", "size", "blank_index", "unk_index", "chars"}
payload["vocab"].get("acoustic_only", False)
payload.get("frame_classes")  # ("silence", "vocalisation", "speech") on v3, else absent
payload["state_dict"]
```

The two schemas differ by exactly one tensor pair, `frame_classifier.weight` and
`frame_classifier.bias`. Build the module with `frame_classes=len(...)` when the
key is present and `0` when it is not; everything else is unchanged, so one
loader covers both.

The module it belongs to:

```python
from torch import nn


class ResidualConvBlock(nn.Module):
    """Dilated depthwise-separable conv, pre-norm, residual.

    Convolutional rather than attentional on purpose: alignment is a monotonic,
    local problem, and a conv stack cannot learn to reorder time the way
    self-attention can.
    """

    def __init__(self, channels, dilation):
        super().__init__()
        self.norm = nn.LayerNorm(channels)
        self.depthwise = nn.Conv1d(
            channels, channels, kernel_size=5,
            padding=2 * dilation, dilation=dilation, groups=channels,
        )
        self.pointwise = nn.Conv1d(channels, channels, kernel_size=1)
        self.activation = nn.GELU()
        self.dropout = nn.Dropout(0.0)

    def forward(self, x):
        y = self.norm(x).transpose(1, 2)
        y = self.pointwise(self.activation(self.depthwise(y)))
        return x + self.dropout(y.transpose(1, 2))


class CtcAlignmentHead(nn.Module):
    def __init__(self, vocab_size, input_dim=2048, hidden_dim=512,
                 upsample=2, blocks=4, frame_classes=0):
        super().__init__()
        self.upsample = upsample
        self.input_norm = nn.LayerNorm(input_dim)
        self.project = nn.Linear(input_dim, hidden_dim)
        self.expand = nn.ConvTranspose1d(
            hidden_dim, hidden_dim, kernel_size=upsample, stride=upsample
        ) if upsample > 1 else None
        self.blocks = nn.ModuleList(
            [ResidualConvBlock(hidden_dim, dilation=2**i) for i in range(blocks)]
        )
        self.output_norm = nn.LayerNorm(hidden_dim)
        self.classifier = nn.Linear(hidden_dim, vocab_size)
        # Present only in `asr_ctc_alignment_head_v2`. Same trunk, second
        # question - see "Readings of the same tensor" above.
        self.frame_classifier = (
            nn.Linear(hidden_dim, frame_classes) if frame_classes else None
        )

    def trunk(self, features):
        x = self.project(self.input_norm(features))
        if self.expand is not None:
            x = self.expand(x.transpose(1, 2)).transpose(1, 2)
        for block in self.blocks:
            x = block(x)
        return self.output_norm(x)

    def forward(self, features):
        """(B, T, input_dim) -> (B, T*upsample, vocab) log-probabilities."""
        return nn.functional.log_softmax(
            self.classifier(self.trunk(features)), dim=-1
        )

    def forward_with_frames(self, features):
        """As `forward`, plus (B, T*upsample, 3) frame-class log-probabilities.

        Returns `None` for the second element on a v1 payload, so a caller can
        ask for the classes without first checking which file it loaded.
        """
        x = self.trunk(features)
        ctc = nn.functional.log_softmax(self.classifier(x), dim=-1)
        if self.frame_classifier is None:
            return ctc, None
        return ctc, nn.functional.log_softmax(self.frame_classifier(x), dim=-1)


head = CtcAlignmentHead(
    vocab_size=payload["vocab"]["size"],
    input_dim=payload["input_dim"],
    hidden_dim=payload["hidden_dim"],
    upsample=payload["upsample"],
    blocks=payload["blocks"],
    frame_classes=len(payload.get("frame_classes") or ()),
)
head.load_state_dict(payload["state_dict"])
head.eval()
```

For the acoustic-only JAV variant, punctuation in the known ASR transcript is
retained as zero-width text metadata rather than assigned an acoustic frame. A
consumer must keep those zero-width punctuation spans when rebuilding text; it
must not drop them as malformed timestamps.

### Running it

Feed it the audio encoder's output for the same audio, then read the result.

```python
import unicodedata

import torch
from transformers import AutoModelForMultimodalLM, AutoProcessor

model_id = "jaykwok/Qwen3-ASR-1.7B-JA-Anime-Galgame-hf"
processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForMultimodalLM.from_pretrained(model_id, torch_dtype="auto")

inputs = processor.apply_transcription_request(
    audio="path/to/audio.wav", language="Japanese",
).to(model.device, model.dtype)

with torch.inference_mode():
    encoded = model.get_audio_features(
        input_features=inputs["input_features"],
        input_features_mask=inputs["input_features_mask"],
    )
    features = encoded.pooler_output.float().cpu()    # (frames, 2048) at 13 fps
    log_probs = head(features.unsqueeze(0))[0]        # (frames*2, payload["vocab"]["size"])
```

Note that `pooler_output` is the batch's valid frames *concatenated*, not a
padded `(B, T, 2048)` tensor. With a batch of one it is exactly that clip's
frames; for a real batch, slice it with the per-item frame count:

```python
def audio_output_lengths(input_lengths):
    """Mel frames -> encoder frames, 13 per 100."""
    leave = input_lengths % 100
    feat = (leave - 1) // 2 + 1
    return ((feat - 1) // 2 + 1 - 1) // 2 + 1 + (input_lengths // 100) * 13

lengths = audio_output_lengths(inputs["input_features_mask"].sum(dim=1))
```

Character indices, for building CTC targets:

```python
chars = payload["vocab"]["chars"]                    # tuple of single chars
lookup = {ch: i + 2 for i, ch in enumerate(chars)}   # 0 blank, 1 unk

def encode(text):
    folded = unicodedata.normalize("NFKC", text)
    folded = "".join(ch for ch in folded if not ch.isspace())
    return [lookup.get(ch, 1) for ch in folded]
```

Out-of-vocabulary characters map to `<unk>` rather than being dropped: they
still consume audio, and dropping them would shift every later timestamp.

Frame `f` of the output starts at `f * (1 / 13) / upsample` seconds. Blank runs
need no extra machinery:

```python
blank = log_probs.argmax(dim=-1).eq(0)   # per output frame
```

For character timestamps, run a standard CTC forced alignment (Viterbi over the
blank-interleaved target lattice, backtracked to per-character frame spans)
against `encode(transcript)`. `torchaudio.functional.forced_align` does this if
you have a torchaudio build for your Python/CUDA combination; otherwise it is
about a hundred lines to implement directly, and doing so removes the dependency
entirely.

Treat the head as a measured improvement over proportional timing, not as
ground truth.

## Changelog

- **2026-09-03** — added `ctc_aligner_jav_vocalisation_v3.pt`
  (`asr_ctc_alignment_head_v2`). It is `ctc_aligner_jav_vocalisation_v2.pt`'s
  training recipe plus a three-class frame head (`silence` / `vocalisation` /
  `speech`, 1,539 parameters) on the shared trunk, so one forward pass answers
  both "which character was here" and "what kind of sound was here". Nothing was
  overwritten: v2 and the original general head are unchanged and still
  selectable by filename. On an eight-film held-out pool the CTC reading is not
  worse than v2 (pooled blank-run AUC 0.9611 -> 0.9639, winning 8/8 films), and
  the frame reading reaches 0.9666. Word-boundary agreement with an independent
  reference transcriber is unchanged within measurement noise on two films.
  Frame supervision comes from three label sources at a 0.5 loss weight;
  55% of training frames carry a class label and the rest are ignored rather
  than guessed.

- **2026-09-02** — `chat_template.jinja` gained an `assistant`-role rendering
  block, copied verbatim from the base `Qwen/Qwen3-ASR-1.7B-hf` /
  `Qwen/Qwen3-ASR-0.6B-hf` template (both are byte-identical). `transformers`
  5.15.0 changed `Qwen3ASRProcessor.apply_transcription_request()`'s language
  forcing from a system-prompt string + `add_generation_prompt=True` to an
  assistant-turn prefill (`"language <NAME><asr_text>"`) +
  `continue_final_message=True` (upstream commit `c7f9c881`). This
  repository's template previously had no branch for `assistant`-role
  messages at all, so `continue_final_message` raised
  `ValueError("continue_final_message is set but the final message does not
  appear in the chat...")` on every transcription request under
  `transformers>=5.15.0`. The fix is purely additive: the existing
  `system`/`user` rendering and the `add_generation_prompt` branch are
  unchanged, so callers still on `transformers<5.15.0` see no behavior
  change.

## Conversion

This repository was produced with:

```powershell
uv run python -m tools.asr.convert_qwen3_asr_to_hf `
  --source-model-dir models/jaykwok-Qwen3-ASR-1.7B-JA-Anime-Galgame `
  --output-dir agents/temp/20260630_123000_qwen3_asr_hf_conversion `
  --template-repo Qwen/Qwen3-ASR-1.7B-hf `
  --max-shard-size 768MB
```

## Notes

This model is specialized for Japanese anime / galgame style speech. It should
be evaluated on your own data before production use.
