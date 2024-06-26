'''
Functions to load powergrid nodes and lines from csv files (`grid_csv`) and
converts them to coordinates and a graph (`graph`).
'''

import io

import numpy as np, numpy.lib.recfunctions as npr, scipy.sparse


def bus_csv(csv_file, fieldmap=None, delimiter=';', encoding='utf8'):
    '''
    Loads `bus` records from the `csv_file`. The `csv_file` is expected to use
    `delimiter` to separate fields and to be stored in the given `encoding`.

    The `csv_file` file must at least include the fields `name`, `x` and `y`.

    >>> bus = bus_csv(io.StringIO("""
    ... name;x;y
    ... b1;0;0
    ... b2;1;0
    ... """))
    >>> bus
    rec.array([('b1', 0, 0), ('b2', 1, 0)],
              dtype=[('name', '<U2'), ('x', '<i8'), ('y', '<i8')])

    While missing fields cause errors, additional fields are supported.

    >>> bus_csv(io.StringIO('spam'))
    Traceback (most recent call last):
    ...
    ValueError: Missing required bus fields: ['name', 'x', 'y']
    >>> bus = bus_csv(io.StringIO('name;x;y;spam'))
    >>> bus.dtype.names
    ('name', 'x', 'y', 'spam')

    Names of fields can be remapped using `fieldmap`:

    >>> bus = bus_csv(
    ...     io.StringIO('a;b;c'), fieldmap={'a': 'name', 'b': 'x', 'c': 'y'}
    ... )
    >>> bus.dtype.names
    ('name', 'x', 'y')

    '''
    bus = np.genfromtxt(
        csv_file, names=True, delimiter=delimiter, dtype=None,
        encoding=encoding, ndmin=1, autostrip=True
    )

    if fieldmap:
        bus = npr.rename_fields(bus, fieldmap)

    missing = {'name', 'x', 'y'} - set(bus.dtype.names)
    if missing:
        raise ValueError(f'Missing required bus fields: {sorted(missing)}')

    # View buses as recarray.
    return bus.view(np.recarray)


def line_csv(csv_file, fieldmap=None, delimiter=';', encoding='utf8'):
    '''
    Loads `line` records from the `csv_file`. The `csv_file` is expected to use
    `delimiter` to separate fields and to be stored in the given `encoding`.

    The `csv_file` must at least include the fields `name`, `bus0` and `bus1`.

    >>> line = line_csv(io.StringIO("""
    ... name;bus0;bus1
    ... l0;b0;b1
    ... l1;b1;b2
    ... """))
    >>> line #doctest: +NORMALIZE_WHITESPACE
    rec.array([('l0', 'b0', 'b1'), ('l1', 'b1', 'b2')],
              dtype=[('name', '<U2'), ('bus0', '<U2'), ('bus1', '<U2')])

    While missing fields cause errors, additional fields are supported:

    >>> line_csv(io.StringIO('spam'))
    Traceback (most recent call last):
    ...
    ValueError: Missing required line fields: ['bus0', 'bus1', 'name']
    >>> line = line_csv(io.StringIO('name;bus0;bus1;spam'))
    >>> line.dtype.names
    ('name', 'bus0', 'bus1', 'spam')

    Names of fields can be remapped using `fieldmap`:

    >>> line = line_csv(
    ...     io.StringIO('a;b;c'),
    ...     fieldmap={'a': 'name', 'b': 'bus0', 'c': 'bus1'}
    ... )
    >>> line.dtype.names
    ('name', 'bus0', 'bus1')

    '''
    line = np.genfromtxt(
        csv_file, names=True, delimiter=delimiter, dtype=None,
        encoding=encoding, ndmin=1,
    )

    if fieldmap:
        line = npr.rename_fields(line, fieldmap)

    missing = {'name', 'bus0', 'bus1'} - set(line.dtype.names)
    if missing:
        raise ValueError(f'Missing required line fields: {sorted(missing)}')

    # View lines as recarray.
    return line.view(np.recarray)


