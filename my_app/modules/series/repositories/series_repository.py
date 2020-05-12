from sqlalchemy import func
from sqlalchemy.orm import joinedload

from my_app.models import Series, Season
from my_app.modules.common.repositories.base_repository import BaseRepository


class SeriesRepo(BaseRepository):
    def __init__(self):
        super(SeriesRepo, self).__init__()
        self.model = Series

    def get_by_name(self, name):
        """
        fetch Series by name
        :param name: the name of Series to be fetched
        :return: a sports_ops.models.Series
        """
        return Series.query.filter(
            func.lower(Series.name) == func.lower(name)).first()

    def get_with_seasons_by_id(self, id):
        """
        fetch Series with Seasons by Series id
        :param id: Series id
        :return: a sports_ops.models.Series
        """
        return self.session().query(Series) \
            .options(joinedload(Series.seasons)) \
            .join(Season, Series.seasons) \
            .filter(Series.id == id) \
            .first()
