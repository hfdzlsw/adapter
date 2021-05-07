"""
mns服务

@author sven
@create 2021-05-06
"""
import traceback
from mns_sdk.mns.account import Account
from .base_service import BaseService
from utils.config_util import read_mns_config
from utils.log_util import get_logger


class MnsService(BaseService):
    queue_type = "mns"

    def __init__(self):
        self.log = get_logger("mns_service.log")
        self.account = ""
        try:
            accid, acckey, endpoint, token = read_mns_config()
            self.account = Account(endpoint, accid, acckey, token)
        except Exception as e:
            self.log.info(''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))
        self.wait_seconds = 3

    def get_message(self, queue_name):
        if not self.account:
            return
        queue = self.account.get_queue(queue_name)
        queue.set_encoding(True)
        while True:
            # 读取消息
            try:
                recv_msg = queue.receive_message(self.wait_seconds)
                self.log.info("Receive Message Succeed! ReceiptHandle:%s MessageBody:%s MessageID:%s" % (recv_msg.receipt_handle, recv_msg.message_body, recv_msg.message_id))
                yield recv_msg.message_body
            except Exception as e:
                # except MNSServerException as e:
                if e.type == u"QueueNotExist":
                    self.log.info("Queue not exist, please create queue before receive message.")
                    break
                elif e.type == u"MessageNotExist":
                    self.log.info("Queue is empty!")
                    break
                self.log.info("Receive Message Fail! Exception:%s\n" % e)
                continue

            # 删除消息
            try:
                queue.delete_message(recv_msg.receipt_handle)
                self.log.info("Delete Message Succeed!  ReceiptHandle:%s" % recv_msg.receipt_handle)
            except Exception as e:
                self.log.info("Delete Message Fail! Exception:%s\n" % ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))

