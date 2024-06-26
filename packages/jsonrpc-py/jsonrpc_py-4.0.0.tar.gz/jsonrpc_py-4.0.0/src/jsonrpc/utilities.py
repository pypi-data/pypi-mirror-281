from __future__ import annotations

from asyncio import Runner, TaskGroup, get_event_loop_policy, get_running_loop
from collections.abc import MutableMapping
from contextvars import copy_context
from dataclasses import dataclass, field
from functools import partial, total_ordering
from heapq import heappop, heappush
from inspect import iscoroutine, iscoroutinefunction
from threading import Thread
from typing import TYPE_CHECKING, Generic, ParamSpec, TypeVar, overload

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop, AbstractEventLoopPolicy, Task
    from collections.abc import Callable, Coroutine, Generator, Iterable, Iterator
    from contextvars import Context
    from typing import Any, TypeGuard

__all__: tuple[str, ...] = (
    "CancellableGather",
    "ensure_async",
    "is_iterable",
    "make_hashable",
    "PrioritizedItem",
    "run_in_background",
)

T = TypeVar("T")
P = ParamSpec("P")


@total_ordering
@dataclass(slots=True)
class PrioritizedItem(Generic[T]):
    priority: int
    item: T

    def __eq__(self, obj: Any) -> bool:
        if not isinstance(obj, self.__class__):
            return NotImplemented
        return self.priority == obj.priority

    def __lt__(self, obj: Any) -> bool:
        if not isinstance(obj, self.__class__):
            return NotImplemented
        return self.priority < obj.priority


@dataclass(slots=True)
class CancellableGather(Generic[T]):
    coroutines: Iterable[Coroutine[Any, Any, T]]
    results: list[PrioritizedItem[T]] = field(default_factory=list, init=False)

    def __await__(self) -> Generator[Any, None, tuple[T, ...]]:
        #: ---
        #: Create a suitable iterator by calling __await__ on a coroutine.
        return self.__await_impl__().__await__()

    async def __await_impl__(self) -> tuple[T, ...]:
        context: Context = copy_context()
        try:
            async with TaskGroup() as group:
                for priority, coroutine in enumerate(self.coroutines):
                    task: Task[T] = group.create_task(coroutine, context=context)
                    callback: partial[None] = partial(self.populate_results, priority=priority)
                    task.add_done_callback(callback, context=context)
        except BaseExceptionGroup as exc_group:
            #: ---
            #: Propagate the first raised exception from exception group:
            for exc in self.exception_from_group(exc_group):
                raise exc from None

        return tuple(self.iter_results())

    def populate_results(self, task: Task[T], *, priority: int) -> None:
        if not task.cancelled() and task.exception() is None:
            result: PrioritizedItem[T] = PrioritizedItem(priority, task.result())
            heappush(self.results, result)

    def exception_from_group(self, exc: BaseException) -> Iterator[BaseException]:
        if isinstance(exc, BaseExceptionGroup):
            for nested in exc.exceptions:
                yield from self.exception_from_group(nested)
        else:
            yield exc

    def iter_results(self) -> Iterator[T]:
        while True:
            try:
                result: PrioritizedItem[T] = heappop(self.results)
                yield result.item
            except IndexError:
                break


@overload
async def ensure_async(user_function: Callable[P, Coroutine[Any, Any, T]], /, *args: P.args, **kwargs: P.kwargs) -> T: ...


@overload
async def ensure_async(user_function: Callable[P, T], /, *args: P.args, **kwargs: P.kwargs) -> T: ...


async def ensure_async(user_function: Callable[P, Any], /, *args: P.args, **kwargs: P.kwargs) -> Any:
    loop: AbstractEventLoop = get_running_loop()
    context: Context = copy_context()

    if iscoroutinefunction(callback := partial(user_function, *args, **kwargs)):
        return await loop.create_task(callback(), context=context)
    else:
        return await loop.run_in_executor(None, context.run, callback)


def is_iterable(obj: Any, /) -> TypeGuard[Iterable[Any]]:
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return True


def make_hashable(obj: Any, /) -> Any:
    if isinstance(obj, MutableMapping):
        return tuple((key, make_hashable(value)) for key, value in sorted(obj.items()))
    #: ---
    #: Try hash to avoid converting a hashable iterable (e.g. string, frozenset)
    #: to a tuple:
    try:
        hash(obj)
    except TypeError:
        if is_iterable(obj):
            return tuple(map(make_hashable, obj))
        #: ---
        #: Non-hashable, non-iterable:
        raise

    return obj


def run_in_background(coroutine: Coroutine[Any, Any, Any], /) -> None:
    if not iscoroutine(coroutine):
        raise ValueError(f"a coroutine was expected, got {type(coroutine).__name__!r}")

    def asyncio_run(policy: AbstractEventLoopPolicy, context: Context) -> None:
        with Runner(loop_factory=policy.new_event_loop) as runner:
            runner.run(coroutine, context=context)

    def start_new_thread(user_function: Callable[P, Any], /, *args: P.args, **kwargs: P.kwargs) -> None:
        thread: Thread = Thread(target=user_function, args=args, kwargs=kwargs)
        thread.start()

    start_new_thread(
        asyncio_run,
        policy=get_event_loop_policy(),
        context=copy_context(),
    )
