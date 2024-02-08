from itertools import chain
from pathlib import Path
import re
from typing import BinaryIO
from typing import Optional
from typing import TextIO

import click
import platformdirs

from .data import essential_columns
from .data import optional_columns
from .ical import ical
from .input import read_input_csv
from .input import read_strava_offline


class SizeType(click.ParamType):
    _regex = re.compile(r"(\d+)\s*([KM]?)")
    _suffixes = {'': 1, 'K': 1_000, 'M': 1_000_000}

    name = "size"

    def convert(self, value, param, ctx):
        if isinstance(value, int):
            return value
        elif m := self._regex.fullmatch(value):
            return int(m[1]) * self._suffixes[m[2]]
        else:
            self.fail(f"{value!r} is not a valid size", param, ctx)


@click.command(context_settings={'max_content_width': 120})
@click.option(
    '--csv', type=click.File('r'),
    help=f"""
    Load activities from CSV instead of the strava-offline database
    (columns: {", ".join(sorted(chain(essential_columns, optional_columns)))})
    """)
@click.option(
    '--strava-database', type=click.Path(path_type=Path),  # type: ignore [type-var] # debian typeshed compat
    default=platformdirs.user_data_path(appname='strava_offline') / 'strava.sqlite',
    show_default=True,
    help="Location of the strava-offline database")
@click.option(
    '-o', '--output', type=click.File('wb'), default='-', show_default=True,
    help="Output file")
@click.option(
    '-m', '--max-size', type=SizeType(),
    help="Maximum size of the output file in bytes (accepts K and M suffixes as well)")
def cli(csv: Optional[TextIO], strava_database: Path, output: BinaryIO, max_size: Optional[int]):
    """
    Generate iCalendar with your Strava activities
    """
    if csv:
        activities = read_input_csv(csv)
    else:
        activities = read_strava_offline(strava_database)
    output.write(ical(activities, max_size=max_size))
