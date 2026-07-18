from gateway.config import GatewayConfig
from gateway.fake_provider import FakeProvider
from gateway.provider import ModelProvider
from gateway.uppercase_provider import UppercaseProvider


def create_provider(config: GatewayConfig) -> ModelProvider:
    if config.provider == "fake":
        return FakeProvider()

    return UppercaseProvider()
