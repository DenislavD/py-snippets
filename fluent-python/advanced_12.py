# Fluent Python: Coroutines with asyncio full example

import asyncio
from collections import Counter
from http import HTTPStatus
from pathlib import Path

# these are not part of the standard library
import httpx
import tqdm

from z_flags2_common import main, DownloadStatus, save_flag

DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000

# filesystem I/O
async def get_flag(client: httpx.AsyncClient, base_url: str, cc: str) -> bytes:
    url = f'{base_url}/{cc}/{cc}.gif'.lower()
    response = await client.get(url, timeout=3.1, follow_redirects=True) # coroutine
    response.raise_for_status()
    return response.content

# network I/O
async def download_one(client: httpx.AsyncClient, base_url: str, cc: str,
    semaphore: asyncio.BoundedSemaphore, verbose: bool) -> DownloadStatus:
    try:
        async with semaphore:
            # the program is not blocked, only this coroutine is suspended when
            # the internal counter=0. Acquiring a coroutine += 1, releasing -= 1
            image = await get_flag(client, base_url, cc)
    except httpx.HTTPStatusError as exc:
        res = exc.response
        if res.status_code == HTTPStatus.NOT_FOUND:
            status = DownloadStatus.NOT_FOUND
            msg = f'not found: {res.url}'
        else:
            raise # re-raise other types of errors
    else:
        # asyncio has no filesystem I/O async methods, so using an asyncio-provided thread
        await asyncio.to_thread(save_flag, image, f'{cc}.gif')
        status = DownloadStatus.OK
        msg = 'OK'

    if verbose and msg:
        print(cc, msg)
    return status

# main coroutine
async def supervisor(base_url: str, cc_list: list[str], verbose: bool,
    concur_req: int) -> Counter[DownloadStatus]:
    counter: Counter[DownloadStatus] = Counter()

    # the Semaphore base lock will allow max concur_req active coroutines amongst those using it
    semaphore = asyncio.BoundedSemaphore(concur_req)

    async with httpx.AsyncClient() as client:
        # get coroutines list
        to_do = [download_one(client, base_url, cc, semaphore, verbose) for cc in sorted(cc_list)]
        to_do_iter = asyncio.as_completed(to_do) # create iter to allow tdqm wrapping
        if not verbose:
            to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))

        error: httpx.HTTPError | None = None

        for coroutine in to_do_iter:
            try:
                status = await coroutine # non-blocking as as_completed only yields done
            # Error handling
            except httpx.HTTPStatusError as exc:
                error_msg = 'HTTP Error {r.status_code} - {r.reason_phrase}'
                error_msg = error_msg.format(r=exc.response)
                error = exc # exc variable scope is limited to the except clause in Python
            except httpx.RequestError as exc:
                error_msg = f'{exc} {type(exc)}'.strip()
                error = exc
            except KeyboardInterrupt:
                break

            if error:
                status = DownloadStatus.ERROR
                if verbose:
                    url = str(error.request.url)
                    cc = Path(url).stem.upper()
                    print(f'{cc} error: {error_msg}')

            counter[status] += 1

    return counter

# in order to be able to use main from flag2_common, we must call download_many,
# as a normal function, so providing the same arguments to the async supervisor.
def download_many(base_url: str, cc_list: list[str], verbose: bool,
    concur_req: int) -> Counter[DownloadStatus]:
    main_coroutine = supervisor(base_url, cc_list, verbose, concur_req)
    counts = asyncio.run(main_coroutine)

    return counts

if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ) # re-using main from common

