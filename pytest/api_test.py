import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("GOOGLE_API_KEY", "dummy-api-key")

from api.api import api  # noqa: E402


class FakeTemplates:
    def __init__(self):
        self.calls = []

    def TemplateResponse(self, *args):
        self.calls.append(args)
        return args


class FakeModels:
    def __init__(self, response=None, exception=None):
        self.response = response or SimpleNamespace(text="generated text")
        self.exception = exception
        self.calls = []

    def generate_content(self, **kwargs):
        self.calls.append(kwargs)
        if self.exception:
            raise self.exception
        return self.response


def test_return_template_renders_index_with_default_context(monkeypatch):
    fake_templates = FakeTemplates()
    monkeypatch.setattr(api, "templates", fake_templates)

    request = SimpleNamespace()
    response = api.returnTemplate(request)

    assert response == fake_templates.calls[0]
    assert fake_templates.calls[0][0] is request
    assert fake_templates.calls[0][1] == "index.html"
    assert fake_templates.calls[0][2] == {
        "prompt": "",
        "result": None,
        "model": api.modelName,
    }


def test_return_text_generates_content_and_renders_result(monkeypatch):
    fake_templates = FakeTemplates()
    fake_models = FakeModels(response=SimpleNamespace(text="converted text"))
    monkeypatch.setattr(api, "templates", fake_templates)
    monkeypatch.setattr(api, "client", SimpleNamespace(models=fake_models))

    request = SimpleNamespace()
    response = api.return_text(request, "input prompt")

    assert response == fake_templates.calls[0]
    assert fake_models.calls[0]["model"] == api.modelName
    assert fake_models.calls[0]["contents"] == "input prompt"
    assert fake_models.calls[0]["config"].system_instruction == api.systemInstruction
    assert fake_templates.calls[0][0] is request
    assert fake_templates.calls[0][1] == "index.html"
    assert fake_templates.calls[0][2] == {
        "prompt": "input prompt",
        "result": "converted text",
        "model": api.modelName,
    }


def test_return_text_raises_http_exception_when_gemini_fails(monkeypatch):
    fake_models = FakeModels(exception=RuntimeError("api failed"))
    monkeypatch.setattr(api, "client", SimpleNamespace(models=fake_models))

    with pytest.raises(HTTPException) as exc_info:
        api.return_text(SimpleNamespace(), "input prompt")

    assert exc_info.value.status_code == 500
    assert "Gemini API error: api failed" in exc_info.value.detail
