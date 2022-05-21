# First we need the asyncio library
import asyncio

# Then we need a loop to work with
loop = asyncio.get_event_loop()

# We also need something to run
async def main():
    for char in 'Hello, world!\n':
        print(char, end='', flush=True)
        await asyncio.sleep(0.5)

# Then, we need to run the loop with a task
loop.run_until_complete(main())