from typing import Literal

from pydantic import BaseModel


class GatewayConfig(BaseModel):
    provider: Literal["fake", "uppercase"]
