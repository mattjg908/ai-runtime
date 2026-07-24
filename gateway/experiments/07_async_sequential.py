import asyncio
import time


async def model_call(name: str, delay: float) -> str:
    print(f"{name}: started")

    await asyncio.sleep(delay)

    print(f"{name}: finished")

    return f"{name}: response"


async def main() -> None:
    start = time.monotonic()

    first = await model_call("first", 2.0)
    second = await model_call("second", 2.0)
    third = await model_call("third", 2.0)

    elapsed = time.monotonic() - start

    print(first)
    print(second)
    print(third)
    print(f"elapsed: {elapsed:.2f} seconds")


asyncio.run(main())
