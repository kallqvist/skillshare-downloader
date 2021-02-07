import requests
import json
import sys
import re
import os
from slugify import slugify


class Downloader(object):
    def __init__(
        self,
        cookie,
        subtitle_lang,
        download_path=os.environ.get('FILE_PATH', './data'),
        pk='BCpkADawqM2OOcM6njnM7hf9EaK6lIFlqiXB0iWjqGWUQjU7R8965xUvIQNqdQbnDTLz0IAO7E6Ir2rIbXJtFdzrGtitoee0n1XXRliD-RH9A-svuvNW9qgo3Bh34HEZjXjG4Nml4iyz3KqF',
        brightcove_account_id=3695997568001,
    ):
        self.cookie = cookie.strip().strip('"')
        self.download_path = download_path
        self.subtitle_lang = subtitle_lang
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
        res = requests.get(
            url='https://api.skillshare.com/classes/{}'.format(class_id),
            headers={
                'Accept': 'application/vnd.skillshare.class+json;,version=0.8',
                'User-Agent': 'Skillshare/5.3.0; Android 9.0.1',
                'Host': 'api.skillshare.com',
                'Referer': 'https://www.skillshare.com/',
                'cookie': self.cookie,
            }
        )

        if not res.status_code == 200:
            raise Exception('Fetch error, code == {}'.format(res.status_code))

        return res.json()
    def download_subtitle(self,fpath,st_url):
        print('Downloading subtitles...')
        
        res = requests.get(
            url=st_url,
            headers={
                'Accept': 'text/plain,text/html',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
                'Origin': 'https://www.skillshare.com'
            }
        )
        
        if not res.status_code == 200:
            raise Exception('Fetch error, code == {}'.format(res.status_code))
        
        file_contents = res.content
        
        replacement = re.sub(r"(\d\d:\d\d:\d\d).(\d\d\d) --> (\d\d:\d\d:\d\d).(\d\d\d)(?:[ \-\w]+:[\w\%\d:]+)*\n", r"\1,\2 --> \3,\4\n", file_contents)
        replacement = re.sub(r"(\d\d:\d\d).(\d\d\d) --> (\d\d:\d\d).(\d\d\d)(?:[ \-\w]+:[\w\%\d:]+)*\n", r"\1,\2 --> \3,\4\n", replacement)
        replacement = re.sub(r"(\d\d).(\d\d\d) --> (\d\d).(\d\d\d)(?:[ \-\w]+:[\w\%\d:]+)*\n", r"\1,\2 --> \3,\4\n", replacement)
        replacement = re.sub(r"WEBVTT\n", "", replacement)
        replacement = re.sub(r"Kind:[ \-\w]+\n", "", replacement)
        replacement = re.sub(r"Language:[ \-\w]+\n", "", replacement)
        replacement = re.sub(r"<c[.\w\d]*>", "", replacement)
        replacement = re.sub(r"</c>", "", replacement)
        replacement = re.sub(r"<\d\d:\d\d:\d\d.\d\d\d>", "", replacement)
        replacement = re.sub(r"::[\-\w]+\([\-.\w\d]+\)[ ]*{[.,:;\(\) \-\w\d]+\n }\n", "", replacement)
        final_st = re.sub(r"Style:\n##\n", "", replacement)
        
        f = open(fpath+".srt", "w")
        f.write(final_st)
        f.close()

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
            if 'container' in x:
                if x['container'] == 'MP4' and 'src' in x:
                    dl_url = x['src']
                    break

        for x in meta_res.json()['text_tracks']:
            if 'label' in x:
                if x['label'] == self.subtitle_lang and 'src' in x:
                    st_url = x['src']
                    break

        print('Downloading {}...'.format(fpath+".mp4"))

        if os.path.exists(fpath+".mp4"):
            if os.path.exists(fpath+".srt"):
                print('Video and subtitles already downloaded...')
                return
            self.download_subtitle(fpath,st_url)
            return

        self.download_subtitle(fpath,st_url)
        
        with open(fpath+".mp4", 'wb') as f:
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
