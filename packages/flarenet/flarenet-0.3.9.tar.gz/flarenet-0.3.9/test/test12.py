from typing import Callable, Generator, TypeVar, Any, ParamSpec
import inspect
import functools

T = TypeVar("T")
P = ParamSpec("P")


def run_generator(
    g: Callable[P, Generator[Any, None, T]],
    /,
    *args: P.args,
    **kwargs: P.kwargs,
) -> T:
    try:
        gen = g(*args, **kwargs)

        while True:
            _ = next(gen)

    except StopIteration as e:
        return e.value


def generator_to_function(
    generator: Callable[P, Generator[Any, None, T]] | Callable[P, T], /
) -> Callable[P, T]:
    if not inspect.isgeneratorfunction(generator):
        return generator  # type: ignore

    @functools.wraps(generator)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
        gen = generator(*args, **kwargs)

        try:
            while True:
                _ = next(gen)

        except StopIteration as e:
            return e.value

    return wrapped
