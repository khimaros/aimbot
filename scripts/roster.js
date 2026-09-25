// the roster's arithmetic, with no page around it.
//
// this is everything the dashboard COMPUTES rather than displays: which quant
// fits a box, what its kv cache costs, how far a context can be stretched, what
// a quant cost in quality, and the composite that ranks the result. it touches
// no dom and reads no localStorage, so it runs the same under node as it does
// in a browser.
//
// it exists because three things need those answers and only one of them is a
// browser. `docs/index.html` inlines this file and puts controls on it,
// `scripts/aimbot` requires it to answer from a terminal, and
// `research/dashboard-table` requires it to generate MODELS.md's ranking. one
// implementation, because two of them drifted once already -- the page scored a
// mean of percentiles while a second composite in python min-max normalised raw
// values, and they disagreed about which model was first.
//
// the FACTS come from `docs/data.json`, which `scripts/build-viewer` writes out
// of `registry/models.yaml` and the research captures. the DEFAULTS come from
// `registry/dashboard.yaml` through the same file. nothing is hardcoded here
// that a reader of the registry would want to argue with.

let D = null;                       // the payload
let W = {};                         // facet key -> weight
// the page overwrites this from localStorage once it boots; a module with no
// browser around it starts where a first-time reader starts
let sort = {k: 'score', dir: -1};
// the runtimes selected by default: the three that load most of this roster and
// that a reader here is likely to have built. it is a multi-select rather than
// one choice because a model can have two -- whisper's files load in crispasr
// and in stock whisper.cpp -- and because narrowing to one runtime is a
// question about a box rather than about the models.
let DEFAULT_ENGINES = [];
// the licence tiers selected by default. `permissive` alone: a reader here is
// deciding what to run, and a licence they cannot ship under is not a
// candidate. the other two tiers are a tick away rather than unreachable.
let DEFAULT_LICENSES = [];
// `params` is a band in BILLIONS and is not the same question as whether a
// model fits: a 27b at Q1_0 is 3.5 gib and is not a small model. off by
// default at both ends, the way every other filter here is.
let filters = {q: '', kind: new Set(), pub: '', flags: new Set(),
               engines: new Set(), mods: new Set(), pubs: new Set(),
               licenses: new Set(), minParams: null, maxParams: null};
let folded = new Set();             // collapsed factor groups
let hidden = new Set();
let order = [];
let openRepo = null;
let tab = 'overview';

