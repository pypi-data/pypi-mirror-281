import math

import flarejax as fj
import jax.numpy as jnp
import jax.random as jrandom
from jaxtyping import Array, Float, PRNGKeyArray, jaxtyped

from ._utils import tag_mode_sow

__all__ = [
    "Linear",
    "Bias",
    "Scale",
    "Constant",
]


class Linear(fj.Module):
    """
    Apply a learanable affine transformation to the input data. That takes the
    form of a matrix multiplication and an optional bias addition.

    The last input axis has dimensionality 'dim_in', the output shares all axes,
    except the last one with the input, which has dimensionality 'dim'.

    Attributes:
    ---
    w: jax.Array
        The learnable weights of the layer. This has shape (dim_in, dim).

    b: jax.Array | None
        The learnable bias of the layer. This has shape (dim,) or is None, if
        the layer does not have a bias.
    """

    __module_name = "flarenet.Linear"

    w: Float[Array, "dim_in dim"]
    b: Float[Array, "dim"] | None

    @fj.typecheck
    @classmethod
    def init(
        cls,
        key: PRNGKeyArray,
        dim_in: int,
        dim: int,
        use_bias: bool = True,
    ):
        """
        Initialize the layer with random weights and biases. The default
        initialization is based on the Glorot uniform initialization, which
        is the same as the PyTorch default.

        Parameters:
        ---
        key: PRNGKey
            The random key to use for initialization.

        dim_in: int
            The number of input features.

        dim: int
            The number of output features.

        use_bias: bool
            Whether to use a bias term in the layer.

        Returns:
        ---
        Linear
            The initialized layer.
        """
        scale = 1 / math.sqrt(dim_in)
        w_key, b_key = jrandom.split(key)

        w = jrandom.uniform(w_key, (dim_in, dim), minval=-1, maxval=1) * scale

        if use_bias:
            b = jrandom.uniform(b_key, (dim,), minval=-1, maxval=1) * scale
        else:
            b = None

        return cls(w=w, b=b)

    @jaxtyped(typechecker=fj.typecheck)
    def __call__(
        self,
        x: Float[Array, "*b {self.dim_in}"],
    ) -> Float[Array, "*b {self.dim}"]:
        y = jnp.dot(x, self.w)

        y = tag_mode_sow(y, name="x @ w")

        if self.has_bias:
            y += self.b
            y = tag_mode_sow(y, name="x @ w + b")

        return y

    @fj.typecheck
    @property
    def dim_in(self) -> int:
        return self.w.shape[0]

    @fj.typecheck
    @property
    def dim(self) -> int:
        return self.w.shape[1]

    @fj.typecheck
    @property
    def has_bias(self) -> bool:
        return self.b is not None


class Bias(fj.Module):
    __module_name = "flarenet.Bias"

    b: Float[Array, "..."]

    @fj.typecheck
    @classmethod
    def init(cls, dim: int):
        return cls(b=jnp.zeros((dim,)))

    @jaxtyped(typechecker=fj.typecheck)
    def __call__(
        self,
        x: Float[Array, "*b {self.dim}"],
    ) -> Float[Array, "*b {self.dim}"]:
        y = x + self.b
        y = tag_mode_sow(y, name="x + b")
        return y

    @fj.typecheck
    @property
    def dim(self) -> int:
        return self.b.shape[0]


class Scale(fj.Module):
    __module_name = "flarenet.Scale"

    s: Float[Array, "..."]

    @classmethod
    def init(cls, dim: int):
        return cls(s=jnp.ones((dim,)))

    @jaxtyped(typechecker=fj.typecheck)
    def __call__(
        self, x: Float[Array, "*b {self.dim}"]
    ) -> Float[Array, "*b {self.dim}"]:
        y = x * self.s
        y = tag_mode_sow(y, name="x * s")
        return y

    @property
    def dim(self) -> int:
        return self.s.shape[0]


class Constant(fj.Module):
    __module_name = "flarenet.Constant"

    x: Float[Array, "..."]

    @classmethod
    def random_normal(
        cls,
        key: PRNGKeyArray,
        shape: tuple[int, ...],
        std: float = 1.0,
    ):
        return cls(x=jrandom.normal(key, shape) * std)

    @classmethod
    def random_uniform(
        cls,
        key: PRNGKeyArray,
        shape: tuple[int, ...],
        low: float = -1.0,
        high: float = 1.0,
    ):
        return cls(x=jrandom.uniform(key, shape, minval=low, maxval=high))

    @classmethod
    def full(cls, x: float = 0.0, shape: tuple[int, ...] = ()):
        return cls(x=jnp.full(shape, x))

    @property
    def shape(self) -> tuple[int, ...]:
        return self.x.shape

    @property
    def dtype(self) -> jnp.dtype:
        return self.x.dtype

    @fj.typecheck
    def __call__(self, *args, **kwargs) -> Array:
        return self.x
