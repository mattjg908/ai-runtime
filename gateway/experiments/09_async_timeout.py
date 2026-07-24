import asyncio


async def model_call(delay: float) -> str:
    print("model call started")

    try:
        await asyncio.sleep(delay)
    except asyncio.CancelledError:
        print("model call cancelled")
        raise

    print("model call finished")

    return "response"


async def main() -> None:
    try:
        response = await asyncio.wait_for(
            model_call(5.0),
            timeout=1.0,
        )
        print(response)
    except TimeoutError:
        print("model call timed out")


asyncio.run(main())
