from ucloud.ufile import config as ufile_config
from ucloud.ufile import putufile
from ucloud.ufile import downloadufile
from ucloud.logger import logger
import logging
import config

logger.setLevel(logging.CRITICAL)
ufile_config.set_default(connection_timeout=60)
ufile_config.set_default(expires=None)


class UFile(object):
    config.ufile['public_key']
    __public_key = config.ufile['public_key']
    __private_key = config.ufile['private_key']
    __bucket = config.ufile['bucket']

    __pf = putufile.PutUFile(__public_key, __private_key)
    __dl = downloadufile.DownloadUFile(__public_key, __private_key)

    @classmethod
    def put_stream(cls, path, stream):
        return cls.__pf.putstream(cls.__bucket, path, stream)

    @classmethod
    def get_dl_url(cls, path):
        return cls.__dl.private_download_url(cls.__bucket, path, expires=None)
