'''
Functions to plot the grids.
'''

import pathlib

import numpy as np, scipy.sparse, scipy.spatial
import matplotlib.collections, matplotlib.patches, matplotlib.pyplot

import dlr.esy.grid.match.powergrid


def graph_patch(coord, graph, linecolor=None, linewidth=None, linestyle=None):
    '''
    Renders `graph` with nodes at `coord` into a
    `matplotlib.collections.PatchCollection`.

    >>> coord = np.array([[0, 0], [0.5, 3 ** 0.5 * 0.5], [1, 0]])
    >>> graph = scipy.sparse.coo_array(
    ...     ([1, 1, 1], ([0, 1, 2], [1, 2, 0])), shape=(3, 3)
    ... )
    >>> plot(
    ...     graph_patch(coord, graph, linecolor=('r', 'g', 'b'), linewidth=2),
    ...     size=(6, 2), save='figures/test/graph_patch.svg'
    ... )

    ![](../../../../figures/test/graph_patch.svg)
    '''
    coords = np.asarray(coord)

    if type(linecolor) not in (list, tuple):
        linecolor = (linecolor,) * graph.row.size
    if type(linewidth) not in (list, tuple):
        linewidth = (linewidth,) * graph.row.size
    if type(linestyle) not in (list, tuple):
        linestyle = (linestyle,) * graph.row.size

    if len(linecolor) != graph.row.size:
        raise ValueError('Mismatching linecolor') #pragma: nocover
    if len(linewidth) != graph.row.size:
        raise ValueError('Mismatching linewidth') #pragma: nocover
    if len(linestyle) != graph.row.size:
        raise ValueError('Mismatching linestyle') #pragma: nocover
        
    codes = np.array([matplotlib.path.Path.MOVETO, matplotlib.path.Path.LINETO])
    return matplotlib.collections.PatchCollection(
        [
            matplotlib.patches.PathPatch(
                matplotlib.path.Path(vertices, codes, closed=False),
                edgecolor=linecolor[i], linewidth=linewidth[i],
                linestyle=linestyle[i],
            )
            for i, vertices in enumerate(
                    coord[np.array([graph.row, graph.col]).T]
            )
        ],
        match_original=True
    )


def edge_index(graph, index):
    '''
    Applies `index` to the edges of `graph`.

    >>> a = scipy.sparse.coo_array(
    ...     ([1, 2, 3, 4], ([0, 1, 2, 3], [3, 2, 1, 0])), shape=(4, 4)
    ... )
    >>> b = edge_index(a, [0, 2])
    >>> b.data.tolist(), b.row.tolist(), b.col.tolist()
    ([1, 3], [0, 2], [3, 1])
    '''
    return scipy.sparse.coo_array(
        (graph.data[index], (graph.row[index], graph.col[index])),
        shape=graph.shape
    )


def cluster_hulls(bus):
    '''Generates convex hulls of `bus` clusters.'''
    xy = np.stack([bus.x, bus.y], axis=-1)

    centers = np.unique(bus.center)
    for center in np.unique(bus.center):
        cluster = bus.center == center
        if np.sum(cluster) > 2:
            hull = scipy.spatial.ConvexHull(xy[cluster])
            yield center, hull.points[hull.vertices]
        else:
            yield center, xy[cluster]


def draw_grid(
    ax, grid, buscolor='orange', bussize=None, linecolor=None,
    linestyle='-', linewidth=2, label=None
):
    '''
    Draws `grid` onto the axes `ax`.

    Buses can be styled with `buscolor` and `bussize`, while lines can be styled
    with `linecolor`, `linestyle` and `linewidth`.
    '''
    bus, line = grid

    xy = np.stack([bus.x, bus.y], axis=-1)
    g = dlr.esy.grid.match.powergrid.graph(bus, line)

    ax.scatter(*xy.T, s=bussize, c=buscolor, label=label)
    ax.add_collection(graph_patch(
        xy, g, linecolor=linecolor if linecolor is not None else buscolor,
        linestyle=linestyle, linewidth=linewidth,
    ))


