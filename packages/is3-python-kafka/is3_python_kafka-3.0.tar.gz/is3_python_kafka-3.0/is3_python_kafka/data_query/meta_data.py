from is3_python_kafka.utils.is3_request_util import RequestUtil


def get_meta_table_list():
    url = 'http://118.195.242.175:31900' + '/data-main/operation/getDataByCondition'
    data = {
        "prjId": "1763414873275895809",
        "metaTableCode": "temp_humidity_sensor",
        "startTime": "2000-01-01 00:00:00",
        "endTime": "2024-06-25 13:57:28",
        "keyValueCompareEnum": [
            {
                "field": "deviceCode",
                "compare": "EQ",
                "value": "temp_1"
            }
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "X-Access-Key": "KMWCDmr5g-rPLtA3X70RSQ",
        "X-Secret-Key": "RMM-KdGDO130-SS2brugn4asZKYchaq_MlHqWS-C3Fc"
    }
    return RequestUtil.post(url, data, headers)
