---
library_name: transformers
license: mit
license_link: https://huggingface.co/ornith-ai/Ornith-1.5-122B/blob/main/LICENSE
pipeline_tag: text-generation
---


<img width="600px" src="assets/ornith_logo.png">


# Ornith-1.5-122B

Chirp Chirp! 🐦 Meet Ornith-1.5-122B: No Tradeoff Between Strong and Fast
Stronger. Faster. Leaner.  It delivers stronger benchmark results, finishes tasks faster, and produces shorter outputs, bringing better instruction following, stronger task decomposition, and deeper knowledge of real-world work scenarios, and it runs on a single DGX. It achieves state-of-the-art performance among open-source models of comparable size. Open weights under the MIT license.
<img style="width: 100%; max-width: 900px;" src="assets/ornith_122b_eval.png" alt="Ornith 1.5 122B Benchmark Results" title="Ornith 1.5 122B Benchmark Results">

## Ornith 1.5 122B

This model card documents **Ornith-1.5-122B**, the most capable and efficient.member of the Ornith-1.5 family — a 122B MOE model designed for efficient single-GPU deployment, and edge-deployable on mobile devices via its quantized Ornith-1.5-122B-Mobile variant.

### Benchmarks


<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;width:100%;margin:0 auto;padding:16px 0">
<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;width:100%">
<table style="min-width:860px;width:100%;table-layout:fixed;border-collapse:collapse;font-size:13px">
<thead><tr>
<th style="width:16%;padding:10px 7px;text-align:left;font-weight:600;border-bottom:2px solid #FD8E5B;color:#FD8E5B"></th>
<th style="width:14%;padding:10px 7px;text-align:center;font-weight:700;border-bottom:2px solid #FD8E5B;color:#FD8E5B;font-size:14px;background:rgba(253, 142, 91, 0.12)">Ornith-1.5-122B</th>
<th style="width:14%;padding:10px 7px;text-align:center;font-weight:500;border-bottom:2px solid #FD8E5B;color:#FD8E5B;font-size:14px">Qwen3.8-Flash-Next <sub><small>(125B)</small></sub></th>
<th style="width:14%;padding:10px 7px;text-align:center;font-weight:500;border-bottom:2px solid #FD8E5B;color:#FD8E5B;font-size:14px">Qwen3.8 <sub><small>(27B dense)</small></sub></th>
<th style="width:14%;padding:10px 7px;text-align:center;font-weight:500;border-bottom:2px solid #FD8E5B;color:#FD8E5B;font-size:14px">Nemotron 3.5 Super VL <sub><small>(120B)</small></sub></th>
<th style="width:14%;padding:10px 7px;text-align:center;font-weight:500;border-bottom:2px solid #FD8E5B;color:#FD8E5B;font-size:14px">DeepSeek-V4-Flash-0731 <sub><small>(284B)</small></sub></th>
<th style="width:14%;padding:10px 7px;text-align:center;font-weight:500;border-bottom:2px solid #FD8E5B;color:#FD8E5B;font-size:14px">Beam <sub><small>(501B)</small></sub></th>
</tr></thead>
<tbody>
<tr><td colspan="7" style="padding:8px 12px;font-weight:600;color:#FD8E5B;border-bottom:1px solid rgba(253, 142, 91, 0.2);background:rgba(253, 142, 91, 0.1)">Coding</td></tr>
<tr>
<td style="padding:7px 7px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">TerminalBench 2.1</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15);font-weight:600;color:#FD8E5B;background:rgba(253, 142, 91, 0.06)">81.2</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">83.4</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">71.9</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">66.7</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">82.7</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">80.1</td>
</tr>
<tr>
<td style="padding:7px 7px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">CyberGym</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15);font-weight:600;color:#FD8E5B;background:rgba(253, 142, 91, 0.06)">80</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">78</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">55</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">34</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">76.7</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">59</td>
</tr>
<tr>
<td style="padding:7px 7px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">NL2Repo</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15);font-weight:600;color:#FD8E5B;background:rgba(253, 142, 91, 0.06)">51.2</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">45.2</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">42.3</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">21</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">54.2</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">49.4</td>
</tr>
<tr>
<td style="padding:7px 7px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">SWE-bench Pro<br><sub><small>(no-hack)</small></sub></td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15);font-weight:600;color:#FD8E5B;background:rgba(253, 142, 91, 0.06)">76.9</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">43.9</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">65.5</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">42.5</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">-</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">57</td>
</tr>
<tr>
<td style="padding:7px 7px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">SWE-bench Verified<br><sub><small>(non-hack)</small></sub></td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15);font-weight:600;color:#FD8E5B;background:rgba(253, 142, 91, 0.06)">84.5</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">82.8</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">76.8</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">61.2</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">-</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">-</td>
</tr>
<tr>
<td style="padding:7px 7px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">SWE-bench Multilingual<br><sub><small>(non-hack)</small></sub></td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15);font-weight:600;color:#FD8E5B;background:rgba(253, 142, 91, 0.06)">76.4</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">73.0</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">70.3</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">48.0</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">-</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">-</td>
</tr>
<tr><td colspan="7" style="padding:8px 12px;font-weight:600;color:#FD8E5B;border-bottom:1px solid rgba(253, 142, 91, 0.2);background:rgba(253, 142, 91, 0.1)">Reasoning</td></tr>
<tr>
<td style="padding:7px 7px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">HLE <sub><small>(with tools)</small></sub></td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15);font-weight:600;color:#FD8E5B;background:rgba(253, 142, 91, 0.06)">48</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">38</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">31.3</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">33.2</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">50.8</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">51.1</td>
</tr>
<tr>
<td style="padding:7px 7px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">HLE <sub><small>(w/o tools)</small></sub></td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15);font-weight:600;color:#FD8E5B;background:rgba(253, 142, 91, 0.06)">37.68</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">34.16</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">29.32</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">31.79</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">-</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">-</td>
</tr>
<tr>
<td style="padding:7px 7px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">SciCode</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15);font-weight:600;color:#FD8E5B;background:rgba(253, 142, 91, 0.06)">53.8</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">47.5</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">43.6</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">47.1</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">-</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">-</td>
</tr>
<tr><td colspan="7" style="padding:8px 12px;font-weight:600;color:#FD8E5B;border-bottom:1px solid rgba(253, 142, 91, 0.2);background:rgba(253, 142, 91, 0.1)">Agentic</td></tr>
<tr>
<td style="padding:7px 7px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">WideSearch</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15);font-weight:600;color:#FD8E5B;background:rgba(253, 142, 91, 0.06)">75.2</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">71.8</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">62.6</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">69.2</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">77.3</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">68.5</td>
</tr>
<tr>
<td style="padding:7px 7px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">BrowseComp</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15);font-weight:600;color:#FD8E5B;background:rgba(253, 142, 91, 0.06)">78.5</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">75.3</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">71.4</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">61</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">80.2</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">67.6</td>
</tr>
<tr>
<td style="padding:7px 7px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">MCP-Atlas</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15);font-weight:600;color:#FD8E5B;background:rgba(253, 142, 91, 0.06)">74.6</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">74.1</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">69</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">63.3</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">74.6</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">-</td>
</tr>
<tr>
<td style="padding:7px 7px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">Toolathlon-Verified</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15);font-weight:600;color:#FD8E5B;background:rgba(253, 142, 91, 0.06)">70.8</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">71.4</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">67.1</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">60.1</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">70.3</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">63.5</td>
</tr>
<tr>
<td style="padding:7px 7px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">ClawEval</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15);font-weight:600;color:#FD8E5B;background:rgba(253, 142, 91, 0.06)">79.4</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">76.5</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">75.4</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">61.2</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">-</td>
<td style="padding:7px 7px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">-</td>
</tr>
</tbody>
</table>
</div>

