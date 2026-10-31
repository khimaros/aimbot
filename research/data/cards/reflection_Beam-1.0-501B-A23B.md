---
license: apache-2.0
language:
  - en
pipeline_tag: text-generation
tags:
  - mixture-of-experts
  - reasoning
  - code
  - tool-use
---

<p align="center">
  <img src="https://cdn-uploads.huggingface.co/production/uploads/620a77b7dbba8fc1fbb8bdb4/N-HiEVXlqtoniRSdFo0RG.png" width="100%" alt="Model Card banner">
</p>


<p align="center">
  <a href="https://huggingface.co/reflection">Hugging Face</a> |
  <a href="https://github.com/reflection-oss">GitHub</a> |
  <a href="https://reflection.ai/blog">Launch Blog</a> |
  <a href="https://developers.reflection.ai/introduction">Documentation</a> |
  Technical Report (coming)
  <br>
  <b>License</b>: <a href="https://huggingface.co/reflection/Beam-1.0-501B-A23B/blob/main/LICENSE">Apache 2.0</a> |
  <b>Authors</b>: <a href="https://reflection.ai/">Reflection</a>
</p>

Beam is an open model built by Reflection. Beam takes text as input and generates text as output. This release includes the instruction-tuned model in BF16, FP8, and NVFP4 numerics. Beam uses a sparse mixture-of-experts (MoE) architecture with 501B total parameters and 23B active parameters. It supports a context window of 1M tokens and was developed predominantly for English.

### Primary capabilities

- **Token-efficient reasoning:** Reaches comparable solution quality to leading open models using approximately 3x fewer inference-time reasoning tokens.

- **Software engineering:** Resolves real-world GitHub issues, operates in CLI and DevOps environments, and integrates directly with agentic coding harnesses. Code generation supported across languages.

- **Agentic tool use:**  Long-horizon task completion, MCP-based tool integration, and browsing. Executes multi-step workflows from natural-language instructions.

- **Reasoning (math and science):** Graduate-level science problem solving, theorem proving, and applied mathematics. Reasoning quality transfers to debugging, planning, and self-correction during agentic execution.

## Model Overview

Beam models are designed to deliver strong performance for areas such as agentic tool use, coding and general reasoning with an emphasis on token efficient usage.

