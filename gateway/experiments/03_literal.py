# python experiments/03_literal.py
# mypy experiments/03_literal.py
from typing import Literal

Provider = Literal["openai", "anthropic"]


def connect(provider: Provider) -> None:
    print(f"Connecting to {provider}")


connect("openai")

# Uncomment.
# connect("google")