<p style="margin-top:12px;font-size:10px;opacity:0.7">
 * Terminal-Bench 2.1 (Claude Code): We evaluate Terminal-Bench 2.1 using Claude Code 2.1.126 with parser=json, temperature=1.0, top_p=1.0, max_new_tokens=131072. Results are averaged over 5 runs. Again, Qwen chat template needs to be modified.</br>
 * SWE-Bench Verified, Pro, and Multilingual: Evaluated using the OpenHands harness with temperature=1.0, top_p=0.95, and a 256K context window. Anti-hacking safeguards are applied throughout evaluation: models are explicitly informed of potential reward-hacking behaviors and instructed to avoid them. Any solution that still exhibits such behavior is marked incorrect.</br>
 * NL2Repo: with temperature=1.0, top_p=1.0, 400K context, 48K output. Access to specified GitHub repositories and pip packages is blocked to prevent reward hacking.</br>
 * HLE: Evaluated using Claude 4.6 Opus as the judge model.</br>
 * MCP-Atlas: All models were evaluated in thinking mode on the 500-task public subset, with a 10-minute timeout per task. We use Claude 4.8 Opus as the judge model.</br>
 * Toolathlon-Verified: We use the official evaluation service with the maximum token limit set to 128K.</br>
 * ClawEval: An agentic code benchmark over real-user task distributions; temp=0.6 and 256K context.</br> 
