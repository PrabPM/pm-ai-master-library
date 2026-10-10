"""Optional: the Python 3.14+ features mentioned in the book's notes.

On Python 3.13 this file prints one line and exits. Nothing else depends on it.
"""
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor


def checksum(seed: int) -> int:
    total = seed
    for i in range(6_000_000):
        total = (total * 31 + i) % 1_000_003
    return total


def main() -> None:
    from compression import zstd                           # new in 3.14
    from concurrent.futures import InterpreterPoolExecutor  # new in 3.14

    print("python", sys.version.split()[0])
    first, second = uuid.uuid7(), uuid.uuid7()             # new in 3.14
    print("uuid7 version:", first.version, "| time-ordered:", first < second)

    class Journal:
        def reverse(self) -> Journal:   # no quotes needed: annotations are deferred
            return self
    print("annotation resolved lazily:", Journal.reverse.__annotations__["return"])

    print("GIL enabled in this build:", sys._is_gil_enabled())
    for name, pool_type in (("4 threads", ThreadPoolExecutor),
                            ("4 interpreters", InterpreterPoolExecutor)):
        start = time.perf_counter()
        with pool_type(max_workers=4) as pool:
            list(pool.map(checksum, range(4)))
        print(f"{name:<16}{time.perf_counter() - start:4.1f}s")

    data = b"pay_1001,m_harbor,12000,USD\n" * 1000
    print("zstd:", len(data), "bytes ->", len(zstd.compress(data)), "bytes")


if __name__ == "__main__":
    if sys.version_info < (3, 14):
        print("Python 3.14 or later is needed for this file; skipping.")
    else:
        main()
