from openai import AsyncOpenAI

from gateway.config import GatewayConfig
from gateway.fake_provider import FakeProvider
from gateway.openai_provider import OpenAIProvider
from gateway.provider import ModelProvider
from gateway.uppercase_provider import UppercaseProvider


def create_provider(
    config: GatewayConfig,
    openai_client: AsyncOpenAI | None = None,
) -> ModelProvider:
    if config.provider == "fake":
        return FakeProvider()

    if config.provider == "uppercase":
        return UppercaseProvider()

    if openai_client is None:
        raise ValueError("openai_client is required for the OpenAI provider")

    return OpenAIProvider(
        client=openai_client,
        model=config.model,
    )
