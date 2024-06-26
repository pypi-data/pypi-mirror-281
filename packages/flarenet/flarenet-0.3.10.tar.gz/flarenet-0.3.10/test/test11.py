from typing import Callable, Generator, TypeVar, Any, ParamSpec, Concatenate
import functools

T = TypeVar("T")
P = ParamSpec("P")


def generator_to_function(
    generator: Callable[P, Generator[Any, None, T]], /
) -> Callable[P, T]:
    @functools.wraps(generator)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
        gen = generator(*args, **kwargs)

        try:
            while True:
                _ = next(gen)

        except StopIteration as e:
            return e.value

    return wrapped


def generator_to_function_maybe(
    generator: Callable[P, Generator[Any, None, T]]
) -> Callable[Concatenate[bool, P], Any | Generator[Any, None, T]]:
    print(type(P.kwargs))
    print(dir(P.kwargs))

    def wrapped(
        *args: P.args,
        **kwargs: P.kwargs | {"as_generator": bool},
    ) -> T | Generator[Any, None, T]:
        if kwargs["as_generator"]:
            return generator(*args, **kwargs)

        gen = generator(*args, **kwargs)

        try:
            while True:
                _ = next(gen)

        except StopIteration as e:
            return e.value

    return wrapped


@generator_to_function_maybe
def g():

    yield 1
    yield 2
    return 3


for i in g(as_generator=True):
    print(i)
