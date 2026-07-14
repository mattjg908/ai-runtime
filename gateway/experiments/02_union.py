# python experiments/02_union.py
# mypy experiments/02_union.py
def stringify(value: int | str) -> str:
    return str(value)


print(stringify(42))
print(stringify("hello"))

# Uncomment.
# print(stringify([1, 2, 3]))
