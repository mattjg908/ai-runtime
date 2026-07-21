import pytest
from openai import OpenAI

from gateway.config import GatewayConfig
from gateway.fake_provider import FakeProvider
from gateway.openai_provider import OpenAIProvider
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


def test_create_provider_creates_openai_provider() -> None:
    config = GatewayConfig(
        provider="openai",
        model="test-model",
    )
    client = OpenAI(api_key="test-api-key")

    provider = create_provider(
        config,
        openai_client=client,
    )

    assert isinstance(provider, OpenAIProvider)


def test_create_provider_requires_client_for_openai() -> None:
    config = GatewayConfig(provider="openai")

    with pytest.raises(
        ValueError,
        match="An OpenAI client is required",
    ):
        create_provider(config)
