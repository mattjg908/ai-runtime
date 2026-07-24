import asyncio


async def model_call(
    name: str,
    delay: float,
    should_fail: bool = False,
) -> str:
    print(f"{name}: started")

    try:
        await asyncio.sleep(delay)

        if should_fail:
            raise RuntimeError(f"{name}: failed")

        print(f"{name}: finished")
        return f"{name}: response"

    except asyncio.CancelledError:
        print(f"{name}: cancelled")
        raise

    finally:
        print(f"{name}: cleanup")


async def main() -> None:
    try:
        async with asyncio.TaskGroup() as task_group:
            task_group.create_task(
                model_call(
                    "first",
                    1.0,
                    should_fail=True,
                )
            )

            task_group.create_task(
                model_call(
                    "second",
                    5.0,
                )
            )

    except* RuntimeError as errors:
        for error in errors.exceptions:
            print(f"main observed: {error}")


asyncio.run(main())
