# Fluent Python: Concurrency models: threads, processes, coroutines, GIL

# 1. Threads version
import itertools, time
from threading import Thread, Event

def spin(msg: str, done: Event) -> None: # this function will run in a separate thread
    for char in itertools.cycle('\\|/-'):
        status = f'\r{char} {msg}'
        print(status, end='', flush=True)
        if done.wait(.1): # returns True when Event.set() by another thread, default False
            # without timer, it waits as blocked (synchronously?)
            break

    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')

def slow() -> int:
    time.sleep(2) # blocks the main thread, but the GIL is released -> other threads can work
    return 42

def supervisor() -> int:
    done = Event() # will manage communication between threads
    spinner = Thread(target=spin, args=('thinking!', done))
    print(f'spinner object: {spinner}') # <Thread(Thread-1 (spin), initial)> (initial=not started)
    spinner.start()
    result = slow() # main thread blocked, secondary running the spinner animation
    done.set()
    spinner.join() # wait until the spinner thread finishes = function returns
    return result

if __name__ == '__main__':
    result = supervisor()
    print(f'Answer: {result}')


# 2. Process version
from multiprocessing import Process, Event, synchronize

# reusing the spin and slow funcs from the threading example

# Same API, only Process instead of Thread !
def supervisor2() -> int:
    done = Event() # here synchronize.Event class returned from Event function
    spinner = Process(target=spin, args=('thinking!', done)) 
    print(f'spinner object: {spinner}') # <Process name='Process-1' parent=7996 initial>
    spinner.start()
    result = slow()
    done.set()
    spinner.join()
    return result    

if __name__ == '__main__':
    result2 = supervisor2()
    print(f'Answer2: {result2}')


# 3. Coroutine (native) version
import asyncio
"Coroutines are driven by an application-level event loop that manages a queue of pending"
"coroutines, drives them one by one, monitors I/O-triggered events, and passes control back"
"when each event happens. The event loop and all coroutines execute in a single thread."

def main() -> None:
    resultC = asyncio.run(supervisorC()) # will return the result of supervisorC
    # starts the event loop to drive the coroutine that will eventually start
    # the other coroutines. The main func will stay blocked until supervisorC returns.
    print(f'AnswerC: {resultC}')

# entry point coroutine
async def supervisorC() -> int:
    spinner = asyncio.create_task(spinC('thinking!'))
    # returns an instance of asyncio.Task, scheduling it for execution
    print(f'spinner object: {spinner}') # <Task pending name='Task-2' coro=<spinC() ..>
    result = await slowC() # transfers control to slow and blocks supervisorC
    # slow's sleep releases the GIL, so spinner can run in the meantime

    # now result is fetched, cancel the spinner (direct instead of an Event)
    spinner.cancel()
    return result

async def spinC(msg: str) -> None:
    for char in itertools.cycle('\\|/-'):
        status = f'\r{char} {msg}'
        print(status, end='', flush=True)
        # different part
        try:
            await asyncio.sleep(.1) # pauses without blocking other coroutines
        except asyncio.CancelledError: # raised on spinner.cancel() at the await
            break

    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')    

async def slowC() -> int:
    await asyncio.sleep(2)
    return 422

if __name__ == '__main__':
    main()
