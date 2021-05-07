"""
队列服务基础类

@author sven
@create 2021-05-07
"""
from abc import ABCMeta, abstractmethod


class BaseService:
    __metaclass__ = ABCMeta
    queue_type = ""

    @abstractmethod
    def get_message(self, queue_name):
        pass