const fmt = new Intl.NumberFormat();
const esc = s => String(s ?? '').replace(/[&<>"]/g, c =>
  ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const num = (v, d = 1) => v === null || v === undefined ? '' : (+v).toFixed(d);
const pctOf = v => Math.round((v || 0) * 100) + '%';
// the thinking vocabulary, with the level a client gets by sending nothing in
// bold. that level is not always the cheap one: kimi k3 defaults to `max`, and
// the gemma 4 templates do not think at all until asked.
const levels = (t, sep = ' ') => {
  // a switch has two states and no vocabulary. the words are for reading --
  // what a client sends is the boolean itself
  if (t.kind === 'boolean') {
    return ['off', 'on'].map(s => t.default === (s === 'on') ? `<b>${s}</b>` : s).join(sep);
  }
  return (t.accepts || []).map(l => l === t.default ? `<b>${esc(l)}</b>` : esc(l)).join(sep);
};
const gib = v => v === undefined || v === null ? '' : (+v).toFixed(1);
const ctxLabel = v => !v ? '' : v >= 1000 ? Math.round(v / 1024) + 'k' : String(v);
// a counted parameter total is 27.78b and the vendor calls it 27b. neither is
// wrong, and one decimal is as much as anyone reads -- the exact figure is on
// hover
const round1 = v => v === undefined || v === null ? '' : (Math.round(v * 10) / 10);

// a note or a verdict, as plain text. the parts carry rendered references --
// `{gib}` became a figure at build time -- and the ones that are objects know
// what they are SHOWN as. lives here rather than with the modal because the
// search haystack reads it, and a grep that could not see a note would miss
// the sentence that says what a model is for.
const proseText = parts => !parts ? ''
  : (Array.isArray(parts) ? parts : [parts])
      .map(p => typeof p === 'string' ? p : p.shown).join('');

// active parameters: the vendor's own naming convention first, since it is
// exact and covers models nobody has scored, then artificial analysis, and for
// a dense model the total it already has. never larger than the total, which
// is what comparing a counted 29.78b against an advertised 30b produced.
function activeB(m) {
  const total = m.facts.params_total_b;
  const a = m.facts.params_active_b ?? m.params.advertised_active_b
    ?? (m.facts.experts ? undefined : total);
  if (a === undefined) return undefined;
  return total ? Math.min(a, total) : a;
}

// --- scoring -----------------------------------------------------------------
//
// a weight key is either a facet key (aa.scicode) or a prefix wildcard
// (card.*), which averages every facet under it. the wildcard exists because
// card claims and epoch runs are per benchmark: a reader wants one knob for
// "how much do i trust what the vendor says", not eleven.

const facetKeys = (m, key) => key.endsWith('.*')
  ? Object.keys(m.facets).filter(k => k.startsWith(key.slice(0, -1)))
  : (m.facets[key] ? [key] : []);

// --- effective values --------------------------------------------------------
//
// a benchmark measures the model; a local roster runs a QUANT of it. `raw` is
// what the source published, `effective` is that discounted by the retention
// build-tables' curve predicts for the pinned quant's bits per weight -- the
// same adjustment MODELS.md's composite makes, from the same curve.
//
// only the three artificial analysis indices are scaled. the other sources
// measured a served endpoint whose precision this repo does not know, so
// discounting them would invent a number rather than adjust one.

let effective = true;
let budget = null;                  // gib of memory, or null
// weights are not the whole resident set: the kv cache grows with context and
// the compute buffers are not free either. what is left after that reserve is
// what a quant has to fit in, which is why build-tables budgets 105 of a 128gb
// box rather than 128.
let reserve = 0;
const usable = () => budget === null ? null : Math.max(0, budget - reserve);

// the quant ladder's ceiling and floor, and every other default, come from
// `registry/dashboard.yaml` through `docs/data.json`. they are judgements --
// how far up the ladder is worth climbing, how much of a box to hold back --
// and they were consts in the page where nothing but the page could read them
// and nobody reviewing the registry would find them. applyConfig fills them in
// before anything reads them.
let CAPS = [];
let FLOORS = [];
let cap = null;
let floor = null;
const capBpw = () => (CAPS.find(c => c[0] === cap) || CAPS[0])[1];
const floorBpw = () => (FLOORS.find(c => c[0] === floor) || FLOORS[0])[1];

// the cap and the floor pick a rung off a LADDER, and a ladder is a text
// model's problem: a speech or image model publishes one or two files and there
// is nothing to choose between. applying them there disqualified every non-text
// model on the roster -- 22 of 87 -- on a box with 116gib free.
//
// the bpw they compare is not trustworthy for those models either, which is why
// this is a rule about ladders rather than a wider cap. `bpw` is size over
// parameter count, and for a speech model the parameter count names a COMPONENT
// where the gguf carries several: qwen3-tts 0.6b ships a 1.23gib file tagged
// Q8_0 against a `0.6` figure counting only the talker, which computes to 17.7
// bits per weight. reading the tag instead is no better -- unsloth's
// UD-Q8_K_XL is genuinely ~11.8 bpw and the 11 ceiling excludes it correctly,
// which a tag saying `Q8` would undo.
const laddered = m => m.kind === 'text';

// the bits a plain quant tag names. `max q8` used to do nothing at all to a
// speech or image model -- the ceiling compares bits per weight, that number is
// not trustworthy there, so the whole test was skipped and z-image went on
// offering its f16 rung under a q8 ceiling. the TAG is trustworthy where the
// bpw is not: a repo that publishes `F16` and `Q8_0` is telling you which is
// which, and a speech repo publishes nothing more exotic than that.
//
// text models keep the bpw comparison, because there the tag is the thing that
// lies: unsloth's UD-Q8_K_XL is genuinely ~11.8 bpw and the ceiling excludes it
// correctly, which a tag reading `Q8` would undo.
const TAG_BITS = /^(?:UD-|AD-)?(?:(?:BF|F)(\d+)|I?Q(\d+))/i;
const tagBits = tag => {
  const m = TAG_BITS.exec(tag || '');
  return m ? +(m[1] || m[2]) : null;
};
const capBits = () => cap === 'none' ? Infinity : +cap.slice(1);

function affordable(m, all, room) {
  const fits = all.filter(c => c.gib && c.gib <= room);
  if (!laddered(m)) {
    // a PREFERENCE, so it yields rather than emptying the list: pyannote
    // publishes one f32 file and nothing else, and a ceiling that hid it would
    // report the model as not fitting a box with room for it fifty times over
    const bits = capBits();
    const under = fits.filter(c => (tagBits(c.quant) ?? 0) <= bits);
    return under.length ? under : fits;
  }
  const ceiling = capBpw(), bottom = floorBpw();
  return fits.filter(c => !c.bpw
    || (ladderBpw(c) <= ceiling && ladderBpw(c) >= bottom));
}

// how far `bpw` may sit from the tensor table before it stops being evidence.
// the two agree within noise on 1671 of 1687 text rungs, so this is about the
// handful where the denominator is wrong rather than about rounding.
const BPW_DISAGREE = 0.25;

// the bits a ceiling should compare. `bpw` is file size over `params_total_b`,
// and that denominator describes the CHECKPOINT rather than the file: minicpm-v
// 4.6 counts its vision encoder, ships it as a separate mmproj and the language
// half alone in the gguf, so every rung reads 1.7x too cheap and its F16 sat
// under a q8 ceiling at a computed 9.32 against a true 16. lfm2.5 2.6b is the
// same fault inverted -- a bundled drafter inflates the file, its Q4_0 reads
// 9.45 against a true 4.70, and a q6 ceiling hid a rung that clears it.
//
// where the tensor table disagrees it wins, because it counted what is in the
// file. where they agree the nominal figure stands: the ceilings are calibrated
// against that scale, and swapping wholesale would throw qwen3.5-0.8b's Q4_K_S
// out of `max q4` on a 10% difference. reading the TAG instead is no fix
// either -- gpt-oss ships mxfp4 under an F16 name at a true 4.48 bpw, which
// belongs under a q8 ceiling and which a tag test would have excluded.
const ladderBpw = c => c.realBpw
  && Math.abs(c.realBpw - c.bpw) / c.bpw > BPW_DISAGREE ? c.realBpw : c.bpw;

// context to serve, and what its kv cache costs. the geometry comes from each
// model's own config: full-attention layers hold a cache that grows with the
// context, windowed layers hold at most their window, and a linear-attention
// layer holds a fixed state that does not scale at all. counting every layer
// as global would overstate gemma 4 31b several times over.
let KV_BYTES = 2;                   // f16 keys and values, llama.cpp's default
let minCtx = 0;

// what one token costs in cache, per layer that holds one. latent attention
// keeps a single compressed vector instead of a key and a value per head, and
// costing it the naive way overstates kimi k3 by 24.7x, ling 3.0 flash by
// 14.2x and deepseek v4 flash by 1.8x -- always as "this will not fit".
const kvPerToken = a => a.latent
  ? a.latent * KV_BYTES : 2 * a.kv_heads * a.head_dim * KV_BYTES;

function kvGib(m, ctx) {
  const a = m.facts.attn;
  if (!a || !ctx) return 0;
  const perTok = kvPerToken(a);
  const windowed = a.window ? a.other_layers * Math.min(ctx, a.window) : 0;
  return perTok * (a.full_layers * ctx + windowed) / (1024 ** 3);
}

// what it was trained on, as opposed to what yarn extends it to. gpt-oss is
// the case that makes the difference worth a column: 4096 trained, 131072
// reported, a factor of 32 of extrapolation between them.
const trainCtx = m => m.facts.context_trained || m.facts.context_native;

// a model that cannot reach the context is not a fit at it. this reads the
// EXTENDED window, since that is what llama.cpp serves out of the gguf without
// a flag; whether the extrapolated part is worth having is the reader's call,
// and the two columns put both numbers in front of them.
//
// a context window is a TEXT model's promise, so the demand is asked of text
// models and of nothing else. two rounds of the same bug got it here.
//
// first: a model publishing NO window has not failed to reach one, and `|| 0`
// said it had, so the whole non-text roster read as `does not fit` on a box
// with 128gib free. that was fixed by passing an absent window.
//
// which left the half the absence was standing in for. breeze-tts-2 is 3.2gib
// at Q8_0 and declares 2048 -- the text its encoder takes, not a chat context
// anybody is going to fill -- and failed a 131072 demand on a 128gib box. so
// did 20 other entries: most of the speech roster, both translators, both
// punctuators. `fits vram` is a control about MEMORY, and answering it with a
// context mismatch is the same category error as reading "no quant fits" off
// zero quants. what makes the rule right for text and wrong here is not
// whether a number was published, it is whether a reader chooses the context:
// that is `kind: text`, a model served as a chat or completion endpoint.
const reaches = m => !minCtx || m.kind !== 'text' || !m.facts.context_native
  || m.facts.context_native >= minCtx;

// and the cache charged against a model is the one it can hold. asking for
// 131072 tokens against a 2048-token window bills for a cache that cannot
// exist, which is the same demand arriving through the arithmetic instead of
// through the filter.
const wantCtx = m => m.facts.context_native
  ? Math.min(minCtx, m.facts.context_native) : minCtx;

// the longest context whose cache fits beside the weights. windowed layers cap
// at their window, so past that only the full-attention layers keep growing.
function fitContext(m) {
  const q = activeQuant(m), a = m.facts.attn, native = m.facts.context_native;
  if (!budget || !q || !q.gib || !a || !native) return null;
  const room = (usable() - q.gib - draftGib(m)) * (1024 ** 3);
  if (room <= 0) return 0;
  const perTok = kvPerToken(a);
  const windowed = a.window ? a.other_layers * a.window * perTok : 0;
  const ctx = (room - windowed) / (perTok * a.full_layers);
  // never above the trained window: going past it needs rope scaling, which is
  // the consumer's decision rather than a number this page can report
  return Math.max(0, Math.min(native, Math.floor(ctx)));
}

// every (repo, quant) this model can be read as. keyed by the pair because a
// model may declare two quants OUT OF THE SAME repo -- gemma 4 31b pins Q8_0
// and UD-Q4_K_XL -- and expanding that repo's listing once per declared quant
// listed all 25 of them twice.
function quantChoices(m) {
  const seen = new Map();
  m.quants.forEach(q => {
    const alt = (q.available || []).length ? q.available
      : [{quant: q.quant, file: q.file, gib: q.gib, bpw: q.bpw}];
    alt.forEach(a => {
      const key = q.repo + ':' + a.quant;
      const was = seen.get(key);
      if (was) { was.pinned = was.pinned || a.quant === q.quant; return; }
      // `file` is what to fetch, `quant` is what to call it. they differ where
      // a repo does not name its files after the tag -- whisper.cpp's
      // `ggml-large-v3-turbo-q8_0.bin` is the Q8_0 rung
      seen.set(key, {repo: q.repo, quant: a.quant, file: a.file || a.quant,
                     gib: a.gib, bpw: a.bpw,
                     // what the file IS, where its tensor table has been read.
                     // `realBpw` is over the block geometry of every tensor;
                     // `bpw` beside it is file size over parameter count
                     types: a.types, realBpw: a.real_bpw,
                     pinned: a.quant === q.quant, speculative: q.speculative,
                     forkType: a.fork_type, crispasr: q.crispasr,
                     note: a.quant === q.quant ? proseText(q.note) : undefined});
    });
  });
  return [...seen.values()];
}

// whether serving from this repo can speculate at all. the capability is a
// property of the GGUF rather than of the model: `draft-mtp` needs the nextn
// head, which qwen ships only in the `-MTP-GGUF` build, so the plain repo of
// the same model cannot draft however the registry describes the model.
const repoSpeculates = (m, repo) =>
  !!((m.speculative || {}).type || (m.speculative || {}).draft_repo)
  && quantChoices(m).some(c => c.repo === repo && c.speculative !== false);

// which quant this model is being READ as. with no budget that is the one the
// registry pins; with one it is the largest that fits, which is the question
// somebody with 128gb is actually asking. the search stays inside the pinned
// quant's repo -- crossing to the -MTP- build changes whether it can speculate
// at all, and that is a choice rather than a size.
// the biggest quant in one repo that clears the vram budget and the ceiling and
// floor set on the main page. the modal opens on this rather than on whatever
// the registry pinned, so what you read there matches the row you clicked.
function bestInRepo(m, repo) {
  const all = quantChoices(m).filter(c => c.repo === repo);
  const pinned = all.find(c => c.pinned) || all[0] || null;
  // no sizes for this repo is not the same answer as nothing fits. hy3's
  // publisher lists no file sizes, and reporting it as too big would be a
  // measurement this repo does not have
  if (!budget || !all.some(c => c.gib)) return pinned;
  if (!reaches(m)) return null;
  const room = usable() - kvGib(m, wantCtx(m)) - draftGib(m);
  const fits = affordable(m, all, room).sort((a, b) => a.gib - b.gib);
  return fits.length ? fits[fits.length - 1] : null;
}

// --- speculative decoding ----------------------------------------------------
//
// drafting proposes n tokens and the target verifies them in ONE pass, keeping
// everything up to the first rejection. so the gain is tokens per target pass,
// and with a per-token acceptance p the expected yield is 1 + sum(p^k) over
// k=1..n -- geometric, which is why the terms past the third are worth almost
// nothing and why the registry drafts 3 for qwen3.8 and 6 for qwen3.6.
//
// p is a single number for every model, which is the weak part of this. it is
// set to the value that reproduces the only end-to-end measurement this repo
// holds: qwen3.8 27b on a strix halo under vulkan with the MTP predictor, at
// 16.68 / 14.24 / 12.74 t/s for UD-Q5_K_XL / Q6_K / Q8_0. against the same
// arithmetic without drafting that is 1.97x, 1.90x and 2.16x; 1 + sum(0.55^k,
// k=1..3) is 2.02. MODELS.md records the same log reporting acceptance between
// 0.546 and 0.88 on one model, so treat this as the middle of a wide range.
const DRAFT_ACCEPT = 0.55;

// the drafter's weights have to be resident either way; what differs is only
// whether the publisher put them in the quant or beside it. qwen's -MTP- build
// carries the head, so the quant already paid; gemma, deepseek and glimmer
// ship a sidecar, so it is added here and comes out of the vram budget.
const draftKind = m => (m.speculative || {}).type || '';
const draftGib = m => ((m.speculative || {}).draft || {}).gib || 0;

// what drafting yields, wherever the vendor ships a drafter. the read cost of
// the draft pass itself is NOT modelled -- for a head of half a gib beside 30
// of weights that is noise, for deepseek's 10gib dspark it is not -- so this
// is an upper bound, tightest where the drafter is smallest.
function draftYield(m) {
  const n = (m.speculative || {}).n_max;
  if (!draftKind(m)) return 1;
  let out = 1, p = 1;
  for (let k = 0; k < (n || 3); k++) { p *= DRAFT_ACCEPT; out += p; }
  return out;
}

// which repo a model is READ from, in the table and in the modal alike. where a
// model ships two builds the registry says which can speculate -- qwen3.6-27b's
// plain repo is marked `speculative: false` and only the -MTP- one carries the
// nextn head -- so taking whichever happened to be listed first threw that away
// and made the row disagree with the modal it opened.
const defaultRepo = m => {
  const repos = [...new Set(quantChoices(m).map(c => c.repo))];
  return repos.find(r => repoSpeculates(m, r)) || repos[0] || null;
};

// which quant a ROW is being read as. an expanded row carries its own; a model
// row asks for the largest that fits.
const activeQuant = m => m._q !== undefined ? m._q : bestInRepo(m, defaultRepo(m));
// an entry with no quants at all -- onnx-only weights the roster carries to say
// what it is MISSING -- has no size to weigh, and answering "does it fit" with
// `no` states something the data does not. it passes here, and the runtime
// filter, which is the one that means unservable, is what hides it. `fits vram`
// is on by default, so getting this wrong makes those entries unreachable.
const fitsBudget = m => !budget || !m.quants.length || !!activeQuant(m);

// what goes after the colon in `repo:TAG`, which llama.cpp resolves against a
// type name or a filename. the type where the rung has one, the filename where
// it does not -- a vae or a voice embedding ships at one precision and names no
// rung, so its `quant:` is absent rather than holding the filename it used to.
const hfTag = q => (q.quant || q.file);

// who built the gguf, which is the repo's owner and usually NOT the model's
// publisher: most rungs here are unsloth's or bartowski's work over somebody
// else's weights, and whose build you are about to download is part of the
// answer to which quant fits.
const quantAuthor = q => (q.repo || '').split('/')[0];

// every quant of the pinned repo the reader is being offered, largest first.
// with `fits vram` on that is what clears the budget, the ceiling and the floor:
// the same test the fit uses, without the last step that picks one, so `every
// quant that fits` and `the one that fits` can never disagree about what fits.
// with it OFF the page is not being asked what fits, and a ladder that still
// stopped at the budget would be answering a question somebody turned off -- it
// read as a fact about the model the size of the box they stopped caring about.
// the row keeps READING the largest that fits, because one row names one quant.
function fittingQuants(m) {
  const q = activeQuant(m);
  if (!q) return [];
  const all = quantChoices(m).filter(c => c.repo === q.repo);
  if (!budget || !all.some(c => c.gib)) return [q];
  if (!filters.flags.has('fits')) {
    // a rung nobody weighed is not a rung that failed the weighing, so it stays
    // on the ladder rather than dropping out with the fit
    const rung = c => (c.gib === undefined ? -Infinity : c.gib);
    return [...all].sort((a, b) => rung(b) - rung(a));
  }
  const room = usable() - kvGib(m, wantCtx(m));
  return affordable(m, all, room).sort((a, b) => b.gib - a.gib);
}

// one row per model, or one per (model, quant). the expanded row inherits the
// model rather than copying it, so every column reads the same facts and only
// the quant differs -- and it carries its own score, because quant adjusted
// discounts by the quant, which is the whole reason to look at the ladder.
function expand(models) {
  if (!allQuants) return models;
  return models.flatMap(m => {
    const qs = fittingQuants(m);
    if (qs.length < 2) return [m];
    return qs.map(q => Object.assign(Object.create(m), {_q: q, _s: null}));
  });
}

// --- speed -------------------------------------------------------------------
//
// the two halves of inference are limited by two different things, so they read
// two different settings and neither is derivable from the other. generating a
// token reads every active weight and the whole cache once, which is bandwidth;
// prefilling a prompt multiplies through the same weights, which is flops.
//
// both selects take the SPEC SHEET number, because that is what a reader knows
// about their box, and the efficiencies below turn it into what the box does.
// they are rules of thumb rather than measurements -- decode streams weights
// almost perfectly, a prefill matmul lands nowhere near peak -- so the columns
// are worth an order of magnitude and a comparison between models, not a
// promise. 256 gb/s of strix halo through this arrives at the 160 gb/s
// build-tables measures.
let BW_EFFICIENCY = 0;
let FLOPS_EFFICIENCY = 0;
let BANDWIDTHS = [];
let FLOPSES = [];
let bandwidth = 0;
let flops = 0;
let allQuants = false;             // one row per model, or one per rung offered

// two bounds rather than one number. decode reads the active weights every
// step, and the whole cache with them -- which starts empty and ends up the
// bigger half for a model that skimped on gqa. `empty` is the figure everyone
// quotes; `full` is what it decays to with the context you asked for resident.
// ling 3.0 flash is the case that makes the difference worth printing: 42 full
// attention layers at 32 kv heads is 84 gib of cache at 128k, against 5 gib of
// active weights.
function tgTps(m) {
  const q = activeQuant(m), a = activeB(m);
  if (!bandwidth || !q || !q.bpw || a === undefined) return null;
  const eff = bandwidth * 1e9 * BW_EFFICIENCY;
  const weights = a * 1e9 * q.bpw / 8;
  const y = draftYield(m);
  return {empty: y * eff / weights,
          full: y * eff / (weights + kvGib(m, wantCtx(m)) * (1024 ** 3)),
          draft: y};
}

// prefill is two flops per active weight per token and ignores attention's
// quadratic term, so it reads optimistic on a long prompt. it does not depend
// on the quant: llama.cpp dequantizes to compute either way.
function ppTps(m) {
  const a = activeB(m);
  return flops && a !== undefined ? flops * 1e12 * FLOPS_EFFICIENCY / (2 * a * 1e9) : null;
}

// the curve for THIS model: its own measurement if somebody ran one ON THE RUNG
// ASKED ABOUT -- the one scored, unless a caller names another -- the median of
// the measured curves once enough models have one, and build-tables' fitted
// curve otherwise. which one answered is never hidden.
//
// a sweep measures FILES, not a model. ISTA's card scores its own GSQ-RCO rungs
// of qwen3.8 27b and unsloth's UD rungs over the same three benchmarks and they
// differ by more than eight points of task average at 2.5 bpw, so lending one
// family's curve to the other's rung would report a number nobody measured.
function curveFor(m, q = activeQuant(m)) {
  const r = D.retention;
  const own = (r.measured || {})[m.repo] || [];
  const mine = own.find(c => q && c.quant_repo === q.repo) || own.find(c => !c.quant_repo);
  if (mine) return {points: mine.points, kind: 'measured', src: mine};
  if (r.median && r.median.points) return {points: r.median.points, kind: 'median', src: r.median};
  return {points: r.fitted.points, kind: 'fitted', src: r.fitted};
}

function interpolate(c, bpw) {
  if (bpw <= c[0][0]) return c[0][1];
  for (let i = 0; i < c.length - 1; i++) {
    const [x0, y0] = c[i], [x1, y1] = c[i + 1];
    if (bpw >= x0 && bpw <= x1) return y0 + (y1 - y0) * (bpw - x0) / (x1 - x0);
  }
  return 1;
}

// a MEASURED curve can be shorter than the fitted one and stop well above the
// rungs a reader can select. quesma ran qwen3.8 27b at three arms on
// terminal-bench and the lowest is 3.11 bpw; clamping there would answer 0.904
// for a two-bit quant where the fit says 0.778 -- a measurement of one model
// making its thin quants look BETTER than the general case, purely because
// nobody ran that arm. below its own range a measured curve therefore defers to
// the fitted one, which is the wider evidence rather than the narrower silence.
function retention(bpw, m, q = activeQuant(m)) {
  const c = curveFor(m, q);
  if (c.kind === 'measured' && bpw < c.points[0][0]) {
    return interpolate(D.retention.fitted.points, bpw);
  }
  return interpolate(c.points, bpw);
}

// a model whose weights are natively low-bpw is not paying a quantization
// penalty for being small, so it is exempt -- the registry says which
function modelRetention(m) {
  if (!effective || m.native_low_bpw) return 1;
  const q = activeQuant(m);
  return q && q.bpw ? retention(q.bpw, m, q) : 1;
}

// whether the rung being served sits below everything the curve measured, where
// `retention` returns the lowest fitted point forever rather than continuing to
// fall. the fitted curve stops at deepseek v3.1's 2.21 bpw and a 1.67 bpw rung
// reads as keeping 77.8%, which is not a prediction -- it is the last thing the
// curve knew. quesma's qwen3.8 27b sweep is the only measurement in that region
// and it found a 27b collapsing to chance at 1.8 bpw, so the flat part is
// evidenced against on the one model anybody has run there.
function belowCurve(m, q = m && activeQuant(m)) {
  if (!m || m.native_low_bpw) return false;
  return !!(q && q.bpw && q.bpw < curveFor(m, q).points[0][0]);
}

// an ALLOWLIST: a facet is discounted only where the curve is evidence about
// what it measures. the curve is one sweep of one model on a code-editing pass
// rate, so it answers for code and says so about everything else. build-viewer
// refuses to build a facet that is on neither list.
let scaledSet = null;
const scaledFacet = key =>
  (scaledSet || (scaledSet = new Set(D.retention.scaled))).has(key);

let evidenceOf = null;
function whyNotScaled(key) {
  if (!evidenceOf) {
    evidenceOf = {};
    D.retention.evidence.forEach(e => e.facets.forEach(k => { evidenceOf[k] = e; }));
  }
  return (evidenceOf[key] || {}).why || '';
}
const facetValue = (m, key) => m.facets[key].value
  * (scaledFacet(key) ? modelRetention(m) : 1);

// percentiles ship precomputed over raw values, so effective mode has to rank
// the cohort again -- against the scaled numbers, or a discount every model
// paid would move nobody
let pctCache = null;

function facetPctRaw(m, key) {
  const f = m.facets[key];
  if (!effective || !scaledFacet(key)) return f.pct;
  if (!pctCache) {
    pctCache = {};
    const all = new Set();
    D.models.forEach(x => Object.keys(x.facets).forEach(k => all.add(k)));
    all.forEach(k => {
      if (!scaledFacet(k)) return;
      pctCache[k] = D.models.filter(x => x.facets[k]).map(x => facetValue(x, k));
    });
  }
  const pop = pctCache[key] || [];
  if (pop.length < 2) return null;
  const v = facetValue(m, key);
  // the same plotting position analyze-usecase computes for the raw values --
  // half the ties counted -- or effective mode would rank a cohort by one rule
  // and raw mode by another, and only one of them would give the bottom of a
  // three-model cohort a number that is not zero
  return Math.round(100 * (pop.filter(x => x < v).length
    + 0.5 * pop.filter(x => x === v).length) / pop.length);
}

function facetPct(m, key) {
  const keys = facetKeys(m, key).map(k => facetPctRaw(m, k)).filter(p => p !== null);
  if (!keys.length) return null;
  return keys.reduce((a, p) => a + p, 0) / keys.length;
}

// whether a weighted factor is a question anybody asks of this model. one
// weight set spans text, speech and image, and a text model has no word error
// rate -- counting the speech sliders against it would read in the evidence
// column as MISSING EVIDENCE rather than as a question nobody put to it.
//
// a board-scored factor asks by CAPABILITY, from `board_needs`, which is
// resolve-ids' own table of what each source measures. kind is close and wrong
// at the edges: gemma 4 e4b is a text model with an audio encoder and voice
// arena publishes its word error rate, and reading `some text model carries
// this` off that one row put a transcription factor in every text model's
// denominator. anything not scored by a board -- a card claim, a forum, a
// per-language rate -- falls back to the kind, where it belongs.
function can(m) {
  const ins = m.modalities.input || [], outs = m.modalities.output || [];
  const out = new Set();
  if (m.kind === 'text') out.add('text');
  if (ins.includes('audio') && outs.includes('text')) out.add('transcribes');
  if (outs.includes('audio')) out.add('synthesizes');
  if (outs.includes('image')) out.add('draws');
  return out;
}

let kindFacets = null;
function asked(m, key) {
  const need = (D.board_needs || {})[key.split('.')[0]];
  if (need) return can(m).has(need);
  if (!kindFacets) {
    kindFacets = {};
    D.models.forEach(x => {
      const s = kindFacets[x.kind] || (kindFacets[x.kind] = new Set());
      Object.keys(x.facets).forEach(k => s.add(k));
    });
  }
  const have = kindFacets[m.kind] || new Set();
  return key.endsWith('.*')
    ? [...have].some(k => k.startsWith(key.slice(0, -1)))
    : have.has(key);
}

// the composite: weighted mean of percentiles over the facets PRESENT, shrunk
// toward the middle by the weight that measured nothing.
//
// dividing by the weight actually used and stopping there is the obvious
// choice and the wrong one, and research/build-tables rejected it first: it
// redistributes the missing weight onto whatever the model DOES have, so a
// model measured by one source has that source counted twenty times harder
// than a model measured by seven. bonsai 27b took 19th of 92 that way, on a
// single forum percentile at weight 0.05 -- ahead of the qwen3.6 27b it is a
// 1-bit rebuild of, which carries six of the seven factors.
//
// so the uncovered weight is scored as the middle instead of as nothing. these
// are percentiles, whose median is 50 by construction, which is what makes the
// prior a constant rather than a fit: `unmeasured` becomes `typical`, which is
// the honest reading of an absence. a model measured on everything has no
// uncovered weight and is untouched by construction.
const SHRINK_PRIOR = 50;            // the percentile an unmeasured factor is worth
const SHRINK_LAMBDA = 0.5;          // how much of the uncovered weight speaks

// the prior cuts both ways, and only one of them is argued for above. it stops
// one good factor carrying a model up, and by the same arithmetic it stops one
// bad factor pulling it down: at 5% coverage the prior is 91% of the
// denominator, so the number is about the roster's median and not about the
// model. minicpm5 1b read 47 off a single 13th-percentile forum score, ahead of
// the 2b that beat it on that factor and on three more.
//
// so below this share of the asked weight there is no number worth printing,
// the same way there is none at zero coverage. this is a share of WEIGHT rather
// than a count of factors because the composite spends weight: four of the 0.05
// factors and one of the 0.3 ones are the same evidence, and `evidence` reports
// this share for that reason.
const COVER_FLOOR = 0.20;

function score(m) {
  let num = 0, den = 0, denMax = 0, have = 0, want = 0;
  for (const [key, w] of Object.entries(W)) {
    // two different questions, and both have to pass: `relevant` is whether the
    // VIEW is asking this, `asked` is whether this model could answer it. a
    // transcription board over the language-model roster fails the first; a
    // coding score for whisper fails the second
    if (!w || !relevant(key) || !asked(m, key)) continue;
    want++; denMax += w;
    const p = facetPct(m, key);
    if (p === null) continue;
    have++; num += w * p; den += w;
  }
  const cover = denMax ? den / denMax : 0;
  if (!den || cover < COVER_FLOOR) return {value: null, have, want, cover};
  const k = SHRINK_LAMBDA * (denMax - den);
  return {value: (num + k * SHRINK_PRIOR) / (den + k), have, want, cover};
}

const scored = m => (m._s || (m._s = score(m)));
// the memo is only valid for the weights, the quant discount and the SHAPE the
// score was computed under, so every setter that moves one of those drops it.
// it was four hand-written copies of this loop before the shape joined them.
const clearScores = () => D.models.forEach(m => { m._s = null; });

// --- columns -----------------------------------------------------------------
//
// defined once: each column knows its label, how to pull a sortable value, and
// how to draw its cell. sorting, hiding and reordering are generic over this
// list rather than written per column.

const facetCell = (m, key, digits) => {
  const f = m.facets[key];
  if (!f) return '<td class="n faint">-</td>';
  const pct = facetPctRaw(m, key);
  const scaled = effective && scaledFacet(key) && modelRetention(m) < 1;
  // a number left alone under `quant adjusted` says so, rather than looking
  // like one the discount forgot
  const held = effective && !scaledFacet(key) && modelRetention(m) < 1;
  return `<td class="n${scaled ? ' eff' : ''}"${scaled
    ? ` title="${num(f.value, digits)} raw, x${modelRetention(m).toFixed(3)} `
      + `${curveFor(m).kind} retention at ${(activeQuant(m) || {}).bpw} bpw"`
    : held ? ` title="published as-is: ${esc(whyNotScaled(key))}"` : ''}>`
    + `<span class="bar" style="--w:${pct === null ? 0 : pct}%">`
    + `<span>${num(facetValue(m, key), digits)}</span></span></td>`;
};
const facetVal = (m, key) => m.facets[key] ? facetValue(m, key) : -1;

// an arithmetic estimate never wears the certainty of a measured column: no
// percentile bar behind it, and a `~` in front of the number
const tps = v => v >= 100 ? String(Math.round(v)) : num(v, 1);
const noEstimate = (on, hint) => on
  ? '<td class="n faint" title="it publishes no active parameter count, or nothing'
    + ' it publishes fits the budget">?</td>'
  : `<td class="n faint" title="${esc(hint)}">-</td>`;

const COLUMNS = [
  {k: 'rank', t: '#', num: true, get: m => m._rank,
   help: 'rank under the current weights. it renumbers when you change them',
   cell: m => `<td class="n faint">${m._rank}</td>`},
  {k: 'short', t: 'model', num: false, get: m => m.short,
   help: "the registry's name for it, and who publishes it",
   // the quant rides along here too: with one row per quant the name repeats,
   // and `fits quant` is a column somebody may have hidden
   cell: m => `<td>${esc(m.short)}<span class="sub"> ${esc(m._q ? m._q.quant
     : m.publisher)}</span></td>`},
  {k: 'score', t: 'quality', num: true, get: m => scored(m).value ?? -1,
   help: "the weighted mean of its percentiles, over the factors it was actually measured on, pulled toward 50 by the weight that measured nothing. under 20% coverage that pull decides the answer, so no number is shown at all -- see the evidence column. set the weights under factors",
   cell: m => {
     const s = scored(m);
     if (s.value === null) {
       return `<td class="n faint" title="${s.have
         ? `measured on ${pctOf(s.cover)} of the weight this view asks for, `
           + `under the ${pctOf(COVER_FLOOR)} a composite needs before it says `
           + `more about this model than about the middle of the roster`
         : 'none of the weighted factors measured this model'}">-</td>`;
     }
     // a percentile is a rank, so it steps rather than slides: the ladder can
     // hold one number over several rungs while the discount behind it moves
     // the whole way. say what the discount was, so a flat column reads as
     // "still ahead of everything" rather than as a number that never updated
     const r = modelRetention(m), q = activeQuant(m);
     // below the curve's lowest measured point the multiplier stops falling, so
     // the number is a floor rather than a prediction and has to say which
     const floored = effective && belowCurve(m)
       ? `; ${q.bpw} bpw is below the lowest rung the curve measured `
         + `(${curveFor(m).points[0][0]}), so this is its floor rather than a `
         + `prediction -- the only sweep run that low found a 27b at chance`
       : '';
     const title = effective && r < 1 && q
       ? ` title="${num(s.value, 1)}, scored at x${r.toFixed(3)} `
         + `${curveFor(m).kind} retention for ${esc(q.quant)} at ${q.bpw} bpw${floored}"`
       : ` title="${num(s.value, 1)}"`;
     return `<td class="n"${title}><span class="bar" style="--w:${s.value}%">`
       + `<span>${num(s.value, 0)}</span></span></td>`;
   }},
  {k: 'evidence', t: 'evidence', num: true, get: m => scored(m).cover,
   help: 'how much of the weight this view asks for was actually measured, as a share. it reads WEIGHT rather than a count of factors because that is what the composite spends -- four of the cheap factors and one of the dear ones are the same evidence. under 20% no quality is reported at all',
   cell: m => {
     const s = scored(m);
     const cls = s.cover >= 0.999 ? 'dim' : s.cover >= COVER_FLOOR ? 'warn' : 'faint';
     return `<td class="n ${cls}" title="${s.have} of ${s.want} weighted factors`
       + ` measured this model, ${pctOf(s.cover)} of the weight asked for">`
       + `${pctOf(s.cover)}</td>`;
   }},
  {k: 'kind', t: 'kind', num: false, get: m => m.kind,
   help: 'text, image or speech',
   cell: m => `<td class="dim">${esc(m.kind)}</td>`},
  {k: 'params', t: 'params', num: true, get: m => m.facts.params_total_b ?? -1,
   help: 'total parameters, counted from the weights that ship. a * means the vendor advertises a different number; hover for both',
   cell: m => {
     const p = m.facts.params_total_b, adv = m.params.advertised_total_b;
     const act = m.params.advertised_active_b;
     if (!p && !adv) return '<td class="n faint">-</td>';
     // the counted total and the advertised one disagree by 7% on deepseek v4
     // flash, so the number is labelled rather than quietly averaged
     const off = p && adv && Math.abs(p - adv) / adv > 0.03;
     const shown = p || adv;
     const named = m.facts.params_source === 'name';
     const title = !p
       ? ` title="${adv}b, the vendor's figure; nothing here counted the tensors"`
       : named
         ? ` title="${p}b, taken from the name -- this repo's safetensors index does not add up"`
         : ` title="${p}b counted from the safetensors index${adv ? `, ${adv}b advertised` : ''}"`;
     return `<td class="n"${title}>${round1(shown)}b`
       + (off ? '<span class="sub" data-help="the counted total and the advertised one'
         + ' disagree by more than 3%; hover the number for both"> *</span>' : '') + '</td>';
   }},
  {k: 'active', t: 'active', num: true, get: m => activeB(m) ?? -1,
   help: 'parameters used per token. taken from the name a vendor encodes it in (-A3B), or artificial analysis where it has one. a dense model uses all of them, so it repeats the total',
   cell: m => {
     const a = activeB(m);
     if (a === undefined) return '<td class="n faint">-</td>';
     return `<td class="n">${round1(a)}b</td>`;
   }},
  {k: 'experts', t: 'experts', num: true, get: m => m.facts.experts ?? -1,
   help: 'experts routed per token, of the total. a count of experts, not of parameters: qwen3.6 35b a3b routes 8 of 256 and that comes to about 3b',
   cell: m => {
     const e = m.facts.experts, a = m.facts.experts_active;
     if (e) return `<td class="n dim">${a ? a + ' / ' : ''}${e}</td>`;
     // a model activating far fewer parameters than it holds is a mixture
     // whose config did not name its experts in any key this reads. calling
     // that dense would be asserting something false
     const act = activeB(m), total = m.facts.params_total_b;
     if (act && total && act < total * 0.9) return '<td class="n faint"'
       + ' data-help="a mixture of experts, but its config does not publish the counts">?</td>';
     return '<td class="n faint">dense</td>';
   }},
  {k: 'ctx', t: 'train ctx', num: true, get: m => trainCtx(m) ?? -1,
   help: 'the window it was actually trained on. where a vendor ships a rope or yarn config the longer number is bought rather than trained, and this is the number before that',
   cell: m => `<td class="n">${ctxLabel(trainCtx(m)) || '<span class="faint">-</span>'}</td>`},
  {k: 'extctx', t: 'ext ctx', num: true, get: m => m.facts.context_native ?? -1,
   help: 'how far rope or yarn scaling takes it, which is what the config reports and what llama.cpp reads out of the gguf. equal to the trained window unless the vendor ships a scaling config',
   cell: m => {
     const ext = m.facts.context_native, r = m.facts.rope;
     if (!ext) return '<td class="n"><span class="faint">-</span></td>';
     return `<td class="n${r ? ' warn' : ' dim'}"${r
       ? ` title="${esc(r.type)} x${r.factor} over a ${ctxLabel(r.original)} trained`
         + ' window: extrapolated, not trained"' : ''}>${ctxLabel(ext)}</td>`;
   }},
  {k: 'fitctx', t: 'fits ctx', num: true, get: m => fitContext(m) ?? -1,
   help: 'the longest context whose kv cache still fits once the weights and the reserve are paid for, capped at what the model was trained for. the cache is sized at f16, llama.cpp\'s default, so quantizing it with --cache-type-k/v q8_0 buys roughly twice this. needs a vram budget',
   cell: m => {
     if (!budget) return '<td class="n faint" title="set a vram budget under hardware">-</td>';
     const c = fitContext(m);
     if (c === null) return '<td class="n faint">-</td>';
     const full = c >= (m.facts.context_native || 0);
     return `<td class="n${full ? '' : ' warn'}">${ctxLabel(c)}</td>`;
   }},
  {k: 'quant', t: 'fits quant', num: false, get: m => (activeQuant(m) || {}).quant || '',
   help: 'the quant being read, and who built it. with a vram budget set, the largest that fits; otherwise the one the registry pins',
   cell: m => {
     const q = activeQuant(m);
     if (!q) return '<td class="faint" title="nothing this repo publishes fits the budget">does not fit</td>';
     return `<td title="${esc(q.repo)}">${esc(q.quant)}`
       + `<span class="sub"> ${esc(quantAuthor(q))}</span></td>`;
   }},
  {k: 'size', t: 'gib', num: true,
   get: m => activeQuant(m) ? activeQuant(m).gib + draftGib(m) : -1,
   help: 'what has to be resident before any cache: the weights at the fitted quant, plus the drafter where the publisher ships it as a separate file rather than folding it into the build. the kv cache is not included -- add the kv gib column for that',
   cell: m => {
     const q = activeQuant(m);
     if (!q || q.gib === undefined) return '<td class="n"><span class="faint">-</span></td>';
     const d = draftGib(m);
     return `<td class="n"${d ? ` title="${gib(q.gib)} weights + ${gib(d)} for `
       + `${esc(m.speculative.draft.file)}, the ${esc(draftKind(m))} head"` : ''}>`
       + `${gib(q.gib + d)}`
       + (d ? '<span class="sub"> +d</span>' : '') + '</td>';
   }},
  {k: 'kv', t: 'kv gib', num: true, get: m => kvGib(m, wantCtx(m)),
   help: 'what the kv cache costs at the context you set, at f16 keys and values -- llama.cpp\'s default, and what this page assumes throughout. --cache-type-k/v q8_0 roughly halves it. resident memory is this plus gib plus the reserve',
   cell: m => {
     const v = kvGib(m, wantCtx(m));
     if (!minCtx) return '<td class="n faint" title="set a context under hardware">-</td>';
     if (!m.facts.attn) return '<td class="n faint" title="its config publishes no attention geometry">?</td>';
     return `<td class="n dim">${gib(v)}</td>`;
   }},
  {k: 'bpw', t: 'bpw', num: true, get: m => (activeQuant(m) || {}).bpw ?? -1,
   help: 'bits per weight. the number that predicts how much the quant cost in quality',
   cell: m => `<td class="n dim">${num((activeQuant(m) || {}).bpw, 2) || '-'}</td>`},
  {k: 'tg', t: 'tg t/s', num: true, get: m => (tgTps(m) || {}).empty ?? -1,
   help: 'estimated tokens generated per second with the cache empty: the bandwidth you set, discounted, over the active weights at the fitted quant, times what speculative decoding yields where the model ships a drafter. it does not charge for reading the drafter itself, so it runs optimistic for a large one. a second, dimmer figure appears where a full cache at your context costs more than 15% of it. arithmetic, never a measurement',
   cell: m => {
     const t = tgTps(m);
     if (!t) return noEstimate(bandwidth, 'set a memory bandwidth under hardware');
     const decay = t.full < t.empty * 0.85;
     return `<td class="n dim" title="${tps(t.empty)} t/s with the cache empty`
       + (minCtx ? `, ${tps(t.full)} t/s with ${ctxLabel(minCtx)} of it resident` : '')
       + (t.draft > 1 ? `. includes x${t.draft.toFixed(2)} from ${esc(draftKind(m))}`
         + ` drafting ${(m.speculative.n_max || 3)} tokens; without it, `
         + `${tps(t.empty / t.draft)} t/s` : '')
       + `">~${tps(t.empty)}`
       + (decay ? `<span class="sub"> ${tps(t.full)}</span>` : '') + '</td>';
   }},
  {k: 'pp', t: 'pp t/s', num: true, get: m => ppTps(m) ?? -1,
   help: 'estimated prompt tokens prefilled per second: the compute you set, discounted, over two flops per active weight. it ignores attention, so it reads optimistic on a long prompt',
   cell: m => {
     const v = ppTps(m);
     return v === null ? noEstimate(flops, 'set a compute figure under hardware')
       : `<td class="n dim">~${tps(v)}</td>`;
   }},
  {k: 'scicode', t: 'aa scicode', num: true, get: m => facetVal(m, 'aa.scicode'),
   help: 'scicode pass rate on artificial analysis\' harness. it carries the coding weight their coding index carried until they retired it',
   cell: m => facetCell(m, 'aa.scicode', 1)},
  {k: 'tbench', t: 'aa tbench', num: true, get: m => facetVal(m, 'aa.terminalbench'),
   help: 'terminal-bench 2.1 pass rate: tool use and multi-step terminal work. it carries the agentic weight their agentic index carried',
   cell: m => facetCell(m, 'aa.terminalbench', 1)},
  {k: 'gbench', t: 'gbench', num: true, get: m => facetVal(m, 'gbench.agentic'),
   help: 'gbench agentic coding score. models play generated games, so there is no problem set to train against',
   cell: m => facetCell(m, 'gbench.agentic', 3)},
  {k: 'swe', t: 'swe-reb', num: true, get: m => facetVal(m, 'swerebench.resolved'),
   help: 'swe-rebench resolved rate, on pull requests merged after the model shipped',
   cell: m => facetCell(m, 'swerebench.resolved', 1)},
  {k: 'arena', t: 'arena', num: true, get: m => facetVal(m, 'lmarena.rating'),
   help: 'lmarena rating, style controlled. human preference rather than a grader',
   cell: m => facetCell(m, 'lmarena.rating', 0)},
  {k: 'community', t: 'community', num: true,
   get: m => facetVal(m, 'community.reddit-localllama'),
   help: 'mentions on r/LocalLLaMA, and how many of the opinionated ones were positive',
   cell: m => {
     const f = m.facets['community.reddit-localllama'];
     if (!f) return '<td class="n faint">-</td>';
     const a = f.approval;
     return `<td class="n"><span class="bar" style="--w:${f.pct || 0}%"><span>${f.mentions}`
       + (a === null || a === undefined ? '' : `<span class="sub"> ${a}%</span>`) + '</span></span></td>';
   }},
  {k: 'langs', t: 'best langs', num: false, get: m => (m.languages[0] || {}).lang || '',
   help: 'the languages gbench scored it highest on',
   cell: m => `<td class="dim">${esc(m.languages.slice(0, 3).map(l => l.lang).join(' ')) || '-'}</td>`},
  {k: 'bestfor', t: 'best for', num: false, get: m => (m.derived.best_for || [])[0] || '',
   help: 'the uses where it lands in the top third of the models measured on them',
   cell: m => `<td class="dim">${esc((m.derived.best_for || []).slice(0, 2).join(', ')) || '-'}</td>`},
  {k: 'think', t: 'thinking', num: false,
   get: m => (m.thinking.accepts || []).join(' / ') || (m.thinking.knob ? 'off / on' : ''),
   help: 'the thinking levels its chat template takes, with the default in bold',
   cell: m => {
     const t = m.thinking;
     if (!t.knob) return '<td class="faint"'
       + ' data-help="its chat template reads no thinking control, so there is nothing to set">'
       + 'none</td>';
     const undef = t.default === undefined && t.gate_default === undefined;
     return `<td class="dim"${undef
       ? ' data-help="no default: sending nothing injects no directive at all, so the model\'s own behaviour applies"'
       : ''}>${levels(t, ' / ')}${undef ? '<span class="sub"> ?</span>' : ''}</td>`;
   }},
  {k: 'profiles', t: 'profiles', num: false, get: m => Object.keys(m.sampling).join(','),
   help: 'the sampling profiles the registry defines for it',
   cell: m => `<td class="dim">${esc(Object.keys(m.sampling).join(' ')) || '-'}</td>`},
  {k: 'spec', t: 'draft', num: false, get: m => m.speculative.type || '',
   help: 'the speculative decoding method it supports, if any',
   cell: m => `<td class="dim">${esc(m.speculative.type || '')}${m.speculative.n_max ? `<span class="sub"> n${m.speculative.n_max}</span>` : ''}</td>`},
  // the id rather than the hub's tag: 29 models declare the tag `other` and
  // sort together under it, which tells a reader nothing. the tier rides in the
  // cell because the filter acts on the tier, and a model that vanished should
  // be identifiable by the same column that explains why
  {k: 'license', t: 'license', num: false, get: m => licenseOf(m).id || '',
   help: 'the licence its huggingface repo declares, under its own name rather than the hub\'s `other`, with how registry/licenses.yaml classifies it. `unknown` is nobody here having read those terms, not a verdict on them',
   cell: m => {
     const l = licenseOf(m);
     return `<td class="dim">${esc(l.id || '-')}`
       + `<span class="sub" title="${esc(l.why || tierHelp(l.tier))}"> ${esc(l.tier)}</span></td>`;
   }},
  {k: 'downloads', t: 'downloads', num: true, get: m => (m.card.hub || {}).downloads ?? -1,
   help: 'huggingface downloads last month. adoption, not quality',
   cell: m => `<td class="n dim">${(m.card.hub || {}).downloads ? fmt.format(m.card.hub.downloads) : '-'}</td>`},
  {k: 'repo', t: 'repo', num: false, get: m => m.repo,
   help: 'the huggingface repo. every join in this registry is keyed on it',
   cell: m => `<td class="dim">${esc(m.repo)}</td>`},
];

