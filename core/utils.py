import datetime
import time

import logging

logger = logging.getLogger(__name__)

def convertToDatetime(text):
    try:
        return datetime.datetime.strptime(text[:19], '%Y/%m/%d %H:%M:%S')
    except ValueError:
        pass

    # 秒数が無いデータ用
    try:
        return datetime.datetime.strptime(text[:16], '%Y/%m/%d %H:%M')
    except ValueError:
        pass

    # 秒、分数が無いデータ用
    try:
        return datetime.datetime.strptime(text[:13], '%Y/%m/%d %H')
    except ValueError:
        pass

    # 時刻が無いデータ用
    try:
        return datetime.datetime.strptime(text[:10], '%Y/%m/%d')
    except ValueError:
        pass

    # 日数が無いデータ用
    try:
        return datetime.datetime.strptime(text[:8], '%Y年%m月')
    except ValueError:
        logger.critical('datetime parse error : {}'.format(text))
        raise

def wait(seconds):
    now = seconds
    for i in range(seconds, 0, -1):
        print('\rwait: {}'.format(i), end='')
        time.sleep(1)
    print('\r' + ' '*20 + '\r', end='')

