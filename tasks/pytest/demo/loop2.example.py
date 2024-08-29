import asyncio


async def task_async(text='Message'):
    while True:
        print(text)
        await asyncio.sleep(1)


loop = asyncio.get_event_loop()

try:
    asyncio.ensure_future(task_async())
    asyncio.ensure_future(task_async('Other Message'))
    loop.run_forever()

except KeyboardInterrupt:
    pass

finally:
    loop.close()