</p>

</div>


## Quickstart

<div style="border-left:4px solid #FD8E5B;background:rgba(253,142,91,0.1);border-radius:6px;padding:12px 16px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;font-size:14px;line-height:1.6">
<div style="font-weight:700;color:#FD8E5B;margin-bottom:6px">📝 NOTE</div>
<p style="margin:0 0 10px"><b>Ornith-1.5-122B</b> is a <b>reasoning model</b>: by default the assistant turn opens with a <code style="background:rgba(253,142,91,0.15);padding:1px 5px;border-radius:4px">&lt;think&gt; … &lt;/think&gt;</code> block before the final answer. The serving recipes below enable a reasoning parser so the chain-of-thought is returned in a separate <code style="background:rgba(253,142,91,0.15);padding:1px 5px;border-radius:4px">reasoning_content</code> field, and a tool-call parser so the model's <code style="background:rgba(253,142,91,0.15);padding:1px 5px;border-radius:4px">&lt;tool_call&gt;</code> blocks are surfaced as OpenAI-style <code style="background:rgba(253,142,91,0.15);padding:1px 5px;border-radius:4px">tool_calls</code>.</p>
<p style="margin:0 0 6px">Serving Ornith-1.5-122B requires recent runtimes:</p>
<ul style="margin:0 0 10px;padding-left:20px">
<li><b>Transformers</b> ≥ 5.8.1</li>
<li><b>vLLM</b> ≥ 0.19.1</li>
<li><b>SGLang</b> ≥ 0.5.9</li>
</ul>
<p style="margin:0 0 6px">Recommended sampling parameters:</p>
<ul style="margin:0;padding-left:20px">
<li><b>For general tasks:</b> <code style="background:rgba(253,142,91,0.15);padding:1px 5px;border-radius:4px">temperature=1.0</code>, <code style="background:rgba(253,142,91,0.15);padding:1px 5px;border-radius:4px">top_p=0.95</code>, <code style="background:rgba(253,142,91,0.15);padding:1px 5px;border-radius:4px">top_k=20</code>, <code style="background:rgba(253,142,91,0.15);padding:1px 5px;border-radius:4px">min_p=0.0</code>, <code style="background:rgba(253,142,91,0.15);padding:1px 5px;border-radius:4px">presence_penalty=1.5</code>, <code style="background:rgba(253,142,91,0.15);padding:1px 5px;border-radius:4px">repetition_penalty=1.0</code></li>
<li><b>For precise coding tasks:</b> <code style="background:rgba(253,142,91,0.15);padding:1px 5px;border-radius:4px">temperature=0.6</code>, <code style="background:rgba(253,142,91,0.15);padding:1px 5px;border-radius:4px">top_p=0.95</code>, <code style="background:rgba(253,142,91,0.15);padding:1px 5px;border-radius:4px">top_k=20</code>, <code style="background:rgba(253,142,91,0.15);padding:1px 5px;border-radius:4px">min_p=0.0</code>, <code style="background:rgba(253,142,91,0.15);padding:1px 5px;border-radius:4px">presence_penalty=0.0</code>, <code style="background:rgba(253,142,91,0.15);padding:1px 5px;border-radius:4px">repetition_penalty=1.0</code></li>
</ul>
</div>

