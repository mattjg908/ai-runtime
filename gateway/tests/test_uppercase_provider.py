from gateway.models import GenerateRequest
from gateway.provider import ModelProvider
from gateway.uppercase_provider import UppercaseProvider


def test_uppercase_provider_returns_uppercase_text() -> None:
    provider: ModelProvider = UppercaseProvider()

    response = provider.generate(
        GenerateRequest(prompt="hello world"),
    )

    assert response.text == "HELLO WORLD"
    assert response.usage.input_tokens == 0
    assert response.usage.output_tokens == 0
