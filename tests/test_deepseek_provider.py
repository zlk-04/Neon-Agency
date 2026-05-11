import json

from neon_agency.config import DeepSeekConfig
from neon_agency.providers.deepseek import DeepSeekDialogueProvider


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


class FakeOpener:
    def __init__(self, payload):
        self.payload = payload
        self.requests = []

    def __call__(self, request, timeout):
        self.requests.append((request, timeout))
        return FakeResponse(self.payload)


def test_deepseek_provider_builds_request_and_parses_response():
    opener = FakeOpener({"choices": [{"message": {"content": "Generated line."}}]})
    provider = DeepSeekDialogueProvider(
        DeepSeekConfig(api_key="secret", model="deepseek-v4-pro", base_url="https://api.deepseek.com"),
        opener=opener,
    )

    line = provider.generate("Prompt text")

    request, timeout = opener.requests[0]
    body = json.loads(request.data.decode("utf-8"))
    assert line == "Generated line."
    assert timeout == 8
    assert request.full_url == "https://api.deepseek.com/chat/completions"
    assert request.headers["Authorization"] == "Bearer secret"
    assert body["model"] == "deepseek-v4-pro"
    assert body["messages"][0]["content"] == "Prompt text"
    assert body["temperature"] == 0.7
    assert body["max_tokens"] == 160


def test_deepseek_provider_uses_reasoning_content_when_content_is_blank():
    opener = FakeOpener({"choices": [{"message": {"content": "", "reasoning_content": "Generated from reasoning."}}]})
    provider = DeepSeekDialogueProvider(
        DeepSeekConfig(api_key="secret", model="deepseek-v4-flash", base_url="https://api.deepseek.com"),
        opener=opener,
    )

    line = provider.generate("Prompt text")

    assert line == "Generated from reasoning."
