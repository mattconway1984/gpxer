import datetime
import random

import geopy.distance


class Config:
    """
    Config data used to fix a GPX track.

    For each segment that resides within the GPX track

    Args:
        start_time (datetime.datetime): Modified start time for the GPX file.
        tracks (list[TrackConfig]): List of configs for each track.
    """

    class SegmentConfig:
        """
        Config data used to fix each GPX segment.

        Args:
            average_speed (float): The average speed (kmh) value to apply.
            jitter (float): Max amount of jitter (kmh) applied to average speed.
        """
        def __init__(self, speed, jitter):
            self.speed = speed
            self.jitter = jitter

    class TrackConfig:
        """
        Config data used to fix each GPX track.

        Args:
            segments (list[SegmentConfig]): List of configs for each segment.
        """
        def __init__(self, segments):
            self.segments = segments

    def __init__(self, start_time, tracks):
        self.tracks = tracks
        self.start_time = start_time

def fix_gpx_timings(gpx_data, config):
    """
    Little function to fix up a GPX track to apply an average speed over
    the all segments contained within the track.

    Args:
        gpx_data (list[str]): XML data, the contents of the GPX file.
        config(Config): Config data that should be aligned with the GPX data.
    """
    first_segment = True
    last_segment_end_time = None
    for track_config, track in zip(config.tracks, gpx_data.tracks):
        for segment_config, segment in zip(track_config.segments, track.segments):
            previous_point = None
            for point in segment.points:
                if previous_point:
                    # Not the first point in this segment.
                    speed = \
                        speed_with_jitter(
                            segment_config.speed,
                            segment_config.jitter)
                    duration = get_duration(point, previous_point, speed)
                    time_delta = datetime.timedelta(seconds=duration)
                    point.time = previous_point.time + time_delta
                    # This might be the last point in the current segment:
                    last_segment_end_time = point.time
                elif first_segment:
                    # First point of first segment.
                    point.time = config.start_time
                    first_segment = False
                else:
                    # First point of a segment (or track)
                    point.time = last_segment_end_time # This could be a config
                previous_point = point

def kmh_to_ms(kmh):
    """
    Convert Kilometers Per Hour to Meters Per Second.
    """
    return kmh * 5 / 18

def speed_with_jitter(speed, jitter):
    """
    Apply a level of random jitter to the average speed

    Args:
        speed (float): The speed to apply jitter.
        jitter (float): The max jitter to apply.

    Returns:
        float: Speed with random jitter applied.
    """
    jitter_value = random.random() * jitter
    if random.choice([True, False]):
        return speed + jitter_value
    return speed - jitter_value

def get_duration(first, second, speed):
    """
    For a distance (in KM), get a time that represents the time it takes to
    travel `distance` at `speed`.

    Args:
        first (tuple): (Latitude, Longitude) co-ordinates for first point.
        second (tuple): (Latitude, Longitude) co-ordinates for second point.
        speed (float): speed

    Returns:
        float: Duration (in seconds) representing modified time between two
            points.
    """
    distance = \
        geopy.distance.distance(
            (first.latitude, first.longitude),
            (second.latitude, second.longitude))
    return distance.m / kmh_to_ms(speed)


# TODO: Rather than apply just some jitter, apply some real logic.
# Use elevation difference between points in the GPX track, and a W/KG
# to give a more accurate estimation.

# weight (kg) x 9.8 x elevation gain (meters) / time (seconds) = power (watts).
# Add 10% for rolling and air resistance.


