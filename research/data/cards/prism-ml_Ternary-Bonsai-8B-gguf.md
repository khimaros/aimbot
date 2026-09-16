---
license: apache-2.0
library_name: gguf
pipeline_tag: text-generation
tags:
- ternary
- 1.58-bit
- gguf
- llama-cpp
- q2_0
- on-device
- prismml
- bonsai
base_model:
- prism-ml/Ternary-Bonsai-8B-unpacked
---

<p align="center">
  <img src="./assets/bonsai-logo.svg" width="280" alt="Bonsai">
</p>

<p align="center">
  <a href="https://prismml.com"><b>Prism ML Website</b></a> &nbsp;|&nbsp;
  <a href="https://github.com/PrismML-Eng/Bonsai-demo/blob/main/ternary-bonsai-8b-whitepaper.pdf"><b>White Paper</b></a> &nbsp;|&nbsp;
  <a href="https://github.com/PrismML-Eng/Bonsai-demo"><b>Demo &amp; Examples</b></a> &nbsp;|&nbsp;
  <a href="https://discord.gg/prismml"><b>Discord</b></a>
</p>

# Ternary-Bonsai-8B-gguf

Ternary (1.58-bit) language model in GGUF Q2_0 format for `llama.cpp`


<p align="center">
  <img src="./assets/frontier.svg" width="680" alt="Pareto Frontier">
</p>

## Resources

