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
            groupname = item['groupname'] if 'groupname' in item else spider.groupname
            groupname = groupname.strip() if isinstance(groupname, str) else None
            assert groupname is None or groupname != ''

            sitename = item['sitename'] if 'sitename' in item else None
            sitename = sitename.strip() if isinstance(sitename, str) else None
            assert sitename is not None and sitename != ''

            channel = item['channel'] if 'channel' in item else None
            channel = channel.strip() if isinstance(channel, str) else None
            assert channel is not None and channel != ''

            entry = item['entry'] if 'entry' in item else None
            entry = entry.strip() if isinstance(entry, str) else None
            assert entry is not None and entry != ''

            url = item['url'] if 'url' in item else None
            url = url.decode() if isinstance(url, bytes) else url
            url = url.strip() if isinstance(url, str) else None
            assert url is not None and url != ''

            title = item['title'] if 'title' in item else None
            title = title.strip() if isinstance(title, str) else None
            assert title is not None and title != ''

            source = item['source'] if 'source' in item else None
            source = source.strip() if isinstance(source, str) else None
            assert source is None or source != ''

            author = item['author'] if 'author' in item else None
            author = author.strip() if isinstance(author, str) else None
            assert author is None or author != ''

            pubtime = item['pubtime'] if 'pubtime' in item else None
            assert isinstance(pubtime, datetime)
            pubtime = item['pubtime'].strftime('%Y-%m-%d')

            content = item['content'] if 'content' in item else None
            content = content.strip() if isinstance(content, str) else None
            assert content is not None and content != ''
            if sys.maxunicode <= 0xFFFF:
                content = re.sub(r'[\uD800-\uDFFF][\uD800-\uDFFF]',
                                 lambda m: '&#' + str(struct.unpack('>L', m.group(0).encode('UTF-32-BE'))[0]), content)
            else:
                content = re.sub(r'[\U00010000-\U0010FFFF]', lambda m: '&#' + str(ord(m.group(0))), content)
            content = re.sub(r'<\s*[Aa][^<>]*>', '', content, flags=re.I)
            content = re.sub(r'<\s*/\s*[Aa]\s*>', '', content, flags=re.I)
            content = re.sub(r'<script(.|\n)+?</script>', '', content, flags=re.I)

            md5 = hashlib.md5()
            seed = 'sitename=' + quote(sitename)
            seed += '&channel=' + quote(channel)
            seed += '&entry=' + quote(entry)
            seed += '&url=' + quote(url)
            if title is not None:
                seed += '&title=' + quote(title)
            if source is not None:
                seed += '&source=' + quote(source)
            if author is not None:
                seed += '&author=' + quote(author)
            if pubtime is not None:
                seed += '&pubtime=' + quote(pubtime)
            if content is not None:
                seed += '&content=' + quote(content)
            md5.update(seed.encode('utf-8'))
            hkey = md5.hexdigest()

            conn = spider.dbPool.acquire()
            cursor = conn.cursor()
            try:
                table = config.news['db']['table']
                cursor.execute('SELECT TOP 1 hkey FROM ' + table + ' WHERE url_entry=%s AND url=%s ORDER BY tmstamp',
                               (entry, url,))
                row = cursor.fetchone()
                if row is None or row['hkey'] != hkey:
                    content = self.__transfer_image(hkey, url, content)
                if row is None:
                    cursor.execute(
                        'INSERT INTO ' + table + ' (hkey,groupname,sitename,channel,url_entry,url,title,source,author,publish_time,content) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (hkey, groupname, sitename, channel, entry, url, title, source, author, pubtime, content,))
                elif row['hkey'] != hkey:
                    cursor.execute(
                        'UPDATE ' + table + ' SET groupname=%s,sitename=%s,channel=%s,title=%s,source=%s,author=%s,publish_time=%s,content=%s WHERE hkey=%s',
                        (groupname, sitename, channel, title, source, author, pubtime, content, row['hkey'],))
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
            groupname = item['groupname'] if 'groupname' in item else spider.groupname
            groupname = groupname.strip() if isinstance(groupname, str) else None
            assert groupname is None or groupname != ''

            sitename = item['sitename'] if 'sitename' in item else None
            sitename = sitename.strip() if isinstance(sitename, str) else None
            assert sitename is not None and sitename != ''

            channel = item['channel'] if 'channel' in item else None
            channel = channel.strip() if isinstance(channel, str) else None
            assert channel is not None and channel != ''

            url = item['url'] if 'url' in item else None
            url = url.decode() if isinstance(url, bytes) else url
            url = url.strip() if isinstance(url, str) else None
            assert url is not None and url != ''

            fund_name = item['fund_name'] if 'fund_name' in item else None
            fund_name = fund_name.strip() if isinstance(fund_name, str) else None
            assert fund_name is not None and fund_name != ''

            statistic_date = item['statistic_date'] if 'statistic_date' in item else None
            assert isinstance(statistic_date, datetime)
            statistic_date = item['statistic_date'].strftime('%Y-%m-%d')

            fund_code = item['fund_code'] if 'fund_code' in item else None
            fund_code = fund_code.strip() if isinstance(fund_code, str) else None
            assert fund_code is None or fund_code != ''

            nav = item['nav'] if 'nav' in item else None
            assert nav is None or isinstance(nav, float) or isinstance(nav, int)

            added_nav = item['added_nav'] if 'added_nav' in item else None
            assert added_nav is None or isinstance(added_nav, float) or isinstance(added_nav, int)

            nav_2 = item['nav_2'] if 'nav_2' in item else None
            assert nav_2 is None or isinstance(nav_2, float) or isinstance(nav_2, int)

            added_nav_2 = item['added_nav_2'] if 'added_nav_2' in item else None
            assert added_nav_2 is None or isinstance(added_nav_2, float) or isinstance(added_nav_2, int)

            total_nav = item['total_nav'] if 'total_nav' in item else None
            assert total_nav is None or isinstance(total_nav, float) or isinstance(total_nav, int)

            share = item['share'] if 'share' in item else None
            assert share is None or isinstance(share, float) or isinstance(share, int)

            income_value_per_ten_thousand = item[
                'income_value_per_ten_thousand'] if 'income_value_per_ten_thousand' in item else None
            assert income_value_per_ten_thousand is None or isinstance(income_value_per_ten_thousand,
                                                                       float) or isinstance(
                income_value_per_ten_thousand, int)

            d7_annualized_return = item['d7_annualized_return'] if 'd7_annualized_return' in item else None
            assert d7_annualized_return is None or isinstance(d7_annualized_return, float) or isinstance(
                d7_annualized_return, int)

            md5 = hashlib.md5()
            seed = 'sitename=' + quote(sitename)
            seed += '&channel=' + quote(channel)
            seed += '&fund_name=' + quote(fund_name)
            seed += '&statistic_date=' + quote(statistic_date)
            if fund_code is not None:
                seed += '&fund_code=' + quote(fund_code)
            if nav is not None:
                seed += '&nav=' + quote(str(nav))
            if added_nav is not None:
                seed += '&added_nav=' + quote(str(added_nav))
            if nav_2 is not None:
                seed += '&nav_2=' + quote(str(nav_2))
            if added_nav_2 is not None:
                seed += '&added_nav_2=' + quote(str(added_nav_2))
            if total_nav is not None:
                seed += '&total_nav=' + quote(str(total_nav))
            if share is not None:
                seed += '&share=' + quote(str(share))
            if income_value_per_ten_thousand is not None:
                seed += '&income_value_per_ten_thousand=' + quote(str(income_value_per_ten_thousand))
            if d7_annualized_return is not None:
                seed += '&d7_annualized_return=' + quote(str(d7_annualized_return))
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
                        'INSERT INTO ' + table + ' (hkey,groupname,sitename,channel,url,fund_name,statistic_date,fund_code,nav,added_nav,nav_2,added_nav_2,total_nav,share,income_value_per_ten_thousand,d7_annualized_return) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                        (hkey, groupname, sitename, channel, url, fund_name, statistic_date, fund_code, nav, added_nav,
                         nav_2, added_nav_2, total_nav, share, income_value_per_ten_thousand, d7_annualized_return,))
                elif row['hkey'] != hkey:
                    cursor.execute(
                        'UPDATE ' + table + ' SET hkey=%s,groupname=%s,url=%s,fund_code=%s,nav=%s,added_nav=%s,nav_2=%s,added_nav_2=%s,total_nav=%s,share=%s,income_value_per_ten_thousand=%s,d7_annualized_return=%s WHERE hkey=%s',
                        (hkey, groupname, url, fund_code, nav, added_nav, nav_2, added_nav_2, total_nav, share,
                         income_value_per_ten_thousand, d7_annualized_return, row['hkey'],))
            finally:
                cursor.close()
                spider.dbPool.release(conn)
        except:
            spider.crawler.engine.close_spider(spider, 'pipeline error!')
            spider.crawler.stats.set_value('exit_emsg', traceback.format_exc())
            spider.crawler.stats.set_value('exit_code', 1)
        finally:
            return item
