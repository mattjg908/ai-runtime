from gateway.app import run
from gateway.config import GatewayConfig


def test_run_with_fake_provider() -> None:
    config = GatewayConfig(provider="fake")

    result = run(config, "hello")

    assert result == "Echo: hello"


def test_run_with_uppercase_provider() -> None:
    config = GatewayConfig(provider="uppercase")

    result = run(config, "hello")

    assert result == "HELLO"
