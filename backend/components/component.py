from abc import ABC, abstractmethod

class BaseComponent(ABC):
    @abstractmethod
    def generate_dxf(self, filepath: str):
        pass