### Serving Ornith-1.5-122B

Ornith-1.5-122B is a MOE 122B model, so it serves on a **single 80GB GPU**. The recipes below stand up an OpenAI-compatible server; add `--tensor-parallel-size` / `--tp` if you want to shard across more GPUs.

*  vLLM

```bash
vllm serve ornith-ai/Ornith-1.5-122B --served-model-name Ornith-1.5-122B --host 0.0.0.0 --port 8000 --max-model-len 262144 --gpu-memory-utilization 0.90 --enable-prefix-caching --enable-auto-tool-choice --tool-call-parser qwen3_xml --reasoning-parser qwen3 --trust-remote-code
```

*  SGLang


```bash
python -m sglang.launch_server --model-path ornith-ai/Ornith-1.5-122B --served-model-name Ornith-1.5-122B --host 0.0.0.0 --port 8000 --context-length 262144 --mem-fraction-static 0.85 --tool-call-parser qwen3_coder --reasoning-parser qwen3
```

#### For Long-Context

Ornith-1.5-122B handles context windows of up to 262,144 tokens. When a task's combined input and output must go beyond this limit, we suggest extending the effective window with RoPE scaling — YaRN is the technique we validate against, and it is already built into both vLLM and SGLang. With a scaling factor of 4.0, the usable window grows to roughly 1M tokens.

You can turn YaRN on in either of two ways:

- **Edit the checkpoint's `config.json`.** Add a `rope_scaling` block to the model configuration:

  ```json
  {
      "rope_scaling": {
          "rope_type": "yarn",
          "factor": 4.0,
          "original_max_position_embeddings": 262144
      }
  }
  ```

- **Override at launch time.** Leave the checkpoint untouched and extend the serve commands above with the equivalent flags.

  vLLM:

  ```bash
  VLLM_ALLOW_LONG_MAX_MODEL_LEN=1 vllm serve ornith-ai/Ornith-1.5-122B ... --hf-overrides '{"rope_scaling": {"rope_type": "yarn", "factor": 4.0, "original_max_position_embeddings": 262144}}' --max-model-len 1000000
  ```

  SGLang:

  ```bash
  SGLANG_ALLOW_OVERWRITE_LONGER_CONTEXT_LEN=1 python -m sglang.launch_server ... --json-model-override-args '{"rope_scaling": {"rope_type": "yarn", "factor": 4.0, "original_max_position_embeddings": 262144}}' --context-length 1000000
  ```

<div style="border-left:4px solid #FD8E5B;background:rgba(253,142,91,0.1);border-radius:6px;padding:12px 16px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;font-size:14px;line-height:1.6">
<div style="font-weight:700;color:#FD8E5B;margin-bottom:6px">📝 NOTE</div>
<p style="margin:0">Open-source runtimes implement YaRN <i>statically</i>: the same scaling factor is applied to every request regardless of its length, which can slightly hurt quality on ordinary-length inputs. Only enable <code style="background:rgba(253,142,91,0.15);padding:1px 5px;border-radius:4px">rope_scaling</code> when your workload genuinely needs the longer window, and size <code style="background:rgba(253,142,91,0.15);padding:1px 5px;border-radius:4px">factor</code> to match it — the target window is roughly <code style="background:rgba(253,142,91,0.15);padding:1px 5px;border-radius:4px">factor</code> × 262,144, so if your requests top out around 524,288 tokens, <code style="background:rgba(253,142,91,0.15);padding:1px 5px;border-radius:4px">factor: 2.0</code> is the better setting.</p>
</div>

### Using Ornith-1.5-122B via the Chat Completions API

Once a vLLM or SGLang server is running, talk to it with any OpenAI-compatible client.

#### Basic Usage

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY",  # any non-empty string works for a local server
)

response = client.chat.completions.create(
    model="Ornith-1.5-122B",
    messages=[
        {"role": "user", "content": "Write a one-line Python lambda that squares a number."}
    ],
    temperature=0.6,
    top_p=0.95,
    max_tokens=1024,
)

