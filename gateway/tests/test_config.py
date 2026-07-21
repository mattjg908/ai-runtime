import pytest
from pydantic import ValidationError

from gateway.config import GatewayConfig


def test_gateway_config_defaults_to_fake_provider() -> None:
    config = GatewayConfig()

    assert config.provider == "fake"


def test_gateway_config_has_default_model() -> None:
    config = GatewayConfig()

    assert config.model == "gpt-5-mini"


def test_gateway_config_accepts_uppercase_provider() -> None:
    config = GatewayConfig(provider="uppercase")

    assert config.provider == "uppercase"


def test_gateway_config_accepts_openai_provider() -> None:
    config = GatewayConfig(provider="openai")

    assert config.provider == "openai"


def test_gateway_config_accepts_custom_model() -> None:
    config = GatewayConfig(
        provider="openai",
        model="test-model",
    )

    assert config.model == "test-model"


def test_gateway_config_loads_environment_variables(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GATEWAY_PROVIDER", "openai")
    monkeypatch.setenv("GATEWAY_MODEL", "environment-model")

    config = GatewayConfig()

    assert config.provider == "openai"
    assert config.model == "environment-model"


def test_gateway_config_rejects_unknown_provider() -> None:
    with pytest.raises(ValidationError):
        GatewayConfig.model_validate(
            {
                "provider": "unknown",
            }
        )