<div class="dark:hidden" style="overflow-x:auto;">
<table align="center" style="display:table;width:auto;max-width:100%;margin-left:auto;margin-right:auto;border-collapse:collapse;">
<thead>
<tr>
<th scope="col" style="padding:12px;text-align:left;background:#274E13;color:#FFFFFF;border-bottom:2px solid #274E13;">Property</th>
<th scope="col" style="padding:12px;text-align:center;background:#274E13;color:#FFFFFF;border-bottom:2px solid #274E13;">Beam 501B A23B MoE</th>
</tr>
</thead>
<tbody>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1">Total Parameters</th>
<td style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1">501.3B</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1">Active Parameters</th>
<td style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1">23.4B</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1">Layers</th>
<td style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1">52: 3 dense + 49 MoE</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1">Attention</th>
<td style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1">Gated GQA + Sliding Window Attention</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1">Context Length</th>
<td style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1">1M</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1">Vocabulary Size</th>
<td style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1">152k tokens</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1">Expert Count</th>
<td style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1">256</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1">Supported Modalities</th>
<td style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1">Text</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1">Chat Template</th>
<td style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1">Modified Harmony format</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1">Numerics</th>
<td style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1">BF16, FP8, NVFP4</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1">Knowledge cutoff</th>
<td style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1">June 30, 2026</td>
</tr>
</tbody>
</table>
</div>
<div class="hidden dark:block" style="overflow-x:auto;">
<table align="center" style="display:table;width:auto;max-width:100%;margin-left:auto;margin-right:auto;border-collapse:collapse;">
<thead>
<tr>
<th scope="col" style="padding:12px;text-align:left;background:#274E13;color:#FFFFFF;border-bottom:2px solid #274E13;">Property</th>
<th scope="col" style="padding:12px;text-align:center;background:#274E13;color:#FFFFFF;border-bottom:2px solid #274E13;">Beam 501B A23B MoE</th>
</tr>
</thead>
<tbody>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">Total Parameters</th>
<td style="padding:10px 12px;text-align:left;color:#B7C2B6;border-bottom:1px solid #243624">501.3B</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">Active Parameters</th>
<td style="padding:10px 12px;text-align:left;color:#B7C2B6;border-bottom:1px solid #243624">23.4B</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">Layers</th>
<td style="padding:10px 12px;text-align:left;color:#B7C2B6;border-bottom:1px solid #243624">52: 3 dense + 49 MoE</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">Attention</th>
<td style="padding:10px 12px;text-align:left;color:#B7C2B6;border-bottom:1px solid #243624">Gated GQA + Sliding Window Attention</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">Context Length</th>
<td style="padding:10px 12px;text-align:left;color:#B7C2B6;border-bottom:1px solid #243624">1M</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">Vocabulary Size</th>
<td style="padding:10px 12px;text-align:left;color:#B7C2B6;border-bottom:1px solid #243624">152k tokens</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">Expert Count</th>
<td style="padding:10px 12px;text-align:left;color:#B7C2B6;border-bottom:1px solid #243624">256</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">Supported Modalities</th>
<td style="padding:10px 12px;text-align:left;color:#B7C2B6;border-bottom:1px solid #243624">Text</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">Chat Template</th>
<td style="padding:10px 12px;text-align:left;color:#B7C2B6;border-bottom:1px solid #243624">Modified Harmony format</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">Numerics</th>
<td style="padding:10px 12px;text-align:left;color:#B7C2B6;border-bottom:1px solid #243624">BF16, FP8, NVFP4</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">Knowledge cutoff</th>
<td style="padding:10px 12px;text-align:left;color:#B7C2B6;border-bottom:1px solid #243624">June 30, 2026</td>
</tr>
</tbody>
</table>
</div>

## Benchmark Results

These models were evaluated against a large collection of different datasets and metrics to cover different aspects of text generation. Evaluation results marked in the table are for instruction-tuned models spanning all released numerics. Note: All evaluations were done using temp=0.7, top_p=0.99.

