import asyncio

async def hello(delay):
    await asyncio.sleep(delay)  # await tells the loop this task is "busy"
    print('hello')  # eventually the loop resumes the code here

async def world(delay):
    # the loop decides this method should run first
    await asyncio.sleep(delay)  # await tells the loop this task is "busy"
    print('world')  # eventually the loop finishes all tasks

loop = asyncio.get_event_loop()  # get the default loop for the main thread
loop.create_task(world(2))  # create the world task, passing 2 as delay
loop.create_task(hello(delay=1))  # another task, but with delay 1
try:
    # run the event loop forever; ctrl+c to stop it
    # we could also run the loop for three seconds:
    #     loop.run_until_complete(asyncio.sleep(3))
    loop.run_forever()
except KeyboardInterrupt:
    pass