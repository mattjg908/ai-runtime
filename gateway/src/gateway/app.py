from openai import OpenAI

from gateway.config import GatewayConfig
from gateway.models import GenerateResponse
from gateway.provider_factory import create_provider
from gateway.runtime import generate as runtime_generate


async def generate(
    prompt: str,
    config: GatewayConfig | None = None,
) -> GenerateResponse:
    resolved_config = config if config is not None else GatewayConfig()

    if resolved_config.provider == "openai":
        provider = create_provider(
            resolved_config,
            openai_client=OpenAI(),
        )
    else:
        provider = create_provider(resolved_config)

    return await runtime_generate(
        provider=provider,
        prompt=prompt,
    )
