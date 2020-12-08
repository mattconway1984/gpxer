import datetime
import pathlib

import gpxpy
import gpxpy.gpx

from gpxer.gpxer import fix_gpx_timings, Config

SOURCE_PATH = pathlib.Path("route.gpx")
DEST_PATH = pathlib.Path("output.gpx")
START_TIME = datetime.datetime(year=2012, month=4, day=12, hour=11, minute=22, second=14)


# Track one has 2x Segments; first is the climb, second is the descent:
TRACK_ONE = Config.TrackConfig([
    Config.SegmentConfig(speed=12.1, jitter=3),
    Config.SegmentConfig(speed=50, jitter=10)
])

# GPX file only has 1x track:
CONFIG = Config(start_time=START_TIME, tracks=[TRACK_ONE])

if __name__ == "__main__":
    gpx_data = None
    with SOURCE_PATH.open("r") as source:
        gpx_data = gpxpy.parse(source)
        fix_gpx_timings(gpx_data, CONFIG)
    with DEST_PATH.open("w") as destination:
        destination.write(gpx_data.to_xml())
