# TODO

from typing import Any
import flarejax as fj

from jaxtyping import Array, Float


class Conv2D(fj.Module):
    w: Float[Array, "dim dim_in h w"]
    b: Float[Array, "dim"]

    @classmethod
    def init(cls):
        raise NotImplementedError

    def __call__(self, x):
        raise NotImplementedError
