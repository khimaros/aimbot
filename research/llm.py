"""An OpenAI-compatible chat client, for the steps no collector can do.

Every other collector here asks a source a question with one right answer. This
one asks a model to make a judgement, which is a different kind of input and is
kept at arm's length accordingly: nothing that calls this writes
`registry/models.yaml` or `usecase-assessed.json`. It writes a proposal file a
human reads, and every claim it is asked for is one an index already here can
refute.

Configured from `.env` at the repo root, or from the environment directly:

    AIMBOT_LLM_URL     an OpenAI-compatible base, default http://localhost:8080/v1
    AIMBOT_LLM_MODEL   the model name to send; llama-server ignores it
    AIMBOT_LLM_KEY     optional bearer token
    AIMBOT_LLM_EFFORT  how hard to think WHERE A CALLER ASKS: low, medium,
                       high, xhigh, or `off` to gate it out everywhere

`.env` is gitignored and `.env.example` is the copy that is committed, so an
endpoint and a key can be kept without either landing in version control. A
value already in the environment WINS over the file, which is the order that
lets one run be pointed somewhere else without editing anything:

    AIMBOT_LLM_MODEL=gpt-oss-120b:Q8_0 make llm

Parsed here rather than with python-dotenv: three variables do not justify a
dependency in a repo whose collectors are otherwise stdlib, curl and pyyaml.

That covers llama-server on the box that already runs the roster, anything
speaking the same protocol behind a proxy, and a hosted api -- without this repo
having an opinion about which. `configured()` is false when nothing is listening,
and every caller is expected to skip rather than fail: a sweep on a machine with
no model must still collect, derive, build and check.

Requests go out with urllib rather than through ./httpcache, because httpcache
is a GET/etag cache and these are POSTs whose response is not addressable by
url. Reproducibility is handled where it belongs instead -- the caller commits
what came back, keyed by a hash of the prompt, and re-asks only on --refresh.
"""

import hashlib
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_URL = "http://localhost:8080/v1"
TIMEOUT = 180
ENV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
# what a caller that ASKS for thinking gets, unless AIMBOT_LLM_EFFORT says
# otherwise. the vendor's own default for this family is xhigh and that is not
# what this repository wants: the registry records that level at 15k-52k
# thinking tokens per call, which over 211 registry notes is a sweep nobody
# waits for, and the first xhigh run here reasoned past 4000 and returned
# nothing at all. medium buys the composition this needs at a fraction of it.
DEFAULT_EFFORT = "medium"
# and the value that gates thinking out again without editing a caller
NO_EFFORT = "off"
# what a reasoning run spends BEFORE the answer starts, per level. the registry
# records qwen3.8 27b's xhigh at 15k-52k thinking tokens in reported traces
# against qwen3.6's 3k, so a budget sized for the answer alone returns an EMPTY
# string rather than a short one: `finish_reason: length` with nothing in
# `content`. the caller says how much ANSWER it wants and this adds the rest,
# because the caller knows the one and the effort decides the other.
REASONING_TOKENS = {"low": 4000, "medium": 16000, "high": 48000, "xhigh": 65536}


def load_env(path=None):
    """Read `.env` into the process, without overriding what is already set.

    `path` resolves against ENV_FILE at CALL time rather than as a default
    argument, which python would bind once at import and never look at again --
    the module constant would then be decorative and untestable.

    `KEY=value`, one per line, `#` comments, optional `export ` prefix and
    optional quotes around the value -- the subset every other tool agrees on.
    A line this cannot parse is skipped rather than guessed at, and a missing
    file is the normal case.

    Not overriding is the important half. It is what makes a one-off override
    work without editing the file, and it is what stops a stale `.env` from
    silently winning over an endpoint somebody exported on purpose.
    """
    try:
        lines = open(path or ENV_FILE).read().split("\n")
    except IOError:
        return {}
    seen = {}
    for line in lines:
        text = line.strip()
        if not text or text.startswith("#"):
            continue
        if text.startswith("export "):
            text = text[len("export "):].lstrip()
        key, sep, value = text.partition("=")
        key = key.strip()
        if not sep or not key:
            continue
        value = value.strip()
        if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        seen[key] = value
        os.environ.setdefault(key, value)
    return seen


def configured():
    """(base, model, key) if an endpoint is set up, else None."""
    load_env()
    base = (os.environ.get("AIMBOT_LLM_URL") or "").strip() or DEFAULT_URL
    model = (os.environ.get("AIMBOT_LLM_MODEL") or "").strip()
    if not model:
        return None
    return base.rstrip("/"), model, (os.environ.get("AIMBOT_LLM_KEY") or "").strip()


