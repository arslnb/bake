from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

bake = Flask(__name__, instance_relative_config=True)
bake.config.from_object('config')
bake.config.from_pyfile('config.py')

db = SQLAlchemy(bake)
migrate = Migrate(bake, db)

manager = Manager(bake)
manager.add_command('db', MigrateCommand)

from bake import views, models


