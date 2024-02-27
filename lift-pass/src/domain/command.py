from abc import abstractmethod, ABC


class Command(ABC):
    pass


class CommandHandler(ABC):
    @abstractmethod
    def execute(self, command: Command) -> None:
        raise NotImplementedError
