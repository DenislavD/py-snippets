# Fluent Python: Coroutines with asyncio simple example

#!usr/bin/env python3
import asyncio
import socket
from keyword import kwlist

MAX_KEYWORD_LEN = 4

async def probe(domain: str) -> tuple[str, bool]:
    loop = asyncio.get_running_loop()
    try:
        # predefined coroutine method of the asyncio Event loop
        await loop.getaddrinfo(domain, None)
    except socket.gaierror: # this is why we imported socket
        return (domain, False)
    return (domain,True)

# main must be a (native) coroutine, so we can use await in it.
async def main() -> None:
    names = (kw for kw in kwlist if len(kw) <= MAX_KEYWORD_LEN)
    domains = (f'{name}.dev'.lower() for name in names)
    coroutines = [probe(domain) for domain in domains]
    for coroutine in asyncio.as_completed(coroutines):
        domain, found = await coroutine
        # at this point, this one coroutine is done - this is how as_completed works
        mark = '+' if found else ' '
        print('{} {}'.format(mark, domain))

if __name__ == '__main__':
    # the next line starts the Event loop and returns only when the loop exits.
    # this is a standard practice - async def main and run it from here
    asyncio.run(main())
