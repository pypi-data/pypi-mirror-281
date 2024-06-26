'''
Functions to perfom different operations on pairs of grids. Mainly identify
clusters of nodes on both (`compare`) or create a joinned grid (`join`). It
also contains the necessary functions to achieve this, such as cluster nearest
neighbor pairs (`nearest`), map nodes to nearest cluster pair via shortest
paths (`shortest_path`), or find the clusters with maximum resolution
(`max_res`).
'''
import io

import numpy as np, numpy.lib.recfunctions as npr, scipy.sparse

import dlr.esy.grid.match.powergrid


def nearest(a, b):
    '''
    Computes distances and indices `((d_ab, d_ba), (i_ab, i_ba))` of nearest
    neighbors from `a` and `b`.

    >>> dists, maps = nearest([[0], [1], [2]], [[0], [2]])
    >>> dists
    (array([0., 1., 0.]), array([0., 0.]))
    >>> maps
    (array([0, 0, 1]), array([0, 2]))

    '''

    a, b = [np.asarray(x) for x in (a, b)]
    return tuple(
        zip(*(scipy.spatial.KDTree(x).query(y) for x, y in ((b, a), (a, b))))
    )


def nearest_bus(a_bus, b_bus):
    '''
    Computes distances and indices `((d_ab, d_ba), (i_ab, i_ba))` of nearest
    nodes from `a_bus` and `b_bus`.
    '''
    return nearest(
        np.array([a_bus.x, a_bus.y]).T, np.array([b_bus.x, b_bus.y]).T
    )


def _as_int32_coo_array(a):
    '''
    If necessary, constructs a sparse array from `a` with `int32` indices.
    '''
    if type(a) is not scipy.sparse.coo_array: #pragma: nocover
        raise ValueError(f'Expected a coo_array, but got {type(a).__name__}')

    if a.row.dtype == a.col.dtype == np.int32:
        return a

    return scipy.sparse.coo_array( #pragma: nocover
        (a.data, (a.row.astype(np.int32), a.col.astype(np.int32))),
        shape=a.shape
    )


def shortest_path(ga, map_ab, gb, map_ba):
    '''
    Maps nodes of graphs `ga` and `gb` to clusters from index maps `map_ab` and
    `map_ba`.

    >>> map_ab = [0, 0, 1]
    >>> ga = scipy.sparse.coo_array(([2., 1.], ([0, 1], [1, 2])), shape=(3, 3))
    >>> map_ba = [0, 2]
    >>> gb = scipy.sparse.coo_array(([3.], ([0], [1])), shape=(2, 2))
    >>> a_center, b_center = shortest_path(ga, map_ab, gb, map_ba)
    >>> a_center.tolist(), b_center.tolist()
    ([0, 2, 2], [0, 1])

    '''
    map_ab, map_ba = (np.asarray(x) for x in (map_ab, map_ba))

    # Since scipy 1.11, sparse arrays constructed with int64 indices will no
    # longer automatically downcast to int32. However, dijkstra does not yet
    # support int64 sparse matrices. Force conversion to int32 for the time
    # being.
    ga, gb = (_as_int32_coo_array(x) for x in (ga, gb))

    # Compute shortest paths from all non-cluster nodes to cluster-nodes.
    _, _, s_a = scipy.sparse.csgraph.dijkstra(
        ga, indices=np.where(map_ba[map_ab] == np.arange(len(map_ab)))[0],
        directed=False, min_only=True, return_predecessors=True
    )
    _, _, s_b = scipy.sparse.csgraph.dijkstra(
        gb, indices=np.where(map_ab[map_ba] == np.arange(len(map_ba)))[0],
        directed=False, min_only=True, return_predecessors=True
    )

    return s_a, s_b


