from datetime import timedelta
import json
import sqlite3
from typing import Any
from typing import Dict
from typing import Iterable

from dateutil.parser import isoparse


class Activity:
    def __init__(self, row: Dict[str, Any]):
        self._row = row
        self._json = json.loads(row['json'])

    def __getitem__(self, key):
        if key in self._row:
            return self._row[key]
        else:
            return self._json[key]

    @property
    def id(self) -> int:
        return self['id']

    @property
    def name(self) -> str:
        return self['name']

    @property
    def distance(self) -> float:
        return self['distance']  # meters

    @property
    def total_elevation_gain(self) -> float:
        return self['total_elevation_gain']  # meters

    @property
    def moving_time(self) -> timedelta:
        return timedelta(seconds=self['moving_time'])

    @property
    def elapsed_time(self) -> timedelta:
        return timedelta(seconds=self['elapsed_time'])

    @property
    def start_latlng(self):
        try:
            [lat, lng] = self['start_latlng']
            return lat, lng
        except ValueError:
            return None

    @property
    def start_datetime(self):
        return isoparse(self['start_date'])

    @property
    def end_datetime(self):
        return self.start_datetime + self.elapsed_time


def read_strava_offline(db_filename: str) -> Iterable[Activity]:
    """
    Read activities from strava-offline database.
    """
    with sqlite3.connect(db_filename) as db:
        db.row_factory = sqlite3.Row

        for r in db.execute('SELECT * FROM activity'):
            yield Activity({**r})
