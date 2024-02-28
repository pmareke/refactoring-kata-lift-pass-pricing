from abc import abstractmethod, ABC


class Query(ABC):
    pass


class QueryHandler(ABC):
    @abstractmethod
    def execute(self, command: Query) -> list:
        raise NotImplementedError