def compare(grids):
    '''
    Compares two `grids` and attaches the `cluster` field to both their nodes.
    `grids` is defined as `(a_bus, a_line), (b_bus, b_line)`.

    The records `a_bus` and `b_bus` will be augmented with new fields `center`
    and `map`. `center` points to the cluster center, which is an integer with
    the position of the node identified as the cluster center. `map` maps the
    node to the nearest node of the other grid, respectively.

    >>> from dlr.esy.grid.match.powergrid import load_tables
    >>> grids = load_tables("""
    ... name;x;y | name;bus0;bus1 || name;x;y | name;bus0;bus1
    ... A0;0;0   | A0-1;A0;A1     || B0;0;0   | B0-1;B0;B1
    ... A1;0;2   | A1-2;A1;A2     || B1;2;1   |
    ... A2;2;2   |                ||          |
    ... """)
    >>> (a_bus, a_line), (b_bus, b_line) = compare(grids)
    >>> list(zip(a_bus.name.tolist(), a_bus.center.tolist(), a_bus.map.tolist()))
    [('A0', 0, 0), ('A1', 0, 0), ('A2', 2, 1)]
    >>> list(zip(b_bus.name.tolist(), b_bus.center.tolist(), b_bus.map.tolist()))
    [('B0', 0, 0), ('B1', 1, 2)]

    '''

    (a_bus, a_line), (b_bus, b_line) = grids

    a_graph = dlr.esy.grid.match.powergrid.graph(a_bus, a_line)
    b_graph = dlr.esy.grid.match.powergrid.graph(b_bus, b_line)

    _, (map_ab, map_ba) = nearest_bus(a_bus, b_bus)
    a_center, b_center = shortest_path(a_graph, map_ab, b_graph, map_ba)

    a_bus = npr.rec_append_fields(a_bus, ('center', 'map'), (a_center, map_ab))
    b_bus = npr.rec_append_fields(b_bus, ('center', 'map'), (b_center, map_ba))

    return (a_bus, a_line), (b_bus, b_line)


def max_res(a_bus, b_bus, key='join'):
    '''
    Annotates nodes from `a_bus` and `b_bus` which are suitable for joining in a
    field named `key`.

    For `a_bus`, this field will be `True`, if the nodes cluster is equal or
    larger than its mapped cluster in `b_bus`.

    >>> from dlr.esy.grid.match.powergrid import bus_csv
    >>> a_bus_csv_file = io.StringIO("""
    ... name;x;y;center;map
    ... A0;0;0;0;0
    ... A1;0;1;0;0
    ... A2;3;0;2;3
    ... A3;0;3;3;1
    ... """)
    >>> a_bus = bus_csv(a_bus_csv_file)
    >>> b_bus_csv_file = io.StringIO("""
    ... name;x;y;center;map
    ... B0;0;0;0;0
    ... B1;0;3;1;3
    ... B2;0;2;3;3
    ... B3;3;0;3;2
    ... """)
    >>> b_bus = bus_csv(b_bus_csv_file)
    >>> a_bus, b_bus = max_res(a_bus, b_bus)
    >>> list(zip(a_bus.name.tolist(), a_bus.join.tolist()))
    [('A0', True), ('A1', True), ('A2', False), ('A3', True)]
    >>> list(zip(b_bus.name.tolist(), b_bus.join.tolist()))
    [('B0', False), ('B1', False), ('B2', True), ('B3', True)]
    '''

    a_unique, a_count = np.unique(a_bus.center, return_counts=True)
    b_unique, b_inverse, b_count = np.unique(
        b_bus.center, return_inverse=True, return_counts=True
    )

    a_region = np.zeros(a_bus.size, dtype=bool)
    a_region[a_unique[a_count >= b_count[b_inverse[a_bus.map[a_unique]]]]] = 1

    a_bus = npr.rec_append_fields(
        a_bus, key, a_region[a_bus.center]
    )
    b_bus = npr.rec_append_fields(
        b_bus, key, ~a_region[b_bus.map[b_bus.center]]
    )

    return a_bus, b_bus


def promote_common_field_types(a, b):
    '''
    Promotes common fields of structured data types `a` and `b`.

    Each common field data type gets promoted via `numpy.promote_types`. For
    example:

    >>> promote_common_field_types(
    ...     np.dtype('i4, u4, i4'), np.dtype('f8, i8, U2')
    ... )
    dtype([('f0', '<f8'), ('f1', '<i8'), ('f2', '<U11')])

    Array-scalar types are not supported:

    >>> promote_common_field_types(np.int32, np.int32)
    Traceback (most recent call last):
      ...
    AttributeError: type object 'numpy.int32' has no attribute 'fields'
    '''
    af, bf = a.fields, b.fields
    return np.dtype([
        (name, np.promote_types(af[name][0], bf[name][0]))
        for name in a.fields if name in b.fields
    ])


