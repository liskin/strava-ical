import textwrap

from click.testing import CliRunner

from strava_ical.cli import cli
from strava_ical.data import Activity
from strava_ical.ical import ical

activities = [
    Activity({
        'id': 1,
        'name': 'Morning Ride',
        'distance': 1500,
        'total_elevation_gain': 200,
        'moving_time': 600,
        'elapsed_time': 660,
        'start_date': '2024-02-06T10:00:00Z',
        'type': 'Ride',
    }),
    Activity({
        'id': 2,
        'name': 'Morning Skate',
        'distance': 1500,
        'total_elevation_gain': 200,
        'moving_time': 600,
        'elapsed_time': 660,
        'start_date': '2024-02-05T10:00:00Z',
        'type': 'InlineSkate',
        'start_latlng': [51.0, 0.0],
    }),
]


def test_ical():
    expected = textwrap.dedent("""\
        BEGIN:VCALENDAR
        VERSION:2.0
        PRODID:strava-ical
        BEGIN:VEVENT
        SUMMARY:🚴 Morning Ride
        DTSTART:20240206T100000Z
        DTEND:20240206T101100Z
        UID:1@strava.com
        DESCRIPTION:Distance: 1.50 km\\nElev Gain: 200 m\\nMoving Time: 0:10:00\\nStr
         ava: https://www.strava.com/activities/1
        URL:https://www.strava.com/activities/1
        END:VEVENT
        BEGIN:VEVENT
        SUMMARY:🛼 Morning Skate
        DTSTART:20240205T100000Z
        DTEND:20240205T101100Z
        UID:2@strava.com
        DESCRIPTION:Distance: 1.50 km\\nElev Gain: 200 m\\nMoving Time: 0:10:00\\nStr
         ava: https://www.strava.com/activities/2
        GEO:51.0;0.0
        URL:https://www.strava.com/activities/2
        END:VEVENT
        END:VCALENDAR
    """).replace('\n', '\r\n')
    assert ical(activities) == expected.encode('utf-8')


def test_ical_max_size():
    empty_size = len(ical([]))
    full_size = len(ical(activities))
    assert empty_size < full_size
    assert len(ical(activities, max_size=full_size)) == full_size
    assert empty_size < len(ical(activities, max_size=full_size - 1)) < full_size


def test_cli_missing_database_is_clean_error(tmp_path):
    missing = tmp_path / "no-such.sqlite"
    result = CliRunner().invoke(cli, ["--strava-database", str(missing)])
    assert result.exit_code == 1
    assert "not found" in result.output
    assert isinstance(result.exception, SystemExit)
    # sqlite3 must not leave a stray empty file behind
    assert not missing.exists()
