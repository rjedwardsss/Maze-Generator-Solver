from __future__ import annotations

from typing import List, NamedTuple, Tuple

from maze.model import DIRS, Maze, Pos
from maze.rng import Mulberry32

SIZE_PRESETS = {
    "small": (8, 8, 42),
    "medium": (12, 12, 7),
    "large": (16, 16, 99),
}


class CarveStep(NamedTuple):
    row: int
    col: int
    from_row: int | None
    from_col: int | None


def recursive_backtrack(rows: int, cols: int, seed: int) -> Tuple[Maze, List[CarveStep]]:
    maze = Maze(rows, cols)
    rng = Mulberry32(seed)
    visited = [[False] * cols for _ in range(rows)]
    steps: List[CarveStep] = []

    def carve(r: int, c: int, fr: int | None, fc: int | None) -> None:
        visited[r][c] = True
        steps.append(CarveStep(r, c, fr, fc))
        neighbors = []
        for dr, dc, self_side, neigh_side in DIRS:
            nr, nc = r + dr, c + dc
            if maze.in_bounds(nr, nc) and not visited[nr][nc]:
                neighbors.append((nr, nc, self_side, neigh_side))
        rng.shuffle(neighbors)
        for nr, nc, self_side, neigh_side in neighbors:
            if not visited[nr][nc]:
                maze.remove_wall(r, c, nr, nc, self_side, neigh_side)
                carve(nr, nc, r, c)

    carve(0, 0, None, None)
    return maze, steps
