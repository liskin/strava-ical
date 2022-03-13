# strava-ical

**Generate iCalendar with your [Strava][] activities**

[![PyPI Python Version badge](https://img.shields.io/pypi/pyversions/strava-ical)](https://pypi.org/project/strava-ical/)
[![PyPI Version badge](https://img.shields.io/pypi/v/strava-ical)](https://pypi.org/project/strava-ical/)
![License badge](https://img.shields.io/github/license/liskin/strava-ical)

Uses [strava-offline][] to keep and incrementally sync with a local database of activities.

![Example screenshot](TODO)

[strava-offline]: https://github.com/liskin/strava-offline#readme
[Strava]: https://strava.com/
[pipx]: https://github.com/pypa/pipx

## Installation

Using [pipx][]:

```
pipx ensurepath
pipx install "strava-ical[strava]"
```

Alternatively, if you don't need the isolated virtualenv that [pipx][]
provides, feel free to just:

```
pip install "strava-ical[strava]"
```

If you've already installed [strava-offline][] and use it separately, you can
omit the `[strava]` bit to avoid installing strava-offline twice.

## Setup and usage

* Run `strava-ical-sync` (or `strava-offline sqlite` if you chose to install
  [strava-offline][] separately) to synchronize activities metadata to a local
  sqlite database. This takes a while: first time a couple dozen seconds, then
  it syncs incrementally which only takes a few seconds each time. Add `-v` to
  see progress.

  The first time you do this, it will open Strava in a browser and ask for
  permissions. Should you run into any trouble at this point, consult
  [strava-offline][] readme or open an issue.

  If you make changes to older activities (to assign a different bike to a
  ride, for example), you may need a `--full` re-sync rathen than the default
  incremental one. See the [note about incremental synchronization](https://github.com/liskin/strava-offline#note-about-incremental-synchronization)
  for a detailed explanation.

* Run `strava-ical`:

  TODO

## Command line options

<!-- include .readme.md/cmdline.md -->
<!--
    $ export COLUMNS=120
-->

    $ strava-ical --help
    Usage: strava-ical [OPTIONS]
    
    Options:
      --help  Show this message and exit.
<!-- end include -->

## Donations (♥ = €)

If you like this tool and wish to support its development and maintenance,
please consider [a small donation](https://www.paypal.me/lisknisi/5EUR) or
[recurrent support through GitHub Sponsors](https://github.com/sponsors/liskin).

By donating, you'll also support the development of my other projects. You
might like these:

* [strava-offline](https://github.com/liskin/strava-offline) – Keep a local mirror of Strava activities for further analysis/processing
* [strava-gear](https://github.com/liskin/strava-gear) – Rule based tracker of gear and component wear primarily for Strava
* [strava-map-switcher](https://github.com/liskin/strava-map-switcher) – Map switcher for Strava website
