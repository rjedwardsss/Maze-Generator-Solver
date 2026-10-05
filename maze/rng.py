"""Mulberry32 PRNG — same algorithm as Portfolio/lib/maze.ts for seed parity."""

from __future__ import annotations


def _imul(a: int, b: int) -> int:
    """32-bit signed multiply (Math.imul)."""
    return ((a & 0xFFFFFFFF) * (b & 0xFFFFFFFF)) & 0xFFFFFFFF


class Mulberry32:
    def __init__(self, seed: int) -> None:
        self._state = seed & 0xFFFFFFFF

    def next_u32(self) -> int:
        self._state = (self._state + 0x6D2B79F5) & 0xFFFFFFFF
        t = self._state
        t = _imul(t ^ (t >> 15), t | 1)
        t ^= (t + _imul(t ^ (t >> 7), t | 61)) & 0xFFFFFFFF
        return (t ^ (t >> 14)) & 0xFFFFFFFF

    def random(self) -> float:
        return self.next_u32() / 4294967296.0

    def shuffle(self, items: list) -> None:
        for i in range(len(items) - 1, 0, -1):
            j = int(self.random() * (i + 1))
            items[i], items[j] = items[j], items[i]
