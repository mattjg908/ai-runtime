import asyncio
import random

from .models import GenerateRequest, GenerateResponse, ProviderError
from .provider import ModelProvider


class ReliableProvider:
    def __init__(
        self,
        provider: ModelProvider,
        timeout_seconds: float,
        max_attempts: int = 1,
        backoff_seconds: float = 0.0,
        jitter_seconds: float = 0.0,
    ) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")

        if backoff_seconds < 0:
            raise ValueError("backoff_seconds cannot be negative")

        if jitter_seconds < 0:
            raise ValueError("jitter_seconds cannot be negative")

        self._provider = provider
        self._timeout_seconds = timeout_seconds
        self._max_attempts = max_attempts
        self._backoff_seconds = backoff_seconds
        self._jitter_seconds = jitter_seconds

    async def generate(
        self,
        request: GenerateRequest,
    ) -> GenerateResponse:
        for attempt in range(1, self._max_attempts + 1):
            try:
                return await asyncio.wait_for(
                    self._provider.generate(request),
                    timeout=self._timeout_seconds,
                )

            except TimeoutError:
                if attempt == self._max_attempts:
                    raise

            except ProviderError as error:
                if not error.retryable:
                    raise

                if attempt == self._max_attempts:
                    raise

            backoff = self._backoff_seconds * (2 ** (attempt - 1))
            jitter = random.uniform(0.0, self._jitter_seconds)

            await asyncio.sleep(backoff + jitter)

        raise RuntimeError("unreachable")
