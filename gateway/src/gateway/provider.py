from typing import Protocol

from .models import GenerateRequest, GenerateResponse


class ModelProvider(Protocol):
    async def generate(
        self,
        request: GenerateRequest,
    ) -> GenerateResponse: ...
