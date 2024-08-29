import asyncio


async def task_async(text='Message'):
    print(text)


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

try:
    loop.run_until_complete(task_async())
    loop.run_forever()

except KeyboardInterrupt:
    pass
finally:
    loop.close()
