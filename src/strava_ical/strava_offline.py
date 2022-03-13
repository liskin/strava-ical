from datetime import datetime
from datetime import timedelta
import json
from os import PathLike
import sqlite3
from typing import Any
from typing import Dict
from typing import Iterable
from typing import Optional
from typing import Tuple
from typing import Union

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
    def start_latlng(self) -> Optional[Tuple[float, float]]:
        try:
            [lat, lng] = self['start_latlng']
            return lat, lng
        except ValueError:
            return None

    @property
    def start_datetime(self) -> datetime:
        return isoparse(self['start_date'])

    @property
    def end_datetime(self) -> datetime:
        return self.start_datetime + self.elapsed_time

    @property
    def type(self) -> str:
        return self['type']

    # see https://developers.strava.com/docs/reference/#api-models-ActivityType
    _type_emojis = {
        'AlpineSki': '⛷',
        'BackcountrySki': '🎿',
        'Canoeing': '🛶',
        'Crossfit': '🤸',
        'EBikeRide': '🛵',
        'Elliptical': '🏃',
        'Golf': '🏌',
        'Handcycle': '🚴',
        'Hike': '🥾',
        'IceSkate': '⛸',
        'InlineSkate': '🛼',
        'Kayaking': '🛶',
        'Kitesurf': '🏄',
        'NordicSki': '🎿',
        'Ride': '🚴',
        'RockClimbing': '🧗',
        'RollerSki': '🎿',
        'Rowing': '🚣',
        'Run': '🏃',
        'Sail': '⛵',
        'Skateboard': '🛹',
        'Snowboard': '🏂',
        'Snowshoe': '🎿',
        'Soccer': '⚽',
        'StairStepper': '🪜',
        'StandUpPaddling': '🛶',
        'Surfing': '🏄',
        'Swim': '🏊',
        'Velomobile': '🏎',
        'VirtualRide': '🚴',
        'VirtualRun': '🏃',
        'Walk': '🚶',
        'WeightTraining': '🏋',
        'Wheelchair': '🧑‍🦽',
        'Windsurf': '🏄',
        'Workout': '💪',
        'Yoga': '🧘',
    }

    @property
    def type_emoji(self) -> str:
        return self._type_emojis.get(self.type, "⏱")


def read_strava_offline(db_filename: Union[str, PathLike]) -> Iterable[Activity]:
    """
    Read activities from strava-offline database.
    """
    with sqlite3.connect(db_filename) as db:
        db.row_factory = sqlite3.Row

        for r in db.execute('SELECT * FROM activity'):
            yield Activity({**r})
