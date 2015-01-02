# coding: utf-8

from flask.ext.wtf import Form
from wtforms import (TextField, SubmitField, DecimalField,
                     HiddenField, PasswordField, BooleanField,
                     TextAreaField, SelectField, SelectMultipleField,
                     IntegerField, Field)
from wtforms.ext.dateutil.fields import DateTimeField, DateField
from flask.ext.wtf.html5 import EmailField, URLField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.validators import required, Required, EqualTo, Optional, ValidationError
from ..models.location import Location
from wtforms.widgets import TextInput
from wtforms import widgets
import re
from dateutil.parser import *
import datetime
import time


class Location_Form(Form):
    name = TextField('Name', validators=[Required()])
    desc = TextField('Beschreibung')
    addr = TextField('Adresse')
    longitude = DecimalField('Longitude', validators=[Optional()])
    latitude = DecimalField('Latitude', validators=[Optional()])
    url = URLField('Homepage (url)')
    tags = TextField('Tags')
    email_contact = EmailField('Kontakt Email')
    submit = SubmitField('Speichern')


# Query Factories
def get_locations():
    return Location.query.all()


class TimeField(DateTimeField):
    def __init__(self, label='', validators=None, format='%H:%M', **kwargs):
        super(TimeField, self).__init__(label, validators, format, **kwargs)
        self.format = format

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                date_str = ' '.join(valuelist)
                timetuple = time.strptime(date_str, self.format)
                self.data = datetime.time(*timetuple[3:6])
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Invalid time input'))


class BootstrapInlineWidget(object):
    def __init__(self, class_=''):
        self.css_class = class_ 

    def __call__(self, field, **kwargs):
        html = []
        for subfield in field:
            html.append('<label class="%s-inline">%s %s</label>' % (self.css_class, subfield(), subfield.label.text) )
        return widgets.HTMLString(''.join(html))


class CheckboxSelectMultipleField(SelectMultipleField):
    widget = BootstrapInlineWidget(class_='checkbox')
    option_widget=widgets.CheckboxInput()
    

class Event_Form(Form):
    title = TextField('Titel', validators=[Required()])
    subtitle = TextAreaField('Untertitel, Kurzbeschreibung', validators=[Optional(strip_whitespace=True)])
    desc = TextAreaField('Beschreibung', validators=[Optional(strip_whitespace=True)])

    dtstart_date = DateField("Datum", display_format='%d/%m/%Y', validators=[Required()])
    dtstart_time = TimeField("Uhrzeit", display_format='%H:%M', validators=[Required()])
    dtend = TimeField("Ende (Uhrzeit)", display_format='%H:%M', validators=[Optional()], default=None)
    location = QuerySelectField(query_factory=get_locations)

    recurrence = SelectField('Wiederholung',choices=[('0', 'Keine Wiederholung'),
                                                      ('1', 'Täglich'),
                                                      ('2', 'Wöchentlich'),
                                                      ('3', 'Monatlich'),
                                                      ('4', 'Expert_in')])
    until = DateField("Bis (Datum)",  validators=[Optional(strip_whitespace=True)], default=None)
    repeat = IntegerField("Wiederholungen", validators=[Optional(strip_whitespace=True)], default=None)

    # weekly
    weekly_days = CheckboxSelectMultipleField("An den Tagen",  choices=[('0', 'Montag'),
                                                                         ('1', 'Dienstag'),
                                                                         ('2', 'Mittwoch'),
                                                                         ('3', 'Donnerstag'),
                                                                         ('4', 'Freitag'),
                                                                         ('5', 'Samstag'),
                                                                         ('6', 'Sonntag')])
    weekly_repeat = IntegerField("Woche", validators=[Optional()], default=1)

    ## monthly
    monthly_days = CheckboxSelectMultipleField('Jeden folgenden Tag', choices=[ (str(x), str(x)) for x in range(1,32)])
    rrule = TextField("iCal RRULE (RFC 5545)", validators=[Optional()], default=None)
    submit = SubmitField('Speichern')

    def validate_dtstart_date(form,field):
        if field.data < datetime.datetime.now().date():
            raise ValidationError("Your date is in the past")

    def validate_dtstart_time(form, field):
        dtstart = datetime.datetime.combine(form.dtstart_date.data, field.data)
        if dtstart < datetime.datetime.now():
            raise ValidationError("Your Time is in the past")
                                 
    def validate_dtend(form, field):
        if field.data:
            if field.data < form.dtstart_time.data:
                raise ValidationError("Your end time is earlier than the start time")

    def validate_until(form, field):
        if form.recurrence.data in ['1', '2', '3']:
            if field.data is None and form.repeat.data is None:
                raise ValidationError("You need either until or repeat values")

    def validate_repeat(form, field):
        if form.recurrence.data in ['1', '2', '3']:
            if field.data is None and form.until.data is None:
                raise ValidationError("You need either until or repeat values")
            
    def validate_weekly_days(form, field):
        if form.recurrence.data == '2':
            if not len(field.data):
                raise ValidationError("You need to select a Day")

    def validate_monthly_days(form, field):
        if form.recurrence.data == '3':
            if not len(field.data):
                raise ValidationError("You need to select a Day")

class Login_Form(Form):
    next = HiddenField()
    remember = BooleanField("Remember me")
    uid = TextField("Username",
                    validators=[required(message="You must provide a username")
            ])
    password = PasswordField("Password")
    submit = SubmitField("Login")

class Signup_Form(Form):
    next = HiddenField()
    username = TextField("Username",
                         validators=[required(message="You must provide a username")])
    password = PasswordField("Password",
                             validators=[Required()])
    password2 = PasswordField("Repeat Password",
                              validators=[EqualTo('password', message='Passwords do not match')])
    email = TextField("E-Mail", validators=[Required(),
                                            #Email("not a valid email adress")
                                            ])
    invitecode1 = TextField("Invite Code (1)", validators=[Required()])
    invitecode2 = TextField("Invite Code (2)", validators=[Required()])
    submit = SubmitField("Sign Up")