<div class="dark:hidden" style="overflow-x:auto;">
<table align="center" style="display:table;width:auto;max-width:100%;margin-left:auto;margin-right:auto;border-collapse:collapse;">
<thead>
<tr>
<th scope="col" style="padding:12px;text-align:left;background:#274E13;color:#FFFFFF;border-bottom:2px solid #274E13;">Benchmark</th>
<th scope="col" style="padding:12px;text-align:center;background:#274E13;color:#FFFFFF;border-bottom:2px solid #274E13;">Beam<br>(BF16)</th>
<th scope="col" style="padding:12px;text-align:center;background:#274E13;color:#FFFFFF;border-bottom:2px solid #274E13;">Beam<br>(FP8)</th>
<th scope="col" style="padding:12px;text-align:center;background:#274E13;color:#FFFFFF;border-bottom:2px solid #274E13;">Beam<br>(NVFP4)</th>
</tr>
</thead>
<tbody>
<tr><th colspan="4" scope="colgroup" style="padding:10px 12px;text-align:left;background:#D9E8D1;color:#274E13;border-bottom:1px solid #B8CFA9;">Agentic Coding / Terminal</th></tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">DeepSWE v1.1</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">43.3%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">43.0%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">42.7%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">SWE Bench Pro v2-Hard</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">76.5%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">78.4%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">78.6%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">SWE Bench Pro v1</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">66.1%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">65.9%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">65.6%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">Terminal Bench v2.1</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">80.1%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">78.9%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">78.4%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">SWE Atlas Codebase QnA</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">31.8%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">32.2%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">31.4%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">SWEBench Multilingual</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">78.3%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">78.1%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">77.5%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">SWEBench Verified</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">81.6%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">80.2%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">80.7%</td>
</tr>
<tr><th colspan="4" scope="colgroup" style="padding:10px 12px;text-align:left;background:#D9E8D1;color:#274E13;border-bottom:1px solid #B8CFA9;">Reasoning</th></tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">AIME 2026</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">97.7%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">98.0%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">97.5%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">HLE (no tools)</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">36.0%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">36.0%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">34.8%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">HLE (with tools)</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">51.1%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">51.1%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">51.1%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">SciCode</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">49.2%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">48.3%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">46.9%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">CriPT AA</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">16.3%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">17.4%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">15.4%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">GPQA Diamond</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">90.6%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">90.3%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">89.3%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">LiveCodeBench</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">88.3%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">88.1%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">88.3%</td>
</tr>
<tr><th colspan="4" scope="colgroup" style="padding:10px 12px;text-align:left;background:#D9E8D1;color:#274E13;border-bottom:1px solid #B8CFA9;">Tool Calling / Search</th></tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">AutomationBench - public split only</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">39.3%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">38.2%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">39.8%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">MCP Atlas</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">80.8%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">81.5%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">80.5%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">Tau3 Banking</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">36.1%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">36.8%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">35.4%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">BrowseComp w/ context management</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">76.8%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">76.7%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">75.6%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">DeepSearchQA w/ context management</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">80.5%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">79.6%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">81.1%</td>
</tr>
<tr><th colspan="4" scope="colgroup" style="padding:10px 12px;text-align:left;background:#D9E8D1;color:#274E13;border-bottom:1px solid #B8CFA9;">General Capabilities</th></tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">AA-LCR</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">78.2%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">79.4%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">78.7%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">LongBench v2</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">67.5%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">67.6%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">67.2%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">IFBench</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">79.6%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">80.7%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">79.2%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">AA Omniscience (index) - public split only</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">10.8</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">8.8</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">9.8</td>
</tr>
</tbody>
</table>
</div>
<div class="hidden dark:block" style="overflow-x:auto;">
<table align="center" style="display:table;width:auto;max-width:100%;margin-left:auto;margin-right:auto;border-collapse:collapse;">
<thead>
<tr>
<th scope="col" style="padding:12px;text-align:left;background:#274E13;color:#FFFFFF;border-bottom:2px solid #274E13;">Benchmark</th>
<th scope="col" style="padding:12px;text-align:center;background:#274E13;color:#FFFFFF;border-bottom:2px solid #274E13;">Beam<br>(BF16)</th>
<th scope="col" style="padding:12px;text-align:center;background:#274E13;color:#FFFFFF;border-bottom:2px solid #274E13;">Beam<br>(FP8)</th>
<th scope="col" style="padding:12px;text-align:center;background:#274E13;color:#FFFFFF;border-bottom:2px solid #274E13;">Beam<br>(NVFP4)</th>
</tr>
</thead>
<tbody>
<tr><th colspan="4" scope="colgroup" style="padding:10px 12px;text-align:left;background:#152414;color:#C9DCB8;border-bottom:1px solid #29422A">Agentic Coding / Terminal</th></tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">DeepSWE v1.1</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">43.3%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">43.0%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">42.7%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">SWE Bench Pro v2-Hard</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">76.5%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">78.4%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">78.6%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">SWE Bench Pro v1</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">66.1%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">65.9%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">65.6%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">Terminal Bench v2.1</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">80.1%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">78.9%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">78.4%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">SWE Atlas Codebase QnA</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">31.8%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">32.2%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">31.4%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">SWEBench Multilingual</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">78.3%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">78.1%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">77.5%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">SWEBench Verified</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">81.6%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">80.2%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">80.7%</td>
</tr>
<tr><th colspan="4" scope="colgroup" style="padding:10px 12px;text-align:left;background:#152414;color:#C9DCB8;border-bottom:1px solid #29422A">Reasoning</th></tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">AIME 2026</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">97.7%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">98.0%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">97.5%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">HLE (no tools)</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">36.0%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">36.0%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">34.8%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">HLE (with tools)</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">51.1%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">51.1%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">51.1%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">SciCode</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">49.2%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">48.3%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">46.9%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">CriPT AA</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">16.3%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">17.4%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">15.4%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">GPQA Diamond</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">90.6%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">90.3%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">89.3%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">LiveCodeBench</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">88.3%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">88.1%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">88.3%</td>
</tr>
<tr><th colspan="4" scope="colgroup" style="padding:10px 12px;text-align:left;background:#152414;color:#C9DCB8;border-bottom:1px solid #29422A">Tool Calling / Search</th></tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">AutomationBench - public split only</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">39.3%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">38.2%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">39.8%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">MCP Atlas</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">80.8%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">81.5%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">80.5%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">Tau3 Banking</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">36.1%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">36.8%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">35.4%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">BrowseComp w/ context management</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">76.8%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">76.7%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">75.6%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">DeepSearchQA w/ context management</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">80.5%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">79.6%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">81.1%</td>
</tr>
<tr><th colspan="4" scope="colgroup" style="padding:10px 12px;text-align:left;background:#152414;color:#C9DCB8;border-bottom:1px solid #29422A">General Capabilities</th></tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">AA-LCR</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">78.2%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">79.4%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">78.7%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">LongBench v2</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">67.5%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">67.6%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">67.2%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">IFBench</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">79.6%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">80.7%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">79.2%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">AA Omniscience (index) - public split only</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">10.8</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">8.8</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">9.8</td>
</tr>
</tbody>
</table>
</div>

