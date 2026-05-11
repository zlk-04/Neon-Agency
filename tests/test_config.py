from pathlib import Path

from neon_agency.config import load_deepseek_config, load_env_file


def test_load_env_file_reads_simple_key_values(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "DEEPSEEK_API_KEY=from-file",
                "DEEPSEEK_MODEL=deepseek-v4-pro",
                "IGNORED_LINE",
            ]
        ),
        encoding="utf-8",
    )

    values = load_env_file(env_file)

    assert values["DEEPSEEK_API_KEY"] == "from-file"
    assert values["DEEPSEEK_MODEL"] == "deepseek-v4-pro"
    assert "IGNORED_LINE" not in values


def test_deepseek_config_prefers_environment_over_env_file(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("DEEPSEEK_API_KEY=from-file\nDEEPSEEK_MODEL=file-model\n", encoding="utf-8")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "from-env")

    config = load_deepseek_config(env_file)

    assert config.api_key == "from-env"
    assert config.model == "file-model"
    assert config.base_url == "https://api.deepseek.com"


def test_deepseek_config_returns_none_without_key(tmp_path, monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

    config = load_deepseek_config(tmp_path / ".env")

    assert config is None
