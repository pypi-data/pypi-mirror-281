from typing import TypeVar

import oryx.core.interpreters.harvest as harvest

T = TypeVar("T")


def tag_mode_sow(x: T, /, *, name: str) -> T:
    x = harvest.sow(x, name=name, tag="strict", mode="strict")
    x = harvest.sow(x, name=name, tag="clobber", mode="clobber")
    x = harvest.sow(x, name=name, tag="append", mode="append")
    return x
