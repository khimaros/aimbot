---
license: mit
base_model: deepseek-ai/DeepSeek-V4.1-Flash
base_model_relation: quantized
library_name: gguf
pipeline_tag: text-generation
tags:
- gguf
- deepseek
- deepseek-v4.1
- llama.cpp
quantized_by: vcruz305
---

# DeepSeek-V4.1-Flash GGUF

llama.cpp GGUF of [deepseek-ai/DeepSeek-V4.1-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash).

This is **V4.1-Flash** (`DeepseekV41ForCausalLM`), a causal decoder with engram n-gram lookup
tables, hyper-connections and sparse attention. It is not V4-Flash-0731.

## Recipe

How to build the engine, serve it, and the gotchas, plus the current status:
[vcruz305/DeepSeek-V4.1-Flash-GGUF-DGX-Spark-recipe](https://github.com/vcruz305/DeepSeek-V4.1-Flash-GGUF-DGX-Spark-recipe)

## Status

**These files do not run on upstream llama.cpp yet.** Conversion works and is open as
[ggml-org/llama.cpp#28696](https://github.com/ggml-org/llama.cpp/pull/28696). The runtime is in
progress on the `runtime/deepseek41` branch of
[vcruz305/llama.cpp](https://github.com/vcruz305/llama.cpp): the loader, the engram tables and the
hyper-connections work and are verified against the reference implementation, and the sparse
attention is the remaining piece.

Weights land here as each rung finishes. Anything converted before 2026-09-10 carries
`general.architecture = deepseek4` and is being redone as `deepseek41`.

The architecture string is `deepseek41`, following llama.cpp's habit of dropping the `_v`
(`deepseek_v2` became `deepseek2`, `deepseek_v3.2` became `deepseek32`).

**2026-09-11 fix:** the 4 Engram KV keys (`head_count`, `key_length`, `max_ngram_size`,
`layer_ids`) were written with a hardcoded `deepseek4.engram.*` prefix instead of resolving
`{arch}.engram.*` like every other arch-scoped key in the file. `general.architecture` and all
38 other arch-scoped keys were already correct (`deepseek41.*`); only these 4 were wrong, which
would have made the `runtime/deepseek41` loader fail to find Engram config on an otherwise
loadable file. Fixed in place via a KV-only rewrite (tensor data untouched, verified
byte-identical by SHA-256) on all five quant rungs' first shard, where GGUF split files store
metadata. Confirmed live: all five now read `deepseek41.engram.*`.

## Files

Ladder in order: **Q2_K, Q3_K_M, Q4_K_M**. Measured tensor payload:

| File | Quant | Bytes | GiB |
| --- | --- | ---: | ---: |
| `DeepSeek-V4.1-Flash-Q2_K.gguf` | Q2_K | 264,514,761,248 | 246.3 |
| `DeepSeek-V4.1-Flash-Q3_K_M.gguf` | Q3_K_M | 347,270,954,112 | 323.4 |
| `DeepSeek-V4.1-Flash-Q4_K_M.gguf` | Q4_K_M | pending | |

Split into parts, since each exceeds the Hub's single file limit.

### Withdrawn

**Q1_0 was removed on 2026-09-12.** It loaded and ran, and it emitted one repeated token for
every prompt, so it was not a usable rung.

The cause is the format rather than the pack. Three routed expert matrices and the engram table
are 99% of that file, and q1_0 gives back every weight in a 128 wide block at a single magnitude
with a sign on it, at 1.125 bpw, with no way to express that a weight is small. Rebuilding it
with every other tensor at q6_K, which is higher precision than the working Q2_K rung carries,
produced the same single token, and the same token across unrelated prompts. Lifting the experts
and the engram table off one bit costs about what Q2_K costs, and Q2_K already works.

Q2_K is the floor.

Q5_K_M is skipped unless asked for. The routed experts arrive as MXFP4 at 4.25 bpw, so higher rungs
move parts of the mixture *up* rather than down: Q3_K_M already lands at 0.684 of the Q8_0 staging
file, and Q5_K_M would be close enough to Q8_0 to be poor value.

Most of the file is the two engram tables, roughly 196.6B parameters between them. They follow the
rung, 99,611 to 40,284 MiB each between q8_0 and q3_K.

Apache/MIT from upstream. Credit: DeepSeek. GGUF pack: Victor Cruz (`vcruz305`).
