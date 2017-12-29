# coding: utf8
import json
import time
import base64

import pow as poW
import captcha


POW = poW
CAPTCHA = captcha.captcha_valid()


def getNowTime():
    return int(time.time())  # 取十位


def formatTime(timestamp, format='%Y-%m-%d %H:%M:%S'):
    timeObj = time.localtime(int(timestamp))
    return time.strftime(format, timeObj)


def object2Json(dictObject):
    try:
        result = json.dumps(dictObject)
        return result
    except Exception, e:
        return False


def json2Object(jsonString):
    try:
        result = json.loads(jsonString)
        return result
    except Exception, e:
        return False


def base64Encode(raw):
    return base64.b64encode(raw)


def base64Decode(raw):
    return base64.b64decode(raw)
