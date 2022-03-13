from typing import Iterable

import icalendar  # type: ignore [import]

from .strava_offline import Activity


def ical(activities: Iterable[Activity]) -> bytes:
    cal = icalendar.Calendar()
    cal.add('prodid', "strava-ical")
    cal.add('version', "2.0")

    for activity in activities:
        description = []
        if activity.distance > 0:
            description.append(f"Distance: {activity.distance / 1000:.2f} km")
        if activity.total_elevation_gain > 0:
            description.append(f"Elev Gain: {activity.total_elevation_gain:.0f} m")
        if activity.moving_time:
            description.append(f"Moving Time: {activity.moving_time}")

        ev = icalendar.Event()
        ev.add('uid', f"{activity.id}@strava.com")
        ev.add('url', f"https://www.strava.com/activities/{activity.id}")
        ev.add('dtstart', activity.start_datetime)
        ev.add('dtend', activity.end_datetime)
        ev.add('summary', activity.name)  # TODO: type emoji, custom format
        ev.add('description', "\n".join(description))
        if activity.start_latlng:
            ev.add('geo', activity.start_latlng)
        cal.add_component(ev)

    return cal.to_ical()
