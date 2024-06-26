'''
Generates GeoJSON features from `bus` and `line` entries.
'''

import sys, json, math, numbers

import numpy as np

import dlr.esy.grid.match.visualize


def normalize_value(value):
    '''
    Normalizes `value` to a JSON encodable value.

    JSON only supports a limited set of types and values. For example, `NaN` and
    infinity values of `float` are not supported. numpy number types are also
    not JSON encodable.

    This function normalizes `numbers.Integral` types to `int`,
    `numbers.Real` types to `float` and replaces non-finite values with the
    string `'-'`:

    >>> print(json.dumps(list(map(normalize_value, [
    ...     None, True, 'x', float('inf'), np.float64(1.2), np.int32(3)
    ... ]))))
    [null, true, "x", "-", 1.2, 3]

    Other types cause a `ValueError`:

    >>> normalize_value(object()) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: Cannot normalize <object ...>
    '''
    if value is None:
        return value
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value
    if isinstance(value, numbers.Integral):
        return int(value)
    if isinstance(value, numbers.Real):
        return float(value) if math.isfinite(value) else '-'
    raise ValueError(f'Cannot normalize {value}')


def bus_features(bus):
    '''
    Generates GeoJSON representations of `bus` entries.

    >>> import io, dlr.esy.grid.match.powergrid, json
    >>> bus = dlr.esy.grid.match.powergrid.bus_csv(io.StringIO("""
    ... name; x; y; aux
    ... A0;   0; 0; eggs
    ... """))
    >>> list(bus_features(bus)) == [{
    ...     "type": "Feature",
    ...     "geometry": {"type": "Point", "coordinates": [0, 0]},
    ...     "properties": {"marker-size": "small", "name": "A0", "aux": "eggs"}
    ... }]
    True

    '''

    for b in bus:
        yield {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [normalize_value(b.x), normalize_value(b.y)],
            },
            'properties': {
                'marker-size': 'small',
                **{
                    f: normalize_value(getattr(b, f).item())
                    for f in bus.dtype.fields
                    if f not in ('x', 'y')
                }
            },
        }


def line_features(bus, line):
    '''
    Generates GeoJSON representations of `line` entries.

    >>> import dlr.esy.grid.match.powergrid
    >>> (bus, line), = dlr.esy.grid.match.powergrid.load_tables("""
    ... name;x;y | name;bus0;bus1
    ... A0;0;0   | A0-1;A0;A1
    ... A1;1;1   |
    ... """)
    >>> list(line_features(bus, line)) == [{
    ...     "type": "Feature",
    ...     "geometry": {"type": "LineString", "coordinates": [[0, 0], [1, 1]]},
    ...     "properties": {"stroke": "red", "name": "A0-1"}
    ... }]
    True

    '''

    line_i0, line_i1 = dlr.esy.grid.match.powergrid.line_index(bus, line)
    line_coords = np.moveaxis(
        [[bus.x[line_i0], bus.y[line_i0]], [bus.x[line_i1], bus.y[line_i1]]],
        -1, 0
    )
    intra_cluster = (
        bus.center[line_i0] == bus.center[line_i1]
        if 'center' in bus.dtype.names else
        np.zeros(len(bus))
    )
    fields = [
        f for f in line.dtype.fields
        if f not in {'bus0', 'bus1', 'i0', 'i1'}
    ]
    for l, c, intra in zip(line, line_coords, intra_cluster):
        yield {
            'type': 'Feature',
            'geometry': {'type': 'LineString', 'coordinates': c.tolist()},
            'properties': {
                'stroke': 'orange' if intra else 'red',
                **{f: normalize_value(getattr(l, f).item()) for f in fields}
            },
        }


def cluster_hull_features(bus):
    '''
    Generates GeoJSON representation of `bus` cluster hulls.

    >>> import io, dlr.esy.grid.match.powergrid
    >>> bus = dlr.esy.grid.match.powergrid.bus_csv(io.StringIO("""
    ... name;x;y;center
    ... A0;0;0;1
    ... A1;0;1;1
    ... A2;1;1;1
    ... """))
    >>> list(cluster_hull_features(bus)) == [{
    ...     'type': 'Feature', 'geometry': {
    ...         'type': 'Polygon',
    ...         'coordinates': [[[0.0, 0.0], [1.0, 1.0], [0.0, 1.0]]]
    ...     },
    ...     'properties': {
    ...         'fill': 'orange', 'stroke-width': 0,
    ...         'name': 'A1', 'x': 0, 'y': 1, 'center': 1
    ...     }
    ... }]
    True

    '''
    fields = list(bus.dtype.fields)
    for center, hull in dlr.esy.grid.match.visualize.cluster_hulls(bus):
        b = bus[center]
        yield {
            'type': 'Feature',
            'geometry': {'type': 'Polygon', 'coordinates': [hull.tolist()]},
            'properties': {
                'fill': 'orange', 'stroke-width': 0,
                **{
                    f: normalize_value(getattr(b, f).item())
                    for f in bus.dtype.fields
                }
            },
        }


def grid_features(bus, line):
    '''
    Generates `cluster_hull_features`, `line_features` and `bus_features` from
    `bus` and `line`.
    '''

    yield from cluster_hull_features(bus)
    yield from line_features(bus, line)
    yield from bus_features(bus)


def grid(grids, file=sys.stdout, show=None, browser=False):
    '''
    Renders the grid named `show` from `grids` as GeoJSON to `file`.

    If `show` isn't given, the first grid from `grids` is selected.

    Optionally, if `browser` is given, a webbrowser will be opened, showing the
    `https://geojson.io/` visualization of the GeoJSON data.
    '''
    if show is None:
        show = grids[0][0]

    for name, (bus, line) in grids:
        if name == show:
            break
    else: #pragma: nocover
        raise KeyError(f'Grid "{show}" not found')

    data = {
        'type': 'FeatureCollection',
        'features': list(grid_features(bus, line)),
    }

    if browser: #pragma: nocover
        import io, webbrowser, http.server

        class DataHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                text = io.TextIOWrapper(self.wfile, encoding='utf-8')
                json.dump(data, text)
                # Prevent TextIOWrapper from closing wfile.
                text.detach()

        httpd = http.server.HTTPServer(('localhost', 0), DataHandler)
        host, port = httpd.server_address
        webbrowser.open(
            f'https://geojson.io/#data=data:text/x-url,http://{host}:{port}'
        )
        httpd.handle_request()
    else:
        json.dump(data, file)
