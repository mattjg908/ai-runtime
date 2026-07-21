import pytest

from gateway.app import generate
from gateway.config import GatewayConfig


def test_generate_uses_fake_provider() -> None:
    config = GatewayConfig(provider="fake")

    response = generate(
        prompt="Hello",
        config=config,
    )

    assert response.text == "Echo: Hello"


def test_generate_uses_environment_config(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GATEWAY_PROVIDER", "uppercase")

    response = generate(prompt="Hello world")

    assert response.text == "HELLO WORLD"
