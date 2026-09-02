# Fluent Python: Concurrency models, GIL

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
    time.sleep(3) # blocks the main thread, but the GIL is released -> other threads can work
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

def main() -> None:
    result = supervisor()
    print(f'Answer: {result}')

if __name__ == '__main__':
    main()

