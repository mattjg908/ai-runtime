import pytest
from pydantic import ValidationError

from gateway.models import (
    GenerateRequest,
    GenerateResponse,
    ProviderError,
    Usage,
)


def test_usage_accepts_valid_token_counts() -> None:
    usage = Usage(
        input_tokens=123,
        output_tokens=45,
    )

    assert usage.input_tokens == 123
    assert usage.output_tokens == 45


def test_usage_rejects_non_integer_input_tokens() -> None:
    with pytest.raises(ValidationError):
        Usage.model_validate(
            {
                "input_tokens": "abc",
                "output_tokens": 45,
            }
        )


def test_generate_request_accepts_a_prompt() -> None:
    request = GenerateRequest(prompt="Explain an OTP supervision tree.")

    assert request.prompt == "Explain an OTP supervision tree."


def test_generate_request_rejects_a_missing_prompt() -> None:
    with pytest.raises(ValidationError):
        GenerateRequest.model_validate({})


def test_generate_response_contains_text_and_usage() -> None:
    response = GenerateResponse(
        text="A supervision tree organizes processes by ownership and failure.",
        usage=Usage(
            input_tokens=10,
            output_tokens=15,
        ),
    )

    assert response.text.startswith("A supervision tree")
    assert response.usage.input_tokens == 10
    assert response.usage.output_tokens == 15


def test_generate_response_builds_nested_usage_from_a_dictionary() -> None:
    response = GenerateResponse.model_validate(
        {
            "text": "Generated response",
            "usage": {
                "input_tokens": 5,
                "output_tokens": 8,
            },
        }
    )

    assert isinstance(response.usage, Usage)
    assert response.usage.input_tokens == 5
    assert response.usage.output_tokens == 8


def test_generate_response_rejects_invalid_nested_usage() -> None:
    with pytest.raises(ValidationError):
        GenerateResponse.model_validate(
            {
                "text": "Generated response",
                "usage": {
                    "input_tokens": "invalid",
                    "output_tokens": 8,
                },
            }
        )


def test_provider_error_accepts_a_message() -> None:
    error = ProviderError(message="Provider timed out.")

    assert error.message == "Provider timed out."


def test_provider_error_rejects_a_missing_message() -> None:
    with pytest.raises(ValidationError):
        ProviderError.model_validate({})
