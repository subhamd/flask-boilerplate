from enum import Enum

from sqlalchemy import CheckConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from my_app.extensions import db
from my_app.models.base_model import BaseModel, TimeStampMixin


class State(Enum):
    UPCOMING = 'U'
    LIVE = 'L'
    CONCLUDED = 'C'


class Season(BaseModel, TimeStampMixin):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(300))
    display_name = db.Column(db.VARCHAR(300))
    series_id = db.Column(db.INTEGER, db.ForeignKey('series.id'))
    state = db.Column(db.CHAR, nullable=False)
    start_date = db.Column(db.DateTime(timezone=True))
    end_date = db.Column(db.DateTime(timezone=True))
    total_episodes = db.Column(db.VARCHAR(200))
    thumbnail_url = db.Column(db.VARCHAR(200))

    __tablename__ = 'season'

    __table_args__ = (
        CheckConstraint(
            state.in_([state.value for state in State])),
    )

    series = relationship("Series")
    dynamic_attributes = relationship('SeasonAttribute', cascade="save-update, delete, delete-orphan")

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.display_name = kwargs.get('display_name')
        self.series_id = kwargs.get('series_id')
        self.state = kwargs.get('state')
        self.start_date = kwargs.get('start_date')
        self.end_date = kwargs.get('end_date')
        self.total_episodes = kwargs.get('total_episodes')
        self.thumbnail_url = kwargs.get('thumbnail_url')


class SeasonAttribute(BaseModel, TimeStampMixin):
    season_id = db.Column(db.INTEGER, db.ForeignKey('season.id'), nullable=False)
    key = db.Column(db.VARCHAR(100), nullable=False)
    value = db.Column(db.VARCHAR(2000))

    __table_args__ = (
        PrimaryKeyConstraint('season_id', 'key'),
    )

    __tablename__ = 'season_attribute'

    season = relationship("Season", back_populates="dynamic_attributes")

    def __init__(self, key, value, season_id=None):
        if season_id:
            self.season_id = season_id
        self.key = key
        self.value = value
