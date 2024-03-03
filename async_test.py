import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    print(f"started at {time.strftime('%X')}")

    await say_after(1, "hello")
    await say_after(2, "world")

    print(f"finished at {time.strftime('%X')}")


# task groups
async def main2():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(say_after(1, "hello"))

        task2 = tg.create_task(say_after(2, "world"))

        print(f"started at {time.strftime('%X')}")

    # The wait is implicit when the context manager exits.

    print(f"finished at {time.strftime('%X')}")


# threads
def blocking_io():
    print(f"start blocking_io at {time.strftime('%X')}")
    # Note that time.sleep() can be replaced with any blocking
    # IO-bound operation, such as file operations.
    time.sleep(1)
    print(f"blocking_io complete at {time.strftime('%X')}")


async def main3():
    print(f"started main at {time.strftime('%X')}")

    await asyncio.gather(asyncio.to_thread(blocking_io), asyncio.sleep(4))

    print(f"finished main at {time.strftime('%X')}")


asyncio.run(main3())
