from abc import ABC, abstractmethod
from typing import List
from alfred.models.result import AlfredResult

class Handler(ABC):
    def __init__(self, command: str):
        self.command = command

    @abstractmethod
    def handle(self, arg: List) -> AlfredResult:
        pass 