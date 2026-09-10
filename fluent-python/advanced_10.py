# Fluent Python: Multiprocessing full example

"""
Each instance of the Python interpreter (~CPython) is a process.
The interpreter uses a single thread to run the user's program.
Access to internal interpreter state is controlled by a lock, GIL.
Only one Python thread can hold the GIL at any time (execute code).
Current thread is paused every 5ms by default, releasing the GIL.
syscalls release the GIL (disk I/O, network I/O, sleep).
To run CPU-intensive Python code on multiple cores, processes.
"""

import math

def is_prime(n: int) -> bool:
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False

    root = math.isqrt(n)
    for i in range(3, root + 1, 2):
        if n % i == 0: return False
    return True # prime!

PRIME_FIXTURE = [
    (2, True),
    (142702110479723, True),
    (299593572317531, True),
    (3333333333333301, True),
    (3333333333333333, False),
    (3333335652092209, False),
    (4444444444444423, True),
    (4444444444444444, False),
    (4444444488888889, False),
    (5555553133149889, False),
    (5555555555555503, True),
    (5555555555555555, False),
    (6666666666666666, False),
    (6666666666666719, True),
    (6666667141414921, False),
    (7777777536340681, False),
    (7777777777777753, True),
    (7777777777777777, False),
    (9999999999999917, True),
    (9999999999999999, False),
]
NUMBERS = [n for n, _ in PRIME_FIXTURE]

import sys
from time import perf_counter
from typing import NamedTuple
from multiprocessing import Process, SimpleQueue, cpu_count, queues

class PrimeResult(NamedTuple):
    n: int
    prime: bool
    elapsed: float

JobQueue = queues.SimpleQueue[int] # Type aliases
ResultQueue = queues.SimpleQueue[PrimeResult]

# CPU intensive task
def check(n: int) -> PrimeResult:
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n, res, perf_counter() - t0)

def worker(jobs: JobQueue, results: ResultQueue) -> None:
    while n:= jobs.get():
        results.put(check(n))
    # poison pill - sentinel that worker has finished -> info to the main loop
    results.put(PrimeResult(0, False, 0.0))

def start_jobs(procs: int, jobs: JobQueue, results: ResultQueue) -> None:
    for n in NUMBERS:
        jobs.put(n)
    for _ in range(procs):
        # fork a child process for each worker
        proc = Process(target=worker, args=(jobs, results)) # jobs, results are SHARED objs
        proc.start()
        jobs.put(0) # will signal the worker to finish, one for each process/worker

def main() -> None:
    if len(sys.argv) < 2:
        procs = cpu_count()
    else:
        procs = int(sys.argv[1])

    print(f'Checking {len(NUMBERS)} numbers with {procs} processes:')
    t0 = perf_counter()
    jobs: JobQueue = SimpleQueue()
    results: ResultQueue = SimpleQueue()
    start_jobs(procs, jobs, results)
    checked = report(procs, results)
    elapsed = perf_counter() - t0
    print(f'{checked} checks in {elapsed:.2f}s')

def report(procs: int, results: ResultQueue) -> int:
    checked = 0
    procs_done = 0
    while procs_done < procs:
        n, prime, elapsed = results.get()
        # calling .get() on a queue blocks until there is an item in the queue!

        if n == 0: # the poison pill
            procs_done += 1
        else:
            checked += 1
            label = 'P' if prime else ' '
            print(f'{n:16} {label} {elapsed:9.6f}s')

    return checked

if __name__ == '__main__':
    main()









