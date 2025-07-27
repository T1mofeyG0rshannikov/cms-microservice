import abc


class BaseDBFilters:
    @abc.abstractmethod
    def db_field_mappers(cls):
        ...

    @abc.abstractmethod
    def get_special_queries(cls):
        ...

    @abc.abstractmethod
    def build_query(self):
        ...
