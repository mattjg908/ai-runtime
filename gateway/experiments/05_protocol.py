# python experiments/05_protocol.py
# mypy experiments/05_protocol.py
from typing import Protocol, runtime_checkable


@runtime_checkable
class Animal(Protocol):
    def speak(self) -> str: ...


class Dog:
    def speak(self) -> str:
        return "Woof!"


class Cat:
    def speak(self) -> str:
        return "Meow!"


def make_noise(animal: Animal) -> None:
    print(animal.speak())


# class Fish:
#    pass

make_noise(Dog())
make_noise(Cat())
# make_noise(Fish())

print(isinstance(Dog(), Animal))
