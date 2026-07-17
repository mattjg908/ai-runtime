from gateway.models import GenerateRequest
from gateway.provider import ModelProvider


def generate_text(
    provider: ModelProvider,
    prompt: str,
) -> str:
    request = GenerateRequest(
        prompt=prompt,
    )

    response = provider.generate(request)

    return response.text
