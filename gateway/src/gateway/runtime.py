from gateway.models import GenerateRequest, GenerateResponse
from gateway.provider import ModelProvider


def generate(
    provider: ModelProvider,
    prompt: str,
) -> GenerateResponse:
    request = GenerateRequest(
        prompt=prompt,
    )

    return provider.generate(request)
