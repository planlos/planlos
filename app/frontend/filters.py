# coding: utf-8

from flask.ext.babel import gettext

def jinja2_filter_datetime(date, fmt=None):
    if fmt:
        return date.strftime(fmt)
    else:
        return date.strftime(gettext('%%a %%d. %%B %%Y'))
