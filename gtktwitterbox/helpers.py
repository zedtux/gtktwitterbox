# Based from http://www.siafoo.net/snippet/89

from datetime import datetime

def distance_of_time_in_words(from_date, since_date=None, target_tz=None, include_seconds=False):
    '''
    Returns the age as a string
    '''
    
    from_date = datetime.strptime(from_date, "%a %b %d %H:%M:%S +0000 %Y")

    if since_date is None:
        since_date = datetime.now(target_tz)
    
    distance_in_time = since_date - from_date
    distance_in_seconds = int(round(abs(distance_in_time.days * 86400 + distance_in_time.seconds)))
    distance_in_minutes = int(round(distance_in_seconds/60))

    if distance_in_minutes <= 1:
        if include_seconds:
            for remainder in [5, 10, 20]:
                if distance_in_seconds < remainder:
                    return "less than %s seconds" % remainder
            if distance_in_seconds < 40:
                return "half a minute"
            elif distance_in_seconds < 60:
                return "less than a minute"
            else:
                return "1 minute"
        else:
            if distance_in_minutes == 0:
                return "less than a minute"
            else:
                return "1 minute"
    elif distance_in_minutes < 45:
        return "%sm" % distance_in_minutes
    elif distance_in_minutes < 90:
        return "1h"
    elif distance_in_minutes < 1440:
        return "%dh" % (round(distance_in_minutes / 60.0))
    else:
        return from_date.strftime("%d %b")