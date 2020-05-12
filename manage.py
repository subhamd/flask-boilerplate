from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from my_app.app import app
from my_app.extensions import db

migrate = Migrate(app, db, directory='my_app/migrations', compare_type=True)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
