import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DeepSeekConfig:
    api_key: str
    model: str = "deepseek-v4-pro"
    base_url: str = "https://api.deepseek.com"


def load_env_file(path):
    path = Path(path)
    if not path.exists():
        return {}

    values = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = _clean_env_value(value.strip())
    return values


def load_deepseek_config(env_path=".env"):
    file_values = load_env_file(env_path)
    api_key = os.environ.get("DEEPSEEK_API_KEY") or file_values.get("DEEPSEEK_API_KEY")
    if not api_key:
        return None

    return DeepSeekConfig(
        api_key=api_key,
        model=os.environ.get("DEEPSEEK_MODEL") or file_values.get("DEEPSEEK_MODEL", "deepseek-v4-pro"),
        base_url=os.environ.get("DEEPSEEK_BASE_URL") or file_values.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
    )


def _clean_env_value(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value
