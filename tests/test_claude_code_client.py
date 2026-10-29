import json
import subprocess

import pytest

from evals.contract_summary import claude_code_client as ccc


def fake_run(payload):
    def run(args, **kw):
        fake_run.args = args
        return subprocess.CompletedProcess(args, 0, stdout=json.dumps(payload), stderr="")
    return run


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(ccc.shutil, "which", lambda name: "claude")
    return ccc.ClaudeCodeClient(timeout=10)


def call(client, **cfg):
    return client.messages.create(model="claude-haiku-5-5", system="s", max_tokens=100,
                                  messages=[{"role": "user", "content": "u"}], **cfg)


def test_success_maps_to_sdk_shape(client, monkeypatch):
    monkeypatch.setattr(ccc.subprocess, "run", fake_run({
        "is_error": False, "result": "Resumo.", "stop_reason": "end_turn",
        "usage": {"input_tokens": 900, "output_tokens": 60, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0},
        "modelUsage": {"claude-haiku-5-5": {}}}))
    r = call(client, output_config={"effort": "low"})
    assert r.content[0].text == "Resumo." and r.model == "claude-haiku-5-5" and r.usage.output_tokens == 60
    assert fake_run.args[fake_run.args.index("--tools") + 1] == "" and "--strict-mcp-config" in fake_run.args
    assert fake_run.args[fake_run.args.index("--effort") + 1] == "low"


def test_structured_output_is_returned_as_json_text(client, monkeypatch):
    monkeypatch.setattr(ccc.subprocess, "run", fake_run({
        "is_error": False, "result": "", "structured_output": {"faithful": {"pass": True, "reason": "ok"}},
        "usage": {}, "modelUsage": {"claude-sonnet-5-5": {}}}))
    r = call(client, output_config={"format": {"type": "json_schema", "schema": {"type": "object"}}})
    assert json.loads(r.content[0].text)["faithful"]["pass"] is True
    assert "--json-schema" in fake_run.args


def test_auth_error_is_not_retried(client, monkeypatch):
    monkeypatch.setattr(ccc.subprocess, "run", fake_run(
        {"is_error": True, "result": "Failed to authenticate: OAuth session expired", "api_error_status": None}))
    with pytest.raises(ccc.ClaudeCodeError) as e:
        call(client)
    assert not isinstance(e.value, ccc.ClaudeCodeRateLimit)


def test_usage_limit_is_retriable(client, monkeypatch):
    monkeypatch.setattr(ccc.subprocess, "run", fake_run(
        {"is_error": True, "result": "Claude usage limit reached", "api_error_status": 429}))
    with pytest.raises(ccc.ClaudeCodeRateLimit):
        call(client)
