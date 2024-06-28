from typing import Any, TypeVar, ParamSpec, Callable, Generic, overload

import flarejax as fj
import inspect


T = TypeVar("T")
P = ParamSpec("P")


class Return(fj.Module, Generic[T]):
    self: Any
    hook: Any
    x: T

    def __iter__(self):
        return iter((self.self, self.x, self.hook))


@overload
def apply(f: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> Return[T]: ...


@overload
def apply(
    f: Callable[P, Return[T]], *args: P.args, **kwargs: P.kwargs
) -> Return[T]: ...


def apply(
    f: Callable[P, T] | Callable[P, Return[T]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Return[T]:
    r = f(*args, **kwargs)

    if isinstance(r, Return):
        return r

    return Return(
        self=None,
        hook=None,
        x=r,
    )
