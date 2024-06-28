from typing import Any, TypeVar

import flarejax as fj
import jax
import jax.numpy as jnp
import oryx.core.interpreters.harvest as harvest

T = TypeVar("T")


__all__ = [
    "Add",
    "Multiply",
    "Concat",
    "Identity",
    "Residual",
    "Index",
]


class Sequential(fj.ModuleSequence):
    __module_name = "flarenet.Sequential"

    @fj.typecheck
    def __call__(self, x, *args, **kwargs) -> Any:
        for i, layer in enumerate(self):
            assert callable(layer), f"Layer {layer} is not callable."

            # layer = harvest.nest(layer, scope=str(i))
            x = layer(x, *args, **kwargs)

        return x


class Add(Sequential):
    __module_name = "flarenet.Add"

    @fj.typecheck
    def __call__(self, x, *args, **kwargs) -> Any:
        y = 0

        for i, layer in enumerate(self):
            assert callable(layer), f"Layer {layer} is not callable."

            layer = harvest.nest(layer, scope=str(i))
            y = y + layer(x, *args, **kwargs)

        return y


class Multiply(Sequential):
    __module_name = "flarenet.Multiply"

    @fj.typecheck
    def __call__(self, x, *args, **kwargs) -> Any:
        y = 1

        for i, layer in enumerate(self):
            assert callable(layer), f"Layer {layer} is not callable."

            layer = harvest.nest(layer, scope=str(i))
            y = y * layer(x, *args, **kwargs)

        return y


class Concat(Sequential):
    __module_name = "flarenet.Concat"

    @fj.typecheck
    def __call__(self, x, *args, **kwargs) -> jax.Array:
        ys = []

        for i, layer in enumerate(self):
            assert callable(layer), f"Layer {layer} is not callable."

            layer = harvest.nest(layer, scope=str(i))
            ys.append(layer(x, *args, **kwargs))

        return jnp.concatenate(ys, axis=-1)


class Identity(fj.Module):
    __module_name = "flarenet.Identity"

    @fj.typecheck
    def __call__(self, x: T, *args, **kwargs) -> T:
        return x


class Residual(fj.Module):
    __module_name = "flarenet.Residual"

    layer: fj.Module

    @fj.typecheck
    def __call__(self, x, *args, **kwargs) -> Any:
        assert callable(self.layer), f"Layer {self.layer} is not callable."
        return x + self.layer(x, *args, **kwargs)


class Index(fj.Module):
    __module_name = "flarenet.Index"

    index: int | slice | tuple[int | slice, ...]

    @fj.typecheck
    def __call__(self, x) -> Any:
        return x[self.index]
