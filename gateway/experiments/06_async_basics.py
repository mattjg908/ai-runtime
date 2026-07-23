import asyncio


async def fetch_model_response() -> str:
    print("request started")

    try:
        await asyncio.sleep(10.0)
    except asyncio.CancelledError:
        print("request was cancelled")
        raise

    print("request finished")

    return "response"


async def main() -> None:
    try:
        response = await asyncio.wait_for(
            fetch_model_response(),
            timeout=1.0,
        )
        print(response)
    except TimeoutError:
        print("request timed out")


asyncio.run(main())
