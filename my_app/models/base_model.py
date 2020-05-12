from datetime import datetime, date

from sqlalchemy import func

from my_app.extensions import db


class TimeStampMixin(object):
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())


class BaseModel(db.Model):
    """
    Base data model for all objects
    """
    __abstract__ = True

    def __repr__(self):
        """
        Define a base way to print models
        """
        return '%s(%s)' % (self.__class__.__name__, {
            column: value for column, value in self.__dict__.items()
        })

    def json(self):
        """
        Define a base way to jsonify models, dealing with datetime objects
        """
        data = {}
        for column, value in self.__dict__.items():
            if isinstance(value, (date, datetime, )):
                data[column] = value.strftime('%Y-%m-%d %H:%M:%S %z')
            elif isinstance(value, (BaseModel, )):
                data[column] = value.json()
            elif isinstance(value, (list, )) and len(value) > 0 and isinstance(value[0], (BaseModel, )):
                data[column] = [model.json() for model in value]
            else:
                data[column] = value

        data.pop('_sa_instance_state', None)
        data.pop('created_at', None)
        data.pop('updated_at', None)
        return data


def jsonify_models(models):
    if isinstance(models, (list,)):
        data = [model.json() for model in models]
    else:
        data = models.json()
    return data
