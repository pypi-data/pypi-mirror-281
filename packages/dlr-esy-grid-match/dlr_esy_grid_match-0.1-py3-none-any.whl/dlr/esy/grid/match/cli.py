'''
Functions for the command line interface.
'''
import sys, inspect, functools, importlib, argparse, pathlib


def grid():
    '''
    Visualizes powergrids in a figure.
    '''
    def call(*args, **kwargs):
        import dlr.esy.grid.match.visualize
        return dlr.esy.grid.match.visualize.grids(*args, **kwargs)
    return call


def cluster():
    '''
    Visualizes clusters of powergrids in a figure.
    '''
    def call(*args, **kwargs):
        import dlr.esy.grid.match.visualize
        return dlr.esy.grid.match.visualize.cluster(*args, **kwargs)
    return call


def geojson(show=None, browser=False):
    '''
    Generates a geojson visualization.
    '''
    def call(grids):
        import dlr.esy.grid.match.geojson
        return dlr.esy.grid.match.geojson.grid(grids, show=show, browser=browser)
    return call


def compare(
    a='a', a_bus_fields=None, a_line_fields=None,
    b='b', b_bus_fields=None, b_line_fields=None
):
    '''
    Compares two powergrids.

    `a` and `b` are expected to be directories, each containing the files
    `bus.csv` and `line.csv`.
    '''

    a_bus_fields, a_line_fields, b_bus_fields, b_line_fields = (
        dict(f.split(':', 1) for f in fieldmap.split(',')) if fieldmap else None
        for fieldmap in (
            a_bus_fields, a_line_fields, b_bus_fields, b_line_fields
        )
    )

    def call():
        import pathlib, dlr.esy.grid.match.powergrid, dlr.esy.grid.match.cluster
        ap, bp = pathlib.Path(a), pathlib.Path(b)
        ag, bg = dlr.esy.grid.match.cluster.compare((
            dlr.esy.grid.match.powergrid.grid_csv(
                ap / 'bus.csv', ap / 'line.csv',
                bus_fieldmap=a_bus_fields, line_fieldmap=a_line_fields,
            ),
            dlr.esy.grid.match.powergrid.grid_csv(
                bp / 'bus.csv', bp / 'line.csv',
                bus_fieldmap=b_bus_fields, line_fieldmap=b_line_fields,
            ),
        ))
        return (ap.name, ag), (bp.name, bg)
    return call


def max_res(key='join'):
    '''
    Identifies nodes suitable for joining.

    A field named `key` will be annotated to bus records.
    '''
    def call(grids):
        import dlr.esy.grid.match.cluster
        (a_name, (a_bus, a_line)), (b_name, (b_bus, b_line)) = grids
        a_bus, b_bus = dlr.esy.grid.match.cluster.max_res(a_bus, b_bus, key)
        return (a_name, (a_bus, a_line)), (b_name, (b_bus, b_line))
    return call


def join(name='join', key='join'):
    '''
    Joins a pair of grids into a grid with the given `name`. The tables of 
    nodes need a column called `join` which indicates with a 0 that a node 
    belongs to a region and 1 otherwise.
    '''
    def call(grids):
        import dlr.esy.grid.match.cluster
        (a_name, (a_bus, a_line)), (b_name, (b_bus, b_line)) = grids
        bus, line = dlr.esy.grid.match.cluster.join_by(
            ((a_bus, a_line), (b_bus, b_line)), key
        )
        return ((name, (bus, line)),)
    return call


def example():
    '''
    Creates an example datasets.
    '''
    return lambda: None


def simple(path):
    '''
    Writes a simple example dataset to `path`.
    '''

    example_names = (('a/bus.csv', 'a/line.csv'), ('b/bus.csv', 'b/line.csv'))
    example = '''
    name;x;y | name;bus0;bus1 || name;x;y  | name;bus0;bus1
    A0;-2;-1 | A0-1;A0;A1     || B0;2;-1   | B0-2;B0;B2
    A1;-2;1  | A0-2;A0;A2     || B1;2;1    | B1-2;B1;B2
    A2;-1;0  | A1-2;A1;A2     || B2;1;0    | B2-3;B2;B3
    A3;1.5;0 | A2-3;A2;A3     || B3;-1.5;0 |
    '''

    def call():
        import pathlib, dlr.esy.grid.match.powergrid

        dirpath = pathlib.Path(path)
        datasets = dlr.esy.grid.match.powergrid.parse_tables(example)
        for names, dataset in zip(example_names, datasets):
            for name, data in zip(names, dataset):
                p = dirpath / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(data)

    return call


