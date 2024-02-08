from typing import Iterable
from typing import Optional

import icalendar  # type: ignore [import]

from .data import Activity


def ical(activities: Iterable[Activity], max_size: Optional[int] = None) -> bytes:
    cal = icalendar.Calendar()
    cal.add('prodid', "strava-ical")
    cal.add('version', "2.0")

    cal_size = len(cal.to_ical())

    for activity in activities:
        description = []
        if activity.distance > 0:
            description.append(f"Distance: {activity.distance / 1000:.2f} km")
        if activity.total_elevation_gain > 0:
            description.append(f"Elev Gain: {activity.total_elevation_gain:.0f} m")
        if activity.moving_time:
            description.append(f"Moving Time: {activity.moving_time}")
        description.append(f"Strava: https://www.strava.com/activities/{activity.id}")

        ev = icalendar.Event()
        ev.add('uid', f"{activity.id}@strava.com")
        ev.add('url', f"https://www.strava.com/activities/{activity.id}")
        ev.add('dtstart', activity.start_datetime)
        ev.add('dtend', activity.end_datetime)
        ev.add('summary', f"{activity.type_emoji} {activity.name}")  # TODO: custom format
        ev.add('description', "\n".join(description))
        if activity.start_latlng:
            ev.add('geo', activity.start_latlng)

        ev_size = len(ev.to_ical())
        if max_size is not None and cal_size + ev_size > max_size:
            break

        cal.add_component(ev)
        cal_size += ev_size

    return cal.to_ical()
