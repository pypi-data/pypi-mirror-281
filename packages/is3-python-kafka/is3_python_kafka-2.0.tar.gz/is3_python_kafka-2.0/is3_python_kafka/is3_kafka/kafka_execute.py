import json

from ..custom.execute import Execute
from ..utils.kafka_component_util import kafkaComponent
from ..utils.redis_util import RedisUtil


class KafkaProcessor:
    def __init__(self, serverName):
        self.serverName = serverName
        self.group_id = 'data-central-group'
        self.kafka_component = kafkaComponent(topic=serverName, group_id=self.group_id)

    def processor(self, execute: Execute):
        serverName = self.serverName
        redisUtil = RedisUtil()
        while True:
            self.__init__(serverName)
            # 接收消息
            data = self.kafka_component.receive()
            # 算法处理
            custom = execute
            message = custom.execute_custom(data)
            taskId = message['taskId']
            taskInstanceId = message['taskInstanceId']
            h_key = str(taskId) + "_" + str(taskInstanceId)
            redisUtil.h_set(key="is3.task.result", h_key=h_key, value=json.dumps(message))
