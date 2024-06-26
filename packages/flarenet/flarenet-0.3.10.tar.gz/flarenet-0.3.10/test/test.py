# %%
import flarejax as fj
import flarenet as fn

from typing import Any, TypeVar, ParamSpec, Callable, Generic, overload
import inspect

import jax
import jax.numpy as jnp
import jax.random as jrandom


key = jrandom.PRNGKey(0)
key1, key2, key3 = jrandom.split(key, 3)

model = fj.Sequential(
    (
        fn.Linear.init(key, 2, 32),
        fn.GELU(),
        fn.Linear.init(key2, 32, 32),
        fn.GELU(),
        fn.Linear.init(key3, 32, 2),
    )
)
model

# %%
type(model.__call__.__self__)

# %%
T = TypeVar("T")
P = ParamSpec("P")


class Return(fj.Module, Generic[T], register=False):
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
    signature = inspect.signature(inspect.unwrap(f))
    print(signature)

    r = f(*args, **kwargs)

    if isinstance(r, Return):
        return r

    return Return(
        self=None,
        hook=None,
        x=r,
    )


x = jnp.ones((1, 2))
self, y, hook = apply(model, x)
print(y)

# %%
(lambda x: x)(1, 2)
