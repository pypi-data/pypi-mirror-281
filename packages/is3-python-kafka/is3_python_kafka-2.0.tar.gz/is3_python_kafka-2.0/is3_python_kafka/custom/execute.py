from abc import ABC, abstractmethod


# 定义抽象基类
class Execute(ABC):
    @abstractmethod
    def execute_custom(self, data):
        pass
