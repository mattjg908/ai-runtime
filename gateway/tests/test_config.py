import pytest
from pydantic import ValidationError

from gateway.config import GatewayConfig


def test_gateway_config_accepts_fake_provider() -> None:
    config = GatewayConfig(provider="fake")

    assert config.provider == "fake"


def test_gateway_config_accepts_uppercase_provider() -> None:
    config = GatewayConfig(provider="uppercase")

    assert config.provider == "uppercase"


def test_gateway_config_rejects_unknown_provider() -> None:
    with pytest.raises(ValidationError):
        GatewayConfig.model_validate(
            {
                "provider": "openai",
            }
        )
