import functools
import time


def timer(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        run_time = time.perf_counter() - start
        print(f"{func.__name__} took {run_time:.4f} secs")
        return result
    return _wrapper
