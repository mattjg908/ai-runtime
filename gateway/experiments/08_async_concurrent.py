import asyncio
import time


async def model_call(name: str, delay: float) -> str:
    print(f"{name}: started")

    await asyncio.sleep(delay)

    print(f"{name}: finished")

    return f"{name}: response"


async def main() -> None:
    start = time.monotonic()

    first_task = asyncio.create_task(model_call("first", 2.0))
    second_task = asyncio.create_task(model_call("second", 2.0))
    third_task = asyncio.create_task(model_call("third", 2.0))

    first = await first_task
    second = await second_task
    third = await third_task

    elapsed = time.monotonic() - start

    print(first)
    print(second)
    print(third)
    print(f"elapsed: {elapsed:.2f} seconds")


asyncio.run(main())
