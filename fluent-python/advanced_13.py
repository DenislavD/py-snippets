# Fluent Python: async iteration, generators and comprehension

# from Python 3.8 : Asynchronous Python interpreter: py -m asyncio

import asyncio
import socket
from collections.abc import Iterable, AsyncIterator
from typing import NamedTuple, Optional

class Result(NamedTuple): domain: str; found: bool

async def probe(domain: str, loop: asyncio.AbstractEventLoop | None=None) -> Result:
    if loop is None:
        loop = asyncio.get_running_loop()
    try:
        await loop.getaddrinfo(domain, None)
    except socket.gaierror:
        return Result(domain, False)
    return Result(domain, True)

# an asyncronous generator function produces an async generator object (AsyncIterator)
async def multiprobe(domains: Iterable[str]) -> AsyncIterator[Result]:
    loop = asyncio.get_running_loop()
    coroutines = [probe(domain, loop) for domain in domains]
    for coroutine in asyncio.as_completed(coroutines): # as_completed is a normal generator
        result = await coroutine
        yield result # this makes the coroutine an async generator function


""" console tests:
await asyncio.sleep(3, 'Rise and shine!')

--- Asynchronous iteration ---
import advanced_13 as dl
await dl.probe('python.org')    # Result(domain='python.org', found=True)
dl.probe('python.org')          # <coroutine object probe at 0x00000230319766C0>
dl.multiprobe(names)            # <async_generator object multiprobe at 0x00000230318779A0>

names = 'python.org rust-lang.org golang.org no-lang.invalid'.split()
async for result in dl.multiprobe(names):
    print(*result, sep='\t')

for r in dl.multiprobe(names):
    print('here', r)
# TypeError: 'async_generator' object is not iterable
# implements __aiter__ instead of __iter__

--- Asynchronous comprehension ---
[await dl.probe(name) for name in names]

# same as:
coros = [dl.probe(name) for name in names]
await asyncio.gather(*coros) # *better than the comprehension, because it has error handling

# dictcomp
{name: found async for name, found in dl.multiprobe(names)}

# setcomp
{name for name in names if (await dl.probe(name)).found}

Note: These can only appear inside an async def body or in the special async console!
"""