def nonconformative(path):
    '''
    Writes a non-conformative example dataset to `path`.
    '''

    example_names = (('a/bus.csv', 'a/line.csv'), ('b/bus.csv', 'b/line.csv'))
    example = '''
    bus;x;y  | line;bus0;bus1 || bus;x;y   | line;bus0;bus1
    A0;-2;-1 | A0-1;A0;A1     || B0;2;-1   | B0-2;B0;B2
    A1;-2;1  | A0-2;A0;A2     || B1;2;1    | B1-2;B1;B2
    A2;-1;0  | A1-2;A1;A2     || B2;1;0    | B2-3;B2;B3
    A3;1.5;0 | A2-3;A2;A3     || B3;-1.5;0 |
    '''

    def call():
        import pathlib, dlr.esy.grid.match.powergrid

        dirpath = pathlib.Path(path)
        datasets = dlr.esy.grid.match.powergrid.parse_tables(example)
        for names, dataset in zip(example_names, datasets):
            for name, data in zip(names, dataset):
                p = dirpath / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(data)

    return call


def csv(path, delimiter=';'):
    '''
    Writes `grids` as CSV files to `path`.
    '''
    path = pathlib.Path(path)

    def call(grids):
        import numpy as np
        from dlr.esy.grid.match.powergrid import recarray_csv

        for grid, (bus, line) in grids:
            (path / grid).mkdir(parents=True, exist_ok=True)
            (path / grid / 'bus.csv').write_text(recarray_csv(bus, delimiter))
            (path / grid / 'line.csv').write_text(recarray_csv(line, delimiter))

    return call


def plot(save=None):
    '''
    Plots a figure.
    '''
    def call(figure):
        import dlr.esy.grid.match.visualize
        dlr.esy.grid.match.visualize.plot(figure, save)
    return call


def show_help(parser):
    '''
    Command function to show the help text of `parser`.
    '''
    def print_help(*args, **kwargs): #pragma: nocover
        parser.print_help()
        sys.exit(1)
    return print_help


def top():
    '''
    Command-line interface for grid comparisons.
    '''
    return lambda: None


def apply_arguments(func, **args):
    '''
    Applies keyword arguments `args` on `func`.

    >>> apply_arguments(lambda a, b, c: (a, b, c), a=1, b=2, c=3, d=4)
    (1, 2, 3)

    '''
    params = inspect.signature(func).parameters
    return func(**{n: args[n] for n in params if n in args})


def compose_command(*commands):
    '''
    Composes commands in order.
    '''
    def call(**args):
        value = None
        for command in commands:
            func = apply_arguments(command, **args)
            value = func(value) if value else func()
        return value
    return call


def build_parser(parser, command, *subcommands, stack=()):
    '''
    Recursively builds `parser` from the parameters of the `command` function 
    and its `subcommands`.
    '''
    # Set parser description and inspect parameters from command function
    # signature.
    parser.description = command.__doc__
    for param in inspect.signature(command).parameters.values():
        if param.default is param.empty:
            parser.add_argument(param.name)
        else:
            parser.add_argument(
                f'--{param.name}',
                help='(default: "%(default)s")' if param.default else None,
                default=param.default
            )

    if subcommands:
        # Recurse into each subcommand.
        subparsers, substack = parser.add_subparsers(), (*stack, command)
        for subcommand, *subsubcommands in subcommands:
            # Create subparser with first line of docstring as help text.
            subparser = subparsers.add_parser(
                subcommand.__name__, help=subcommand.__doc__.strip(),
            )
            build_parser(subparser, subcommand, *subsubcommands, stack=substack)
        parser.set_defaults(__func__=show_help(parser))
    else:
        parser.set_defaults(__func__=compose_command(*stack, command))


def main(argv=None, prog=None):
    parser = argparse.ArgumentParser(prog=prog)
    build_parser(
        parser,
        top,
        (
            compare,
            (grid, (plot,)), (cluster, (plot,)), (geojson,),
            (join, (grid, (plot,)), (csv,)),
            (max_res, (join, (grid, (plot,)), (csv,))),
            (csv,),
        ),
        (example, (simple,), (nonconformative,)),
    )
    args = vars(parser.parse_args(argv))
    args.pop('__func__')(**args)


if __name__ == '__main__':
    main() #pragma: nocover
