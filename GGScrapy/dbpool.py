from ggmssql.pool import Pool
import config


class DBPool(object):
    __pool = Pool(config.database['host'],
                  config.database['port'],
                  config.database['user'],
                  config.database['pswd'],
                  config.database['name'],
                  timeout=config.database['timeout'])

    @classmethod
    def acquire(cls):
        return cls.__pool.acquire()

    @classmethod
    def release(cls, conn):
        cls.__pool.release(conn)
