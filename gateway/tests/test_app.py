import pytest

from gateway.app import generate
from gateway.config import GatewayConfig


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_generate_with_fake_provider() -> None:
    config = GatewayConfig(provider="fake")

    response = await generate(
        prompt="hello",
        config=config,
    )

    assert response.text == "Echo: hello"


@pytest.mark.anyio
async def test_generate_with_uppercase_provider() -> None:
    config = GatewayConfig(provider="uppercase")

    response = await generate(
        prompt="hello",
        config=config,
    )

    assert response.text == "HELLO"
