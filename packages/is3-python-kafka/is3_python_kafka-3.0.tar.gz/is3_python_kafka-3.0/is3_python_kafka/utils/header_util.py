from is3_python_kafka.utils.load_config import load_config


def get_header(filePath, key):
    # 上传的文件路径
    key_config = load_config(filePath)[key]
    headers = {
        'Content-Type': 'application/json',
        'X-Access-Key': key_config.get('X-Access-Key'),
        'X-Secret-Key': key_config.get('X-Secret-Key')
    }
    return headers