def concatenate(grids):
    '''
    Concatenate two `grids`, keeping all fields both grids have in common.

    >>> from dlr.esy.grid.match import powergrid
    >>> bus, line = concatenate(powergrid.load_tables("""
    ... name;x;y;a;b | name;bus0;bus1;a;b || name;x;y;a | name;bus0;bus1;a
    ... A0;0;0;0;0   | A0-1;A0;A1;0;0     || B0;0;0;0   | B0-1;B0;B1;0
    ... A1;0;2;1;1   | A1-2;A1;A2;1;1     || B1;2;1;1   | B1-2;B1;B2;1
    ... A2;2;2;2;2   |                    || B2;2;0;1   |
    ... """))

    The concatenated `bus` contains field `a`, but field `b` has been dropped:

    >>> bus.dtype.descr
    [('name', '<U2'), ('x', '<i8'), ('y', '<i8'), ('a', '<i8')]
    >>> bus.name.tolist(), bus.a.tolist()
    (['A0', 'A1', 'A2', 'B0', 'B1', 'B2'], [0, 1, 2, 0, 1, 1])

    Likewise, the concatenated `line` contains field `a`, but no field `b`:

    >>> line.dtype.descr
    [('name', '<U4'), ('bus0', '<U2'), ('bus1', '<U2'), ('a', '<i8')]
    >>> line.bus0.tolist(), line.bus1.tolist(), line.a.tolist()
    (['A0', 'A1', 'B0', 'B1'], ['A1', 'A2', 'B1', 'B2'], [0, 1, 0, 1])

    Bus names must be unique:

    >>> concatenate(powergrid.load_tables("""
    ... name;x;y | name;bus0;bus1 || name;x;y | name;bus0;bus1
    ... A0;0;0   |                || A0;0;0   |
    ... """))
    Traceback (most recent call last):
        ...
    ValueError: Duplicate bus id: A0
    '''
    (a_bus, a_line), (b_bus, b_line) = grids

    # Promote bus dtypes and concatenate.
    bus_dtype = promote_common_field_types(a_bus.dtype, b_bus.dtype)
    bus = np.concatenate([
        npr.require_fields(v, bus_dtype).view(np.recarray)
        for v in (a_bus, b_bus)
    ]).view(np.recarray)

    # Assert bus names are unique.
    unique = np.unique(bus.name)
    if len(unique) < len(bus):
        _, counts = np.unique(bus.name, return_counts=True)
        dups = unique[counts > 1].tolist()
        raise ValueError(f'Duplicate bus id: {", ".join(dups)}')

    # Promote line dtypes and concatenate.
    line_dtype = promote_common_field_types(a_line.dtype, b_line.dtype)
    line = np.concatenate([
        npr.require_fields(v, line_dtype).view(np.recarray)
        for v in (a_line, b_line)
    ]).view(np.recarray)

    return bus, line


