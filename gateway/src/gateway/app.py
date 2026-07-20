from gateway.config import GatewayConfig
from gateway.provider_factory import create_provider
from gateway.runtime import generate


def run(config: GatewayConfig, prompt: str) -> str:
    provider = create_provider(config)
    response = generate(provider, prompt)

    return response.text
