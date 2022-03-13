from pathlib import Path
from typing import BinaryIO

import click
import platformdirs

from .ical import ical
from .strava_offline import read_strava_offline


@click.command(context_settings={'max_content_width': 120})
@click.option(
    '--strava-database', type=click.Path(path_type=Path),  # type: ignore [type-var] # debian typeshed compat
    default=platformdirs.user_data_path(appname='strava_offline') / 'strava.sqlite',
    show_default=True,
    help="Location of the strava-offline database")
@click.option(
    '-o', '--output', type=click.File('wb'), default='-', show_default=True,
    help="Output file")
def main(strava_database: Path, output: BinaryIO):
    activities = read_strava_offline(strava_database)
    output.write(ical(activities))


if __name__ == "__main__":
    main()
