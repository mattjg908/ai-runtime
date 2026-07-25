from typing import cast
from unittest.mock import AsyncMock, MagicMock

import pytest
from openai import AsyncOpenAI

from gateway.models import GenerateRequest
from gateway.openai_provider import OpenAIProvider


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_generate_returns_gateway_response() -> None:
    client = MagicMock()
    api_response = MagicMock()

    api_response.output_text = "Hello from OpenAI"
    api_response.usage.input_tokens = 4
    api_response.usage.output_tokens = 3

    client.responses.create = AsyncMock(
        return_value=api_response,
    )

    provider = OpenAIProvider(
        client=cast(AsyncOpenAI, client),
        model="test-model",
    )

    response = await provider.generate(GenerateRequest(prompt="Say hello"))

    assert response.text == "Hello from OpenAI"
    assert response.usage.input_tokens == 4
    assert response.usage.output_tokens == 3

    client.responses.create.assert_awaited_once_with(
        model="test-model",
        input="Say hello",
    )


@pytest.mark.anyio
async def test_generate_raises_when_usage_is_missing() -> None:
    client = MagicMock()
    api_response = MagicMock()

    api_response.output_text = "Hello"
    api_response.usage = None

    client.responses.create = AsyncMock(
        return_value=api_response,
    )

    provider = OpenAIProvider(
        client=cast(AsyncOpenAI, client),
        model="test-model",
    )

    with pytest.raises(
        RuntimeError,
        match="OpenAI response did not contain usage data",
    ):
        await provider.generate(GenerateRequest(prompt="Say hello"))
