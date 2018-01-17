import re
import sys
import ssl
import time
import struct
import socket
import hashlib
import traceback
from urllib import request
from datetime import datetime
from urllib.parse import quote
from urllib.error import URLError
from urllib.error import HTTPError
from http.client import IncompleteRead
from urllib.parse import urljoin
from urllib.parse import urlparse
from .ufile import UFile
from GGScrapy.settings import DEFAULT_REQUEST_HEADERS
import config


# 新闻资讯Pipeline
class GGNewsPipeline(object):
    def process_item(self, item, spider):
        try:
            sitename = item['sitename']
            channel = item['channel']
            url = item['url']

            md5 = hashlib.md5()
            md5.update(url.encode('utf-8'))
            hkey = md5.hexdigest()

            if 'groupname' in item:
                groupname = item['groupname']
            else:
                groupname = None

            title = item['title']
            if title is not None:
                title = title.strip()
            if title is None or len(title) < 1:
                return item

            source = item['source']
            if source is not None:
                source = source.strip()

            author = item['author']
            if author is not None:
                author = author.strip()

            pubtime = item['pubtime']
            if pubtime is not None:
                pubtime = pubtime.strip()
            if pubtime is None or len(pubtime) < 1:
                return item

            content = item['content']
            if content is None or len(content.strip()) < 1:
                return item
            if sys.maxunicode <= 0xFFFF:
                content = re.sub(r'[\uD800-\uDFFF][\uD800-\uDFFF]',
                                 lambda m: '&#' + str(struct.unpack('>L', m.group(0).encode('UTF-32-BE'))[0]), content)
            else:
                content = re.sub(r'[\U00010000-\U0010FFFF]', lambda m: '&#' + str(ord(m.group(0))), content)
            content = re.sub(r'<\s*[Aa][^<>]*>', '', content, flags=re.I)
            content = re.sub(r'<\s*/\s*[Aa]\s*>', '', content, flags=re.I)
            content = re.sub(r'<script(.|\n)+?</script>', '', content, flags=re.I)

            conn = spider.dbPool.acquire()
            cursor = conn.cursor()
            try:
                table = config.news['db']['table']
                cursor.execute('select top 1 * from ' + table + ' where hkey=%s', (hkey,))
                row = cursor.fetchone()
                if row is None or spider.update:
                    content = self.__transfer_image(hkey, url, content)
                if row is None:
                    cursor.execute(
                        'INSERT INTO ' + table + ' (hkey, sitename, channel, groupname, url, title, source, author, publish_time, content) \
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (hkey, sitename, channel, groupname, url, title, source, author, pubtime, content,))
                elif spider.update:
                    cursor.execute(
                        'UPDATE ' + table + ' SET sitename=%s, channel=%s, groupname=%s, title=%s, source=%s, author=%s, publish_time=%s, content=%s \
                         WHERE hkey=%s',
                        (sitename, channel, groupname, title, source, author, pubtime, content, hkey,))
            finally:
                cursor.close()
                spider.dbPool.release(conn)
        except:
            spider.crawler.engine.close_spider(spider, 'pipeline error!')
            spider.crawler.stats.set_value('exit_emsg', traceback.format_exc())
            spider.crawler.stats.set_value('exit_code', 1)
        finally:
            return item

    @staticmethod
    def __transfer_image(hkey, url, content):
        headers = DEFAULT_REQUEST_HEADERS.copy()
        headers['Accept'] = 'image/webp,image/apng,image/*,*/*;q=0.8'
        headers['Referer'] = url

        def download(src, attempt=3, timeout=30):
            for i in range(attempt):
                req = request.Request(src, headers=headers)
                try:
                    rsp = request.urlopen(req, timeout=timeout, context=ssl._create_unverified_context())
                except HTTPError as e:
                    if e.code == 403 and urlparse(src).netloc == urlparse(url).netloc:
                        raise
                    else:
                        traceback.print_exc()
                        break
                except URLError:
                    traceback.print_exc()
                    break
                except (socket.timeout, ConnectionError):
                    traceback.print_exc()
                    if i + 1 >= attempt:
                        break
                    else:
                        time.sleep(5)
                        continue
                if rsp.status == 200:
                    info = rsp.info()
                    mtype = info.get_content_maintype()
                    stype = info.get_content_subtype()
                    if mtype.lower() == 'image':
                        try:
                            b = rsp.read()
                        except (socket.timeout, ConnectionError, IncompleteRead):
                            traceback.print_exc()
                            if i + 1 >= attempt:
                                break
                            else:
                                time.sleep(5)
                                continue
                        md5 = hashlib.md5()
                        md5.update(b)
                        h = md5.hexdigest()
                        ext = stype
                        if stype == 'jpeg':
                            ext = 'jpg'
                        f = h + '.' + ext
                        return f, b
            return None, None

        def replace(m):
            prefix = m.group(1)
            src = m.group(3).strip()
            suffix = m.group(4)

            if src[0:5].lower() != 'data:':
                src = urljoin(url, src)
                attempt = 3
                f, b = download(src, attempt, 30)
                if f is not None:
                    path = config.news['ufile']['group'] + '/' + hkey[0:2] + '/' + hkey + '/' + f
                    for i in range(attempt):
                        ret, resp = UFile.put_stream(path, b)
                        if resp.status_code == 200:
                            src = UFile.get_dl_url(path)
                            break

            text = prefix + src + suffix
            return text

        return re.sub(r'(<img(\s+?[^<>\n]+?)*?\s+?src=")([^<">\n]+?)("(\s+?[^<>\n]+?)*?>)', replace, content,
                      flags=re.I)


# 基金净值Pipeline
class GGFundNavPipeline(object):
    def process_item(self, item, spider):
        try:
            sitename = item['sitename']
            channel = item['channel']
            url = item['url']

            if 'groupname' in item:
                groupname = item['groupname']
            else:
                groupname = spider.groupname

            fund_name = item['fund_name']
            assert isinstance(fund_name, str)
            fund_name = fund_name.strip()
            assert len(fund_name) >= 1

            statistic_date = item['statistic_date']
            assert isinstance(statistic_date, datetime)
            statistic_date = item['statistic_date'].strftime('%Y-%m-%d')

            nav = item['nav'] if 'nav' in item else None
            assert nav is None or isinstance(nav, float) or isinstance(nav, int)

            added_nav = item['added_nav'] if 'added_nav' in item else None
            assert added_nav is None or isinstance(added_nav, float) or isinstance(nav, int)

            nav_2 = item['nav_2'] if 'nav_2' in item else None
            assert nav_2 is None or isinstance(nav_2, float) or isinstance(nav, int)

            added_nav_2 = item['added_nav_2'] if 'added_nav_2' in item else None
            assert added_nav_2 is None or isinstance(added_nav_2, float) or isinstance(nav, int)

            md5 = hashlib.md5()
            seed = 'sitename=' + quote(sitename)
            seed += '&channel=' + quote(channel)
            seed += '&fund_name=' + quote(fund_name)
            seed += '&statistic_date=' + quote(statistic_date)
            seed += '&nav=' + quote(str(nav))
            seed += '&added_nav=' + quote(str(added_nav))
            md5.update(seed.encode('utf-8'))
            hkey = md5.hexdigest()

            conn = spider.dbPool.acquire()
            cursor = conn.cursor()
            try:
                table = config.fund_nav['db']['table']
                cursor.execute(
                    'SELECT TOP 1 hkey FROM ' + table + ' WHERE sitename=%s AND channel=%s AND fund_name=%s AND statistic_date=%s ORDER BY tmstamp',
                    (sitename, channel, fund_name, statistic_date,))
                row = cursor.fetchone()
                if row is None:
                    cursor.execute(
                        'INSERT INTO ' + table + ' (hkey, sitename, channel, url, groupname, fund_name, statistic_date, nav, added_nav, nav_2, added_nav_2) \
                                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (hkey, sitename, channel, url, groupname, fund_name, statistic_date, nav, added_nav, nav_2,
                         added_nav_2,))
                elif row['hkey'] != hkey:
                    cursor.execute(
                        'UPDATE ' + table + ' SET hkey=%s, url=%s, groupname=%s, nav=%s, added_nav=%s, nav_2=%s, added_nav_2=%s WHERE hkey=%s',
                        (hkey, url, groupname, nav, added_nav, nav_2, added_nav_2, row['hkey'],))
            finally:
                cursor.close()
                spider.dbPool.release(conn)
        except:
            spider.crawler.engine.close_spider(spider, 'pipeline error!')
            spider.crawler.stats.set_value('exit_emsg', traceback.format_exc())
            spider.crawler.stats.set_value('exit_code', 1)
        finally:
            return item
