from typing import Protocol

from .models import GenerateRequest, GenerateResponse


class ModelProvider(Protocol):
    def generate(self, request: GenerateRequest) -> GenerateResponse: ...
