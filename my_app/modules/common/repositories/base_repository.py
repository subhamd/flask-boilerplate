from my_app import extensions

from my_app.exceptions.custom_exception import InvalidRequestException, RecordNotFoundInDBException


class BaseRepository(object):
    """
    Base repository
    """

    def __init__(self, db=None):
        self.db = db or extensions.db
        self.model = None  # set this in the subclass (child class)

    def session(self):
        """
        returns session
        :return:
        """
        return self.db.session

    def add(self, item):
        """
        adds the specified model instance in DB
        :param item: the model instance to be inserted in DB
        :return: Inserted model instance with id
        """
        self.session().add(item)
        self.session().flush()

        self.session().refresh(item)
        return item

    def add_all(self, items, return_with_created_ids=False):
        """
        adds multiple model instances in DB
        :param items: model instances to be inserted in DB
        :param return_with_created_ids: a bool

        If set to True, ids of the records being inserted will be returned but the records will be inserted one by one,
        in a sequence. Resultant query would look like the following:

            INSERT INTO table (column1, column2, columnN) VALUES (value1, value2, valueN) RETURNING id;
            INSERT INTO table (column1, column2, columnN) VALUES (value11, value22, valueNN) RETURNING id;
            INSERT INTO table (column1, column2, columnN) VALUES (value111, value222, valueNNN) RETURNING id;

        If set to False, ids of the records being inserted will be not be returned but the records will be inserted at
        once, i.e., bulk insert operation would be performed. Resultant query would look like the following:

            INSERT INTO table (column1, column2, columnN) VALUES
                (value1, value2, valueN),
                (value11, value22, valueNN),
                (value111, value222, valueNNN);

        :return: Inserted model instances with id set or unset based on the value of param: return_with_created_ids
        """
        self.session().bulk_save_objects(items, return_defaults=return_with_created_ids)
        self.session().flush()
        return items

    def update(self, item):
        """
        updates the specified model instance in DB
        :param item: the model instance to be updated in DB
        :return: Updated model instance
        """
        self.session().add(item)
        self.session().flush()

        self.session().refresh(item)
        return item

    def update_all(self, mappings):
        """

        :param mappings:
        """
        model = self._get_model()

        self.session().bulk_update_mappings(model, mappings)
        self.session().flush()

    def update_attributes(self, item, **kwargs):
        """
        updates the specified model instance's attributes in DB
        :param item: the model instance to be updated in DB
        :param kwargs: key-value pairs of attributes that need to be updated
        :return: Updated model instance
        """
        for k, v in kwargs.items():
            if k not in item.__dict__.keys():
                raise InvalidRequestException('Invalid attribute: %s' % k)
            setattr(item, k, v)

        self.update(item)

    def delete(self, item):
        """
        Deletes the specified model instance in DB
        :param item: the model instance to be deleted
        """
        self.session().delete(item)
        self.session().flush()

    def delete_by_id(self, id):
        """
        Deletes the model instance in DB corresponding to the id
        :param id: the id of the model instance to be deleted
        """
        model = self._get_model()

        model.query.get(id).delete()
        self.session().flush()

    def get_all(self):
        """
        fetch all instances from DB corresponding to a model
        :return: a list of model instances
        """
        model = self._get_model()

        return model.query.all()

    def get_by_id(self, id):
        """
        fetch a model instance from DB corresponding to the id
        :param id: the id of the model instance to be fetched
        :return: A model instance or None if no instance exists corresponding to the id
        """
        model = self._get_model()

        return model.query.get(id)

    def get_by_ids(self, ids):
        """
        fetch model instances from DB corresponding to the ids
        :param ids: ids of the model instances to be fetched
        :return: a list of model instances
        """
        model = self._get_model()

        return model.query.filter(model.id.in_(ids)).all()

    def _get_model(self):
        if not self.model:
            raise InvalidRequestException('Attr: model not set')

        return self.model
