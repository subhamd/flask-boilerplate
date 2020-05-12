from my_app.modules.repository_factory import repo_factory
from my_app.modules.series.services.series_service import SeriesService
from my_app.constants import Constants
from my_app.exceptions.custom_exception import ServiceNotFoundException


class ServiceFactory:
    def __init__(self):
        self.services = {}

    def register_service(self, service_name, service_instance):
        self.services[service_name] = service_instance

    def get_service(self, service_name):
        if service_name in self.services:
            return self.services[service_name]
        else:
            raise ServiceNotFoundException('Service: {service_name} not found'.
                                           format(service_name=service_name))


service_factory = ServiceFactory()

services = [
    {'service_class': SeriesService, 'name': Constants.SERIES_SERVICE,
     'repo': repo_factory.series_repository}
]

for item in services:
    service = item['service_class'](item['repo'])
    service_factory.register_service(item['name'], service)
