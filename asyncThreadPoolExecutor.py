T = typing.TypeVar("T")


async def async_pool_executor(coros: list[typing.Awaitable[T]], workers=10) -> list[T]:
    bar = tqdm.tqdm(total=len(coros))

    def next_bar():
        return bar.update(1)

    async def work(queue: asyncio.Queue[tuple[int, typing.Awaitable[T]]]) -> list[tuple[int, T]]:
        res_list = []
        while True:
            try:
                i, coro = queue.get_nowait()
            except asyncio.QueueEmpty:
                break
            else:
                res_list.append((i, await coro))
                queue.task_done()
                next_bar()
        return res_list

    base_time = time.time()
    queue: asyncio.Queue[tuple[int, typing.Awaitable[T]]] = asyncio.Queue()
    for i, coro in enumerate(coros):
        queue.put_nowait((i, coro))
    niggers_work_result = await asyncio.gather(*[work(queue) for _ in range(workers)])
    indexed_res: list[tuple[int, T]] = list(itertools.chain(*niggers_work_result))
    bar.close()
    res = [x[1] for x in sorted(indexed_res, key=lambda x: x[0])]
    logger.info(f"{time.time() - base_time}s spent on async_pool_executor *_*")
    return res
