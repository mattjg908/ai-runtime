import pytest

from gateway.models import GenerateRequest
from gateway.uppercase_provider import UppercaseProvider


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_uppercase_provider_returns_uppercase_text() -> None:
    provider = UppercaseProvider()
    request = GenerateRequest(prompt="hello")

    response = await provider.generate(request)

    assert response.text == "HELLO"
    assert response.usage.input_tokens == 0
    assert response.usage.output_tokens == 0
