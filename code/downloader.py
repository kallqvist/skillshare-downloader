import requests
import json
import sys
import re
import os


class Downloader(object):
    def __init__(self,
                 cookie,
                 download_path='/data',
                 pk='BCpkADawqM2OOcM6njnM7hf9EaK6lIFlqiXB0iWjqGWUQjU7R8965xUvIQNqdQbnDTLz0IAO7E6Ir2rIbXJtFdzrGtitoee0n1XXRliD-RH9A-svuvNW9qgo3Bh34HEZjXjG4Nml4iyz3KqF',
                 brightcove_account_id=3695997568001,
                 ):
        self.cookie = cookie.strip()
        self.download_path = download_path
        self.pk = pk.strip()
        self.brightcove_account_id = brightcove_account_id

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
        if teacher_name is None:
            teacher_name = data['_embedded']['teacher']['full_name']
        if teacher_name is None:
            raise Exception('Failed to read teacher name from data')
        if isinstance(teacher_name, unicode):
            teacher_name = teacher_name.encode('ascii', 'replace')

        title = data['title']
        title = title.replace(":", "-") # prevent error when title have colon character
        title = title.replace(u'\u2018', "'")  # single quote left
        title = title.replace(u'\u2019', "'")  # signle quote right
        if isinstance(title, unicode):
            title = title.encode('ascii', 'replace')  # ignore any weird char

        base_path = '{download_path}/{teacher_name}/{class_name}/'.format(
            download_path=self.download_path.rstrip('/'),
            teacher_name=teacher_name,
            class_name=title,
        ).rstrip('/')
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        for u in data['_embedded']['units']['_embedded']['units']:
            for s in u['_embedded']['sessions']['_embedded']['sessions']:
                video_id = None
                if 'video_hashed_id' in s and s['video_hashed_id']:
                    video_id = s['video_hashed_id'].split(':')[1]
                if video_id is None:
                    # NOTE: this happens sometimes...
                    # seems random and temporary but might be some random
                    # server-side check on user-agent etc?
                    # ...think it's more stable now with those set to
                    # emulate an android device
                    raise Exception('Failed to read video ID from data')

                s_title = s['title']
                s_title = s_title.replace(u'\u2018', "'")  # single quote left
                s_title = s_title.replace(u'\u2019', "'")  # signle quote right
                if isinstance(s_title, unicode):
                    s_title = s_title.encode('ascii', 'replace')  # ignore any weird char

                file_name = '{} - {}'.format(
                    str(s['index'] + 1).zfill(2),
                    s_title,
                )
                file_name = file_name.replace('/', '-')
                file_name = file_name.replace(':', '-')

                self.download_video(
                    fpath='{base_path}/{session}.mp4'.format(
                        base_path=base_path,
                        session=file_name,
                    ),
                    video_id=video_id,
                )
                print('')

    def fetch_course_data_by_class_id(self, class_id):
        res = requests.get(
            url='https://api.skillshare.com/classes/{}'.format(class_id),
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
        meta_res = requests.get(
            meta_url,
            headers={
                'Accept': 'application/json;pk={}'.format(self.pk),
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
                'Origin': 'https://www.skillshare.com'
            }
        )
        if meta_res.status_code != 200:
            raise Exception('Failed to fetch video meta')
        for x in meta_res.json()['sources']:
            if x['container'] == 'MP4' and 'src' in x:
                dl_url = x['src']
                break

        print('Downloading {}...'.format(fpath))
        fpath = re.sub(r'[*?:"<>|]',"",fpath)
        if os.path.exists(fpath):
            print('Video already downloaded, skipping...')
            return
        with open(fpath, 'wb') as f:
            response = requests.get(dl_url, allow_redirects=True, stream=True)
            total_length = response.headers.get('content-length')
            if total_length is None:
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )
                    sys.stdout.flush()
            print('')