// the tier a licence nobody has classified lands in. spelled in
// registry/licenses.yaml; named here so the column, the filter and that file
// cannot disagree about it. the filter names no tier of its own -- it selects
// over whatever that file declares, so a fourth tier would need no code here.
//
// `license` is JOINED in build-viewer out of the captured string and the
// classification table, so this is a read rather than a derivation: the licence
// is a fact and the tier is a judgement, and neither moves when a reader moves
// a slider.
const UNKNOWN_TIER = 'unknown';
const licenseOf = m => m.license || {tier: UNKNOWN_TIER};
const tierHelp = k => ((D.licenses || []).find(t => t.k === k) || {}).help || '';

// which table columns read a scaled facet, so the header can say so
const SCALED_COLUMNS = {scicode: 'aa.scicode', tbench: 'aa.terminalbench',
                        gbench: 'gbench.agentic', swe: 'swerebench.resolved',
                        arena: 'lmarena.rating'};

// what the page opens on, all of it out of `registry/dashboard.yaml`: the
// column order and which of them start hidden, the box a reader is assumed to
// have, and the filters that are already pressed.
//
// `pp` and `tg` are hidden AND gated on their hardware figure: switching one
// on under the gear does nothing until there is a bandwidth or a compute
// number for it to read.
//
// the modality list is carried as a set because the filter tests membership
// and the share link carries a list, but the control is ONE choice: the shapes
// overlap rather than partition -- `audio to text` and `language models` share
// gemma 4, `any to text` contains both -- so picking two of them says less
// than picking the one that describes what you are after.
let DEFAULT_ORDER = [];
let DEFAULT_HIDDEN = [];
let DEFAULT_HARDWARE = {};
let DEFAULT_FLAGS = [];
let DEFAULT_MODALITIES = [];
let DEFAULT_MODALITY = '';
const col = k => COLUMNS.find(c => c.k === k);
// a column of `-` reads as missing data rather than as a setting you have not
// made, so the two estimates come and go with the hardware figure behind them
// instead of being one more thing to find under the gear
const NEEDS = {tg: () => !!bandwidth, pp: () => !!flops};
const available = k => !NEEDS[k] || NEEDS[k]();
const shown = () => order.filter(k => !hidden.has(k) && available(k));

