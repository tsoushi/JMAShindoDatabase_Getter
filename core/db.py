import sqlite3

from .utils import convertToDatetime

import logging

logger = logging.getLogger(__name__)


def saveRecords(dbpath, records, overwrite=False):
    logger.info('saving records to database : {}'.format(dbpath))
    logger.debug('{} records suplised'.format(len(records)))

    checkDb(dbpath)

    db = sqlite3.connect(dbpath)

    insertSql = 'INSERT INTO records(id, time, time_orig, hypocenter_name, latitude, longitude, latitude_S, longitude_s, depth, magnitude, max_intensity, maxIcls, maxS, maxScls) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
    updateSql = 'UPDATE records SET id = ?, time = ?, time_orig = ?, hypocenter_name = ?, latitude = ?, longitude = ?, latitude_S = ?, longitude_s = ?, depth = ?, magnitude = ?, max_intensity = ?, maxIcls = ?, maxS = ?, maxScls = ?, log_updated_at = CURRENT_TIMESTAMP WHERE id = ?;'

    duplicateCount = 0
    addCount = 0
    for i in records:
        data = (i['id'], convertToDatetime(i['ot']), i['ot'], i['name'], i['latS'], i['lonS'], i['lat'], i['lon'], i['dep'], i['mag'], i['maxI'], i['maxIcls'], i['maxS'], i['maxScls'])

        # データベースに同じIDが存在していた場合
        if db.execute('SELECT 1 FROM records WHERE id = ?', (i['id'],)).fetchone():
            duplicateCount += 1
            if overwrite:
                logger.debug('duplicate record (id - {}): update this record'.format(i['id']))

                db.execute(updateSql, (*data, i['id']))
            else:
                logger.debug('duplicate record (id - {}): skip this record'.format(i['id']))
        else:
            db.execute(insertSql, data)
            addCount += 1

    logger.info('duplicate {} records'.format(duplicateCount))
    logger.info('new {} records'.format(addCount))

    db.commit()
    db.close()

    logger.info('saving is complete')

    
def checkDb(dbpath):
    db = None
    try:
        db = sqlite3.connect(dbpath)
        db.execute('SELECT * FROM records;')
    except sqlite3.OperationalError:
        logger.info('database {} was not initialized'.format(dbpath))
        initDb(dbpath)
    finally:
        if db:
            db.close()

def initDb(dbpath):
    logger.info('initializing database {}'.format(dbpath))

    db = sqlite3.connect(dbpath)
    db.execute('''\
CREATE TABLE records(
    id TEXT PRIMARY KEY,
    time TEXT,
    time_orig TEXT,
    hypocenter_name TEXT,
    latitude TEXT,
    longitude TEXT,
    latitude_S TEXT,
    longitude_S TEXT,
    depth TEXT,
    magnitude TEXT,
    max_intensity TEXT,
    maxIcls TEXT,
    maxS TEXT,
    maxScls TEXT,
    log_updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);''')
    db.close()

    logger.info('initializing is complete')