- **[White Paper](https://github.com/PrismML-Eng/Bonsai-demo/blob/main/ternary-bonsai-8b-whitepaper.pdf)**
- **[Demo repo](https://github.com/PrismML-Eng/Bonsai-demo)** — examples for serving, benchmarking, and integrating Bonsai
- **[Discord](https://discord.gg/prismml)** — community support and updates
- **Kernels**: Q2_0 is not yet in mainline `llama.cpp`. Use our fork at [PrismML-Eng/llama.cpp](https://github.com/PrismML-Eng/llama.cpp) (`prism` branch, default) which adds Q2_0 support for CPU (NEON/generic) and Metal. Upstream PR coming soon.

## Model Overview

| Item             | Specification                                                            |
| :--------------- | :----------------------------------------------------------------------- |
| Base model       | Qwen3-8B                                                                 |
| Parameters       | 8.19B (~6.95B non-embedding)                                             |
| Architecture     | GQA (32 query / 8 KV heads), SwiGLU MLP, RoPE, RMSNorm                   |
| Layers           | 36 Transformer decoder blocks                                            |
| Context length   | 65,536 tokens                                                            |
| Vocab size       | 151,936                                                                  |
| Weight format    | GGUF Q2_0 g128: {-1, 0, +1} with FP16 group-wise scaling                 |
| Packed Q2_0 size | **2.03 GiB** (2.18 GB)                                                   |
| Ternary coverage | Embeddings, attention projections, MLP projections, LM head              |
| License          | Apache 2.0                                                               |

## Quantization Format: GGUF Q2_0 (g128)

Each weight takes a value from {-1, 0, +1}, with one shared FP16 scale per group of 128 weights:

```
w_i = scale_g * t_i,    t_i in {-1, 0, +1}
```

Q2_0 encodes each weight as a 2-bit code `q in {0, 1, 2, 3}`, dequantized via `w = (q - 1) * scale`. One 128-element block is 34 bytes (2 bytes FP16 scale + 32 bytes of packed 2-bit codes) for an effective **2.125 bits/weight**. The fourth code point (`q = 3`, reconstructing to `+2 * scale`) is reserved for future extensions; for ternary weights it is unused.

### Memory

| Format            | Size         | Reduction | Ratio      |
| :---------------- | ----------:  | --------: | ---------: |
| FP16              | 16.38 GB     | --        | 1.0x       |
| **GGUF Q2_0 g128**| **2.03 GiB** (2.18 GB) | **86.7%** | **7.5x**   |

## Files in this repo

| File                            | Format | Size   | Recommended |
| :------------------------------ | :----- | -----: | :---------- |
| `Ternary-Bonsai-8B-F16.gguf`    | FP16   | 16.38 GB | baseline / re-quantization source |
| `Ternary-Bonsai-8B-Q2_0.gguf`   | Q2_0 (g128) | 2.03 GiB | **recommended** (lossless for ternary) |

## Quickstart

### Build from the Prism fork

```bash
git clone https://github.com/PrismML-Eng/llama.cpp
cd llama.cpp
cmake -B build -DGGML_METAL=ON   # or -DGGML_CUDA=ON, -DGGML_VULKAN=ON
cmake --build build -j
```

### `llama.cpp` CLI

```bash
./build/bin/llama-cli \
  -m Ternary-Bonsai-8B-Q2_0.gguf \
  -p "Explain quantum computing in simple terms." \
  -n 256
```

### `llama.cpp` server

```bash
./build/bin/llama-server -m Ternary-Bonsai-8B-Q2_0.gguf -c 4096
```


## Throughput (llama.cpp, Apple M4 Pro 48 GB)

| Backend          | PP512 (tok/s) | TG128 (tok/s) |
| :--------------- | ------------: | ------------: |
| Metal (GPU)      | 455           | **76**        |
| NEON CPU (10 t)  | 146           | **32**        |

Flags: `-ngl 99 -fa 1` for Metal; `-ngl 0 -fa 1 -t 10` for CPU.

## Benchmarks

Evaluated with EvalScope v1.4.2 + vLLM 0.15.1 on NVIDIA H100 under identical infrastructure, generation parameters, and scoring. All models are in the 6B-9B parameter range.

| Model                     | Size         | Avg      | MMLU-R | MuSR | GSM8K | HE+  | IFEval | BFCL |
| :------------------------ | ----------:  | -------: | -----: | ---: | ----: | ---: | -----: | ---: |
| Qwen 3 8B                 | 16.38 GB     | **79.3** | 83     | 55   | 93    | 82.3 | 81.5   | 81   |
| **Ternary Bonsai 8B**     | **2.18 GB**  | **75.5** | 72.6   | 56.2 | 91    | 77.4 | 81.8   | 73.9 |
| *1-bit Bonsai 8B (prior)* | *1.15 GB*    | *70.5*   | 65.7   | 50   | 88    | 73.8 | 79.8   | 65.7 |
| RNJ 8B                    | 16.63 GB     | **73.1** | 75.5   | 50.4 | 93.7  | 84.2 | 73.8   | 61.1 |
| Ministral3 8B             | 16.04 GB     | **71.0** | 68.9   | 53.8 | 87.9  | 72.6 | 67.4   | 75.4 |
| Olmo 3 7B                 | 14.60 GB     | **70.9** | 72     | 56.1 | 92.5  | 79.3 | 87.1   | 38.4 |

Ternary Bonsai 8B ranks **2nd** among all compared models despite being 1/8th the size.

## Intelligence Density

```
density = -ln(1 - score/100) / size_GB
```

| Model                     | Size        | Intelligence Density (1/GB) |
| :------------------------ | ----------: | --------------------------: |
| **Ternary Bonsai 8B**     | **2.18 GB** | **0.645**                   |
| *1-bit Bonsai 8B (prior)* | *1.15 GB*   | *1.062*                     |
| Qwen 3 8B                 | 16.38 GB    | 0.096                       |
| RNJ 8B                    | 16.62 GB    | 0.079                       |

## Citation

```bibtex
@techreport{ternarybonsai,
    title   = {Ternary Bonsai: 1.58-bit Language Models at 8B, 4B, and 1.7B Scale},
    author  = {Prism ML},
    year    = {2026},
    month   = {April},
    url     = {https://prismml.com}
}
```

## Contact

For questions, feedback, or collaboration inquiries: **contact@prismml.com**