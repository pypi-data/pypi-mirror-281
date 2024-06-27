import asyncio


async def tool_await(time=1):
    await asyncio.sleep(time)
    return True


if __name__ == '__main__':
    pass