def grid_csv(
    bus_csv_file, line_csv_file, delimiter=';', encoding='utf8',
    bus_fieldmap=None, line_fieldmap=None
):
    '''
    Loads `(bus, line)` records from `bus_csv_file` and `line_csv_file` files and
    maps lines to buses. The csv files are expected to use `delimiter` to
    separate fields and to be stored in `encoding`.

    See `bus_csv` and `line_csv` for required fields.

    >>> bus_csv_file = io.StringIO("""
    ... name;x;y
    ... b0;0;0
    ... b1;1;0
    ... b2;2;0
    ... """)
    >>> line_csv_file = io.StringIO("""
    ... name;bus0;bus1
    ... l0;b0;b1
    ... l1;b1;b2
    ... """)
    >>> bus, line = grid_csv(bus_csv_file, line_csv_file)
    >>> np.stack([line.name, line.bus0, line.bus1], axis=-1)
    array([['l0', 'b0', 'b1'],
           ['l1', 'b1', 'b2']], dtype='<U2')

    Line bus fields `bus0` and `bus1` are validated:

    >>> bus_csv_file = io.StringIO("""
    ... name;x;y
    ... b0;0;0
    ... """)
    >>> line_csv_file = io.StringIO("""
    ... name;bus0;bus1
    ... l0;b0;b1
    ... """)
    >>> grid_csv(bus_csv_file, line_csv_file)
    Traceback (most recent call last):
        ...
    ValueError: b1 not found

    '''
    bus = bus_csv(
        bus_csv_file, fieldmap=bus_fieldmap, delimiter=delimiter,
        encoding=encoding,
    )
    line = line_csv(
        line_csv_file, fieldmap=line_fieldmap, delimiter=delimiter,
        encoding=encoding,
    )

    # Validate lines.
    line_index(bus, line)

    return bus, line


def recarray_csv(a, delimiter=';'):
    '''
    Converts the record array `a` to CSV with the given `delimiter`.

    >>> print(recarray_csv(np.array(
    ...     [('a', 0), ('b', 1)], dtype=[('key', 'U1'), ('value', 'i')]
    ... )))
    key;value
    a;0
    b;1

    '''
    return '\n'.join([
        ';'.join(a.dtype.names),
        *(';'.join(str(x) for x in entry) for entry in a)
    ])


def parse_tables(text):
    '''
    Parses the `text` into a list of lists that can be used as tables.
    '''
    tables = list(zip(*(
        line.split('||') for line in text.split('\n') if line.strip()
    )))
    grid_datasets = list(
        list(zip(*([c.strip() for c in row.split('|')] for row in table)))
        for table in tables
    )
    return [
        ['\n'.join(dataset) for dataset in datasets]
        for datasets in grid_datasets
    ]


def load_tables(text):
    '''
    Loads tables after parsing the `text`.
    '''
    return [
        grid_csv(*(io.StringIO(dataset) for dataset in datasets))
        for datasets in parse_tables(text)
    ]


def index(a, v, sorter=True):
    '''
    Computes the `index` of values `v` in `a`. `a` is sorted using the indice of
    `sorter`, the indice are automatically computed if `sorted` is `True`.

    >>> index([1, 2, 0], [0, 1, 2]).tolist()
    [2, 0, 1]

    Non-existing elements results in a `ValueError`:

    >>> index([1, 2, 0], [-1, 1, 3])
    Traceback (most recent call last):
        ...
    ValueError: -1, 3 not found

    '''
    a, v = np.asarray(a), np.asarray(v)

    if len(v) == 0:
        return np.zeros(0)

    # Construct sorter if necessary.
    sorter = np.argsort(a) if sorter is True else sorter
    index = np.searchsorted(a, v, sorter=sorter).astype(np.int32)


    # Set unmatched entries to index 0.
    valid = index < len(a)
    index[~valid] = 0

    if sorter is not None:
        # Remap index to base order.
        index[valid] = sorter[index[valid]]

    # Validate.
    invalid = a[index] != v
    if np.any(invalid):
        raise ValueError(f'{", ".join(map(str, v[invalid]))} not found')
    return index


def line_index(bus, line):
    '''
    Returns the index of the lines.
    '''
    return index(bus.name, line.bus0), index(bus.name, line.bus1)


def graph(bus, line):
    '''
    Constructs a `graph` from `bus` and `line` arrays. The weights of
    `graph` are the euclidean distances between the buses `line['bus0']` and
    `line['bus1']`.

    >>> bus_csv_file = io.StringIO("""
    ... name;x;y
    ... b1;0;0
    ... b2;1;0
    ... b0;0;1
    ... """.strip())
    >>> line_csv_file = io.StringIO("""
    ... name;bus0;bus1
    ... l0;b0;b1
    ... l1;b1;b2
    ... l2;b2;b0
    ... """.strip())
    >>> bus, line = grid_csv(bus_csv_file, line_csv_file)
    >>> g = graph(bus, line)
    >>> g.data.tolist(), g.row.tolist(), g.col.tolist()
    ([1.0, 1.0, 1.4142135623730951], [2, 0, 1], [0, 1, 2])
    >>> g.todense()
    array([[0.        , 1.        , 0.        ],
           [0.        , 0.        , 1.41421356],
           [1.        , 0.        , 0.        ]])
    '''
    coords = np.stack([bus['x'], bus['y']], axis=-1)
    row, col = line_index(bus, line)
    dists = np.sum((coords[row] - coords[col]) ** 2, axis=-1) ** 0.5
    return scipy.sparse.coo_array((dists, (row, col)), shape=(len(bus),) * 2)