## Evaluating Beam

See the [evaluation guide](./EVALUATION.md) for recommended settings, Beam Verifier and a SWE-bench Verified example.

## Model Data

Beam is pretrained on a diverse variety of textual data from publicly available sources and data obtained through commercial partner agreements. The corpus includes general web content, source code, technical documentation, reference materials, and educational and scientific documents. Mid-training uses data derived from curated real-world examples to develop reasoning, tool-use, and long-context capabilities, including structured code repositories, long-horizon tasks, and long-form documents. Reinforcement learning uses environments spanning coding, agentic tasks, and STEM, built primarily through synthetic pipelines and supplemented by proprietary vendor data and open-source sources.

Data processing includes quality filtering, deduplication, and evaluation decontamination to reduce benchmark contamination. For all types of pretraining data, we measure document quality with in-house trained classifiers, divide data into fine-grained quality tiers, and weigh training toward stronger material. We perform multiple forms of deduplication, exact and approximate. We curate code data via language-specific filtration and removal of low-quality and autogenerated content. We also transform educational material from PDF form into textual training data using commercially available vision-language OCR models and a curation pipeline to filter low-quality artifacts. RL tasks are iteratively filtered for quality and difficulty. We also curate datasets to reduce personally identifiable information and harmful or sensitive content.

## Safety & Alignment

