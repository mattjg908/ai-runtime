from gateway.fake_provider import FakeProvider
from gateway.runtime import generate
from gateway.uppercase_provider import UppercaseProvider


def test_generate_with_fake_provider() -> None:
    response = generate(FakeProvider(), "hello")

    assert response.text == "Echo: hello"
    assert response.usage.input_tokens == 0
    assert response.usage.output_tokens == 0


def test_generate_with_uppercase_provider() -> None:
    response = generate(UppercaseProvider(), "hello")

    assert response.text == "HELLO"
    assert response.usage.input_tokens == 0
    assert response.usage.output_tokens == 0
