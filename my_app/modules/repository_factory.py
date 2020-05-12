from my_app.modules.series.repositories.series_repository import SeriesRepo


class RepositoryFactory(object):
    """
    Provides repo
    """

    def __init__(self):
        # Initialize all Repositories corresponding to all models here
        self.series_repository = SeriesRepo()


repo_factory = RepositoryFactory()
