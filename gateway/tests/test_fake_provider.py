import time

import pytest

from gateway.fake_provider import FakeProvider
from gateway.models import GenerateRequest


def test_fake_provider_returns_an_echo_response() -> None:
    provider = FakeProvider()
    request = GenerateRequest(prompt="Hello")

    response = provider.generate(request)

    assert response.text == "Echo: Hello"
    assert response.usage.input_tokens == 1
    assert response.usage.output_tokens == 2


def test_fake_provider_can_simulate_failure() -> None:
    provider = FakeProvider(should_fail=True)
    request = GenerateRequest(prompt="Hello")

    with pytest.raises(RuntimeError, match="Fake provider failure"):
        provider.generate(request)


def test_fake_provider_can_simulate_latency() -> None:
    provider = FakeProvider(latency_seconds=0.05)
    request = GenerateRequest(prompt="Hello")

    start = time.monotonic()
    response = provider.generate(request)
    elapsed = time.monotonic() - start

    assert response.text == "Echo: Hello"
    assert elapsed >= 0.05
