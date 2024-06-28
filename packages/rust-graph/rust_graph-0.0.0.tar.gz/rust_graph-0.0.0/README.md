# fast-graph

Graph algorithms implemented in Rust, available as a Python package.

So far, there is only one function implemented: `all_pairs_dijkstra_path_length`.

## Installation

```bash
pip install fast-graph
```

## Usage

```python
from fast_graph import all_pairs_dijkstra_path_length

weighted_edges = [
    (0, 1, 1.0),
    (1, 2, 2.0),
    (2, 3, 3.0),
    (3, 0, 4.0),
    (0, 3, 5.0),
]

shortest_paths = all_pairs_dijkstra_path_length(weighted_edges, cutoff=3.0)
```

```python
>>> shortest_paths
{3: {3: 0.0, 2: 3.0}, 2: {2: 0.0, 1: 2.0, 0: 3.0, 3: 3.0}, 1: {0: 1.0, 2: 2.0, 1: 0.0}, 0: {1: 1.0, 0: 0.0, 2: 3.0}}
```

## Benchmark