// --- filtering ---------------------------------------------------------------

// what a model turns into what. `text` and `vision` used to be two chips you
// could hold down together, which said "a text model that also takes images"
// and could say nothing at all about the speech half of the roster -- there is
// no combination of two toggles that means audio in and text out. one list of
// shapes replaces them, and the shapes are the ones llama-swap-groups derives
// its group membership from, so a reader and a host name the same things.
//
// `text` stays first and stays the default because it is what a reader of this
// roster is usually after. it used to stay for a second reason -- MODELS.md's
// ranking blocks are generated by booting this page, so the default view WAS
// the document's roster -- and `research/dashboard-table` pins its own now,
// modality and flags both, because a ui default that rewrites a document is one
// decision doing two jobs.
//
// `language models` is the registry's own `kind`, which is a classification
// rather than a shape: it means an LLM you serve as a chat endpoint. that is
// neither a superset nor a subset of `any to text` -- 34 of its members take
// images,
// video or audio in, one of them emits embeddings and no text at all, and the
// twelve transcribers that DO emit text are `kind: speech` and not in it.
const MODALITIES = [
  {k: 'text', t: 'language models', test: m => m.kind === 'text',
   help: 'the registry `kind`: an LLM you serve as a chat or completion endpoint, whatever else it also takes in. this is the roster MODELS.md ranks'},
  {k: 'any2t', t: 'any to text', test: m => modOut(m, 'text'),
   help: 'everything that emits text, which is the language models plus the transcribers -- a wider roster than that one and a different one'},
  {k: 't2t', t: 'text to text', test: m => m.kind === 'text'
     && !modIn(m, 'image') && !modIn(m, 'audio'),
   help: 'text in, text out, and nothing else in'},
  {k: 'v2t', t: 'vision to text', test: m => m.kind === 'text' && modIn(m, 'image'),
   help: 'takes images in, according to its own config'},
  // no `kind` test: this used to read `kind === 'speech'` on the grounds that an
  // LLM which merely accepts audio is not a transcription model, and the
  // evidence went the other way. crispasr carries a backend for gemma 4 and
  // voice arena publishes its word error rate in seven languages -- it
  // transcribes, in 140 languages, and a filter for `audio in, text out` that
  // hides it is answering a different question than the one it asks
  {k: 'a2t', t: 'audio to text', test: m => modIn(m, 'audio') && modOut(m, 'text'),
   help: 'transcription: audio in, text out, whether that is all it does or one of several things'},
  {k: 't2a', t: 'text to audio', test: m => modOut(m, 'audio'),
   help: 'speech synthesis'},
  {k: 't2i', t: 'text to image', test: m => modOut(m, 'image'),
   help: 'image generation'},
  // the same binary as `text to image` and a different output. without its own
  // chip a model that emits frames sits in the image roster answering a
  // question it was not asked, and its percentiles would be computed against
  // models no image board scores
  {k: 't2v', t: 'text to video', test: m => modOut(m, 'video'),
   help: 'video generation, on the same stable-diffusion.cpp binary as the image models. no board this repo collects rates them, so they carry no score'},
  {k: 't2e', t: 'text to embeddings', test: m => modOut(m, 'embeddings'),
   help: 'embedding models'},
  {k: 'diar', t: 'diarization', test: m => m.kind === 'diarize',
   help: 'weights --diarize loads beside an ASR model. they transcribe nothing and are scored by nobody'},
  // `post` and `translate` carry no `modalities` block on purpose, the way the
  // diarizers do not: they run inside crispasr's pipeline rather than being
  // served, and declaring text in / text out would put a punctuation restorer
  // in `any to text` beside the language models. that leaves the kind as the
  // only thing to select them by
  {k: 'post', t: 'transcript post', test: m => m.kind === 'post',
   help: 'punctuation and language id, applied to a transcript after it exists. crispasr runs them by flag rather than by --backend, and no board scores them'},
  {k: 'mt', t: 'translation', test: m => m.kind === 'translate',
   help: 'text in, text in another language out. crispasr loads them to translate a transcript, and they are scored by nobody here'},
];
const modIn = (m, x) => (m.modalities.input || []).includes(x);
const modOut = (m, x) => (m.modalities.output || []).includes(x);
// the shapes currently picked. nothing picked filters nothing out, so the test
// is a union over what IS picked rather than over the whole list.
const modsOn = () => MODALITIES.filter(x => filters.mods.has(x.k));
const inModality = m => !filters.mods.size || modsOn().some(x => x.test(m));

