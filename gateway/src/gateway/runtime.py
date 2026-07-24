from .models import GenerateRequest, GenerateResponse
from .provider import ModelProvider


async def generate(
    provider: ModelProvider,
    prompt: str,
) -> GenerateResponse:
    request = GenerateRequest(
        prompt=prompt,
    )

    return await provider.generate(request)
