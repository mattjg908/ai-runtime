import time

from .models import (
    GenerateRequest,
    GenerateResponse,
    Usage,
)


class FakeProvider:
    def __init__(
        self,
        should_fail: bool = False,
        latency_seconds: float = 0.0,
    ) -> None:
        self._should_fail = should_fail
        self._latency_seconds = latency_seconds

    def generate(
        self,
        request: GenerateRequest,
    ) -> GenerateResponse:
        if self._latency_seconds > 0:
            time.sleep(self._latency_seconds)

        if self._should_fail:
            raise RuntimeError("Fake provider failure")

        response_text = f"Echo: {request.prompt}"

        return GenerateResponse(
            text=response_text,
            usage=Usage(
                input_tokens=len(request.prompt.split()),
                output_tokens=len(response_text.split()),
            ),
        )
