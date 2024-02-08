<!--
    $ export COLUMNS=120
-->

    $ strava-ical --help
    Usage: strava-ical [OPTIONS]
    
      Generate iCalendar with your Strava activities
    
    Options:
      --csv FILENAME          Load activities from CSV instead of the strava-offline database (columns: distance,
                              elapsed_time, id, moving_time, name, start_date, start_latlng, total_elevation_gain, type)
      --strava-database PATH  Location of the strava-offline database  [default:
                              /home/user/.local/share/strava_offline/strava.sqlite]
      -o, --output FILENAME   Output file  [default: -]
      -m, --max-size SIZE     Maximum size of the output file in bytes (accepts K and M suffixes as well)
      --help                  Show this message and exit.