def effort():
    """How hard to think where a caller asks for it."""
    load_env()
    return (os.environ.get("AIMBOT_LLM_EFFORT") or "").strip() or DEFAULT_EFFORT


def thinking_body(body, wants):
    """`body` with the thinking knobs a chat template reads.

    Two separate things, because the roster's own registry records them
    separately: a GATE (`enable_thinking`) and a graded KNOB
    (`reasoning_effort`). A template that has one and not the other ignores the
    field rather than failing the request, which is why both are always sent
    together rather than sniffed per model.

    A caller that did not ask is gated off whatever the setting says. That is
    the whole reason this is per-caller: turning thinking on globally is what
    broke triage, where a reasoning run invented a base model and eight calls
    came back empty having reasoned past the budget.
    """
    want = effort()
    if not wants or want == NO_EFFORT:
        body["chat_template_kwargs"] = {"enable_thinking": False}
        return body
    body["chat_template_kwargs"] = {"enable_thinking": True,
                                    "reasoning_effort": want}
    # the openai field for the same idea, for an endpoint that reads that one
    body["reasoning_effort"] = want
    return body


def budget_for(answer_tokens, wants):
    """`max_tokens` that leaves room to think and still answer."""
    want = effort()
    if not wants or want == NO_EFFORT:
        return answer_tokens
    return answer_tokens + REASONING_TOKENS.get(want, REASONING_TOKENS[DEFAULT_EFFORT])


def prompt_key(*parts):
    """A stable id for a prompt, so a captured answer can be found again."""
    h = hashlib.sha256("\x00".join(str(p) for p in parts).encode())
    return h.hexdigest()[:16]


def chat(messages, temperature=0.0, max_tokens=1200, schema=None, thinking=False):
    """One completion, or None if the endpoint is absent or refused.

    Returns None rather than raising for every transport failure, because a
    model that is not running is the normal case on a machine that is not the
    one serving the roster, and it must not take a sweep down.

    Thinking is OFF unless the CALLER asks, and that is not a cost decision.
    A model reasoning into `reasoning_content` leaves `content` empty until it
    is done, so a budget that would be generous for the answer truncates
    mid-thought and the reply arrives as an empty string -- the first eight
    triage calls here failed exactly that way, `finish_reason: length` with
    nothing in `content`. The answers also got no better for it: asked to name a
    base model, the thinking run invented `Large Language Model (LLM) / AI Model
    Repository` where the non-thinking one gave the repo id.

    That finding is about EXTRACTION, where there is one right answer and
    reasoning only finds ways to miss it. Composing prose from a fact sheet is
    the other shape, so the prose callers pass `thinking=True` and raise their
    budget to match; `AIMBOT_LLM_EFFORT` says how hard, and `off` settles it for
    a machine that does not want it at all.
    """
    cfg = configured()
    if not cfg:
        return None
    base, model, key = cfg
    body = thinking_body({"model": model, "messages": messages,
                          "temperature": temperature,
                          "max_tokens": budget_for(max_tokens, thinking)},
                         thinking)
    if schema:
        # llama-server and the openai api both take this; a server that does not
        # understand it still returns prose, which the caller has to parse anyway
        body["response_format"] = {"type": "json_schema",
                                   "json_schema": {"name": "proposal",
                                                   "schema": schema,
                                                   "strict": True}}
    req = urllib.request.Request(
        base + "/chat/completions", method="POST",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json",
                 **({"Authorization": "Bearer " + key} if key else {})})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            got = json.loads(r.read().decode())
    except (urllib.error.URLError, OSError, ValueError, TimeoutError) as e:
        print("  llm: %s" % str(e)[:120], file=sys.stderr)
        return None
    try:
        choice = got["choices"][0]
    except (KeyError, IndexError, TypeError):
        return None
    content = (choice.get("message") or {}).get("content") or ""
    if not content.strip():
        # an empty content with a reason attached is the truncation above, and
        # it is worth naming: silently returning None reads as "the endpoint is
        # down" when the endpoint answered and the budget was wrong
        print("  llm: empty reply (finish_reason=%s)%s"
              % (choice.get("finish_reason"),
                 "; the model reasoned past max_tokens"
                 if (choice.get("message") or {}).get("reasoning_content") else ""),
              file=sys.stderr)
        return None
    return content


def as_json(text):
    """The first JSON object in a reply, or None.

    A local model asked for json still sometimes wraps it in a fence or writes a
    sentence first, and rejecting that outright throws away a good answer over
    punctuation. Anything past the outermost braces is ignored rather than
    repaired -- a reply this cannot read is a miss, not something to guess at.
    """
    if not text:
        return None
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        return json.loads(text[start:end + 1])
    except ValueError:
        return None
