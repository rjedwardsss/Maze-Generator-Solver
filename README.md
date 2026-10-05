# Maze Generator + Solver

A **Python** console app that **generates** mazes with **recursive backtracking** (DFS carve) and **solves** them with **BFS** (shortest path in an unweighted grid of passages). Stdlib only — no external dependencies.

An interactive **browser demo** (TypeScript / Next.js) is available on the live portfolio site: [rjedwards.dev/projects/maze](https://rjedwards.dev/projects/maze).

## Algorithms

| Phase | Algorithm | Notes |
|-------|-----------|--------|
| **Generate** | Recursive backtracking | Seeded Mulberry32 shuffle of N/E/S/W neighbors |
| **Solve** | BFS | Guarantees shortest path through open walls |

Start is top-left `(0,0)`; exit is bottom-right. Size presets: **small** 8×8, **medium** 12×12, **large** 16×16 (default seeds shared with the portfolio demo).

## Requirements

- Python 3.10+

## Run

From the repository root:

```bash
python -m maze.app
```

Follow the prompts to pick a size, seed, and optional carve/solve step-through.

## Project layout

```
maze/
  model.py      Walls grid + passage helpers
  rng.py        Mulberry32 (parity with TypeScript)
  generate.py   Recursive backtracking
  solve.py      BFS solver
  render.py     ASCII renderer
  app.py        Console UI
```
