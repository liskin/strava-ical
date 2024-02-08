import csv
import json
from os import PathLike
import sqlite3
from typing import Iterable
from typing import TextIO
from typing import Union

from .data import Activity
from .data import essential_columns


def read_input_csv(inp: TextIO) -> Iterable[Activity]:
    """
    Read activities from CSV generated from this command:

        sqlite3 ~/.local/share/strava_offline/strava.sqlite \
            ".mode csv" \
            ".headers on" \
            "SELECT distance, elapsed_time, id, moving_time, name, start_date, \
                json_extract(json, '$.start_latlng') AS 'start_latlng', total_elevation_gain, type FROM activity \
                ORDER BY start_date DESC" \
            >activities.csv
    """
    for r in csv.DictReader(inp):
        assert essential_columns <= r.keys()
        r['id'] = int(r['id'])
        r['distance'] = float(r['distance'])
        r['total_elevation_gain'] = float(r['total_elevation_gain'])
        r['moving_time'] = int(r['moving_time'])
        r['elapsed_time'] = int(r['elapsed_time'])
        if 'start_latlng' in r:
            r['start_latlng'] = json.loads(r['start_latlng'])
        yield Activity(r)


def read_strava_offline(db_filename: Union[str, PathLike]) -> Iterable[Activity]:
    """
    Read activities from strava-offline database.
    """
    with sqlite3.connect(db_filename) as db:
        db.row_factory = sqlite3.Row

        for r in db.execute('SELECT * FROM activity ORDER BY start_date DESC'):
            r_json = json.loads(r['json'])
            r = {**r_json, **r}
            assert essential_columns <= set(r.keys())
            yield Activity(r)
