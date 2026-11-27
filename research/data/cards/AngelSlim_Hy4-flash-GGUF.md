---
language:
- zh
- en
base_model:
- tencent/Hy4-flash
---
[中文](./README_CN.md) ｜ English

<p align="center">
  <img src="https://github.com/Tencent/AngelSlim/blob/main/docs/source/assets/logos/angelslim_logo.png?raw=true" alt="AngelSlim" width="70%">
</p>

### A more accessible, comprehensive, and efficient toolkit for large model compression.

<p align="center">
  ✒️ <a href="https://arxiv.org/abs/2602.21233">TechnicalReport</a>&nbsp;&nbsp;|&nbsp;&nbsp;📖 <a href="https://angelslim.readthedocs.io/">Documentation</a>&nbsp;&nbsp;|&nbsp;&nbsp;🤗 <a href="https://huggingface.co/AngelSlim">Hugging Face</a>&nbsp;&nbsp;|&nbsp;&nbsp;🤖 <a href="https://modelscope.cn/organization/AngelSlim">ModelScope</a>
  <br>
  💬 <a href="https://github.com/Tencent/AngelSlim/blob/main/docs/source/assets/angel_slim_wechat.png?raw=true">WeChat</a>&nbsp;&nbsp;|&nbsp;&nbsp;🫨 <a href="https://discord.com/invite/dHVNeuNdFt">Discord</a>
</p>

<p align="center">
  <img src="https://huggingface.co/AngelSlim/Hy4-flash-GGUF/resolve/main/angelslim-hy4flash-edge-light.gif" alt="AngelSlim x Hy4-flash: bringing a 224B-parameter MoE model to the devices on your desk" width="100%">
</p>


# Hy4-flash GGUF

