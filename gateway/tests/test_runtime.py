from gateway.fake_provider import FakeProvider
from gateway.runtime import generate_text
from gateway.uppercase_provider import UppercaseProvider


def test_runtime_works_with_fake_provider() -> None:
    text = generate_text(
        FakeProvider(),
        "hello",
    )

    assert text == "Echo: hello"


def test_runtime_works_with_uppercase_provider() -> None:
    text = generate_text(
        UppercaseProvider(),
        "hello",
    )

    assert text == "HELLO"
