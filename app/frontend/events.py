# coding: utf-8

from ..services import events
from ..services import locations as location_service

from flask import Blueprint
from flask import render_template, abort, current_app, redirect, url_for
from flask.ext.login import login_required
from datetime import datetime, timedelta
from datetime import date as datetime_date
from dateutil.relativedelta import*
# from app.permissions import Edit_Event_Permission
from .forms import Event_Form

mod = Blueprint('events', __name__,
                template_folder='templates')

#####
##### Termine
#####

@mod.route('/termine')
def termine():
    return redirect(url_for('events.event_range', timerange='heute'))

@login_required
@mod.route('/eintragen')
def eintragen():
    return render_template('eintragen.html')


@mod.route("/events/event/<id>")
@mod.route("/termine/termin/<id>")
def termin_by_id(id):
    event = events.get_or_404(id)
    baseurl=current_app.config['UPLOADED_FLYERS_URL']
    size=450
    date=datetime.now().date()
    return render_template('events/show.html', **locals())


@mod.route("/termine/<int:year>/<int:month>/<int:day>")
def events_by_day(year, month, day):
    date = datetime(year=year,month=month, day=day, hour=0).date()
    entries = events.get_by_date(date)
    return render_template('events/index.html', **locals())


@mod.route('/termine/<timerange>')
def event_range(timerange):
    entries = None
    date = None
    date2 = None
    header = ''
    if timerange == 'heute':
        date = datetime_date.today()
        header = 'Heute'
    elif timerange == 'morgen':
        date = datetime_date.today()+timedelta(days=1)
        header = 'Morgen'
    elif timerange == 'wochenende':
        date = datetime_date.today()
        if date.weekday() in [4,5,6]: # fr(4), sa(5), so(6)
            date = date+relativedelta(days=-(date.weekday()-3))
        date = date+relativedelta(weekday=FR)
        date2 = date+relativedelta(weekday=SU)
        header = 'Wochenende'
    elif timerange == 'monat':
        date = datetime_date.today()
        date2 = datetime.today()+timedelta(days=31)
        header = 'Monatsübersicht'
    entries = events.get_by_date(date, date2)
    if entries is None:
        abort(404)
    return render_template('events/index.html', **locals())

 
@mod.route("/termine/by/tag/<tag>")
def termine_by_tag(tag):
    entries = events.get_by_tag(tag)
    header = "Tag: "+tag
    return render_template('events/index.html', **locals())


def fillup_event_form(event):
    f = Event_Form(obj=event)
    f.dtstart_date.data = event.dtstart.date()
    f.dtstart_time.data = event.dtstart.time()
    return f


@login_required
@mod.route("/termine/termin/<id>/edit", methods = ['GET', 'POST'])
def event_edit(id):
    permission = Edit_Event_Permission(id)
    form = Event_Form()
    if permission.can():
        event = events.get_or_404(id)
        if form.validate_on_submit():
            events.update(event, **form.data)
            events.save(event)

        form = fillup_event_form(event)
        context = {}
        context.update({ 'event': event})
        context.update({ 'form': form})
        context.update({ 'baseurl': current_app.config['UPLOADED_FLYERS_URL']})
        context.update({ 'size': 450})
        context.update({ 'date': datetime.now().date()})
        return render_template('events/edit.html', form=form, event=event)
    abort(403)
