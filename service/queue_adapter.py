"""
队列服务适配器

@author sven
@create 2021-05-07
"""
from utils.log_util import get_logger
from utils.module_util import load_all_classes
from service.queue_service.base_service import BaseService

all_queue_service = load_all_classes(['service.queue_service'], "queue_type", BaseService)


class QueueAdapter:
    def __init__(self):
        self.log = get_logger("queue_adapter.log")

    def get_queue_service(self, queue_type):
        if queue_type not in all_queue_service:
            self.log.info("“{}”没有对应的类".format(queue_type))
            return None
        queue_service = all_queue_service[queue_type]
        return queue_service

    def get_message(self, target_obj, queue_name):
        if not hasattr(target_obj, "get_message"):
            self.log.info("传入的对象没有实现get_message方法")
            return
        return target_obj.get_message(queue_name)


# if __name__ == "__main__":
#     obj = QueueAdapter()
#     print(obj.get_queue_service("mns"))
