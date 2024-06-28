from typing import Generator, Any, TypeVar, Callable, ParamSpec
import functools
import inspect

T = TypeVar("T")
P = ParamSpec("P")


def generator_to_function(
    generator: Callable[P, Generator[Any, T, T]] | Callable[P, T],
    /,
) -> Callable[P, T]:
    @functools.wraps(generator)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
        gen = generator(*args, **kwargs)

        if not inspect.isgenerator(gen):
            return gen  # type: ignore

        try:
            x, _ = next(gen)

            while True:
                x, _ = gen.send(x)

        except StopIteration as e:
            return e.value

    return wrapped


def function_to_generator(
    function: Callable[P, T],
    /,
) -> Callable[P, Generator[tuple[T, tuple[str]], T, T]]:
    @functools.wraps(function)
    def wrapped(
        *args: P.args, **kwargs: P.kwargs
    ) -> Generator[tuple[T, tuple[str]], T, T]:

        x = function(*args, **kwargs)
        x = yield x, ("FunctionToGenerator",)
        return x

    return wrapped


class Bias:
    def __call__(self, x):
        x = yield x + 1, ("Bias",)
        return x


class Linear:
    def __call__(self, x):
        x = yield x * 2, ("Linear",)
        return x


class Affine:
    def __init__(self):
        self.bias = Bias()
        self.linear = Linear()

    def __call__(self, x):
        x = add_info(self.linear(x), "Affine")
        x = yield from x
        x = yield from add_info(self.bias(x), "Affine")
        return x


class Sequential:
    def __init__(self, *layers):
        self.layers = layers

    def __call__(self, x):
        for layer in self.layers:
            # print(x)
            x = yield from add_info(layer(x), "Sequential")

        return x


def add_info(gen, info):
    try:
        x, info_old = next(gen)
        x = yield (x, (info,) + info_old)

        while True:
            x, info_old = gen.send(x)
            x = yield (x, (info,) + info_old)

    except StopIteration as e:
        return e.value


model = Sequential(Affine(), Affine())
model = generator_to_function(model)

print(model(1))
