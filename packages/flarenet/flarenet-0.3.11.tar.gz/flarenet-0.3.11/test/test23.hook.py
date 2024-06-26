import dataclasses
from typing import Any, Generic, Hashable, Self, TypeVar

import flarejax as fj
import jax
from jaxtyping import PRNGKeyArray


# TODO forget state, if people want statefull computations f them


class Return(fj.Module):
    self: Any
    x: Any
    hook: Any

    def __iter__(self):
        return iter((self.self, self.x, self.hook))


K = TypeVar("K", bound=Hashable)
T = TypeVar("T")


def _nested_dict(input_dict):
    def insert_nested_dict(d, keys, value):
        if len(keys) == 1:
            d[keys[0]] = value
        else:
            if keys[0] not in d:
                d[keys[0]] = {}
            insert_nested_dict(d[keys[0]], keys[1:], value)

    nested_dict = {}
    for k, v in input_dict.items():
        insert_nested_dict(nested_dict, k, v)

    return nested_dict


class Hook(fj.Module, Generic[K, T]):
    _key: PRNGKeyArray
    _context: tuple[K, ...] = fj.field(default=(), static=True)
    _watched: fj.ModuleMapping[tuple[K, ...], T] = fj.field(
        default_factory=fj.ModuleMapping
    )

    @property
    def context(self) -> tuple[K, ...]:
        return self._context

    @property
    def watched(self) -> dict:
        return _nested_dict(self._watched._data)

    def get_key(self) -> tuple[Self, PRNGKeyArray]:
        key, subkey = jax.random.split(self._key)
        return dataclasses.replace(self, _key=subkey), key

    def add(self: Self, x: "Hook[K, T]", /) -> Self:
        watched = self._watched.update(x._watched._data)
        return dataclasses.replace(self, _watched=watched)

    def sub(self: Self, c: K, /):
        return dataclasses.replace(self, _context=(*self._context, c))

    def __call__(self: Self, k: K, v: Any, /) -> tuple[Self, Any]:
        watch = self.watch(k, v)

        if watch is not None:
            watched = self._watched.update({(*self._context, k): v})
            self = dataclasses.replace(self, _watched=watched)

        return self.plant(k, v), self

    def watch(self, k: K, v: Any, /) -> Any:
        return v

    def plant(self, k: K, v: Any, /) -> Self:
        return v


class Linear(fj.Module):
    # The __init__ method is automatically generated
    w: jax.Array
    b: jax.Array

    # additional intialization methods via classmethods
    @classmethod
    def init(cls, key, dim_in, dim):
        w = jax.random.normal(key, (dim_in, dim)) * 0.02
        b = jax.numpy.zeros((dim,))
        return cls(w=w, b=b)

    def __call__(self, x, *, hook: Hook):
        y = x @ self.w
        y, hook = hook("x @ w", y)

        y = y + self.b
        y, hook = hook("y + b", y)

        return Return(self, y, hook)


class Sequential(fj.ModuleSequence):
    __module_name = "flarenet.Sequential"

    def __call__(self, x, *, hook: Hook):
        for i, layer in enumerate(self):
            x = layer(x, hook=hook.sub(f"{self.__class__.__name__}:{i}"))

            if isinstance(x, Return):
                self, x, hook_new = x
                hook = hook.add(hook_new)

        return Return(self, x, hook)


# model = Linear.init(jax.random.PRNGKey(42), 3, 2)
model = Sequential(
    (
        Linear.init(jax.random.PRNGKey(42), 3, 2),
        Linear.init(jax.random.PRNGKey(42), 2, 5),
    )
)

hook = Hook(jax.random.PRNGKey(42))

x = jax.numpy.array([1.0, 2.0, 3.0])
self, y, hook = model(x, hook=hook)


from pprint import pprint

pprint(hook.watched)