def draw_cluster(
    ax, grid, inter_color='red', intra_color='orange', s=None,
    linestyle='-', linewidth=2
):
    '''
    Draws `grid` onto the axes `ax`.

    Buses that are a cluster center and the intercluster lines are drawn in
    `inter_color`, while the remaining buses and the intracluster lines are
    drawn in `intra_color`.
    '''
    bus, line = grid

    idx = dlr.esy.grid.match.powergrid.line_index(bus, line)
    inter_cluster = bus.center[idx[0]] != bus.center[idx[1]]
    intra_cluster = bus.center[idx[0]] == bus.center[idx[1]]

    xy = np.stack([bus.x, bus.y], axis=-1)
    g = dlr.esy.grid.match.powergrid.graph(bus, line)

    ax.scatter(*xy.T, s=s, color=intra_color)
    ax.scatter(*xy[bus.center == np.arange(len(bus))].T, s=s, color=inter_color)
    ax.add_collection(graph_patch(
        xy, edge_index(g, inter_cluster), linecolor=inter_color,
        linestyle=linestyle, linewidth=linewidth
    ))
    ax.add_collection(graph_patch(
        xy, edge_index(g, intra_cluster), linecolor=intra_color,
        linestyle=linestyle, linewidth=linewidth
    ))


def draw_cluster_hulls(ax, bus, **options):
    '''
    Draws the convex hulls of `bus` clusters onto the axes `ax`. `options` are
    used to specify properties of the hulls polygon.
    '''
    for center, hull in cluster_hulls(bus):
        ax.add_artist(matplotlib.patches.Polygon(hull, **options))


def grids(grids, options=None):
    '''
    Visualizes `grids` in a figure. `grids` is defined as a tuple of named grid
    entries, like `((a_name, (a_bus, a_line)), (b_name, (b_bus, b_line)), ...)`.

    A dictionary or a list of dictionaries can be used as visualization
    `options` for each grid (if `options` is a dictionary, it will be used for
    all grids). See `draw_grid` for available options.
    '''
    fig, ax = matplotlib.pyplot.subplots(layout='constrained')
    if options is None:
        options = {}
    if type(options) is dict:
        options = (options,) * len(grids)
    if len(options) != len(grids):
        raise ValueError('Expected options for each grid') #pragma: nocover
    for i, ((name, grid), option) in enumerate(zip(grids, options)):
        draw_grid(
            ax, grid, label=name,
            buscolor=option.get('buscolor', f'C{i}'),
            bussize=option.get('bussize', None),
            linecolor=option.get('linecolor', None),
            linestyle=option.get('linestyle', '-'),
            linewidth=option.get('linewidth', 2),
        )
    ax.set(aspect='equal')
    ax.legend()
    return fig


def cluster(grids, options=None):
    '''
    Visualizes clusters of `grids` in a figure. `grids` is defined as a tuple of
    named grids, for example `((a_name, (a_bus, a_line)), (b_name, (b_bus,
    b_line)), ...)`.

    Visualization can be customized using `options`, a list of dictionaries with
    options for each grid. If `options` is a dictionary, it will be used for all
    grids.
    '''

    fig, axes = matplotlib.pyplot.subplots(
        1, len(grids), sharex=True, sharey=True, layout='constrained'
    )
    if options is None:
        options = {}
    if type(options) is dict:
        options = (options,) * len(grids)
    if len(options) != len(grids):
        raise ValueError('Expected options for each grid') #pragma: nocover

    for ax, (name, grid), option in zip(axes, grids, options):
        ax.set(title=name, aspect='equal')
        for _, other_grid in grids:
            if other_grid is grid: continue
            other_bus, _ = other_grid
            draw_cluster_hulls(
                ax, other_bus, alpha=option.get('alpha', 0.25),
                facecolor=option.get('otherclustercolor', 'gray'),
            )
        bus, _ = grid
        draw_cluster_hulls(
            ax, bus, alpha=option.get('alpha', 0.25),
            facecolor=option.get('clustercolor', 'orange'),
        )
        draw_cluster(
            ax, grid, inter_color=option.get('inter_color', 'red'),
            intra_color=option.get('intra_color', 'orange'),
            s=option.get('s', None), linestyle=option.get('linestyle', '-'),
            linewidth=option.get('linewidth', 2),
        )
    return fig


def plot(item, save=None, size=None):
    '''
    Renders `item` and write to a file `save`, display if `save` is None.

    `item` may be a `matplotlib.figure.Figure` or `matplotlib.artist.Artist`
    instance.

    `size` can be used to optionally resize the figure.
    '''

    if type(item) is not matplotlib.figure.Figure:
        if isinstance(item, matplotlib.artist.Artist):
            figure, ax = matplotlib.pyplot.subplots()
            ax.add_artist(item)
        else:
            raise ValueError(f'Unsupported {item=}') #pragma: nocover
    else:
        figure = item

    if size:
        figure.set_size_inches(size)

    if not save:
        matplotlib.pyplot.show() #pragma: nocover
    else:
        save = pathlib.Path(save)
        save.parent.mkdir(exist_ok=True)
        figure.savefig(save, bbox_inches='tight')
