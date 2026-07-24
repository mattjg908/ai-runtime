import pytest

from gateway.fake_provider import FakeProvider
from gateway.models import GenerateRequest, ProviderError


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_fake_provider_returns_an_echo_response() -> None:
    provider = FakeProvider()
    request = GenerateRequest(prompt="Hello")

    response = await provider.generate(request)

    assert response.text == "Echo: Hello"
    assert response.usage.input_tokens == 1
    assert response.usage.output_tokens == 2


@pytest.mark.anyio
async def test_fake_provider_can_simulate_failure() -> None:
    provider = FakeProvider(
        should_fail=True,
        retryable_failure=True,
    )
    request = GenerateRequest(prompt="Hello")

    with pytest.raises(
        ProviderError,
        match="Fake provider failure",
    ) as error_info:
        await provider.generate(request)

    assert error_info.value.retryable is True


@pytest.mark.anyio
async def test_fake_provider_can_simulate_non_retryable_failure() -> None:
    provider = FakeProvider(
        should_fail=True,
        retryable_failure=False,
    )
    request = GenerateRequest(prompt="Hello")

    with pytest.raises(
        ProviderError,
        match="Fake provider failure",
    ) as error_info:
        await provider.generate(request)

    assert error_info.value.retryable is False


@pytest.mark.anyio
async def test_fake_provider_can_simulate_latency() -> None:
    provider = FakeProvider(latency_seconds=0.05)
    request = GenerateRequest(prompt="Hello")

    response = await provider.generate(request)

    assert response.text == "Echo: Hello"