message = response.choices[0].message
# reasoning_content holds the <think> trace; content holds the final answer.
print("reasoning:", getattr(message, "reasoning_content", None))
print("answer:", message.content)
```

You can also stream tokens, or hand the model tools — Ornith-1.5-122B emits well-formed function calls that the server parses into the standard `tool_calls` field:

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"],
            },
        },
    }
]

response = client.chat.completions.create(
    model="Ornith-1.5-122B",
    messages=[{"role": "user", "content": "What is the weather in Paris right now?"}],
    tools=tools,
    tool_choice="auto",
    temperature=0.6,
    max_tokens=2048,
)

tool_call = response.choices[0].message.tool_calls[0]
print(tool_call.function.name, tool_call.function.arguments)
# -> get_weather {"city": "Paris"}
```

You can point any OpenAI-compatible SDK (Python, Node.js, etc.) or `curl` at the same `/v1/chat/completions` endpoint.


## Agentic Usage

Ornith-1.5-122B exposes an OpenAI-compatible endpoint with tool calling, it works out of the box with standard agent frameworks. 

**Examples of using Ornith with agents:**


#### Ollama 
```bash
ollama run ornith-1.5:122b
```


#### Atomic.chat
```bash
# Both runtimes load a GGUF build of Ornith (publish one at ornith-ai/Ornith-1.5-122B-GGUF).

# llama.cpp — serve an OpenAI-compatible API on port 8000.
llama-server -hf hf.co/ornith-ai/Ornith-1.5-122B-GGUF --port 8000 -c 262144
```

#### llama.cpp
```bash
# Both runtimes load a GGUF build of Ornith (publish one at ornith-ai/Ornith-1.5-122B-GGUF).

# llama.cpp — serve an OpenAI-compatible API on port 8000.
llama-server -hf hf.co/ornith-ai/Ornith-1.5-122B-GGUF --port 8000 -c 262144
```

#### Hermes Agent
```bash
# Hermes talks to any OpenAI-compatible endpoint — point it at your Ornith server.
export OPENAI_BASE_URL="http://localhost:8000/v1"
export OPENAI_API_KEY="EMPTY"
export MODEL="ornith-ai/Ornith-1.5-122B"
```

#### OpenClaw

```bash
# OpenClaw talks to any OpenAI-compatible endpoint — point it at your Ornith server.
export OPENAI_BASE_URL="http://localhost:8000/v1"
export OPENAI_API_KEY="EMPTY"
export OPENAI_MODEL="ornith-ai/Ornith-1.5-122B"
```

#### Unsloth Studio

```bash
pip install unsloth

# Load Ornith for fast local inference or fine-tuning (Python):
#   from unsloth import FastLanguageModel
#   model, tokenizer = FastLanguageModel.from_pretrained(
#       "unsloth/Ornith-1.5-122B-GGUF",
#       max_seq_length=262144,
#       load_in_4bit=True,
#   )
```


### Coding CLIs

Ornith-1.5-122B is optimized for terminal-based coding agents. Point any OpenAI-compatible coding CLI at your Ornith-1.5-122B endpoint (set `OPENAI_BASE_URL` and `OPENAI_API_KEY`) to understand large codebases, automate tedious work, and ship faster.

#### OpenCode
```bash
# Register your local Ornith endpoint as a provider in ~/.config/opencode/opencode.json:
#
# {
#   "$schema": "https://opencode.ai/config.json",
#   "provider": {
#     "ornith": {
#       "npm": "@ai-sdk/openai-compatible",
#       "name": "Ornith (local)",
#       "options": { "baseURL": "http://localhost:8000/v1", "apiKey": "EMPTY" },
#       "models": { "ornith-ai/Ornith-1.5-122B": { "name": "Ornith-1.5-122B" } }
#     }
#   }
# }

opencode
```

### Citation

If you find our work helpful, feel free to give us a cite.

```bibtex
@misc{ornith_1_5,
    title = {{Ornith-1.5}: From Self-Scaffolding to Self-Improvement},
    url = {https://ornith.ai/ornith_1_5.html},
    author = {{Ornith Team}},
    year = {2026}
}
```
