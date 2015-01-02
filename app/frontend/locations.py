# coding: utf-8

from ..services import locations as location_service

from flask import Blueprint
from flask import render_template

mod = Blueprint('locations', __name__,
                template_folder='templates')

@mod.route("/orte")
def locations():
    locations = location_service.all()
    return render_template('locations/index.html', **locals() )

@mod.route("/orte/<int:id>")
def location_by_id(id):
    location = location_service.get_or_404(id)
    return render_template('locations/show.html', **locals() )


@mod.route("/orte/<regiontag>")
def location_region(regiontag):
    locations = location_service.get_by_region(regiontag)
    return render_template('locations/index.html', **locals())
