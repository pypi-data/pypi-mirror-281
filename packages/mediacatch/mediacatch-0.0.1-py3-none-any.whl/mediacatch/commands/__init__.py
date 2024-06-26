from abc import ABC, abstractmethod
from argparse import ArgumentParser


class BaseCLICommand(ABC):
    @staticmethod
    @abstractmethod
    def register_subcommand(parser: ArgumentParser):
        raise NotImplementedError()

    @staticmethod
    def run(self):
        raise NotImplementedError()