Before releasing Beam, we ran a comprehensive set of safety evaluations to measure its performance and identify potential risks requiring mitigation. We run both [Open Safety Framework](https://reflection.ai/safety) evaluations, external third party assurance evaluations, and The Iris Safety Evaluations (ISE), which is Reflection’s in-house soon-to-be open-sourced safety evaluation suite, combining single-turn, multi-turn, jailbreak, and agentic evaluations to measure adherence to our safety policies. Learn more about our Safety & Alignment methodology and the detailed results of how we’ve evaluated Beam at [reflection.ai/beam-safety-report](http://reflection.ai/beam-safety-report).

<div class="dark:hidden" style="overflow-x:auto;">
<table align="center" style="display:table;width:auto;max-width:100%;margin-left:auto;margin-right:auto;border-collapse:collapse;">
<thead>
<tr>
<th scope="col" style="padding:12px;text-align:left;background:#274E13;color:#FFFFFF;border-bottom:2px solid #274E13;">Benchmark</th>
<th scope="col" style="padding:12px;text-align:center;background:#274E13;color:#FFFFFF;border-bottom:2px solid #274E13;">Beam<br>(BF16)</th>
<th scope="col" style="padding:12px;text-align:center;background:#274E13;color:#FFFFFF;border-bottom:2px solid #274E13;">Beam<br>(FP8)</th>
<th scope="col" style="padding:12px;text-align:center;background:#274E13;color:#FFFFFF;border-bottom:2px solid #274E13;">Beam<br>(NVFP4)</th>
</tr>
</thead>
<tbody>
<tr><th colspan="4" scope="colgroup" style="padding:10px 12px;text-align:left;background:#D9E8D1;color:#274E13;border-bottom:1px solid #B8CFA9;">Iris Safety Evaluations (Combined All Harm Areas)</th></tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">Harmful Requests: Refusal/Pivot Rate</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">88.9%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">89.7%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">88.5%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;border-bottom:1px solid #D9E8D1;font-weight:400;">Harmless Requests: Compliance Rate</th>
<td style="padding:10px 12px;text-align:center;background:#EFF5EB;color:#274E13;border-bottom:1px solid #D9E8D1;">81.5%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">81.6%</td>
<td style="padding:10px 12px;text-align:center;border-bottom:1px solid #D9E8D1;">82.1%</td>
</tr>
</tbody>
</table>
</div>
<div class="hidden dark:block" style="overflow-x:auto;">
<table align="center" style="display:table;width:auto;max-width:100%;margin-left:auto;margin-right:auto;border-collapse:collapse;">
<thead>
<tr>
<th scope="col" style="padding:12px;text-align:left;background:#274E13;color:#FFFFFF;border-bottom:2px solid #274E13;">Benchmark</th>
<th scope="col" style="padding:12px;text-align:center;background:#274E13;color:#FFFFFF;border-bottom:2px solid #274E13;">Beam<br>(BF16)</th>
<th scope="col" style="padding:12px;text-align:center;background:#274E13;color:#FFFFFF;border-bottom:2px solid #274E13;">Beam<br>(FP8)</th>
<th scope="col" style="padding:12px;text-align:center;background:#274E13;color:#FFFFFF;border-bottom:2px solid #274E13;">Beam<br>(NVFP4)</th>
</tr>
</thead>
<tbody>
<tr><th colspan="4" scope="colgroup" style="padding:10px 12px;text-align:left;background:#152414;color:#C9DCB8;border-bottom:1px solid #29422A">Iris Safety Evaluations (Combined All Harm Areas)</th></tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">Harmful Requests: Refusal/Pivot Rate</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">88.9%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">89.7%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">88.5%</td>
</tr>
<tr>
<th scope="row" style="padding:10px 12px;text-align:left;font-weight:400;color:#D5DDD4;border-bottom:1px solid #243624">Harmless Requests: Compliance Rate</th>
<td style="padding:10px 12px;text-align:center;background:#1A2B1A;color:#DCEAD2;border-bottom:1px solid #243624">81.5%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">81.6%</td>
<td style="padding:10px 12px;text-align:center;color:#B7C2B6;border-bottom:1px solid #243624">82.1%</td>
</tr>
</tbody>
</table>
</div>

## Usage

Beam is a text model intended for commercial and research use, including applications such as assistant-style generation, software engineering and agentic coding tasks, long-horizon agentic tasks and summarization, and as a base model for fine-tuning. Reflection does not prohibit distillation, use of outputs to train other models, fine-tuning, parameter-efficient adaptation, quantization, merging, defensive security research on systems you are authorized to test, and good-faith adversarial evaluation of the model.

When building with this model, apply responsible AI practices and verify your use case meets relevant legal requirements (privacy, export compliance, and others). Our [Usage Policy](https://reflection.ai/legal/usage-policy) lists the areas we recommend reviewing. Note: this Model Card is informational only and does not modify or restrict the model's license.

## Reporting

Report suspected misuse, safety concerns or security vulnerabilities to [reports@reflection.ai](mailto:reports@reflection.ai).

## Citation

If you find our work helpful, please consider citing it:

```bibtex
@misc{reflection2026introducingbeam,
  author = {{Reflection}},
  title  = {Introducing {Beam}: {Reflection}'s 501B open-weight model},
  year   = {2026},
  month  = oct,
  url    = {https://reflection.ai/blog/introducing-beam}
}
```
