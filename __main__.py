import core

import argparse
import datetime

import logging

logger = logging.getLogger(__name__)

def setLogger(loglevel):
    if loglevel == 'debug':
        LOGLEVEL = logging.DEBUG
    elif loglevel == 'info':
        LOGLEVEL = logging.INFO
    elif loglevel == 'warning':
        LOGLEVEL = logging.WARNING
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(LOGLEVEL)
    streamHandler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))

    logger = logging.getLogger(__name__)
    logger.addHandler(streamHandler)
    logger.setLevel(LOGLEVEL)
    core_logger = logging.getLogger(core.__name__)
    core_logger.addHandler(streamHandler)
    core_logger.setLevel(LOGLEVEL)

def dateFormat(text):
    return datetime.datetime.strptime(text, '%Y%m%d')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('begin', type=dateFormat, help='検索範囲期間の始めを指定。(yyyymmdd)')
    parser.add_argument('end', type=dateFormat, help='検索範囲期間の終わりを指定。(yyyymmdd)')
    parser.add_argument('--out', '-o', default='records.sqlite3', type=str, help='保存先のデータベースのパス。')
    parser.add_argument('--update', '-u', action='store_true', help='重複したレコードを上書きする')
    parser.add_argument('--sleep', '-s', default=5, type=int, help='検索上限に達したときに、次のデータを再度検索するまでのスリープ時間')
    parser.add_argument('--debug', '-d', default='info', choices=['debug', 'info', 'warning'], type=str, help='表示するログレベル')
    args = parser.parse_args()

    setLogger(args.debug)

    lastTimeDelta = datetime.timedelta(hours=23, minutes=59, seconds=59)

    res = core.api.getJsonAuto(args.begin, args.end+lastTimeDelta, sleep=args.sleep)
    core.db.saveRecords(args.out, res, overwrite=args.update)

main()
