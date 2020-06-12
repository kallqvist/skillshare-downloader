import requests
import json
import sys
import re
import os
from slugify import slugify
import cloudscraper
from bs4 import BeautifulSoup as BS


class Downloader(object):
    def __init__(
        self,
        cookie,
        download_path=os.environ.get('FILE_PATH', './data'),
        pk='BCpkADawqM2OOcM6njnM7hf9EaK6lIFlqiXB0iWjqGWUQjU7R8965xUvIQNqdQbnDTLz0IAO7E6Ir2rIbXJtFdzrGtitoee0n1XXRliD-RH9A-svuvNW9qgo3Bh34HEZjXjG4Nml4iyz3KqF',
        brightcove_account_id=3695997568001,
    ):
        self.cookie = cookie.strip().strip('"')
        self.download_path = download_path
        self.pk = pk.strip()
        self.brightcove_account_id = brightcove_account_id
        self.pythonversion = 3 if sys.version_info >= (3, 0) else 2

    def is_unicode_string(self, string):
        if (self.pythonversion == 3 and isinstance(string, str)) or (self.pythonversion == 2 and isinstance(string, unicode)):
            return True

        else:
            return False

    def download_course_by_url(self, url):
        m = re.match(r'https://www.skillshare.com/classes/.*?/(\d+)', url)

        if not m:
            raise Exception('Failed to parse class ID from URL')

        self.download_course_by_class_id(m.group(1))

    def download_course_by_class_id(self, class_id):
        data = self.fetch_course_data_by_class_id(class_id=class_id)
        teacher_name = None

        if 'vanity_username' in data['_embedded']['teacher']:
            teacher_name = data['_embedded']['teacher']['vanity_username']

        if not teacher_name:
            teacher_name = data['_embedded']['teacher']['full_name']

        if not teacher_name:
            raise Exception('Failed to read teacher name from data')

        if self.is_unicode_string(teacher_name):
            teacher_name = teacher_name.encode('ascii', 'replace')

        title = data['title']

        if self.is_unicode_string(title):
            title = title.encode('ascii', 'replace')  # ignore any weird char

        base_path = os.path.abspath(
            os.path.join(
                self.download_path,
                slugify(teacher_name),
                slugify(title),
            )
        ).rstrip('/')

        if not os.path.exists(base_path):
            os.makedirs(base_path)

        for u in data['_embedded']['units']['_embedded']['units']:
            for s in u['_embedded']['sessions']['_embedded']['sessions']:
                video_id = None

                if 'video_hashed_id' in s and s['video_hashed_id']:
                    video_id = s['video_hashed_id'].split(':')[1]

                if not video_id:
                    # NOTE: this happens sometimes...
                    # seems random and temporary but might be some random
                    # server-side check on user-agent etc?
                    # ...think it's more stable now with those set to
                    # emulate an android device
                    raise Exception('Failed to read video ID from data')

                s_title = s['title']

                if self.is_unicode_string(s_title):
                    s_title = s_title.encode('ascii', 'replace')  # ignore any weird char

                file_name = '{} - {}'.format(
                    str(s['index'] + 1).zfill(2),
                    slugify(s_title),
                )

                self.download_video(
                    fpath='{base_path}/{session}.mp4'.format(
                        base_path=base_path,
                        session=file_name,
                    ),
                    video_id=video_id,
                )

                print('')

    def fetch_course_data_by_class_id(self, class_id):
        url = 'https://api.skillshare.com/classes/{}'.format(class_id)
        scraper = cloudscraper.create_scraper(
            browser={
                'custom': 'Skillshare/4.1.1; Android 5.1.1',
            },
            delay=10
        )

        res = scraper.get(
            url,
            headers={
                'Accept': 'application/vnd.skillshare.class+json;,version=0.8',
                'User-Agent': 'Skillshare/4.1.1; Android 5.1.1',
                'Host': 'api.skillshare.com',
                'cookie': self.cookie,
            }
        )

        if not res.status_code == 200:
            raise Exception('Fetch error, code == {}'.format(res.status_code))

        return res.json()

    def download_video(self, fpath, video_id):
        meta_url = 'https://edge.api.brightcove.com/playback/v1/accounts/{account_id}/videos/{video_id}'.format(
            account_id=self.brightcove_account_id,
            video_id=video_id,
        )

        scraper = cloudscraper.create_scraper(
            browser={
                'custom': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3',
            },
            delay=10
        )

        meta_res = scraper.get(
            meta_url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive',
                'Accept': 'application/json;pk={}'.format(self.pk),
                'Origin': 'https://www.skillshare.com'
            }
        )

        if meta_res.status_code != 200:
            raise Exception('Failed to fetch video meta')

        if meta_res.json()['sources'][6]['container'] == 'MP4' and 'src' in meta_res.json()['sources'][6]:
            dl_url = meta_res.json()['sources'][6]['src']
            # break
        else:
            dl_url = meta_res.json()['sources'][1]['src']

        print('Downloading {}...'.format(fpath))

        if os.path.exists(fpath):
            print('Video already downloaded, skipping...')
            return

        with open(fpath, 'wb') as f:
            response = requests.get(dl_url, allow_redirects=True, stream=True)
            total_length = response.headers.get('content-length')

            if not total_length:
                f.write(response.content)

            else:
                dl = 0
                total_length = int(total_length)

                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()

            print('')
