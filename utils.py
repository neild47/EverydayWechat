import os


def isDebug():
    return os.getenv("DEBUG")


def isJson(resp):
    '''
    判断数据是否能被 Json 化。 True 能，False 否。
    :param resp: request
    :return: bool, True 数据可 Json 化；False 不能 JOSN 化。
    '''
    try:
        resp.json()
        return True
    except:
        return False
