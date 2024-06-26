import requests

from is3_python_kafka.domain.data_dto import DataEntity
from .is3_request_util import RequestUtil


def invoke_plugin_log(message, dataDto: DataEntity):
    url = "http://118.195.242.175:31900/is3-modules-job/task/log/plugin/log"

    try:
        log = {
            'message': message,
            'taskId': dataDto.taskId,
            'logId': dataDto.logId,
            'pluginCode': dataDto.serverName,
            'nodeId': dataDto.nodeId,
            'prjId': dataDto.prjId
        }

        print("log:", log)
        response = RequestUtil.post(url, log, dataDto.headers)
        print("log-response:", response)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