// what each shape is ABOUT, in the same capability vocabulary `board_needs`
// uses. this is a claim about the VIEW rather than about whichever model in it
// happens to qualify, and that distinction is the whole point: eight models are
// `kind: text` and also transcribe -- the gemma 4 family, mimo v2.5, inkling --
// so asking "can any model here be asked this" turned on all 105 factors in
// both `language models` and `audio to text`, and the two lists came out
// byte-identical. it also put inkling 12th on an audio-to-text board on the
// strength of its reasoning scores, where its transcription evidence puts it
// 34th.
//
// `any to text` is the one that is genuinely about both, and says so: its help
// text calls it the language models plus the transcribers. the shapes with an
// empty list are the ones no board this repo collects rates at all.
const MODALITY_ABOUT = {
  text: ['text'], t2t: ['text'], v2t: ['text'],
  any2t: ['text', 'transcribes'],
  a2t: ['transcribes'], t2a: ['synthesizes'], t2i: ['draws'],
  t2v: [], t2e: [], diar: [], post: [], mt: [],
};

// the capabilities the current view is asking about, or null for no restriction
// -- nothing picked is every shape, so it is every question.
function askingAbout() {
  if (!filters.mods.size) return null;
  const out = new Set();
  filters.mods.forEach(k => (MODALITY_ABOUT[k] || []).forEach(c => out.add(c)));
  return out;
}

