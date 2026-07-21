from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class GatewayConfig(BaseSettings):
    provider: Literal["fake", "uppercase", "openai"] = "fake"
    model: str = "gpt-5-mini"

    model_config = SettingsConfigDict(
        env_prefix="GATEWAY_",
    )
