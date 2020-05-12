from sqlalchemy.orm import relationship

from my_app.extensions import db
from my_app.models.base_model import BaseModel, TimeStampMixin


class Series(BaseModel, TimeStampMixin):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(300))
    display_name = db.Column(db.VARCHAR(300))

    __tablename__ = 'series'

    seasons = relationship("Season", back_populates="series")

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.display_name = kwargs.get('display_name')
