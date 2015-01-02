from .forms import Login_Form
from ..services import events
from .helpers import *
import datetime


def add_login_form():
    return dict(login_form=Login_Form())

def next_concert():
    return dict(next_concert=events.get_by_tag('Konzert', slice=1))

def next_demo():
    return dict(next_demo=events.get_by_tag('Demo', slice=1))

def regulars():
    return dict(todays_regluars=events.get_regulars(datetime.datetime.today()))
    


def add_calendar_view():
    today = datetime.date.today()
    next_month = today+relativedelta(months=+1)
    calendar_1 = Calendar_View(today)
    calendar_2 = Calendar_View(next_month)
    d = {
        'cal1': calendar_1,
        'cal2': calendar_2,
        'today': today        
    }
    return dict(calendar=d)
