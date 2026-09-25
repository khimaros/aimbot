---
license: mit
base_model: deepseek-ai/DeepSeek-V4.1-Flash
base_model_relation: quantized
library_name: gguf
pipeline_tag: image-text-to-text
inference: false
tags:
- gguf
- deepseek
- deepseek-v4.1
- mixture-of-experts
- llama.cpp
- vision
quantized_by: smalinin
---

# DeepSeek-V4.1-Flash GGUF

GGUF conversions and mixed-precision quantizations of
[deepseek-ai/DeepSeek-V4.1-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash)
for the experimental DeepSeek-V4.1 runtime in
[smalinin/llama.cpp, branch `my_build_deepseek41`](https://github.com/smalinin/llama.cpp/tree/my_build_deepseek41). [! **ONLY_for_CUDA** ]

This is **DeepSeek-V4.1-Flash** (`DeepseekV41ForCausalLM`), not
DeepSeek-V4-Flash-0731. The architecture includes sparse attention,
hyper-connections, MoE layers, and two very large n-gram Engram lookup tables.

> [!IMPORTANT]
> These files require the linked `my_build_deepseek41` branch. Compatibility
> with stock upstream `llama.cpp` is not claimed.

## Available and planned files

| Variant | Repository state | First shard | Effective whole-model BPW | Total size |
| --- | --- | --- | ---: | ---: |
| **Q2_K backbone + Q5_K Engram** | Available | `Q2_K-Q5/DeepSeek-V4.1-Flash-EngramQ5-Q2_K-00001-of-00010.gguf` | **3.58** | **335.382 GB** |
| **IQ2_XXS gate/up + Q2_K down + Q8_0 Engram (antirez-like)** | Available | `IQ2_XXS_GU-Q2_K_Down-Q8/DeepSeek-V4.1-Flash-EngramQ8-IQ2_XXS_GU-Q2_K_Down-00001-of-00010.gguf` | **3.97** | **371.438 GB** |
| **Protected Q2_K + Q8_0 Engram** | Available | `Q2_K_Protected-Q8/DeepSeek-V4.1-Flash-Protected-Q2_K-Q8_0_Engram-imatrix-00001-of-00010.gguf` | **4.42** | **413.390 GB** |
| **IQ3_XS backbone + Q8_0 Engram** | Available | `IQ3_XS-Q8/DeepSeek-V4.1-Flash-IQ3_XS-Q8_0_Engram-imatrix-00001-of-00010.gguf` | **4.64** | **434.024 GB** |
| **MXFP4 conversion + Q8_0 Engram** | Available | `MXFP4/DeepSeek-V4.1-Flash-MXFP4-00001-of-00010.gguf` | **5.43** | **507.954 GB** |

Download every shard of the selected variant and pass only shard
`00001-of-00010` to `llama-server`; the remaining shards are discovered
automatically.

## Precision and size breakdown

| Variant | Primary backbone format | Nominal format BPW | Backbone and other data | Engram format | Engram BPW | Two Engram tables | Total | Effective total BPW |
| --- | --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| Q2_K + Q5_K Engram | Q2_K | 2.625 | 200.210 GB | Q5_K | 5.50 | 135.172 GB | 335.382 GB | **3.58** |
| IQ2_XXS gate/up + Q2_K down + Q8_0 Engram | IQ2_XXS / Q2_K hybrid | 2.06 / 2.625 | 162.536 GB | Q8_0 | 8.50 | 208.902 GB | 371.438 GB | **3.97** |
| Protected Q2_K + Q8_0 Engram | Q2_K / Q3_K protected hybrid | 2.625 / 3.4375 | 204.488 GB | Q8_0 | 8.50 | 208.902 GB | 413.390 GB | **4.42** |
| IQ3_XS + Q8_0 Engram | IQ3_XS | 3.30 | 225.122 GB | Q8_0 | 8.50 | 208.902 GB | 434.024 GB | **4.64** |
| MXFP4 + Q8_0 Engram | MXFP4 | 4.00 | 299.052 GB | Q8_0 | 8.50 | 208.902 GB | 507.954 GB | **5.43** |

The size split is exact for the completed local ten-shard artifacts. “Two
Engram tables” means only `blk.1.engram_embd.weight` and
`blk.14.engram_embd.weight`. “Backbone and other data” is the total shard size
minus those two tensor payloads, so it also includes embeddings, output and
auxiliary tensors, metadata, alignment, and per-shard overhead.

The nominal BPW column describes the named storage format, not every tensor in
the file. These are deliberately hybrid models: numerically sensitive tensors
remain in higher precision, and K-quant presets may select different types for
different matrices. Consequently, effective whole-model BPW is the useful
number for comparing final download sizes.

The MXFP4 conversion is also mixed precision, not a pure 4-bit model and not a
Q8-equivalent model. Its 1,046 tensors are stored as 120 MXFP4, 332 Q8_0, 65
BF16, and 529 F32 tensors. Both Engram tables are Q8_0.

The antirez-like variant is a deliberately asymmetric MoE quant. Routed
`gate` and `up` expert matrices use IQ2_XXS, while routed `down` matrices use
Q2_K. Attention projections, shared-expert matrices, the output head, and
Engram WKV use Q8_0; token embeddings and Engram Q/K remain BF16. The two
large Engram embedding tables are Q8_0. The quant was produced with the same
published 262,144-token importance matrix used for the other imatrix variants.

### Protected Q2_K: faster than our earlier antirez-like CUDA release

The new `Q2_K_Protected-Q8` release revises **our own earlier
[IQ2_XXS_GU-Q2_K_Down-Q8](https://huggingface.co/smalinin/DeepSeek-V4.1-Flash-GGUF/tree/main/IQ2_XXS_GU-Q2_K_Down-Q8)**
recipe for this CUDA llama.cpp runtime. That earlier recipe was inspired by
antirez's Q2 design; neither release is a requantization of
[antirez's GGUF](https://huggingface.co/antirez/deepseek-v4.1-flash-gguf).
It was quantized from our MXFP4 conversion using the published
262,144-token imatrix. Antirez reports an 8,192-token imatrix for his
DwarfStar release; a larger calibration set is useful coverage, but does not
by itself prove better output quality.

The original antirez release is a **design reference, not the speed baseline**
for the comparison below:

| Design choice | [Original antirez Q2](https://huggingface.co/antirez/deepseek-v4.1-flash-gguf) | This Protected Q2_K release |
| --- | --- | --- |
| Routed gate/up | IQ2_XXS | Q2_K |
| Routed down | Q2_K | Q3_K |
| Attention, shared experts, output | Q8 | Q5_K/Q6_K mixed policy |
| Engram tables | Native FP8 | Q8_0 |
| Activation-imatrix corpus | 8,192 tokens | 262,144 tokens |
| Whole Q2 download | 340.60 GiB | 385.00 GiB |

The extra bits on routed experts and larger calibration corpus are intended
to improve this CUDA-oriented precision/speed balance. The lower-precision
dense tensors, different Engram representation and different checkpoint
revisions mean the table is **not** proof of universally better quality.

Compared with our earlier IQ2_XXS/Q2_K antirez-like variant, this recipe
spends more precision on the routed experts: `gate` and `up` use Q2_K instead
of IQ2_XXS, and `down` uses Q3_K instead of Q2_K. The two huge Engram tables
remain Q8_0. Token embeddings, protected indexer K weights, Engram Q/K and
expert routers remain BF16; mHC tensors remain F32. Indexer Q projections
use Q8_0. To balance the larger expert matrices, attention projections and
the output head use Q6_K, shared-expert gate/up use Q5_K, shared-expert down
and Engram WKV use Q6_K. Those dense tensors were Q8_0 in the previous
antirez-like recipe, so **overall quality superiority has not been
established** without a matched evaluation.

On the maintainer's six-GPU CUDA setup, Protected Q2_K **generates faster
than our earlier IQ2_XXS_GU-Q2_K_Down-Q8 release** in this llama.cpp runtime.
This is a comparison between **our two GGUF variants**, not against antirez's
separate DwarfStar/Metal release. Using Q2_K/Q3_K CUDA kernels for routed
experts is consistent with the observed speedup, but its individual
contribution has not been isolated, and a matched public A/B table is not yet
available. One target-only smoke test of Protected Q2_K measured
`tg32 = 35.70 tok/s` after a 512-token prompt and
`pp60000 = 272.07 tok/s` with `ubatch=256`, six GPUs and a 64K fit context.
These are separate workloads, not a combined request or a quality score.
The extra precision costs space: 413.390 GB versus 371.438 GB for our
IQ2_XXS antirez-like variant. The two Q8_0 Engram tables are mmap/lazy
host-backed with the recommended launch options, not loaded wholesale into
VRAM.

## Which variant should I use?

- **Q2_K + Q5_K Engram** is the smallest release. It is the practical choice
  when storage, RAM, or aggregate GPU memory is the limiting factor.
- **IQ2_XXS gate/up + Q2_K down + Q8_0 Engram** is the antirez-like compact
  hybrid. It saves space in the routed experts while protecting the dense
  path and both Engram tables. It is smaller than IQ3_XS + Q8_0, but IQ2_XXS
  is an aggressive expert quantization and is not guaranteed to be faster
  than Q2_K on every CUDA backend.
- **Protected Q2_K + Q8_0 Engram** generates faster than our earlier
  `IQ2_XXS_GU-Q2_K_Down-Q8` variant on the maintainer's CUDA system. It
  protects routed expert precision and keeps Q8_0 Engram, at the cost of a
  larger download and lower precision
  for some dense tensors. Choose it when CUDA generation speed and the routed
  expert precision budget matter more than the smallest file size.
- **IQ3_XS + Q8_0 Engram** is the middle tier. It uses the calibration
  importance matrix and preserves both Engram tables in Q8_0.
- **MXFP4 + Q8_0 Engram** is the conversion source and highest-precision tier
  in this repository. It avoids a second backbone quantization pass, but is
  substantially larger.

Lower BPW can increase repetition or otherwise reduce output quality. Evaluate
the variants on your own prompts; the format name alone is not a quality
guarantee.

## Reproducible conversion

The source checkpoint used here is:

```text
deepseek-ai/DeepSeek-V4.1-Flash@dba1be0a40aa45a94ad051997016db3960a90277
```

The accepted MXFP4 artifact was converted with the DeepSeek-V4.1 converter at
`smalinin/llama.cpp` commit
`4c7025b52339fec48d8e8bdfcea905db80130b9c`. The examples below use local
paths only as placeholders; change them for your system.

### 0. Build the required branch

```bash
git clone --branch my_build_deepseek41 \
  https://github.com/smalinin/llama.cpp.git
cd llama.cpp

cmake -S . -B build \
  -DGGML_CUDA=ON \
  -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release -j \
  --target llama-server llama-quantize llama-imatrix llama-gguf-split

python3 -m pip install -r requirements.txt
```

Use the CUDA/toolchain settings appropriate for your system. The commands in
the following sections assume this checkout is assigned to `LLAMA_CPP`.

### 1. Create the MXFP4 GGUF

Install the converter requirements from the linked branch first, then run:

```bash
LLAMA_CPP=/path/to/llama.cpp
HF_MODEL=/path/to/DeepSeek-V4.1-Flash
OUT=/path/to/output

mkdir -p "$OUT/tmp"

TMPDIR="$OUT/tmp" \
/usr/bin/time -v python3 "$LLAMA_CPP/convert_hf_to_gguf.py" \
  "$HF_MODEL" \
  --outtype auto \
  --use-temp-file \
  --outfile "$OUT/DeepSeek-V4.1-Flash-MXFP4.gguf"
```

`--outtype auto` invokes the architecture-specific precision policy: supported
official block-FP4 expert weights are written as MXFP4, while tensors requiring
another representation are kept as Q8_0, BF16, or F32.

The conversion needs substantial temporary disk space and RAM. The reference
run had approximately 193 GiB peak RSS and took about 2 h 59 min on the build
machine.

### 2. Split the MXFP4 file

```bash
"$LLAMA_CPP/build/bin/llama-gguf-split" \
  --split \
  --split-max-size 48G \
  "$OUT/DeepSeek-V4.1-Flash-MXFP4.gguf" \
  "$OUT/DeepSeek-V4.1-Flash-MXFP4"
```

This produced ten shards. A single GGUF tensor cannot be split across files,
so a shard containing one of the approximately 104.45 GB Q8_0 Engram tables
can exceed the requested 48G limit.

## Importance matrix

All imatrix quants use the same 262,144-token calibration corpus and the
published `imatrix-dsv41-262144.gguf`. The accepted run used 512 chunks:

```bash
"$LLAMA_CPP/build/bin/llama-imatrix" \
  --model "$OUT/DeepSeek-V4.1-Flash-MXFP4-00001-of-00010.gguf" \
  --file /path/to/calibration.txt \
  --output "$OUT/imatrix-dsv41-262144.gguf" \
  --output-format gguf \
  --ctx-size 512 \
  --batch-size 512 \
  --ubatch-size 128 \
  --parallel 1 \
  --chunks 512 \
  --output-frequency 512 \
  --save-frequency 128 \
  --no-ppl \
  --parse-special \
  --no-escape \
  --n-gpu-layers auto \
  --split-mode layer \
  --fit on \
  --fit-ctx 512 \
  --fit-target 2048 \
  --load-mode mmap \
  --lazy-mode auto \
  --n-cpu-moe 0 \
  --flash-attn on
```

## Quantization commands

The quantizer reads the complete MXFP4 split set through its first shard.
`--keep-split` preserves the shard layout. The output path below is a base GGUF
name; the quantizer creates numbered shards.

### Q2_K backbone + Q5_K Engram

```bash
"$LLAMA_CPP/build/bin/llama-quantize" \
  --allow-requantize \
  --keep-split \
  --max-buffer-size 8192 \
  --imatrix "$OUT/imatrix-dsv41-262144.gguf" \
  --tensor-type 'engram_embd\.weight=q5_k' \
  "$OUT/DeepSeek-V4.1-Flash-MXFP4-00001-of-00010.gguf" \
  "$OUT/DeepSeek-V4.1-Flash-EngramQ5-Q2_K.gguf" \
  Q2_K 20
```

### IQ3_XS backbone + Q8_0 Engram

```bash
"$LLAMA_CPP/build/bin/llama-quantize" \
  --allow-requantize \
  --keep-split \
  --max-buffer-size 8192 \
  --imatrix "$OUT/imatrix-dsv41-262144.gguf" \
  --token-embedding-type q5_k \
  --tensor-type 'engram_embd\.weight=q8_0' \
  "$OUT/DeepSeek-V4.1-Flash-MXFP4-00001-of-00010.gguf" \
  "$OUT/DeepSeek-V4.1-Flash-IQ3_XS-Q8_0_Engram-imatrix.gguf" \
  IQ3_XS 20
```

### IQ2_XXS gate/up + Q2_K down + Q8_0 Engram (antirez-like)

```bash
"$LLAMA_CPP/build/bin/llama-quantize" \
  --allow-requantize \
  --keep-split \
  --max-buffer-size 8192 \
  --imatrix "$OUT/imatrix-dsv41-262144.gguf" \
  --tensor-type 'ffn_(gate|up)_exps\.weight=iq2_xxs' \
  --tensor-type 'ffn_down_exps\.weight=q2_k' \
  --tensor-type 'engram_(embd|wkv)\.weight=q8_0' \
  --tensor-type 'attn_.*\.weight=q8_0' \
  --tensor-type 'ffn_(gate|up|down)_shexp\.weight=q8_0' \
  --tensor-type '^output\.weight=q8_0' \
  --tensor-type '^token_embd\.weight=bf16' \
  "$OUT/DeepSeek-V4.1-Flash-MXFP4-00001-of-00010.gguf" \
  "$OUT/DeepSeek-V4.1-Flash-IQ2_XXS_GU-Q2_K_Down-Q8_0_Engram-imatrix.gguf" \
  Q2_K 20
```

### Protected Q2_K + Q8_0 Engram (faster than our IQ2_XXS/Q2_K variant on CUDA)

```bash
"$LLAMA_CPP/build/bin/llama-quantize" \
  --allow-requantize \
  --keep-split \
  --max-buffer-size 8192 \
  --imatrix "$OUT/imatrix-dsv41-262144.gguf" \
  --tensor-type '^blk\.[0-9]+\.ffn_(gate|up)_exps\.weight=q2_k' \
  --tensor-type '^blk\.[0-9]+\.ffn_down_exps\.weight=q3_k' \
  --tensor-type '^blk\.[0-9]+\.indexer\.attn_(k|q_b)\.weight=q8_0' \
  --tensor-type '^blk\.[0-9]+\.attn_(kv|output_a|output_b|q_a|q_b)\.weight=q6_k' \
  --tensor-type '^blk\.[0-9]+\.ffn_(gate|up)_shexp\.weight=q5_k' \
  --tensor-type '^blk\.[0-9]+\.ffn_down_shexp\.weight=q6_k' \
  --tensor-type '^output\.weight=q6_k' \
  --tensor-type '^token_embd\.weight=bf16' \
  --tensor-type '^blk\.[0-9]+\.engram_embd\.weight=q8_0' \
  --tensor-type '^blk\.[0-9]+\.engram_wkv\.weight=q6_k' \
  --tensor-type '^blk\.[0-9]+\.engram_(q|k)\.weight=bf16' \
  --tensor-type '^blk\.[0-9]+\.ffn_gate_inp\.weight=bf16' \
  --tensor-type '^blk\.[0-9]+\.hc_.*\.weight=f32' \
  "$OUT/DeepSeek-V4.1-Flash-MXFP4-00001-of-00010.gguf" \
  "$OUT/DeepSeek-V4.1-Flash-Protected-Q2_K-Q8_0_Engram-imatrix.gguf" \
  Q2_K 20
```

The quantizer keeps `indexer.attn_k.weight` in BF16 despite the requested
Q8_0 override; the audited dry run verified this protection before writing
the ten shards. The resulting GGUF is 4.42 effective BPW.

The final positional argument is the worker-thread count; tune it for your
machine. `--allow-requantize` is required because the source GGUF is already a
mixed-precision conversion.

## Running with `llama-server`

The following is the tested six-GPU profile for the Q2_K + Q5_K Engram release.
Adjust the GPU order, paths, thread counts, and fit target for your hardware.
For Protected Q2_K, use the same target-only profile and replace `--model`
with `Q2_K_Protected-Q8/DeepSeek-V4.1-Flash-Protected-Q2_K-Q8_0_Engram-imatrix-00001-of-00010.gguf`.

```bash
/path/to/llama.cpp/build/bin/llama-server \
  --model /path/to/Q2_K-Q5/DeepSeek-V4.1-Flash-EngramQ5-Q2_K-00001-of-00010.gguf \
  --host 127.0.0.1 \
  --port 8080 \
  --ctx-size 64000 \
  --batch-size 2048 \
  --ubatch-size 256 \
  --parallel 1 \
  --threads 4 \
  --n-gpu-layers auto \
  --split-mode layer \
  --fit on \
  --fit-ctx 64000 \
  --fit-target 1024 \
  --load-mode mmap \
  --lazy-mode auto \
  --flash-attn on \
  --n-cpu-moe 0 \
  --no-warmup \
  --no-context-shift \
  --jinja \
  --chat-template-kwargs '{"reasoning_effort":80,"enable_thinking":true}' \
  --reasoning-format deepseek \
  --no-reasoning-preserve \
  --no-prefill-assistant
```

### Important launch parameters

| Parameter | Purpose |
| --- | --- |
| `--ctx-size 64000` | Allocates a 64K-token context for the single server slot. A larger capacity increases cache and graph memory. |
| `--batch-size 2048` | Maximum logical prompt batch. It mainly affects prompt processing. |
| `--ubatch-size 256` | Physical micro-batch used to execute prompt work. Reduce it if graph memory is too high. |
| `--parallel 1` | Uses one server slot. With multiple slots, the configured context is divided among them. |
| `--n-gpu-layers auto --split-mode layer` | Lets the custom runtime place layers across the visible GPUs. |
| `--fit on --fit-ctx 64000 --fit-target 1024` | Runs the placement fitter for the requested context while targeting approximately 2 GiB of free VRAM per GPU. |
| `--load-mode mmap --lazy-mode auto` | Memory-maps the very large GGUF and allows the runtime to keep suitable tensors, notably Engram tables, lazily backed by host storage. |
| `--flash-attn on` | Enables the supported Flash Attention path. |
| `--n-cpu-moe 0` | Requests GPU placement for all MoE layers. Change this only when the model does not fit. |
| `--no-warmup` | Skips startup warm-up. Remove this option if you prefer to pay warm-up cost before the first real request. |
| `--no-context-shift` | Disables rolling context reuse. A request that exceeds the configured context must be rejected or shortened instead of silently shifting it. |
| `--jinja --chat-template-file ...` | Uses the supplied DeepSeek-V4.1 chat template. The template file is also included in this repository. |
| `reasoning_effort` | Template value from 1 to 100. Higher values request more thorough and usually longer reasoning; they do not change model weights. |
| `--reasoning-format deepseek` | Parses DeepSeek reasoning into the server's reasoning field. |
| `--no-reasoning-preserve` | Does not preserve extracted reasoning when assistant history is reconstructed. |
| `--no-prefill-assistant` | Disables assistant-message prefill. |

The two Engram tables are intentionally compatible with mmap/lazy host-backed
operation; total GGUF size is therefore not the same as required VRAM. Actual
RAM and VRAM requirements still depend on context length, batch sizes, GPU
topology, and placement selected by the fitter.

### Engram tables and VRAM

With the recommended `--load-mode mmap --lazy-mode auto` configuration, the
two giant `engram_embd.weight` lookup tables are **not loaded into VRAM**.
The DeepSeek-V4.1 runtime marks them for lazy host-side row access: their GGUF
storage is memory-mapped and only the requested rows are gathered for model
execution. Consequently, the approximately 135 GB Q5_K pair or 209 GB Q8_0
pair must not be added directly to the model's VRAM requirement.

Demanded mmap pages can become resident in the operating system's host RAM
page cache and may later be evicted. This is different from permanently
allocating the complete tables in RAM or VRAM. The smaller Engram Q/K and WKV
projection tensors are ordinary model tensors and can be placed separately by
the runtime/fitter.

This statement is specific to lazy mode. Disabling it with
`--lazy-mode off` makes the Engram tables follow ordinary tensor placement and
can dramatically increase RAM or VRAM requirements. Keep
`--load-mode mmap --lazy-mode auto` unless you intentionally want to test a
different placement policy.

## Optional DSpark sidecar

`DeepSeek-V4.1-Flash-DSpark-AUTO.gguf` is an experimental three-stage MTP
speculative-decoding sidecar (approximately 7.97 GB). It is **not enabled in
the recommended command above**: on the tested system it accepted draft tokens
correctly but reduced end-to-end generation speed. If you want to experiment,
add the following options and measure on your own workload:

```bash
  --spec-type draft-dspark \
  --spec-draft-model /path/to/DeepSeek-V4.1-Flash-DSpark-AUTO.gguf \
  --spec-draft-n-max 5 \
  --gpu-layers-draft auto
```

## Scope and limitations

- Text generation is supported; the checkpoint's vision tower is not mapped
  into these GGUF files.
- The native one-million-token training context has not been claimed as a
  validated deployment configuration here. The documented production profile
  uses a 64K context.
- Q2_K is an aggressive quantization. Repetition or quality loss at this size
  is a model-quantization limitation, not necessarily a runtime failure.
- Performance depends heavily on memory placement, PCIe topology, context
  length, page-cache state, and the number and type of GPUs. No universal
  tokens-per-second figure is claimed by this card.

## Samples

### Q2_K + Q5_K Engram

<p align="center">
  <img src="pelican_q2_q5.png" width="400px" alt="Q2_K sample">
</p>

### IQ3_XS + Q8_0 Engram

<p align="center">
  <img src="pelican_iq3_xs_q8.png" width="400px" alt="IQ3_XS sample">
</p>

- used opencode, toolcall, vision
<p align="center">
  <img src="wdp.png" width="400px" alt="IQ3_XS sample">
</p>


### IQ2_XXS gate/up + Q2_K down + Q8_0 Engram (antirez-like recipe)

<p align="center">
  <img src="pelican_iq2_xxs_q8.png" width="400px" alt="Antirez-like IQ2_XXS/Q2_K sample">
</p>

- used opencode, toolcall, vision
<p align="center">
  <img src="wdp_iq2_xxs.png" width="400px" alt="Antirez-like IQ2_XXS/Q2_K vision and tool-use sample">
</p>



### MXFP4 Higher-precision sample

<p align="center">
  <img src="pelican_mxfp4.png" width="400px" alt="MXFP4 higher-precision sample">
</p>



## Acknowledgements

The conversion and runtime work builds on `llama.cpp`, the official DeepSeek
checkpoint and reference implementation, and early DeepSeek-V4.1 conversion
and runtime work by `vcruz305` and `JigSawPT`.
