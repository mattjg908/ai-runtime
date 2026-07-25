from typing import cast
from unittest.mock import MagicMock

import pytest
from openai import AsyncOpenAI

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
    client = cast(AsyncOpenAI, MagicMock())

    provider = create_provider(
        config,
        openai_client=client,
    )

    assert isinstance(provider, OpenAIProvider)


def test_create_provider_requires_openai_client() -> None:
    config = GatewayConfig(
        provider="openai",
        model="test-model",
    )

    with pytest.raises(
        ValueError,
        match="openai_client is required",
    ):
        create_provider(config)
