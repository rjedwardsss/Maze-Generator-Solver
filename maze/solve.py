from __future__ import annotations

from collections import deque
from typing import List, NamedTuple, Optional, Set, Tuple

from maze.model import Maze, Pos


class SolveStep(NamedTuple):
    expanded: Pos
    visited: frozenset
    frontier: frozenset


class SolveResult(NamedTuple):
    found: bool
    path: List[Pos]
    steps: List[SolveStep]
    expanded_count: int


def bfs_solve(maze: Maze) -> SolveResult:
    start = maze.start
    goal = maze.end
    queue: deque[Pos] = deque([start])
    visited: Set[Pos] = {start}
    parent: dict[Pos, Optional[Pos]] = {start: None}
    steps: List[SolveStep] = []
    expanded = 0

    while queue:
        current = queue.popleft()
        expanded += 1
        steps.append(
            SolveStep(
                current,
                frozenset(visited),
                frozenset(queue),
            )
        )
        if current == goal:
            path: List[Pos] = []
            cur: Optional[Pos] = goal
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return SolveResult(True, path, steps, expanded)

        for nxt in maze.open_neighbors(*current):
            if nxt in visited:
                continue
            visited.add(nxt)
            parent[nxt] = current
            queue.append(nxt)

    return SolveResult(False, [], steps, expanded)
