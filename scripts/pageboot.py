"""Boot the shipped viewer under node, with a dom stub thin enough to be honest.

The page is one html file with no build step, no imports and no framework, so
it can be RUN rather than reimplemented -- which is the only way a second
consumer of the same ranking can be guaranteed to agree with it. `tests/e2e`
asserts on the page's arithmetic this way, and `research/dashboard-table`
generates MODELS.md's ranking from it, so the document and the dashboard cannot
drift: there is one implementation and both read it.

The stub memoizes elements by selector, so innerHTML written by drawTable is
readable afterwards. querySelectorAll returns nothing, which means event
handlers never bind -- interaction is driven by calling the function the
handler would have called, which is the same code path.
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PAGE = os.path.join(ROOT, "docs", "index.html")
DATA = os.path.join(ROOT, "docs", "data.json")

STUB = """
const nodes = {};
const el = key => nodes[key] || (nodes[key] = {
  style: {}, dataset: {}, children: [], value: '', textContent: '', innerHTML: '',
  classList: {add(){}, remove(){}, toggle(){}, contains(){return false}},
  setAttribute(){}, getAttribute(){return 'false'}, addEventListener(){},
  querySelector(s){ return el(key + ' ' + s); }, querySelectorAll(){ return []; },
  getBoundingClientRect(){ return {left:0, top:0, bottom:0, width:0, height:0}; },
  onclick: null,
});
global.document = {
  querySelector(s){ return el(s); }, querySelectorAll(){ return []; },
  addEventListener(){}, body: el('body'), title: '',
};
global.window = global;
global.location = {hash: '', pathname: '/', search: ''};
global.history = {replaceState(){}};
const mem = {};
global.localStorage = {
  getItem(k){ return k in mem ? mem[k] : null; },
  setItem(k, v){ mem[k] = v; }, removeItem(k){ delete mem[k]; },
};
global.addEventListener = () => {};
global.innerWidth = 1200;
global.innerHeight = 800;
global.CSS = {escape: s => s};
const PAYLOAD = require('fs').readFileSync(%s, 'utf8');
// the registry's own count, so "the payload is the whole registry" stays the
// assertion when a model is added rather than becoming a number to bump
const REGISTRY_MODELS = %s;
global.fetch = () => Promise.resolve({json: () => JSON.parse(PAYLOAD)});
process.on('unhandledRejection', e => {
  console.log('FAIL boot threw: ' + ((e && e.stack) || e));
  process.exit(1);
});
const html = s => el(s).innerHTML;
"""


def registry_models():
    """How many models the registry carries, counted from the registry."""
    import yaml
    reg = os.path.join(ROOT, "registry", "models.yaml")
    return len(yaml.safe_load(open(reg)).get("models") or {})


def page_script():
    """The page's own script block, verbatim. It is what gets tested and read."""
    for path in (PAGE, DATA):
        if not os.path.exists(path):
            sys.exit("!!! %s is missing, run: make site" % path)
    script = re.search(r"<script>(.*)</script>", open(PAGE).read(), re.S)
    if not script:
        sys.exit("!!! no script block in %s" % PAGE)
    return script.group(1)


def run(body, probe, keep=False, capture=False):
    """Write STUB + the page + `body` to `probe` and run it under node."""
    with open(probe, "w") as f:
        f.write(STUB % (json.dumps(DATA), registry_models()) + page_script() + body)
    try:
        return subprocess.run(["node", probe], cwd=ROOT,
                              stdout=subprocess.PIPE if capture else None, text=True)
    except FileNotFoundError:
        sys.exit("!!! node is not on PATH")
    finally:
        if not keep and os.path.exists(probe):
            os.remove(probe)