// whether the view is asking this question at all, as distinct from whether a
// model could answer it. a group with no declared capability is asked
// everywhere: `community` is the only one, because any model can be discussed.
function relevant(key) {
  const need = (D.board_needs || {})[key.split('.')[0]];
  if (!need) return true;
  const about = askingAbout();
  return !about || about.has(need);
}

// `shown: false` keeps the filter without the button. speculative and the
// thinking knob are columns and detail-page facts as well, and as toggles they
// answered a question nobody was asking of the whole roster -- a shared link
// carrying one still applies, which is why the test stays here.
const FLAGS = [
  {k: 'draft', t: 'speculative', shown: false, test: m => !!m.speculative.type,
   help: 'the registry records a speculative decoding method for it'},
  {k: 'think', t: 'thinking knob', shown: false, test: m => !!m.thinking.knob,
   help: 'its chat template reads a thinking control'},
  {k: 'fits', t: 'fits vram', test: m => fitsBudget(m),
   help: 'some quant of it fits your vram, after the reserve and the context kv cache'},
];

// a stored or shared filter set can name a flag this page no longer offers, the
// way a stored column order can name a column since dropped -- carrying the key
// would put it in every share link with nothing left to test it. the licence
// tiers get the same treatment against registry/licenses.yaml, which is what
// drops a stored `permissive` boolean rather than reading it as a tier
const knownFlags = ks => ks.filter(k => FLAGS.some(f => f.k === k));
const licenseTiers = () => (D.licenses || []).map(t => t.k);
const knownLicenses = ks => ks.filter(k => licenseTiers().includes(k));

