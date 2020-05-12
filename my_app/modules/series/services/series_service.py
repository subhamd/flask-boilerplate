from my_app.constants import Constants
from my_app.exceptions.custom_exception import RecordAlreadyExistInDBException, RecordNotFoundInDBException, \
    KeysNotPresentException, InvalidRequestException
from my_app.models import Series
from my_app.utils.validation_utils import validate_required_keys, validate_for_null_and_empty


class SeriesService:
    def __init__(self, series_repo):
        self.series_repo = series_repo

    def add_series(self, request_data):
        """
        Add a Series in DB from request_data
        :param request_data: a dict
        :return:
        """

        try:
            validate_required_keys(request_data, [Constants.NAME])
        except KeysNotPresentException as e:
            raise InvalidRequestException(f'{e.developer_message} in request body') from None

        series = Series(**request_data)
        return self.series_repo.add(series)

    def update_series(self, series_id, request_data):
        series = self.series_repo.get_by_id(series_id)
        if not series:
            raise RecordNotFoundInDBException(f'Series with id: {series_id} does not exist')

        name = request_data.get(Constants.NAME)
        if name and series.name.lower() != name.lower():
            series = self.series_repo.get_by_name(name)
            if series:
                raise RecordAlreadyExistInDBException(
                    f'Series with name: {name} already exists')
            series.name = name

        if Constants.DISPLAY_NAME in request_data.keys():
            series.display_name = request_data.get(Constants.DISPLAY_NAME)

        return self.series_repo.update(series)

    def get_series_by_id(self, series_id):
        series = self.series_repo.get_by_id(series_id)
        if not series:
            raise RecordNotFoundInDBException(f'Series with id: {series_id} does not exist')

        return series

    def get_series_by_name(self, series_name):
        series = self.series_repo.get_by_name(series_name)
        if not series:
            raise RecordNotFoundInDBException(f'Series with name: {series_name} does not exist')

        return series

    def get_all_series(self):
        return self.series_repo.get_all()

    def delete_series_by_id(self, series_id):
        series = self.series_repo.get_with_seasons_by_id(series_id)
        if not series:
            raise RecordNotFoundInDBException(f'Series with id: {series_id} does not exist')

        if series.seasons:
            raise InvalidRequestException(f'Series has associated Season(s). Delete those first')

        self.series_repo.delete(series)
