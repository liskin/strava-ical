from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Mapping
from typing import Optional
from typing import Tuple

from dateutil.parser import isoparse

essential_columns = {
    'id',
    'name',
    'distance',
    'total_elevation_gain',
    'moving_time',
    'elapsed_time',
    'start_date',
    'type',
}
optional_columns = {
    'start_latlng',
}


class Activity:
    def __init__(self, row: Mapping[str, Any]):
        self._row = row

    def __getitem__(self, key):
        return self._row[key]

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