function haystack(m) {
  return m._hay || (m._hay = [m.repo, m.short, m.match, m.facts.arch, m.facts.model_type,
    proseText(m.notes), m.card.summary, (m.derived.best_for || []).join(' '),
    ((m.card.hub || {}).tags || []).join(' '), Object.keys(m.tasks).join(' '),
    m.quants.map(q => q.repo + ' ' + q.quant).join(' ')].join(' ').toLowerCase());
}

function visible() {
  const q = filters.q.trim().toLowerCase();
  return D.models.filter(m => {
    if (q && !haystack(m).includes(q)) return false;
    if (filters.pubs.size && !filters.pubs.has(m.publisher)) return false;
    if (!inModality(m)) return false;
    // an unknown size cannot satisfy a size band. this is the opposite of the
    // rule the fit uses -- there a model with no context window has not FAILED
    // to reach one, so it passes -- and the difference is what the filter is
    // about: `fits vram` asks a question about a box and this one asks a
    // question about the attribute itself. 32 entries publish no count, and
    // answering "what is in the 1-4b class" with them at the top of the list
    // is answering with the models whose size nobody knows.
    // `!= null` rather than `!== null`, so an UNSET bound is off whether it is
    // null or undefined. the strict test read an absent field as a bound that
    // had been set, and every model publishing no parameter count -- 32 of
    // them -- vanished from every view including the default one
    if (filters.minParams != null || filters.maxParams != null) {
      const tp = m.facts.params_total_b;
      if (tp == null) return false;
      if (filters.minParams != null && tp < filters.minParams) return false;
      if (filters.maxParams != null && tp > filters.maxParams) return false;
    }
    // no runtime selected means no runtime filter, the way no flags does. a
    // model with an EMPTY engine list is one nothing here loads, so it only
    // appears once the filter is off entirely
    if (filters.engines.size
        && !(m.engines || []).some(e => filters.engines.has(e))) return false;
    // the same rule for the licence, over the tiers registry/licenses.yaml
    // declares. every model is in exactly one, so this is a pick rather than
    // the engines' any-of -- and selecting none is no licence filter, which is
    // how the restricted and the unclassified come back
    if (filters.licenses.size
        && !filters.licenses.has(licenseOf(m).tier)) return false;
    for (const f of filters.flags) {
      const flag = FLAGS.find(x => x.k === f);
      if (flag && !flag.test(m)) return false;
    }
    return true;
  });
}

function sorted(rows) {
  const c = col(sort.k) || col('score');
  const out = [...rows].sort((a, b) => {
    const x = c.get(a), y = c.get(b);
    const d = c.num ? (x - y) : String(x).localeCompare(String(y));
    // expanded rows of one model tie on everything the model owns, so the
    // quant breaks it and the ladder reads largest to smallest
    return d * sort.dir || a.short.localeCompare(b.short)
      || ((b._q || {}).gib || 0) - ((a._q || {}).gib || 0);
  });
  return out;
}