def join_by(grids, key='join'):
    '''
    Joins two `grids` via the field `key`.

    >>> from dlr.esy.grid.match import powergrid, visualize
    >>> a, b = powergrid.load_tables("""
    ... name;x;y;join | name;bus0;bus1 || name;x;y;join | name;bus0;bus1
    ... A0;0;0;1      | A0-1;A0;A1     || B0;0;0;0      | B0-1;B0;B1
    ... A1;0;2;1      | A1-2;A1;A2     || B1;2;1;1      | B1-2;B1;B2
    ... A2;2;2;0      |                || B2;2;0;1      |
    ... """)
    >>> visualize.plot(
    ...     visualize.grids((('a', a), ('b', b))), size=(6, 2),
    ...     save='figures/test/cluster-join-grids.svg'
    ... )

    ![](../../../../figures/test/cluster-join-grids.svg)

    >>> c = (bus, line) = join_by((a, b))
    >>> bus.name.tolist()
    ['A0', 'A1', 'B1', 'B2']
    >>> list(zip(line.bus0.tolist(), line.bus1.tolist()))
    [('A0', 'A1'), ('B1', 'B2'), ('A1', 'B1')]
    >>> visualize.plot(
    ...     visualize.grids((('c', c),)), size=(6, 2),
    ...     save='figures/test/cluster-join.svg'
    ... )

    ![](../../../../figures/test/cluster-join.svg)

    Only fields common to both grids are joined and their data types are
    promoted, see `promote_common_field_types` for details. For example, bus
    field `name` gets promoted to a 3-character string and field `f` to a
    `float64`, while fields `a` and `b` get dropped. The line field `s` gets
    promoted to a 32-character string:

    >>> bus, line = join_by(powergrid.load_tables("""
    ... name;x;y;k;f;a | name;bus0;bus1;s || name;x;y;k;f;b | name;bus0;bus1;s
    ... A0;0;0;1;1;0   | L0;A0;A0;1.234   || B00;0;0;1;1.;1 | L0;B00;B00;x
    ... """), key='k')
    >>> bus.dtype.descr
    [('name', '<U3'), ('x', '<i8'), ('y', '<i8'), ('k', '<i8'), ('f', '<f8')]
    >>> line.dtype.descr
    [('name', '<U2'), ('bus0', '<U3'), ('bus1', '<U3'), ('s', '<U32')]

    Bus names must be unique:

    >>> join_by(powergrid.load_tables("""
    ... name;x;y | name;bus0;bus1 || name;x;y | name;bus0;bus1
    ... A0;0;0   |                || A0;0;0   |
    ... """))
    Traceback (most recent call last):
        ...
    ValueError: Duplicate bus id: A0
    '''

    (a_bus, a_line), (b_bus, b_line) = grids

    # Promote bus and line dtypes.
    bus_dtype = promote_common_field_types(a_bus.dtype, b_bus.dtype)
    a_bus, b_bus = (
        npr.require_fields(v, bus_dtype).view(np.recarray)
        for v in (a_bus, b_bus)
    )
    line_dtype = promote_common_field_types(a_line.dtype, b_line.dtype)
    a_line, b_line = (
        npr.require_fields(v, line_dtype).view(np.recarray)
        for v in (a_line, b_line)
    )

    unique = np.unique(np.concatenate([a_bus.name, b_bus.name]))
    if len(unique) < len(a_bus) + len(b_bus):
        _, counts = np.unique(
            np.concatenate([a_bus.name, b_bus.name]), return_counts=True
        )
        dups = unique[counts > 1].tolist()
        raise ValueError(f'Duplicate bus id: {", ".join(dups)}')

    # Convert key fields to boolean.
    a_key, b_key = a_bus[key].astype(bool), b_bus[key].astype(bool)
    a_idx, b_idx = [dlr.esy.grid.match.powergrid.line_index(b, l) for b, l in grids]

    # Construct the new node array by concatenating the join nodes from both
    # grids.
    a_join_bus, b_join_bus = a_bus[a_key], b_bus[b_key]
    bus = np.concatenate([a_join_bus, b_join_bus])

    # Likewise, start constructing join lines.
    if len(a_line) > 0:
        a_join_line = a_line[a_key[a_idx[0]] & a_key[a_idx[1]]]
        b_join_line = b_line[b_key[b_idx[0]] & b_key[b_idx[1]]]
        line = np.concatenate([a_join_line, b_join_line])

        # Identify crossing lines and connect endpoints from grid `a` of those
        # lines to nearest to endpoints from grid `b`.
        for i_src, i_dst, b_dst in ((0, 1, 'bus1'), (1, 0, 'bus0')):
            # Select lines with its source endpoint referencing a `a` node and
            # its target endpoint referencing a `b` node. Find nearest outside
            # node to inside nodes of these lines.
            i = a_key[a_idx[i_src]] & ~a_key[a_idx[i_dst]]
            _, (map_i, _) = nearest_bus(a_bus[a_idx[i_src][i]], b_join_bus)

            # Copy line entries and update references to outside node.
            line_i = np.copy(a_line[i]).view(np.recarray)
            line_i[b_dst] = b_join_bus[map_i].name
            line = np.concatenate([line, line_i])
    else:
        line = np.array([], dtype=line_dtype) #pragma: nocover

    return bus.view(np.recarray), line.view(np.recarray)


def first(data):
    '''
    Picks the first element of `data`.
    '''
    return data[0]


