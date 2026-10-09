"""Chapter 17: asyncio, threads and processes, timed on the same work."""
import asyncio
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

CALLS = 20            # status lookups to NorthBank
WAIT = 0.1            # seconds each lookup spends waiting on the network
CPU_JOBS = 4          # statement files to checksum
CPU_SIZE = 12_000_000  # loop iterations per file


# --- Work that waits (I/O-bound) -------------------------------------------
def lookup_blocking(payment_id: int) -> str:
    time.sleep(WAIT)                     # a blocking library call
    return f"pay_{payment_id}: settled"


async def lookup_async(payment_id: int) -> str:
    await asyncio.sleep(WAIT)            # an async call: pauses, lets others run
    return f"pay_{payment_id}: settled"


async def lookup_wrongly(payment_id: int) -> str:
    time.sleep(WAIT)                     # blocking call inside async: freezes everyone
    return f"pay_{payment_id}: settled"


async def gather_limited(worker, limit: int = 20) -> list[str]:
    gate = asyncio.Semaphore(limit)      # at most `limit` lookups in flight

    async def one(payment_id: int) -> str:
        async with gate:
            return await worker(payment_id)

    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(one(i)) for i in range(CALLS)]
    return [task.result() for task in tasks]


# --- Timeouts inside a task group ------------------------------------------
async def slow_or_fast(payment_id: int) -> str:
    await asyncio.sleep(0.5 if payment_id == 2 else 0.01)   # lookup 2 hangs
    return "settled"


async def all_or_nothing() -> list[str]:
    """One timeout escapes its task, so the group cancels every sibling."""
    async def one(payment_id: int) -> str:
        async with asyncio.timeout(0.1):
            return await slow_or_fast(payment_id)

    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(one(i)) for i in range(5)]
    return [task.result() for task in tasks]


async def each_on_its_own() -> list[str]:
    """Each task turns its own timeout into a value, so the rest still finish."""
    async def one(payment_id: int) -> str:
        try:
            async with asyncio.timeout(0.1):
                return await slow_or_fast(payment_id)
        except TimeoutError:
            return "TIMED OUT"

    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(one(i)) for i in range(5)]
    return [task.result() for task in tasks]


# --- Work that computes (CPU-bound) ----------------------------------------
def checksum(seed: int) -> int:
    total = seed
    for i in range(CPU_SIZE):
        total = (total * 31 + i) % 1_000_003
    return total


def timed(label: str, func) -> None:
    start = time.perf_counter()
    func()
    print(f"{label:<44}{time.perf_counter() - start:5.1f}s")


if __name__ == "__main__":
    print(f"-- {CALLS} lookups that each wait {WAIT}s")
    timed("one after another", lambda: [lookup_blocking(i) for i in range(CALLS)])
    with ThreadPoolExecutor(max_workers=20) as pool:
        timed("20 threads", lambda: list(pool.map(lookup_blocking, range(CALLS))))
    timed("asyncio", lambda: asyncio.run(gather_limited(lookup_async)))
    timed("asyncio with a blocking call inside",
          lambda: asyncio.run(gather_limited(lookup_wrongly)))

    print(f"-- {CPU_JOBS} checksums that each compute")
    timed("one after another", lambda: [checksum(i) for i in range(CPU_JOBS)])
    with ThreadPoolExecutor(max_workers=CPU_JOBS) as pool:
        timed("4 threads", lambda: list(pool.map(checksum, range(CPU_JOBS))))
    with ProcessPoolExecutor(max_workers=CPU_JOBS) as pool:
        timed("4 processes", lambda: list(pool.map(checksum, range(CPU_JOBS))))

    print("-- five lookups, one of them hangs")
    try:
        asyncio.run(all_or_nothing())
    except* TimeoutError as group:
        print("all or nothing: lost the whole batch,", len(group.exceptions), "timeout")
    print("each on its own:", asyncio.run(each_on_its_own()))
