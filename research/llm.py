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


def prompt_key(*parts):
    """A stable id for a prompt, so a captured answer can be found again."""
    h = hashlib.sha256("\x00".join(str(p) for p in parts).encode())
    return h.hexdigest()[:16]


def chat(messages, temperature=0.0, max_tokens=1200, schema=None, thinking=False):
    """One completion, or None if the endpoint is absent or refused.

    Returns None rather than raising for every transport failure, because a
    model that is not running is the normal case on a machine that is not the
    one serving the roster, and it must not take a sweep down.

    Thinking is turned OFF by default and that is not a cost decision. A model
    reasoning into `reasoning_content` leaves `content` empty until it is done,
    so a budget that would be generous for the answer truncates mid-thought and
    the reply arrives as an empty string -- the first eight triage calls here
    failed exactly that way, `finish_reason: length` with nothing in `content`.
    The answers also got no better for it: asked to name a base model, the
    thinking run invented `Large Language Model (LLM) / AI Model Repository`
    where the non-thinking one gave the repo id.
    """
    cfg = configured()
    if not cfg:
        return None
    base, model, key = cfg
    body = {"model": model, "messages": messages, "temperature": temperature,
            "max_tokens": max_tokens}
    if not thinking:
        # llama-server passes these into the chat template; a server that does
        # not take them ignores the field rather than failing the request
        body["chat_template_kwargs"] = {"enable_thinking": False}
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
