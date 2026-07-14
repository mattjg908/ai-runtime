# python experiments/04_typed_dict.py
# mypy experiments/04_typed_dict.py
from typing import TypedDict


class Usage(TypedDict):
    input_tokens: int
    output_tokens: int


usage: Usage = {
    "input_tokens": 123,
    "output_tokens": 45,
}

print(usage)
print(type(usage))

# Uncomment this.
#
# broken_usage: Usage = {
#     "input_token": 123,
#     "output_tokens": 45,
# }
