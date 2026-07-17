from gateway.fake_provider import FakeProvider
from gateway.models import GenerateRequest
from gateway.provider import ModelProvider


def test_fake_provider_returns_an_echo_response() -> None:
    provider: ModelProvider = FakeProvider()

    response = provider.generate(
        GenerateRequest(prompt="Hello"),
    )

    assert response.text == "Echo: Hello"
    assert response.usage.input_tokens == 0
    assert response.usage.output_tokens == 0
