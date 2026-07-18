from gateway.config import GatewayConfig
from gateway.fake_provider import FakeProvider
from gateway.provider_factory import create_provider
from gateway.uppercase_provider import UppercaseProvider


def test_create_provider_creates_fake_provider() -> None:
    config = GatewayConfig(provider="fake")

    provider = create_provider(config)

    assert isinstance(provider, FakeProvider)


def test_create_provider_creates_uppercase_provider() -> None:
    config = GatewayConfig(provider="uppercase")

    provider = create_provider(config)

    assert isinstance(provider, UppercaseProvider)
