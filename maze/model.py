from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple

Pos = Tuple[int, int]

# Neighbor deltas: N, E, S, W (must match Portfolio/lib/maze.ts)
DIRS = [
    (-1, 0, "N", "S"),  # dr, dc, wall_on_self, wall_on_neighbor
    (0, 1, "E", "W"),
    (1, 0, "S", "N"),
    (0, -1, "W", "E"),
]


@dataclass
class Cell:
    n: bool = True
    e: bool = True
    s: bool = True
    w: bool = True

    def wall(self, side: str) -> bool:
        return getattr(self, side.lower())

    def set_wall(self, side: str, value: bool) -> None:
        setattr(self, side.lower(), value)


@dataclass
class Maze:
    rows: int
    cols: int
    cells: List[List[Cell]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.cells:
            self.cells = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]

    @property
    def start(self) -> Pos:
        return (0, 0)

    @property
    def end(self) -> Pos:
        return (self.rows - 1, self.cols - 1)

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    def remove_wall(self, r: int, c: int, nr: int, nc: int, self_side: str, neigh_side: str) -> None:
        self.cells[r][c].set_wall(self_side, False)
        self.cells[nr][nc].set_wall(neigh_side, False)

    def has_passage(self, r: int, c: int, nr: int, nc: int) -> bool:
        if not self.in_bounds(nr, nc):
            return False
        dr, dc = nr - r, nc - c
        if (dr, dc) == (-1, 0):
            return not self.cells[r][c].n
        if (dr, dc) == (1, 0):
            return not self.cells[r][c].s
        if (dr, dc) == (0, 1):
            return not self.cells[r][c].e
        if (dr, dc) == (0, -1):
            return not self.cells[r][c].w
        return False

    def open_neighbors(self, r: int, c: int) -> List[Pos]:
        out: List[Pos] = []
        for dr, dc, _, _ in DIRS:
            nr, nc = r + dr, c + dc
            if self.has_passage(r, c, nr, nc):
                out.append((nr, nc))
        return out

    def fingerprint(self) -> str:
        """Compact wall fingerprint for cross-runtime parity checks."""
        parts: List[str] = []
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.cells[r][c]
                parts.append(
                    f"{r},{c}:{int(cell.n)}{int(cell.e)}{int(cell.s)}{int(cell.w)}"
                )
        return "|".join(parts)
