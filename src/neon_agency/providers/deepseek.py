import json
from urllib import request


class DeepSeekDialogueProvider:
    def __init__(self, config, opener=None, timeout=8, temperature=0.7, max_tokens=80):
        self.config = config
        self.opener = opener or request.urlopen
        self.timeout = timeout
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(self, prompt):
        payload = {
            "model": self.config.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        api_request = request.Request(
            f"{self.config.base_url.rstrip('/')}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with self.opener(api_request, timeout=self.timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"]
