---
license: apache-2.0
base_model: openbmb/MiniCPM-OCR-1.0
base_model_relation: quantized
pipeline_tag: image-text-to-text
library_name: gguf
language:
  - en
  - zh
tags:
  - gguf
  - llama.cpp
  - ocr
  - document-parsing
  - minicpm-ocr
  - minicpm-v
  - table-recognition
  - formula-recognition
  - image-text-to-text
---

# MiniCPM-OCR 1.0 GGUF

<div style="display: flex; gap: 8px; align-items: center; margin-top: 10px; margin-bottom: 10px;">
  <a href="https://atomic.chat/?utm_source=huggingface&utm_medium=referral&utm_campaign=hf_minicpm_ocr_1_0&utm_content=btn_atomic"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_atomic.png" width="162" alt="Atomic Chat"></a>
  <a href="https://discord.gg/8wGSsvmg4V"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_discord.png" width="119" alt="Discord"></a>
  <a href="https://github.com/AtomicBot-ai/Atomic-Chat"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_github.png" width="115" alt="GitHub"></a>
  <a href="https://x.com/atomic_chat_hq"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_x.png" width="108" alt="X"></a>
</div>
<ul style="margin: 0 0 12px 0;">
  <li>You can now run MiniCPM-OCR 1.0 in <a href="https://atomic.chat/?utm_source=huggingface&utm_medium=referral&utm_campaign=hf_minicpm_ocr_1_0&utm_content=bullet_app">Atomic Chat</a> with image input: drop in a page and ask <code>Text Recognition:</code> (llama.cpp engine b11946 or newer, offered as an engine update).</li>
</ul>
<hr style="margin: 0 0 16px 0;">

