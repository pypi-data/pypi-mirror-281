r'''
![](https://gitlab.com/dlr-ve/esy/dlr.esy.grid.match/badges/main/pipeline.svg?key_text=tests)
![](https://gitlab.com/dlr-ve/esy/dlr.esy.grid.match/badges/main/coverage.svg)

`dlr.esy.grid.match` is a grid matching & conversion tool primarily developed
for the comparison of power grids.

# Installation

`dlr.esy.grid.match` is available on [PyPI](https://pypi.org/) and can be
installed into your Python environment via `pip`:

```bash
pip install dlr.esy.grid.match
```

# Command-line interface

`dlr.esy.grid.match` provides a command-line interface (see
`dlr.esy.grid.match.cli` for more details):

```console
$ dlr.esy.grid.match --help
usage: dlr.esy.grid.match [-h] {compare,example} ...
...
Command-line interface for grid comparisons.
...
positional arguments:
  {compare,example}
    compare          Compares two powergrids. `a` and `b` are expected to be
                     directories, each containing the files `bus.csv` and
                     `line.csv`.
    example          Creates an example datasets.
...

```

## Usage

The command `compare` adds the columns `center` and `map` to the grids $a$ and
$b$. The column `center` contains the index of the center of the cluster each
node belongs to and the column `map` the index of the center of the
corresponding cluster in the other grid. See the methodology section for 
details. The subcommand `grids` plots the two grids together and the 
subcommand `plot` shows or saves the plots.

The subcommand `example` can be used to create example datasets and write them
into a directory, like the `simple` dataset:

```console
$ dlr.esy.grid.match example simple example/simple
$ dlr.esy.grid.match compare --a=example/simple/a --b=example/simple/b grid plot --save=figures/grids.svg
```

![](../../../../../figures/grids.svg)

The subcommand `cluster` plots the grids separately highlighting the convex
hulls of each cluster (in orange for the hulls in the plotted grid and in grey
for the ones in the other grid). The centers and the intercluster lines are
plotted in red and the intracluster lines and the rest of the nodes are
plotted in orange.

```console
$ dlr.esy.grid.match compare --a=example/simple/a --b=example/simple/b cluster plot --save=figures/cluster.svg
```

![](../../../../../figures/cluster.svg)

The subcommand `join` produces a third grid with the nodes in gird $a$ which
are in the interior of a region and the nodes in grid $b$ which are outside of
a region. The information about the regions needs to be in a column called
`join` in each grid (0 meaning inside the region and 1 meaning outside).
If the column `join` is missing, it can be added to each grid with the
subcommand `max_res`, as described in the methodology section.

```console
$ dlr.esy.grid.match compare --a=example/simple/a --b=example/simple/b max_res join grid plot --save=figures/join.svg
```

![](../../../../../figures/join.svg)

## Input and output

`dlr.esy.grid.match` supports reading and writing grid data from CSV files. Grid
data may also be converted to geojson data.

`dlr.esy.grid.match` requires `bus` data to contain at least the fields `name`, `x`
and `y`, while `line` data is required to contain at least the fields `name`,
`bus0` and `bus1`.

Input field names can be renamed as in the following example, which reads grid
data from a non-conformative example in the directory `example/nonconformative`
and stores the resulting grid in `example/conformative`:

```console
$ dlr.esy.grid.match example nonconformative example/nonconformative
$ dlr.esy.grid.match compare --a=example/nonconformative/a --a_bus_fields=bus:name --a_line_fields=line:name --b=example/nonconformative/b --b_bus_fields=bus:name --b_line_fields=line:name csv example/conformative
```

The command `geojson` produces a geojson output, which can be used to visualize
the grids with the clusters, for instance by importing it to
[https://geojson.io/](https://geojson.io/).

```console
$ dlr.esy.grid.match compare --a=example/simple/a --b=example/simple/b geojson
{"type": "FeatureCollection", ...}
```

# Methodology

## Comparison methodology

Given two grids $a$ and $b$ with geolocated nodes, clusters of nodes in
each grid are produced and each cluster in $a$ is uniquely identified to
a cluster in $b$. The method has the following steps:

1. For each node $n_a$ in $a$, define $f(n_a)$ to be its closest node in $b$
   (using the Euclidean distance) and, for each node $n_b$ in $b$, define 
   $g(n_b)$ to be its closest node in $a$.

2. Each node $n_a$ in $a$ such that $g(f(n_a))=n_a$ is chosen as center
   of a cluster in $a$ and each node $n_b$ in $b$ such that
   $f(g(n_b))=n_b$ is chosen as center of a cluster in $b$. Notice
   that, by construction, each grid has the same number of clusters and
   there is a one to one correspondence between them. Namely, the center $n_a$
   is associated to the center $n_b = f(n_a)$ and the center $n_b$ is 
   associated to $n_a = g(n_b)$.

3. Each node in $a$ not being a center of any cluster is assigned
   to a cluster using the shortest path (using Euclidean distance) to a
   center. The same is done for $b$.

The output associates to each node the center of its cluster and also the
corresponding center in the other grid. This can be used to compare and
transfer the data associated to the nodes in both grids. It can also be used to
create a third grid with the highest spatial resolution of both, as explained
in the next section.

## Joining methodology

Given two grids $a$ and $b$ in which all nodes are geolocated and assigned to
one of two regions $\Gamma$ or $\Omega$, a new grid is produced having the
nodes of $a$ which belong to $\Gamma$ and the nodes of $b$ which belong
to $\Omega$. The lines of the joined grid are the ones in the three following
groups:

- Lines in $a$ connecting two nodes belonging to $\Gamma$;

- Lines in $b$ connecting two nodes belonging to $\Omega$; and

- for each line in $a$ connecting a node $n_a$ in $\Gamma$ to a node $m_a$ in
$\Omega$ a line connecting $n_a$ to the closest 
node (using Euclidean distance) in $b$ which belongs to $\Omega$.

To get the joined grid with the maximal resolution, the output of the comparison
methodology is used, where a node in $a$ is assigned to $\Gamma$ if it belongs
to a cluster with more or equal number of elements than its corresponding
cluster in $b$.

# Design, Development & Contributing

Design and development notes are available in `dlr.esy.grid.match.test`.

We would be happy to accept contributions via merge requests, but due to
corporate policy we can only accept contributions if you have send us the signed
[contributor license agreement](https://gitlab.com/dlr-ve/esy/dlr.esy.grid.match/-/blob/main/CLA.md).

# License

`dlr.esy.grid.match` is licensed under the [MIT](https://mit-license.org/)
license.

# Contact

Please use the projects issue tracker to get in touch.

# Team

`dlr.esy.grid.match` is developed cooperatively by the
[DLR](https://www.dlr.de/EN/Home/home_node.html) Institute of
[Networked Energy Systems](https://www.dlr.de/ve/en/desktopdefault.aspx/tabid-12472/21440_read-49440/)
in the departement for
[Energy Systems Analysis (ESY)](https://www.dlr.de/ve/en/desktopdefault.aspx/tabid-12471/21741_read-49802/) and
by the
[Institute of Energy and Climate Research](https://www.fz-juelich.de/en/iek) -
[Techno-economic System Analysis (IEK-3)](https://www.fz-juelich.de/en/iek/iek-3)
of the [Forschungszentrum Jülich](https://www.fz-juelich.de/en).

# Footnotes

Test console examples.

```python
>>> import dlr.esy.grid.match.test
>>> dlr.esy.grid.match.test.doctest_console(__doc__)

```
'''

__all__ = ['powergrid', 'cluster', 'visualize', 'geojson', 'cli', 'test']
