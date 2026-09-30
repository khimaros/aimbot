# ROADMAP

```
[ ] determine why the roster only has a single quant per repo, which limits llama-tools use
[ ] clarify whether lowercase "gb" means gigabits or gigabytes
[ ] add more hardware presets: new mac studio, various graphics cards (1080ti, rx5090, etc)

[>] min/max quant as a slider with two segments
[>] llama-server command in dashboard should be identical to production
[>] width of quant layer table should be proportionate to percent (bar chart)
[>] spec decoding defined per-quant in the registry
[>] hide the flops hardware section when t/s column is off
[>] add some "milestone" or "benchmark" frontier models to the tables

[x] create a new favicon with a simple monochrome crosshair
[x] support new backend: https://github.com/0xShug0/audio.cpp
[x] support new backend: https://github.com/gufo-org/gufo/
[x] new benchmark: https://livebench.ai
[x] add quant: https://huggingface.co/TrevorJS/MiMo-V2.6-Flash-RL-GGUF
[x] allow the user to select 1gb memory reserve in the hardware section
[x] create a more intuitive visilbe columns configuration icon
[x] create a more intuitive reset button icon
[x] split the reset button to one button per section;
    if the section hasn't changed from defaults, disable the button;
    clicking the reset button for a section should only reset that section
[x] update url hash as changes are made
[x] when there no results, suggest relaxing specific filters
[x] add the new nemotron diarization/voice models
[x] add a new 'decide' kind for verdict/jev-like models
[x] add decider-4b to the roster
```
