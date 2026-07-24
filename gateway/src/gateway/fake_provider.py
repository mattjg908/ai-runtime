import asyncio

from .models import (
    GenerateRequest,
    GenerateResponse,
    ProviderError,
    Usage,
)


class FakeProvider:
    def __init__(
        self,
        should_fail: bool = False,
        failures_before_success: int = 0,
        latency_seconds: float = 0.0,
        retryable_failure: bool = True,
    ) -> None:
        self._should_fail = should_fail
        self._failures_before_success = failures_before_success
        self._latency_seconds = latency_seconds
        self._retryable_failure = retryable_failure
        self._attempt_count = 0

    @property
    def attempt_count(self) -> int:
        return self._attempt_count

    async def generate(
        self,
        request: GenerateRequest,
    ) -> GenerateResponse:
        self._attempt_count += 1

        if self._latency_seconds > 0:
            await asyncio.sleep(self._latency_seconds)

        if self._should_fail:
            raise ProviderError(
                message="Fake provider failure",
                retryable=self._retryable_failure,
            )

        if self._attempt_count <= self._failures_before_success:
            raise ProviderError(
                message="Fake provider transient failure",
                retryable=True,
            )

        response_text = f"Echo: {request.prompt}"

        return GenerateResponse(
            text=response_text,
            usage=Usage(
                input_tokens=len(request.prompt.split()),
                output_tokens=len(response_text.split()),
            ),
        )
