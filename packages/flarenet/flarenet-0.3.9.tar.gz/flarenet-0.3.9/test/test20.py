from typing import Any, TypeVar, Generic
import dataclasses


T = TypeVar("T")


@dataclasses.dataclass(frozen=True)
class Return(Generic[T]):
    new: T
    out: Any
    fun: Any
