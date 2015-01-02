# coding: utf-8

from datetime import datetime, date
from dateutil.relativedelta import *
import calendar
from app.models.events import Event


class Calendar_View():
    def __init__(self, day_of_month):
        self.today = date.today()
        self.calendar = []
        self.day_of_month = day_of_month
        self.build_calendar()

    def build_calendar(self):
        year = self.day_of_month.year
        month = self.day_of_month.month
        cal = calendar.monthcalendar(year, month)
        start_of_month = datetime(year=year,month=month, day=1)
        start_of_next_month = start_of_month+relativedelta(months=+1)
        entries = Event.query.filter( Event.is_pub==True, Event.dtstart >= start_of_month,
                                      Event.dtstart < start_of_next_month).all()
        self.calendar = []
        for week in cal:
            nweek = []
            for day in week:
                nweek.append( [day, False] )
                if day:
                    dday = date(year, month, day)
                    for j in entries:
                        if j.dtstart.date() == dday:
                            nweek[-1][1] = True
            self.calendar.append(nweek)
        while len(self.calendar) < 6:
            self.calendar.append ( [ [0, False],[0, False],[0, False],
                                     [0, False],[0, False],[0, False],[0, False] ] )


    def year(self):
        return self.day_of_month.year

    def month(self):
        return self.day_of_month.month
