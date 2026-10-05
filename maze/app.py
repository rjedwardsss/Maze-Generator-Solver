from __future__ import annotations

import sys

from maze.generate import SIZE_PRESETS, recursive_backtrack
from maze.render import render_maze
from maze.solve import bfs_solve


def ask_choice(prompt: str, n: int) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            choice = int(raw)
            if 1 <= choice <= n:
                return choice
        except ValueError:
            pass
        print("Invalid choice.")


def ask_yes_no(prompt: str) -> bool:
    while True:
        raw = input(prompt).strip().lower()
        if raw.startswith("y"):
            return True
        if raw.startswith("n"):
            return False
        print("Please enter y or n.")


def main() -> None:
    print("Maze Generator + Solver")
    print("Generate with recursive backtracking; solve with BFS.")
    print()

    names = list(SIZE_PRESETS.keys())
    print("Choose a size:")
    for i, name in enumerate(names, 1):
        rows, cols, seed = SIZE_PRESETS[name]
        print(f"  {i}) {name} ({rows}x{cols}, default seed {seed})")
    idx = ask_choice(f"Enter 1-{len(names)}: ", len(names))
    size_name = names[idx - 1]
    rows, cols, default_seed = SIZE_PRESETS[size_name]

    seed_raw = input(f"Seed [{default_seed}]: ").strip()
    seed = int(seed_raw) if seed_raw else default_seed

    maze, carve_steps = recursive_backtrack(rows, cols, seed)
    print(f"\nGenerated {rows}x{cols} maze (seed={seed}, carve steps={len(carve_steps)})")
    print(render_maze(maze))

    if ask_yes_no("\nStep through carve animation? (y/n): "):
        # Show progressive visit marks without rebuilding walls mid-way —
        # carve is complete; we replay visit order on the finished maze.
        visited: set = set()
        for i, step in enumerate(carve_steps, 1):
            visited.add((step.row, step.col))
            print(f"\nCarve step {i}/{len(carve_steps)} — cell ({step.row},{step.col})")
            print(
                render_maze(
                    maze,
                    visited=visited,
                    highlight=(step.row, step.col),
                )
            )
            if i < len(carve_steps):
                input("Press Enter for next step...")

    result = bfs_solve(maze)
    print("\n--- BFS solve ---")
    print(f"Path found: {'yes' if result.found else 'no'}")
    print(f"Cells expanded: {result.expanded_count}")
    if result.found:
        print(f"Path length (edges): {len(result.path) - 1}")

    if ask_yes_no("\nStep through solve visualization? (y/n): "):
        for i, step in enumerate(result.steps, 1):
            show_path = (
                set(result.path)
                if result.found and i == len(result.steps)
                else set()
            )
            print(f"\nSolve step {i}/{len(result.steps)} — expanded {step.expanded}")
            print(
                render_maze(
                    maze,
                    visited=set(step.visited),
                    path=show_path,
                    highlight=step.expanded,
                )
            )
            if i < len(result.steps):
                input("Press Enter for next step...")
    elif result.found:
        print()
        print(render_maze(maze, path=set(result.path)))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        sys.exit(1)
