#!/usr/bin/env python
from flask.ext.script import Server, Manager


# from werkzeug.wsgi import DispatcherMiddleware


# application = DispatcherMiddleware(frontend_create_app(settings_override="app.config.Development"), {
#     '/api':    api_create_app(settings_override="app.config.Development")
# })

# frontend_app = frontend_create_app(settings_override="app.config.Development")
# migrate = Migrate(frontend_app, db)
# manager = Manager(frontend_app)

manager.add_command("runserver", Server())
# manager.add_command("assets", ManageAssets())
# manager.add_command('db', MigrateCommand)
# manager.add_command('adduser', UserAdd)


@manager.shell
def make_shell_context():
    from app.core import db
    from app.models import User, Location, Event, Flyer, Group, Event_Cache
    return dict(db=db, Flyer=Flyer, User=User, Event=Event, Location=Location, Event_Cache=Event_Cache, Group=Group)


if __name__ == "__main__":
    manager.run()
