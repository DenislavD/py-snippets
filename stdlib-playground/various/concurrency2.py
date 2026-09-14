# Fluent Python: Show the inner workings of executor.map

from concurrent import futures
from time import sleep, strftime

def display(*args):
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)

def loiter(n):
    msg = '{}loiter({}): doing nothing for {}s...'
    display( msg.format('\t'*n, n, n) )
    sleep(n)
    msg = '{}loiter({}): done.'
    display( msg.format('\t'*n, n) )
    return n * 10

def main():
    display('Script starting.')
    executor = futures.ThreadPoolExecutor(max_workers=3) # workers=1 is NOT sequential
    results = executor.map(loiter, range(5)) # this is a nonblocking call
    # results = map(loiter, range(5)) # sequential: TRY IT!
    display('results:', results) # <generator object Executor.map.<locals>.result_iterator..>

    display('Waiting for individual results:')
    # this loop will invoke next(results), which will invoke _f.result() on the internal
    # _f future representing the first call, loiter(0). The result method wil block until
    # the future is done, therefore each iteration in this loop will have to wait for the
    # next result to be ready.
    for i, result in enumerate(results):
        display(f'result {i}: {result}')

if __name__ == '__main__':
    main()


""" BLOCKING
a) with executor: -> blocks on executor.__exit__() until all futures are done
b) results = executor.map -> blocks implicitly later on results.next() iteration (sequential)
c) executor.submit + futures.as_completed -> blocks on as_completed if nothing is done yet
"""
