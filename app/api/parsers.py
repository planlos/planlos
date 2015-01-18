
from flask import Markup
import dateutil

def event_title(value, name):
    # cut length?
    title = value[0:200]
    # not allowed html
    title = Markup(title).striptags()
    # not allowed charactesr
    for c in ";`´":
        title = title.replace(c, '')
    # make First letter upper?
    title = title.capitalize()
    return title


def event_subtitle(value, name):
    # cut length?
    subtitle = value[0:400]
    # not allowed html
    subtitle = Markup(subtitle).striptags()
    # not allowed charactesr
    for c in ";`´":
        subtitle = subtitle.replace(c, '')
    # make First letter upper?
    subtitle = subtitle.capitalize()
    return subtitle


def dtfield(value, name):
    try:
        date = dateutil.parser.parse(value)
        return date
    except:
        raise ValueError("{} is not a parsable Date in field {}".format(value, name))


def rrule_field(value, name):
    pass

#    raise ValueError()
