from typing import Any

import flarejax as fj
import jax


class Hook(fj.Module):
    context: tuple
    key: jax.Array
    mode: Any

    def merge(self, ctx, other):
        pass


class Linear(fj.Module):
    # The __init__ method is automatically generated
    w: jax.Array
    b: jax.Array

    # additional intialization methods via classmethods
    @classmethod
    def init(cls, key, dim_in, dim):
        w = jax.random.normal(key, (dim, dim_in)) * 0.02
        b = jax.numpy.zeros((dim,))
        return cls(w=w, b=b)

    def __call__(self, x, *, hook=None):
        return self.w @ x + self.b


key = jax.random.PRNGKey(42)
key1, key2 = jax.random.split(key)

model = fj.Sequential(
    (
        Linear.init(key1, 3, 2),
        Linear.init(key2, 2, 5),
    )
)
