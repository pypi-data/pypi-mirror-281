import requests

from .is3_request_util import RequestUtil


def invoke_plugin_log(message, headers):
    url = "http://118.195.242.175:31900/is3-modules-job/task/log/plugin/log"

    try:
        request_util = RequestUtil()
        response = request_util.post(url, message, headers)
        print("log response:：", response)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
