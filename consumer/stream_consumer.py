"""
转推流消费者

@author sven
@create 2021-05-06
"""
import time
from service.queue_adapter import QueueAdapter


if __name__ == "__main__":
    queue_adapter = QueueAdapter()
    service_class = queue_adapter.get_queue_service("mns")
    service_obj = service_class()
    while True:
        generator_obj = queue_adapter.get_message(service_obj, "TestQueueLiveTrans")
        for one in generator_obj:
            message = one.decode("utf-8")
        time.sleep(10)
