"""Backend do eval que usa a subscrição Claude através do `claude -p` (Claude Code em modo headless).

Imita `client.messages.create` do SDK para que `summarize` e `judge` corram sem alterações.
Serve para validar o prompt e a rubrica sem custos de API: os tokens e a latência são indicativos,
não os do actor em produção (que chama a API diretamente).
"""

import json
import shutil
import subprocess
import tempfile
from types import SimpleNamespace


class ClaudeCodeError(RuntimeError):
    pass


class ClaudeCodeRateLimit(ClaudeCodeError):
    """Limite de utilização da subscrição; o runner repete com backoff."""


class ClaudeCodeClient:
    def __init__(self, timeout):
        self.timeout = timeout
        self.messages = self
        self.exe = shutil.which("claude")
        if not self.exe:
            raise ClaudeCodeError("o comando 'claude' não está no PATH")

    def create(self, model, system, messages, output_config=None, max_tokens=None):
        cfg = output_config or {}
        args = [self.exe, "-p", "--model", model, "--system-prompt", system, "--output-format", "json",
                # isolamento: sem ferramentas, sem MCP, sem settings/plugins/hooks do utilizador, sem CLAUDE.md
                "--tools", "", "--strict-mcp-config", "--setting-sources", "", "--no-session-persistence"]
        if cfg.get("effort"):
            args += ["--effort", cfg["effort"]]
        if cfg.get("format"):
            args += ["--json-schema", json.dumps(cfg["format"]["schema"])]
        with tempfile.TemporaryDirectory() as cwd:  # pasta vazia: nada do projeto entra no contexto
            proc = subprocess.run(args, input=messages[0]["content"], capture_output=True, text=True,
                                  encoding="utf-8", timeout=self.timeout, cwd=cwd)
        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError:
            raise ClaudeCodeError(f"saída inválida do claude -p (exit {proc.returncode}): {proc.stderr[:300]}")
        if data.get("is_error"):
            msg = str(data.get("result"))
            if "limit" in msg.lower() or data.get("api_error_status") in (429, 529):
                raise ClaudeCodeRateLimit(msg)
            raise ClaudeCodeError(msg)

        text = json.dumps(data["structured_output"]) if data.get("structured_output") is not None else data["result"]
        u = data.get("usage") or {}
        served = next(iter(data.get("modelUsage") or {}), model)
        return SimpleNamespace(
            content=[SimpleNamespace(type="text", text=text)],
            model=served,
            stop_reason=data.get("stop_reason") or "end_turn",
            usage=SimpleNamespace(input_tokens=u.get("input_tokens", 0), output_tokens=u.get("output_tokens", 0),
                                  cache_read_input_tokens=u.get("cache_read_input_tokens", 0),
                                  cache_creation_input_tokens=u.get("cache_creation_input_tokens", 0)),
        )
