from concurrent.futures import * # for example purposes
import time
from random import random, randrange
from pprint import pprint

def simulated_call(filepath, delay):
    print(f'Manipulating file at {filepath}')
    time.sleep(delay)

    if delay < 2:
        raise Exception(f'Opening {filepath} failed ({delay}s)!')

    return {
        'file': filepath,
        'status': 1,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    }

with ThreadPoolExecutor(max_workers=None) as executor:
    futures = [ executor.submit(simulated_call, f'file-{i}', randrange(6)) for i in range(1, 6) ]
    print(type(futures))
    pprint(futures)

    pending = futures.copy() # used in the initial example for the loop (keeps initial futures for reference)
    c = 1
    while futures:
        print(f'Run #{c}, pending: {len(futures)}')
        c += 1
        res = wait(futures, return_when=FIRST_COMPLETED) # FIRST_COMPLETED   FIRST_EXCEPTION   ALL_COMPLETED
        # print(res) # ~DoneAndNotDoneFutures(done={<Future at 0x12ce7fa6c40 state=finished returned dict>}, not_done=set())
        futures = res.not_done
        for future in res.done:
            try:
                result = future.result()
                print(f'{result["file"].capitalize()} success with status {result["status"]} on {result["timestamp"]}.')
            except Exception as exc:
                print(exc, ', sadly')

    # pprint(pending)
    pprint(futures)
    
