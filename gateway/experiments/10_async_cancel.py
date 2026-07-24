import asyncio


async def model_call() -> str:
    print("model call started")

    try:
        await asyncio.sleep(5.0)
        return "response"
    except asyncio.CancelledError:
        print("model call cancelled")
        raise
    finally:
        print("model call cleanup")


async def main() -> None:
    task = asyncio.create_task(model_call())

    await asyncio.sleep(1.0)

    print("requesting cancellation")
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print("main observed cancellation")


asyncio.run(main())
