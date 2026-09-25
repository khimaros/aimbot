---
license: mit
base_model: deepseek-ai/DeepSeek-V4.1-Flash
library_name: llama.cpp
tags:
  - gguf
  - mxfp4
  - deepseek
  - llama.cpp
  - mixture-of-experts
---

# DeepSeek-V4.1-Flash, GGUF with the engram tables

DeepSeek-V4.1-Flash (552B MoE, 40 layers, 384 routed experts, hyper-connections, CSA2 sparse
attention, a 189 GiB n-gram conditional memory) converted for llama.cpp without touching the
released precision: the routed experts are a lossless repack of the released MXFP4 blocks,
attention and dense weights are dequantized from fp8 and stored as Q8_0/BF16, and the two engram
tables travel as their raw fp8 bytes with their scales. 502 GB in 11 shards.

**It runs only on the `dsv41-porte` branch of
[JigSawPT/llama.cpp](https://github.com/JigSawPT/llama.cpp).** Upstream llama.cpp has no runtime for
V4.1 yet; its open conversion PR ([#28696](https://github.com/ggml-org/llama.cpp/pull/28696))
stores the engram tables differently, so this file is not interchangeable with files from that
converter. Reconciling the two is part of the plan to upstream the branch.

**Text only.** DeepSeek-V4.1-Flash also takes images, but the converter on this branch skips the
vision tower: the 11 shards hold 1 012 tensors and none of them is a vision or projector tensor.
Image input is not supported.
If you need image input, a community runtime and GGUF set exist: [smalinin/llama.cpp, branch
`my_build_deepseek41`](https://github.com/smalinin/llama.cpp/tree/my_build_deepseek41) with
[smalinin/DeepSeek-V4.1-Flash-GGUF](https://huggingface.co/smalinin/DeepSeek-V4.1-Flash-GGUF) (CUDA only,
includes an mmproj file). We have not tested them. Upstream PR
[#28696](https://github.com/ggml-org/llama.cpp/pull/28696) now carries a full conversion and runtime path for
V4.1 (`deepseek41`), still unmerged; its files are not interchangeable with these.

## What it needs, and what it gives

Measured on one RTX 5090 (31.8 GiB of VRAM) with 125.7 GiB of RAM and the file on a PCIe 5 NVMe:

| | decode | time to first token |
|---|---:|---:|
| new content (our benchmark: 4 prompts of mixed content x 3 rounds) | **5.1 tokens/s** | 7.7 s |
| resident content (the same prompt again) | **21.4 tokens/s** | 0.26 s |

The experts stream from disk through a VRAM cache (18 GiB) and a pinned host tier (72 GiB);
the engram tables are memory-mapped and read 48 rows per token. Nothing here fits in RAM + VRAM
and nothing has to. On the buffered read path the ceiling of this architecture on this machine is
6.2 tokens/s without any disk miss; 21 tokens/s needs the working set on the card.

Exactness against the reference implementation: logit correlation 0.9967 at 1 401 tokens, equal
to the port against itself across two runs (0.9959). The remaining gap sits at the rounding floor
of the reference's own fp8 arithmetic. Details, method and every negative result:
[the report](https://github.com/JigSawPT/deepseek-v41-flash-on-5090).

## Run

```
llama-server -m DeepSeek-V4.1-Flash-MXFP4-engram-00001-of-00011.gguf -ngl 99 -c 8192 ^
  --moe-stream --moe-stream-cache 18 --moe-stream-l2 72 --moe-stream-direct --reasoning off ^
  --host 127.0.0.1 --port 8080
```

All 11 shards go in the same directory; point `-m` at the first. A bare number after
`--moe-stream-cache` is a budget in GiB: 18 GiB is about 25 expert slots per layer on this file.
The minimum is 18 slots per layer, `--moe-stream-cache 18s`, about 13 GiB. `--moe-stream-l2` above
72 GiB on a 125.7 GiB machine is
slower: it steals page cache from the engram tables. `--moe-stream-io-threads 1` makes runs
bit-for-bit reproducible at 3.6 instead of 4.3 tokens/s. Chat mode (`--reasoning off`) is the
measured configuration; thinking mode at temperature 0 loops on vague prompts.

`--moe-stream-direct` reads the experts with O_DIRECT (`FILE_FLAG_NO_BUFFERING` on Windows) and
falls back to buffered reads where the filesystem refuses it. Added to the line on 23/09/2026: on the
four benchmark prompts it doubles decode on the first pass, when the experts are not cached yet
(3.9–4.9 → 8.9–10.0 tokens/s), and leaves resident decode unchanged (19–22 tokens/s). The table
above was measured without it.

The draft head is published separately
([DeepSeek-V4.1-Flash-DSpark-GGUF](https://huggingface.co/JigSawPT/DeepSeek-V4.1-Flash-DSpark-GGUF));
on this hardware it is neutral on mixed content.

## Files

| shard | GB | contents |
|---|---:|---|
| `-00001-of-00011` | 0.01 | metadata (tokenizer, chat template), engram hashing constants |
| `-00002-of-00011` | 98.3 | engram table, layer 1 (fp8, raw) |
| `-00003-of-00011` | 3.1 | engram table scales, layer 1 (raw) |
| `-00004-of-00011` | 98.3 | engram table, layer 14 (fp8, raw) |
| `-00005-of-00011` | 46.4 | engram table scales, layer 14; routed experts (MXFP4), layers 0–5 |
| `-00006` .. `-00010` | 45.7 each | routed experts (MXFP4), layers 6–37 |
| `-00011-of-00011` | 27.1 | routed experts (MXFP4), layers 37–39; attention, shared experts, router, hyper-connections, norms, engram projections, token embedding and output head (Q8_0/BF16/F32) |

`SHA256SUMS.txt` covers all eleven; run `sha256sum -c SHA256SUMS.txt` in the download directory.
The 299 GB variant without the engram tables is not
published: zeroing the memory is the exact identity of the module, but the model that comes out
does not produce the released model's outputs.

## How it was made

```
python convert_hf_to_gguf.py <DeepSeek-V4.1-Flash> --outtype bf16 --engram --outfile DeepSeek-V4.1-Flash-MXFP4-engram.gguf
llama-gguf-split --split --split-max-size 48G DeepSeek-V4.1-Flash-MXFP4-engram.gguf DeepSeek-V4.1-Flash-MXFP4-engram
```

From the released checkpoint, on the same branch. The MXFP4 repack was verified block by block
(480/480 identical); the split was verified by loading the first shard and comparing the answer
with the monolithic file.

## Credits

DeepSeek for the model and the reference implementation (MIT). nibor1896 for
[Crow](https://github.com/nibor1896/Crow), whose expert-streaming patch series the branch builds on
(MIT). ggml-org/llama.cpp. Engineering assisted by Claude (Anthropic).
