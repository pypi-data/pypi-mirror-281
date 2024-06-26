import functools

from oryx.core.interpreters.harvest import sow, harvest, reap, nest

import jax
import jax.lax as lax
import jax.numpy as jnp

variable = functools.partial(sow, tag="variable")
harvest_variables = functools.partial(harvest, tag="variable")


def body(carry, x):
    def _t(x):
        return variable(x + carry, name="x", mode="clobber")

    def _f(x):
        return variable(x, name="x", mode="clobber")

    x = lax.cond(True, _t, _f, x)
    return x, x


def f(init):
    return lax.scan(jax.jit(body), init, jnp.arange(5.0))


def h(x):
    x = variable(x + 1, name="x", mode="append")
    # x = variable(x + 1, name="x", mode="append")
    return x


def i(x):
    x = nest(h, scope="h1")(x)
    x = nest(h, scope="h2")(x)
    return x


x = reap(i, tag="variable")(1.0)
print(x)
