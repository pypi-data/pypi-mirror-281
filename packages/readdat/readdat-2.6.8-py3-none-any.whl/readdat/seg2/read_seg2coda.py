from typing import List
import warnings
import parse
import obspy
import numpy as np
from obspy.core.utcdatetime import UTCDateTime
import datetime

KNOWN_CODA_VERSIONS = []
# G.EIFFEL IFSTTAR MULTI_ACQ 8/16 VOIES VERSION TTL/Timed 3.5 20/02/2024

def is_seg2coda(stream: obspy.core.stream.Stream) -> bool:
    """
    determines whether a stream read from seg2 file is from CODA or not
    :return answer: True or False
    """

    assert isinstance(stream, obspy.core.stream.Stream), TypeError(type(stream))

    if not hasattr(stream.stats, "seg2"):
        # probably not even a seg2 file
        return False

    if hasattr(stream.stats.seg2, "NOTE"):
        # search in the notes at the stream level
        stream_notes: List[str] = stream.stats.seg2['NOTE']

        for note in stream_notes:
            if "CODA" in note:
                return True

            elif "MULTI_ACQ 8/16 VOIES VERSION" in note:
                return True

    if len(stream):
        # search in the attributes of the first trace
        if hasattr(stream[0].stats.seg2, "UNIV.") \
                and "MULTI_ACQ 8/16 VOIES VERSION" in stream[0].stats.seg2['UNIV.']:
            return True

        trace_notes = stream[0].stats.seg2["NOTE"]
        for note in trace_notes:
            if "CODA" in note:
                return True

            elif "MULTI_ACQ 8/16 VOIES VERSION" in note:
                return True
    else:
        warnings.warn('no traces found in stream')

    return False


def _extract_receiver_location(trace) -> None:
    try:
        # unpack string as 3 floats (x, y, z in meters)
        trace.stats.receiver_x, \
            trace.stats.receiver_y, \
            trace.stats.receiver_z = \
            [float(_) for _ in trace.stats.seg2['RECEIVER_LOCATION'].split()]

    except KeyError as err:
        warnings.warn(str(err))


def _extract_trace_time(trace: obspy.Trace) -> None:
    """Get the date and time of the trace from seg2 metadata as filled by Olivier Durand
    !!! Overwrite the field trace.stats.starttime !!!
    Modified after Pierric Mora, 2023.
    Modif 2023/07/12 ML: the DATE and TIME fields are not always at the same place in the notes

    """
    date_format = "DATE {day:02d}/{month:02d}/{year:04d}"
    time_format = "TIME {hour:02d}:{minute:02d}:{second:02d}"

    for field in trace.stats.seg2['NOTE']:
        if field.startswith('DATE'):
            date_field = field
            break
    else:
        raise ValueError("DATE field not found in the trace notes")

    for field in trace.stats.seg2['NOTE']:
        if field.startswith('TIME'):
            time_field = field
            break
    else:
        raise ValueError("TIME field not found in the trace notes")

    date_ = parse.parse(date_format, date_field)
    time_ = parse.parse(time_format, time_field)

    if date_ is None:
        raise ValueError(f'could not parse {date_field=} into {date_format=}')

    if time_ is None:
        raise ValueError(f'could not parse {time_field=} into {time_format=}')

    kwargs = {**date_.named, **time_.named}  # concatenate dictionaries

    # pass arguments year, month, day, hour, minute, second parsed above
    # local/utc times conversions are handled at a higher level
    utc = obspy.core.utcdatetime.UTCDateTime(**kwargs)

    # OVERWRITE THE ORIGINAL TIME FROM OBSPY BY THE NEW ONE
    trace.stats.starttime = utc


def _extract_temp_rh(trace: obspy.Trace) -> None:
    """
    Extract temperature and relative humidity from the trace notes if present
    """
    temperature_format = "TEMPE_C {temperature_degc:e}"
    relative_humidity_format = "RH_% {relative_humidity_percent:e}"

    temperature_degc = np.nan
    relative_humidity_percent = np.nan

    for field in trace.stats.seg2['NOTE']:
        if field.startswith('TEMPE_C'):
            temperature_degc_ = parse.parse(temperature_format, field)
            if temperature_degc_ is None:
                raise ValueError(f'could not parse {field=} into {temperature_format=}')
            temperature_degc = temperature_degc_["temperature_degc"]
            break
    else:
        # temperature field not found
        pass

    for field in trace.stats.seg2['NOTE']:
        if field.startswith('RH_%'):
            relative_humidity_percent_ = parse.parse(relative_humidity_format, field)
            if relative_humidity_percent_ is None:
                raise ValueError(f'could not parse {field=} into {relative_humidity_format=}')
            relative_humidity_percent = relative_humidity_percent_['relative_humidity_percent']
            break
    else:
        # relative_humidity field not found
        pass

    trace.stats['temperature_degc'] = temperature_degc
    trace.stats['relative_humidity_percent'] = relative_humidity_percent


def seg2coda_to_seg2obspy(stream: obspy.core.stream.Stream, verbose: bool=True) -> obspy.core.stream.Stream:
    """
    Extract information for ondulys files,
    private, do not call directly
    """
    # Modified after O. Abraham, DTLSWI, 08/2022

    # TODO : assert that this is indeed a file from CODA

    for trace in stream:
        trace.stats.station = "CODA"

        # coordinates
        _extract_receiver_location(trace=trace)

        # Times
        _extract_trace_time(trace=trace)

        # Temperature / Relative humidity
        _extract_temp_rh(trace=trace)

    return stream
