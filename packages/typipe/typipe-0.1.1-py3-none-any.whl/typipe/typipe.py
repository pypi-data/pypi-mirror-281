from __future__ import annotations
from collections.abc import Callable as F, Iterable
from itertools import chain
from typing import Any, Concatenate, cast
from attrs import define
import inspect
import toolz

_map = map


@define
class Piped[U]:
    _last: F[..., U] | U
    _stack: list

    def to[V](self, f: F[[U], V]) -> Piped[V]:
        self._stack.append(self._last)
        self._last = f  # type: ignore
        return cast(Piped[V], self)

    def __or__[V](self, f: F[[U], V]) -> Piped[V]:
        return self.to(f)

    def get(self) -> U:
        if not self._stack:
            return cast(U, self._last)
        out = self._stack[0]
        for f in self._stack[1:]:
            out = f(out)
        return cast(F[..., U], self._last)(out)

    def __repr__(self) -> str:
        if not self._stack:
            return f"Piped({self._last}, len=1)"
        try:
            lines: list[str] = (
                inspect.getsource(cast(F, self._last)).strip(" |").split("\n")
            )
            last_src = ";".join(line.strip() for line in lines)
        except TypeError:
            last_src = "<cannot inspect source>"
        return f"Piped({last_src},{" ... , " if self._stack else ""}len = {len(self._stack)+1})"

    def __len__(self) -> int:
        return len(self._stack) + 1


def pipe[T](t: T) -> Piped[T]:
    return Piped(t, [])


def curry[T, U, V](f: F[[T, U], V]) -> F[[T], F[[U], V]]:
    def curried_f(t: T) -> F[[U], V]:
        def c(u: U) -> V:
            return f(t, u)

        return c

    return curried_f


def map[T, U](f: F[[T], U]) -> F[[Iterable[T]], Iterable[U]]:
    """
    Map a function over an iterable.
    """
    return curry(_map)(f)


def starmap[**P, U](f: F[P, U]) -> F[[Iterable[Concatenate[P]]], Iterable[U]]:
    return lambda xs: _map(f, *xs)  # type: ignore


def flatmap[T, U](f: F[[T], Iterable[U]]) -> F[[Iterable[T]], Iterable[U]]:
    return lambda x: chain.from_iterable(_map(f, x))


def reduce[T, U](f: F[[T, U], T], initializer: T) -> F[[Iterable[U]], T]:
    return lambda us: toolz.reduce(f, us, initializer)


reduceleft = reduce


# def reduceright[T, U](f: F[[U, T], T], initializer: T) -> [[Iterable[U]], T]:
# for


def foldleft[U](f: F[[U, U], U]) -> F[[Iterable[U]], U]:
    # raises index error if iterable is empty
    def foldl(iterable: Iterable[U]) -> U:
        us = iter(iterable)
        result = next(us)
        return toolz.reduce(f, us, result)

    return foldl


fold = foldleft


# def foldright[U](f: F[[U, U], U]) -> F[[Iterable[U]], U]:
#     # raises index error if iterable is empty
#     def foldr(iterable: Iterable[U]) -> U:
#         us = iter(list(iterable)[::-1])
#         result = next(us)
#         return toolz.reduce(f, us, result)

#     return foldr


def filter[U](f: F[[U], bool]) -> F[[Iterable[U]], Iterable[U]]:
    return lambda us: toolz.filter(f, us)


@curry
def accumulate[T](iterable: Iterable[T], func: F[[T, T], T]) -> Iterable[T]:
    return toolz.accumulate(func, iterable)


def tapwith[T](side_effect: F[[T], Any]) -> F[[T], T]:
    def tap(t: T) -> T:
        __ = side_effect(t)
        return t

    return tap


tap = tapwith(print)

if __name__ == "__main__":

    def times_two(x: int) -> int:
        return 2 * x

    out = (
        pipe(253)
        | times_two
        | times_two
        | times_two
        | str
        | tap  # prints 2024
        | (lambda s: f"hello {s}!!")
        | (lambda s: cast(str, s).upper())
    )

    print(out.get())  # HELLO 2024!!

    its_typechecked = (
        pipe(253)
        | times_two
        | times_two
        | times_two
        | times_two
        | times_two
        | str
        | times_two  # typechecker should point out error on this line
        | times_two
        | times_two
        | times_two
    )
    x = (
        pipe(1)
        | times_two
        | times_two
        | times_two
        | range
        | map(times_two)
        | map(times_two)
        | map(times_two)
        | list[int]
        | reversed
        | filter(lambda x: cast(int, x) > 20)
    )
    print(x)
    print(list(x.get()))