def aggregate_fields(map, **fields):
    '''
    Aggregates `fields` by applying a function to argument groups using `map`.

    Each of `fields` is a tuple `(func, *args)`, where `func` is applied to
    subset of `args`. The subset of each of `args` are selected via unique
    values of `map`.

    If no `args` are given, `func` is applied to the group mapping itself (which
    for example allows to sum the groups size using `numpy.sum`):

    >>> x = np.core.records.fromarrays(
    ...     (['a', 'b', 'c'], [1, 2, 3]), names=('name', 'value')
    ... )
    >>> result = aggregate_fields(
    ...     [0, 0, 2], name=(first, x.name), mean_value=(np.mean, x.value),
    ...     size=(np.sum,)
    ... )
    >>> tuple(result)
    ('name', 'mean_value', 'size')
    >>> result['name'], result['mean_value'], result['size']
    (array(['a', 'c'], dtype='<U1'), array([1.5, 3. ]), array([2, 1]))

    '''
    data = [
        [
            func(*(a[f] for a in args)) if args else func(f)
            for (func, *args) in fields.values()
        ]
        for f in (i == map for i in np.unique(map) if i >= 0)
    ]
    return dict(zip(fields, (np.array(group) for group in zip(*data))))


def aggregate(
    grid, key='center', bus_fields=None, line_fields=None,
    drop_intra_lines=True
):
    '''
    Aggregates buses and lines of `grid` by a bus field named `key`.

    By default, only the bus fields `name`, `x` and `y` and the line fields
    `bus0` and `bus1` are aggregated and intra cluster lines are dropped.

    Additional fields from buses and lines can be aggregated via `bus_fields`
    and `line_fields`, respectively. The values of these dictionaries are tuples
    `(func, ...args)` where `func` is called to aggregate the clusters subsets
    of each `args` (see `aggregate_fields` for details):

    >>> from dlr.esy.grid.match import powergrid, visualize
    >>> (bus, line), = powergrid.load_tables("""
    ... name;x;y;center;area | name;bus0;bus1;capacity
    ... A0;0;0;0;1           | A0-1;A0;A1;1
    ... A1;0;2;0;2           | A1-0;A1;A0;1
    ... A2;2;2;2;3           | A1-2;A1;A2;3
    ...                      | A0-2;A0;A2;2
    ... """)
    >>> abus, aline = aggregate(
    ...     (bus, line),
    ...     bus_fields=dict(area=(np.sum, bus.area)),
    ...     line_fields=dict(min_cap=(np.min, line.capacity), count=(np.sum,)),
    ... )
    >>> abus.dtype.names, abus.tolist()
    (('name', 'x', 'y', 'area'), [('A0', 0, 0, 3), ('A2', 2, 2, 3)])
    >>> aline.dtype.names, aline.tolist()
    (('bus0', 'bus1', 'min_cap', 'count'), [('A0', 'A2', 2, 2)])

    Furthermore, intra cluster lines can be mapped to a loop:

    >>> abus, aline = aggregate((bus, line), drop_intra_lines=False)
    >>> abus.dtype.names, abus.tolist()
    (('name', 'x', 'y'), [('A0', 0, 0), ('A2', 2, 2)])
    >>> aline.dtype.names, aline.tolist()
    (('bus0', 'bus1'), [('A0', 'A0'), ('A0', 'A2')])
    '''

    bus, line = grid
        
    bus_key = bus[key]
    idx = dlr.esy.grid.match.powergrid.line_index(bus, line)
    line = np.array([bus[bus_key[i]].name for i in idx])

    unique_bus, unique_bus_inverse = np.unique(bus_key, return_inverse=True)
    unique_line, unique_line_index, unique_line_inverse = np.unique(
        # Ensure line[0] < line[1] to aggregate loop.
        np.take_along_axis(line, np.argsort(line, axis=0), axis=0),
        axis=1, return_index=True, return_inverse=True
    )

    if unique_line_inverse.ndim == 2:
        # Since numpy 2, inverse of unique maintains input dimensions.
        unique_line_inverse = unique_line_inverse.squeeze()

    if drop_intra_lines:
        unique_line_inverse[line[0] == line[1]] = -1

    bus_defaults = dict(
        name=(first, bus.name[bus_key]),
        x=(first, bus.x[bus_key]), y=(first, bus.y[bus_key]),
    )
    bus_fields = {**bus_defaults, **(bus_fields if bus_fields else {})}
    bus_cluster = np.core.records.fromarrays(
        aggregate_fields(unique_bus_inverse, **bus_fields).values(),
        names=tuple(bus_fields)
    )

    line_defaults = dict(bus0=(first, line[0]), bus1=(first, line[1]))
    line_fields = {**line_defaults, **(line_fields if line_fields else {})}

    line_cluster = np.core.records.fromarrays(
        aggregate_fields(unique_line_inverse, **line_fields).values(),
        names=tuple(line_fields)
    )

    return bus_cluster, line_cluster