Five GGUF builds of Hy4-flash: [tencent/Hy4-flash](https://huggingface.co/tencent/Hy4-flash)

| file                             | model size | bpw (overall) | bpw (excl. Engram table) |
| -------------------------------- | ---------: | ------------: | -----------------------: |
| `Hy4-flash-Q4_K_M.gguf`          | 156.79 GiB | 6.05          | 5.27                     |
| `Hy4-flash-SPARK-4Bit.gguf`      | 151.3 GiB  | 5.84          | 4.78                     |
| `Hy4-flash-SPARK-4Bit-Fast.gguf` | 148.6 GiB  | 5.74          | 4.63                     |
| `Hy4-flash-Q3_K.gguf`            | 144.70 GiB | 5.58          | 4.62                     |
| `Hy4-flash-IQ2-AH.gguf`          | 125.73 GiB | 4.85          | 3.60                     |

![Hy4-flash GGUF benchmark results](https://huggingface.co/AngelSlim/Hy4-flash-GGUF/resolve/main/hy4-flash-gguf-benchmark.png)

---

## 1. What these are

`Hy4-flash-Q4_K_M.gguf` — standard 4-bit, the safe default. The routed experts follow llama.cpp's
Q4_K_M recipe: `gate`/`up` are Q4_K, and `down` gets Q6_K on 19 layers via llama.cpp's fixed rule and
Q4_K on the other 22. Most non-expert weights are Q8_0. **Use this unless you are memory-constrained.**

`Hy4-flash-SPARK-4Bit.gguf` — the SPARK-4Bit build (NVIDIA's 4-bit floating-point format). **Suited for Spark devices.**

`Hy4-flash-SPARK-4Bit-Fast.gguf` — a variant of the SPARK-4Bit build, 2.7 GiB smaller. **Also suited for Spark devices.**

`Hy4-flash-Q3_K.gguf` — mixed Q3_K/Q4_K experts. The routed-expert `gate`/`up` projections keep
Q4_K on 19 layers chosen by quantization sensitivity and drop to Q3_K on the other 22; `down` is Q4_K.
Everything outside the routed experts is the same as Q4_K_M.

`Hy4-flash-IQ2-AH.gguf` — the smallest of the five. The routed-expert `gate`/`up` projections run
at 2.0625 bpw (IQ2_XXS) and `down` at Q4_K, while most non-expert weights stay in BF16 rather than Q8_0.


**Strata** support: see PR [#7120](https://github.com/Niko1221/Strata/pull/7120).

## 2. SPEED

### 2.1 llama.cpp

The test was conducted in real workbuddy scenarios and cases.

**Mac M5 Max 128GB**

| format | Prefill tok/s (4K / 16K / 32K) | Decode tok/s (4K / 16K / 32K) |
| ------ | ----------------------------: | ----------------------------: |
| Q4_K_M | 629.8 / 448.1 / 418.6         | 48.13 / 45.18 / 44.15         |
| Q3_K   | 743.2 / 563.0 / 520.6         | 50.34 / 49.47 / 47.37         |

For code generation, Q3_K reaches up to 70 tok/s.

**RTX Spark 128GB**

| format          | Prefill tok/s (4K / 16K / 32K) | Decode tok/s (4K / 16K / 32K) |
| --------------- | ----------------------------: | ----------------------------: |
| SPARK-4Bit-Fast | 799 / 717 / 707               | 31.95 / 33.14 / 33.39         |
| SPARK-4Bit      | 765 / 686 / 666               | 25.80 / 28.16 / 30.3          |

For code generation, SPARK-4Bit-Fast reaches up to 40 tok/s.

### 2.2 Strata

**NVIDIA CUDA — 16 GiB VRAM budget**

Full Q4_K_M_MTP_Q8_0 model, 4K input / 512 output tokens, 33,024-token context limit; one run per workload.

| Workload | Decode tok/s (drafting off) | Decode tok/s (DFly Q8_0) |
| -------- | -------------------------: | -----------------------: |
| Prose    | 36.8                       | 38.7                     |
| Code     | 37.5                       | 47.6                     |

**Mac mini M4 Pro 64GB**

IQ2 model, MTP k=2, 8K context: prefill **125–127 tok/s**, decode **17.3 tok/s**
(256 generated tokens; geometric mean of four prompts' medians).

These results use different test conditions from the llama.cpp results above.

## 3. How to use

### 3.1 llama.cpp

**General Usage**

The support is in PR [#32517](https://github.com/ggml-org/llama.cpp/pull/32517) and not merged yet, so check out the PR branch:

```sh
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
git fetch origin pull/32517/head:hy4-flash
git checkout hy4-flash
```

Build:
```sh
cmake -B build                # add -DGGML_CUDA=ON for NVIDIA GPUs; Metal is on by default on macOS
cmake --build build --config Release -j
```

Chat in the terminal:
```sh
./build/bin/llama-cli -m Hy4-flash-Q4_K_M-00001-of-00002.gguf -c 8192 -ngl 99 --jinja
```

OpenAI-compatible server (http://localhost:8080):
```sh
./build/bin/llama-server -m Hy4-flash-Q4_K_M-00001-of-00002.gguf -c 8192 -ngl 99 --jinja --port 8080
```

Image input, with the mmproj file:
```sh
./build/bin/llama-mtmd-cli -m Hy4-flash-Q4_K_M-00001-of-00002.gguf --mmproj mmproj-Hy4-flash-bf16.gguf \
    --image photo.png -p "Describe this image." -c 8192 -ngl 99 --jinja
```


**Mac M5 Max 128GB**

See [README_MAC-Metal.md](https://huggingface.co/AngelSlim/Hy4-flash-GGUF/blob/main/README_MAC-Metal.md)


**RTX Spark 128GB**

See [README_SPARK-4Bit.md](https://huggingface.co/AngelSlim/Hy4-flash-GGUF/blob/main/README_SPARK-4Bit.md)

### 3.2 Strata

Support for NVIDIA CUDA and Apple Silicon Metal is in PR
[#7120](https://github.com/Niko1221/Strata/pull/7120). Check out the PR branch:

```sh
git clone https://github.com/Niko1221/Strata
cd Strata
git fetch origin pull/7120/head:hy4-flash-gguf
git checkout hy4-flash-gguf
```

Follow the [CUDA guide](https://github.com/sjl623/Strata/blob/777267388d3d3316fccee91b521c5a6c60e782ef/docs/hy4-flash/README.md)
or [Metal guide](https://github.com/sjl623/Strata/blob/777267388d3d3316fccee91b521c5a6c60e782ef/docs/hy4-flash/README_MAC-Metal.md)
to build the engine and install dependencies. Keep both GGUF shards together.

**NVIDIA CUDA** — Q4_K_M_MTP_Q8_0, with CPU expert offload and MTP / DFly support:

```sh
MODEL=/path/to/Hy4-flash-Q4_K_M_MTP_Q8_0-00001-of-00002.gguf CTX=32768 \
  ./tools/hy4_flash/launch-hy4-flash.sh --no-tui
```

**Apple Silicon Metal** — IQ2, with SSD expert streaming and built-in MTP:

```sh
MODEL=/path/to/Hy4-flash-IQ2_AH-00001-of-00002.gguf \
  STRATA_BIN="$PWD/build-metal/strata" KV=fp16 CTX=32768 MTP=on DRAFT_TOKENS=2 \
  ./tools/hy4_flash/launch-hy4-flash.sh --no-tui
```

The OpenAI-compatible API runs at `http://localhost:8080/v1`.
For images, place `mmproj-Hy4-flash-bf16.gguf` beside the model and add `--vision on`.
