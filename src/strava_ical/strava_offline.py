import json
from os import PathLike
import sqlite3
from typing import Iterable
from typing import Union

from .data import Activity
from .data import essential_columns


def read_strava_offline(db_filename: Union[str, PathLike]) -> Iterable[Activity]:
    """
    Read activities from strava-offline database.
    """
    with sqlite3.connect(db_filename) as db:
        db.row_factory = sqlite3.Row

        for r in db.execute('SELECT * FROM activity'):
            r_json = json.loads(r['json'])
            r = {**r_json, **r}
            assert essential_columns <= set(r.keys())
            yield Activity(r)
