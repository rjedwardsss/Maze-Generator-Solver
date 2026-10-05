from __future__ import annotations

from typing import Iterable, Optional, Set

from maze.model import Maze, Pos


def render_maze(
    maze: Maze,
    *,
    visited: Optional[Set[Pos]] = None,
    path: Optional[Set[Pos]] = None,
    highlight: Optional[Pos] = None,
) -> str:
    """ASCII wall maze. S = start, E = end, * = path, . = visited, @ = highlight."""
    visited = visited or set()
    path = path or set()
    lines: list[str] = []

    # Top border
    top = "+"
    for c in range(maze.cols):
        top += "---+" if maze.cells[0][c].n else "   +"
    lines.append(top)

    for r in range(maze.rows):
        row_mid = "|"
        row_bot = "+"
        for c in range(maze.cols):
            pos = (r, c)
            if pos == maze.start:
                ch = "S"
            elif pos == maze.end:
                ch = "E"
            elif highlight is not None and pos == highlight:
                ch = "@"
            elif pos in path:
                ch = "*"
            elif pos in visited:
                ch = "."
            else:
                ch = " "
            row_mid += f" {ch} "
            row_mid += " " if not maze.cells[r][c].e else "|"
            row_bot += "   +" if not maze.cells[r][c].s else "---+"
        lines.append(row_mid)
        lines.append(row_bot)

    return "\n".join(lines)
