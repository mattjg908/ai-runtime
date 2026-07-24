import pytest

from gateway.fake_provider import FakeProvider
from gateway.models import GenerateRequest, ProviderError
from gateway.reliable_provider import ReliableProvider


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_reliable_provider_returns_response_before_timeout() -> None:
    provider = ReliableProvider(
        provider=FakeProvider(latency_seconds=0.01),
        timeout_seconds=0.1,
    )
    request = GenerateRequest(prompt="hello")

    response = await provider.generate(request)

    assert response.text == "Echo: hello"


@pytest.mark.anyio
async def test_reliable_provider_times_out_slow_provider() -> None:
    provider = ReliableProvider(
        provider=FakeProvider(latency_seconds=0.2),
        timeout_seconds=0.05,
    )
    request = GenerateRequest(prompt="hello")

    with pytest.raises(TimeoutError):
        await provider.generate(request)


@pytest.mark.anyio
async def test_reliable_provider_retries_transient_failure() -> None:
    fake_provider = FakeProvider(
        failures_before_success=2,
    )
    provider = ReliableProvider(
        provider=fake_provider,
        timeout_seconds=0.1,
        max_attempts=3,
        backoff_seconds=0.0,
    )
    request = GenerateRequest(prompt="hello")

    response = await provider.generate(request)

    assert response.text == "Echo: hello"
    assert fake_provider.attempt_count == 3


@pytest.mark.anyio
async def test_reliable_provider_raises_after_attempts_exhausted() -> None:
    fake_provider = FakeProvider(
        should_fail=True,
        retryable_failure=True,
    )
    provider = ReliableProvider(
        provider=fake_provider,
        timeout_seconds=0.1,
        max_attempts=3,
        backoff_seconds=0.0,
    )
    request = GenerateRequest(prompt="hello")

    with pytest.raises(
        ProviderError,
        match="Fake provider failure",
    ):
        await provider.generate(request)

    assert fake_provider.attempt_count == 3


@pytest.mark.anyio
async def test_reliable_provider_does_not_retry_non_retryable_failure() -> None:
    fake_provider = FakeProvider(
        should_fail=True,
        retryable_failure=False,
    )
    provider = ReliableProvider(
        provider=fake_provider,
        timeout_seconds=0.1,
        max_attempts=3,
        backoff_seconds=0.0,
    )
    request = GenerateRequest(prompt="hello")

    with pytest.raises(
        ProviderError,
        match="Fake provider failure",
    ) as error_info:
        await provider.generate(request)

    assert error_info.value.retryable is False
    assert fake_provider.attempt_count == 1


@pytest.mark.anyio
async def test_reliable_provider_uses_exponential_backoff_and_jitter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleep_delays: list[float] = []

    async def fake_sleep(delay: float) -> None:
        sleep_delays.append(delay)

    def fake_uniform(start: float, end: float) -> float:
        assert start == 0.0
        assert end == 0.1
        return 0.1

    monkeypatch.setattr(
        "gateway.reliable_provider.asyncio.sleep",
        fake_sleep,
    )
    monkeypatch.setattr(
        "gateway.reliable_provider.random.uniform",
        fake_uniform,
    )

    fake_provider = FakeProvider(
        failures_before_success=2,
    )
    provider = ReliableProvider(
        provider=fake_provider,
        timeout_seconds=0.1,
        max_attempts=3,
        backoff_seconds=0.5,
        jitter_seconds=0.1,
    )
    request = GenerateRequest(prompt="hello")

    response = await provider.generate(request)

    assert response.text == "Echo: hello"
    assert fake_provider.attempt_count == 3
    assert sleep_delays == [0.6, 1.1]