GGUF builds of [openbmb/MiniCPM-OCR-1.0](https://huggingface.co/openbmb/MiniCPM-OCR-1.0), OpenBMB's 1.3B model that
reads document images into text, tables (HTML), formulas (LaTeX), charts and seals, in Chinese and English. By
AtomicChat. Every file was run on 40 real document pages and compared with the original.

- **From 1.15 GB on disk for the whole set**: `AD-Q4_K_M` (0.53 GB) with the Q8_0 vision projector (0.62 GB).
  OpenBMB's smallest recommended pair is 1.43 GB (Q4_K_M + F16 projector). On our 40 pages, every file here reads
  within 1.5 points of the original's character error (table below).
- **The text model drifts half as much as stock quants of the same size**: KLD to BF16 0.087 against 0.165 at
  0.53 GB (`AD-Q4_K_M` vs Q4_K_M), 0.027 against 0.051 at 0.58-0.59 GB (`AD-Q5_K_M` vs Q5_K_M).
- **Thinking stays off in the embedded chat template**, as in OpenBMB's own GGUF. With the original template,
  `llama-server` returns the transcription in `reasoning_content` and an empty `content`, and `llama-mtmd-cli` reads
  worse (+6.6 points of character error on our pages, 95% interval +1.6 to +12.4).
- **1.7x faster generation with OpenBMB's DSpark draft** (below): same text on 11 of 12 pages.

![Reading error against size on disk: AtomicChat, OpenBMB and prithivMLmods GGUF files](size-vs-reading-error.png)

## Files

Every text file needs a vision projector (`--mmproj`). The Q8_0 projector is the one to download; the F16 one is
the reference.

| File | Size on disk | Use | Pages within 1% of the original | Reading error vs annotation, change against the original | Text model: KLD / top-1 |
|---|---|---|---|---|---|
| `MiniCPM-OCR-1.0-Q8_0.gguf` | 0.81 GB | closest to the original | 30/40 | +0.2 [-0.8, +1.1] | 0.0039 / 96.1% |
| `MiniCPM-OCR-1.0-AD-Q6_K.gguf` | 0.73 GB | near Q8_0, 0.08 GB smaller | 32/40 | +0.3 [-0.2, +0.8] | 0.0064 / 95.0% |
| `MiniCPM-OCR-1.0-AD-Q5_K_M.gguf` | 0.59 GB | **recommended** | 27/40 | +1.5 [+0.1, +3.2]; with the Q8_0 projector -0.3 [-1.5, +0.7] | 0.0266 / 89.9% |
| `MiniCPM-OCR-1.0-AD-Q4_K_M.gguf` | 0.53 GB | smallest | 19/40 | -0.4 [-4.2, +2.6] | 0.0871 / 83.4% |
| `mmproj-MiniCPM-OCR-1.0-Q8_0.gguf` | 0.62 GB | vision projector | 33/40 (with the BF16 text model) | -0.7 [-1.9, +0.3] | |
| `mmproj-MiniCPM-OCR-1.0-F16.gguf` | 0.90 GB | vision projector, reference | | | |

- **Pages**: 40 from [OmniDocBench](https://huggingface.co/datasets/opendatalab/OmniDocBench), 4 from each of its
  10 sources (slides, papers, books, textbooks, exams, historical documents, magazines, newspapers, notes, reports;
  seed 0), English and Chinese. One request per page, `Text Recognition:`, greedy decoding, llama.cpp `b11953`.
- **The original** is the BF16 GGUF with the F16 projector, on the same stand. It reads these pages with a mean
  character error of 21.6% against OmniDocBench's annotation (median 13.1%). Much of that is format rather than
  misread characters (reading order and markup conventions differ), so the number only compares files with each other.
- **Change against the original**: the file's character error minus the original's, in points, averaged over the
  pages, with a 95% bootstrap interval over pages. An interval that holds 0 means no difference this set can show.
- **Pages within 1%**: the file's text differs from the original's by under 1% of characters. Greedy decoding turns
  one near-tie into a different rest of the page, so this count moves by a few pages between files of the same
  quality (our Q8_0 and OpenBMB's Q8_0, with the same KLD, land at 30 and 35).
- **KLD / top-1**: the text model alone against BF16 logits on 87 x 4096 tokens of general text in 30 languages.
  It speaks to free-form prompts (questions about a page, extraction to JSON) more than to transcription.
- Numbers for all 16 sizes we built (down to 0.30 GB), page by page, are in the
  [metrics repo](https://huggingface.co/datasets/AtomicChat/MiniCPM-OCR-1.0-GGUF-metrics). Below 0.53 GB some pages
  start to repeat until the token limit (2 of 40 at 0.45 GB), so those files are not here. The pages' text is not
  republished: OmniDocBench is for research use only.

## Other GGUF files on the same pages

Same pages, prompt, reference and llama.cpp build. Each file runs with its own publisher's projector (F16 or BF16,
0.90 GB).

| File | Size on disk, with projector | Pages within 1% of the original | Reading error vs annotation, change against the original | Text model: KLD / top-1 |
|---|---|---|---|---|
| openbmb F16 | 1.52 + 0.90 GB | 38/40 | +0.05 [-0.02, +0.17] | 0.0002 / 99.0% |
| openbmb Q8_0 | 0.81 + 0.90 GB | 35/40 | +0.3 [0.0, +0.8] | 0.0039 / 96.1% |
| openbmb Q6_K | 0.63 + 0.90 GB | 26/40 | +4.5 [-0.4, +13.7] | 0.0200 / 91.2% |
| openbmb Q5_K_M | 0.58 + 0.90 GB | 25/40 | -0.6 [-1.7, +0.4] | 0.0513 / 86.5% |
| openbmb Q4_K_M | 0.53 + 0.90 GB | 18/40 | +0.3 [-3.9, +3.6] | 0.1650 / 77.2% |
| openbmb Q4_0 | 0.50 + 0.90 GB | 14/40 | -0.1 [-1.9, +1.7] | 0.2641 / 72.2% |
| prithivMLmods Q4_K_M | 0.53 + 0.90 GB | 5/40 | +14.5 [0.0, +38.6] | 0.1650 / 77.3% |
| prithivMLmods Q3_K_M | 0.47 + 0.90 GB | 2/40 | +141 [+6.9, +375] | 0.5642 / 62.2% |

- On reading error, OpenBMB's files and ours are within the noise of 40 pages at every size. The difference is the
  projector (0.28 GB) and the text model's drift.
- prithivMLmods' Q4_K_M has the same weights as OpenBMB's (same KLD) but the original chat template, which opens a
  thinking block in llama.cpp; that, not the quantization, is most of its gap.

## Run

llama.cpp `b11826` or newer (MiniCPM-OCR support: [#30979](https://github.com/ggml-org/llama.cpp/pull/30979)). These
files were built and measured with `b11953` (commit `a7af149`).

```bash
hf download AtomicChat/MiniCPM-OCR-1.0-GGUF MiniCPM-OCR-1.0-AD-Q5_K_M.gguf mmproj-MiniCPM-OCR-1.0-Q8_0.gguf --local-dir .

# one image, one region type (prompts below)
llama-mtmd-cli -m MiniCPM-OCR-1.0-AD-Q5_K_M.gguf --mmproj mmproj-MiniCPM-OCR-1.0-Q8_0.gguf \
  --jinja --temp 0 -c 16384 -n 8192 --image page.png -p "Text Recognition:"

# OpenAI-compatible server: send the image and the prompt as one user message, temperature 0
llama-server -m MiniCPM-OCR-1.0-AD-Q5_K_M.gguf --mmproj mmproj-MiniCPM-OCR-1.0-Q8_0.gguf \
  --jinja -c 16384 -ngl 99
```

| What is in the image | Prompt | You get |
|---|---|---|
| a page, paragraph, title or text block | `Text Recognition:` | plain text (inline formulas as LaTeX) |
| a table | `Table Recognition:` | HTML |
| a display formula | `Formula Recognition:` | LaTeX |
| a seal | `Seal Recognition:` | the seal's text |
| a chart | `Chart to Table:` | a table |

For whole PDFs with layout (reading order, tables and formulas cropped and recognized separately), OpenBMB's
[`minicpmvocr` SDK](https://github.com/OpenBMB/MiniCPM-OCR) runs on top of `llama-server` (`--backend llamacpp`).

### Faster with DSpark

OpenBMB's [DSpark draft](https://huggingface.co/openbmb/MiniCPM-OCR-1.0-DSpark-gguf) speeds up generation with these
files too (`llama-server` or `llama-cli`; `llama-mtmd-cli` takes no draft model):

```bash
hf download openbmb/MiniCPM-OCR-1.0-DSpark-gguf dspark-MiniCPM-OCR-1_0-Q8_0.gguf --local-dir .
llama-server -m MiniCPM-OCR-1.0-AD-Q5_K_M.gguf --mmproj mmproj-MiniCPM-OCR-1.0-Q8_0.gguf \
  -md dspark-MiniCPM-OCR-1_0-Q8_0.gguf -ngld 99 --spec-type draft-dspark --jinja -c 16384 -ngl 99
```

| Text model | Generation, no draft | With DSpark | Same text |
|---|---|---|---|
| `Q8_0` | 315 tokens/s | 527 tokens/s (1.67x) | 11/12 pages |
| `AD-Q4_K_M` | 337 tokens/s | 565 tokens/s (1.68x) | 11/12 pages |

12 of the pages above, one at a time, one A100 40 GB; 86% of drafted tokens accepted. With greedy decoding a draft
should not change the text; on one page it did, most likely through batched-verification numerics (not checked
further).

## How the files are built

- The text model (Qwen3.5 0.8B, 24 blocks) is quantized with an importance matrix from about 5M tokens of text in
  the model's chat markup (many languages, code, tables, math, long documents), shared with nothing in the
  page set above. The vision encoder is not calibrated: images enter only through the projector.
- AD layouts: the embedding table, which is also the output head here, and the attention output stay at Q6_K or
  higher; the FFN of the first two and last five blocks, and of blocks 2-4, sits one step above the rest.
- `mmproj-...-Q8_0.gguf`: llama.cpp's converter at Q8_0. The SigLIP `ffn_down` weights (rows 4304 wide, not a
  multiple of 32) stay F16 in it, so it is 0.62 GB rather than half of the F16 file.
- The embedded chat template is the original with one change: the assistant turn always starts with an empty
  `<think></think>` block. If you convert the weights yourself, run `llama-server` with `--reasoning off` instead.

## Limits

- Measured on whole pages with `Text Recognition:`. Crops from a layout model (tables, formulas, seals), the way
  OpenBMB's SDK works, are not measured separately here.
- Chinese and English pages only, as the model is trained.
- 40 pages: differences under about 2 points of character error are within the noise.
- Speeds are from one A100 with llama.cpp `b11953`; other hardware differs.

## License

Apache-2.0, as [openbmb/MiniCPM-OCR-1.0](https://huggingface.co/openbmb/MiniCPM-OCR-1.0) (SigLIP vision encoder and
Qwen3.5 text model, trained by OpenBMB from MiniCPM-V 4.6). Built by AtomicChat. Measurements and logs:
[AtomicChat/MiniCPM-OCR-1.0-GGUF-metrics](https://huggingface.co/datasets/AtomicChat/MiniCPM-OCR-1.0-GGUF-metrics).
