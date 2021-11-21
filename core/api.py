import requests
import json
import time
import datetime

from .utils import convertToDatetime, wait

import logging

logger = logging.getLogger(__name__)

basedata = {
 "mode": "search",
 "dateTimeF[]": ["2021-01-01", "00:00"],
 "dateTimeT[]": ["2021-01-01", "23:59"],
 "Comp": "C0",
 "Sort": "S0",
 "additionalC": False,
 "boundsAr[]": [],
 "city[]": ["99"],
 "dep[]": ["000", "999"],
 "epi[]": ["99"],
 "mag[]": ["0.0", "9.9"],
 "maxInt": 1,
 "obsInt": 1,
 "observed": True,
 "pref[]": ["25"],
 "seisCount": False,
 "station[]": ["99"]
}

url = 'https://www.data.jma.go.jp/svd/eqdb/data/shindo/api/api.php'

def getJson(begin, end, order='old'):
    data = basedata.copy()

    if order == 'new':
        data['Sort'] = 'S0'
    elif order == 'old':
        data['Sort'] = 'S1'


    data['dateTimeF[]'][0] = begin.strftime('%Y-%m-%d')
    data['dateTimeF[]'][1] = begin.strftime('%H:%M')
    data['dateTimeT[]'][0] = end.strftime('%Y-%m-%d')
    data['dateTimeT[]'][1] = end.strftime('%H:%M')

    res = requests.post(url, data=data)
    
    return res.json()

def getJsonAuto(begin, end, sleep=5):
    logger.info('getting json data at auto : {} ~ {}'.format(begin, end))

    records = {}
    while 1:
        logger.info('downloading json : {} ~ {}'.format(begin, end))
        res = getJson(begin, end)

        if type(res['res']) is not list:
            # resの中身がなかった場合エラーを起こす
            errorMessage = 'api query error : {}'.format(res['res'])
            logger.critical(errorMessage)
            raise Exception(errorMessage)

        logger.debug('result : {} items'.format(len(res['res'])))

        # 取得結果を辞書に保存
        duplicateCount = 0
        for i in res['res']:
            if i['id'] in records:
                # 重複しているデータの場合はカウントしてスキップ
                duplicateCount += 1
            else:
                # 重複していない場合は追加
                records[i['id']] = i

        logger.debug('duplicate {} items'.format(duplicateCount))

        # apiの件数制限を超えた場合、検索結果の最後尾の日時から再検索する
        if '上限を超えました' in res['str'][1]:
            logger.info('reach the api limit')
            logger.debug('last record time is : {}'.format(res['res'][-1]['ot']))

            newBegin = convertToDatetime(res['res'][-1]['ot'])
            logger.info('next begin datetime is : {}'.format(newBegin))

            if newBegin == begin:
                logger.critical('getting auto error : infinity loop')
                raise Exception('getting auto error : infinity looop')

            begin = newBegin
            
            logger.debug('sleeping {} seconds'.format(sleep))

            wait(sleep)
            continue
        else:
            break

    logger.info('{} records was found'.format(len(records)))

    logger.info('sorting')

    ret = sorted(list(records.values()), key=lambda i: i['id'])

    logger.info('getting is complete')

    return ret