// the rows a table would draw, in order, each carrying the rank it landed at.
// rank is a position in the CURRENT ranking rather than a property of a model,
// so it renumbers when the weights move -- which is the point of it. split out
// of drawTable so that something with no dom can ask for the same list.
function rankedRows() {
  const rows = sorted(expand(visible()));
  rows.forEach((m, i) => { m._rank = i + 1; });
  return rows;
}

// --- configuration -----------------------------------------------------------

// every default, out of the payload. the config travels from
// `registry/dashboard.yaml` through `scripts/build-viewer` into
// `docs/data.json`, so the page, `scripts/aimbot` and MODELS.md read one copy
// of it and a judgement about what the ranking means lives beside the models
// it ranks. must run before anything renders, and before the page restores
// whatever a reader stored over the top.
function applyConfig(cfg) {
  CAPS = cfg.caps.map(c => [c.k, c.bpw === null ? Infinity : c.bpw, c.label]);
  FLOORS = cfg.floors.map(c => [c.k, c.bpw, c.label]);
  cap = cfg.hardware.cap;
  floor = cfg.hardware.floor;
  BW_EFFICIENCY = cfg.speed.bandwidth_efficiency;
  FLOPS_EFFICIENCY = cfg.speed.flops_efficiency;
  KV_BYTES = cfg.speed.kv_bytes;
  BANDWIDTHS = cfg.speed.bandwidths.map(b => [b.value, b.label]);
  FLOPSES = cfg.speed.flopses.map(f => [f.value, f.label]);
  DEFAULT_ORDER = cfg.columns.order;
  DEFAULT_HIDDEN = cfg.columns.hidden;
  DEFAULT_HARDWARE = cfg.hardware;
  DEFAULT_FLAGS = cfg.filters.flags;
  DEFAULT_MODALITIES = cfg.filters.modalities;
  DEFAULT_MODALITY = cfg.filters.modalities[0];
  DEFAULT_ENGINES = cfg.filters.engines;
  DEFAULT_LICENSES = cfg.filters.licenses;
  RUNTIMES = cfg.runtimes;
  // a list in the config so the order it was written in survives a payload
  // written with sorted keys, and an object here because every caller looks a
  // preset up by name
  PRESETS = Object.fromEntries(cfg.presets.map(p => [p.k, {
    t: p.title,
    w: () => {
      if (!p.base) return {...(p.weights || {})};
      const w = {...D.weights};
      (p.drop_prefixes || []).forEach(pre => Object.keys(w).forEach(
        x => { if (x.startsWith(pre)) delete w[x]; }));
      return w;
    },
  }]));
}

// the named weightings and the runtimes a snippet can be written for. filled
// by applyConfig; declared here because the page reads both.
let PRESETS = {};
let RUNTIMES = [];

// the state a reader gets with nothing stored and nothing shared, which is the
// view MODELS.md is generated from. the page calls this and then layers its
// localStorage and any shared link over the top; a consumer with no browser
// calls it and stops, and the two therefore start from the same place.
function loadRoster(payload) {
  D = payload;
  applyConfig(D.config);
  W = {...D.weights};
  order = [...DEFAULT_ORDER];
  COLUMNS.forEach(c => { if (!order.includes(c.k)) order.push(c.k); });
  hidden = new Set(DEFAULT_HIDDEN);
  filters = {q: '', kind: new Set(), pub: '', pubs: new Set(),
             mods: new Set(DEFAULT_MODALITIES), flags: new Set(DEFAULT_FLAGS),
             engines: new Set(DEFAULT_ENGINES),
             licenses: new Set(DEFAULT_LICENSES),
             minParams: null, maxParams: null};
  budget = DEFAULT_HARDWARE.budget;
  reserve = DEFAULT_HARDWARE.reserve;
  minCtx = DEFAULT_HARDWARE.minCtx;
  cap = DEFAULT_HARDWARE.cap;
  floor = DEFAULT_HARDWARE.floor;
  bandwidth = DEFAULT_HARDWARE.bandwidth;
  flops = DEFAULT_HARDWARE.flops;
  return D;
}

// one place to apply the settings a caller without controls would otherwise
// have to reach in and set, which is what a cli is. every field is optional and
// an absent one leaves the default alone.
function applySettings(o) {
  o = o || {};
  // zero is the page's way of saying no budget rather than a budget of none,
  // which is what its own `#ram` control does with it
  if (o.ram !== undefined && o.ram !== null) budget = o.ram > 0 ? o.ram : null;
  if (o.reserve !== undefined && o.reserve !== null) reserve = o.reserve;
  if (o.ctx !== undefined && o.ctx !== null) minCtx = o.ctx;
  if (o.cap) cap = o.cap;
  if (o.floor) floor = o.floor;
  if (o.bandwidth !== undefined && o.bandwidth !== null) bandwidth = o.bandwidth;
  if (o.flops !== undefined && o.flops !== null) flops = o.flops;
  if (o.raw) effective = false;
  if (o.ladder) allQuants = true;
  // the page opens with filters already on, so naming one REPLACES that
  // default and `all` drops the four of them
  if (o.all) {
    filters.mods = new Set(); filters.flags = new Set(); filters.engines = new Set();
    filters.licenses = new Set();
  }
  if (o.modalities && o.modalities.length) filters.mods = new Set(o.modalities);
  if (o.flags && o.flags.length) filters.flags = new Set(o.flags);
  if (o.engines && o.engines.length) filters.engines = new Set(o.engines);
  if (o.licenses && o.licenses.length) filters.licenses = new Set(o.licenses);
  if (o.publishers && o.publishers.length) filters.pubs = new Set(o.publishers);
  if (o.minParams !== undefined && o.minParams !== null) filters.minParams = o.minParams;
  if (o.maxParams !== undefined && o.maxParams !== null) filters.maxParams = o.maxParams;
  if (o.grep) filters.q = o.grep;
  if (o.weights && PRESETS[o.weights]) W = PRESETS[o.weights].w();
  if (o.sort) {
    const c = col(o.sort);
    // a number reads largest first and a name reads A first, which is what the
    // page does when a header is clicked for the first time
    sort = {k: o.sort, dir: o.asc === undefined || o.asc === null
            ? (c && c.num ? -1 : 1) : (o.asc ? 1 : -1)};
  } else if (o.asc !== undefined && o.asc !== null) {
    sort = {k: sort.k, dir: o.asc ? 1 : -1};
  }
  clearScores();
}

// what the page offers, read off this file rather than restated by a consumer.
// a column added here is askable from the cli the same day.
const vocabulary = () => ({
  columns: COLUMNS.map(c => ({k: c.k, t: c.t, num: !!c.num, help: c.help || ''})),
  modalities: MODALITIES.map(m => ({k: m.k, t: m.t, help: m.help || ''})),
  flags: FLAGS.map(f => ({k: f.k, t: f.t, help: f.help || ''})),
  presets: Object.keys(PRESETS).map(k => ({k: k, t: PRESETS[k].t})),
  engines: [...new Set(D.models.flatMap(m => m.engines || []))].sort(),
  publishers: [...new Set(D.models.map(m => m.publisher))].sort(),
  caps: CAPS.map(c => c[0]), floors: FLOORS.map(c => c[0]),
  licenses: (D.licenses || []).map(t => ({k: t.k, t: t.label || t.k,
                                          help: t.help || ''})),
});

// how many models each active filter is responsible for removing, so a caller
// can say WHY the roster is shorter than the registry. one pass per filter with
// that filter ALONE, which is the number a reader is asking for -- "this many
// are not permissive" -- rather than the marginal one, which depends on the
// order they happen to be applied in and is a fact about nothing. they overlap,
// so they do not sum to the difference, and a caller printing them should say
// so rather than imply an accounting.
const filterCounts = () => {
  const total = D.models.length, out = [];
  if (filters.mods.size) {
    out.push({k: 'modality', t: [...filters.mods].join(','),
              dropped: total - D.models.filter(inModality).length});
  }
  if (filters.engines.size) {
    out.push({k: 'engine', t: [...filters.engines].join(','),
              dropped: total - D.models.filter(
                m => (m.engines || []).some(e => filters.engines.has(e))).length});
  }
  if (filters.licenses.size) {
    out.push({k: 'license', t: [...filters.licenses].join(','),
              dropped: total - D.models.filter(
                m => filters.licenses.has(licenseOf(m).tier)).length});
  }
  filters.flags.forEach(k => {
    const flag = FLAGS.find(x => x.k === k);
    if (flag) {
      out.push({k: k, t: flag.t,
                dropped: total - D.models.filter(flag.test).length});
    }
  });
  return out;
};

// the current hardware, for a caller that wants to print what it answered under
const hardware = () => ({budget, reserve, minCtx, cap, floor, effective,
                         bandwidth, flops});

// under node this is a module; inlined into the page it is not, and the page
// reads every one of these as a plain global from the same scope.
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {loadRoster, applySettings, rankedRows, vocabulary, hardware,
                    filterCounts, licenseOf,
                    visible, sorted, expand, col, shown, scored, activeQuant,
                    fittingQuants, quantChoices, kvGib, fitContext, tgTps, ppTps,
                    modelRetention, curveFor, belowCurve, facetValue, facetPctRaw,
                    COLUMNS, MODALITIES, FLAGS, proseText, esc, num, gib, ctxLabel};
}
