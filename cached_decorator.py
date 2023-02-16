def cached(func):
    some_cache = {}

    def caching(*args, **kwargs):
        if not some_cache.get(args):
            cache = func(*args, **kwargs)
            some_cache[args] = cache
            return cache
        else:
            return some_cache[args]

    return caching
