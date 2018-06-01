import sys
import re
from downloader import Downloader

cookie = sys.argv[1]
dl = Downloader(cookie=cookie)

if len(sys.argv) != 3:
    raise Exception('Invalid arguments. Usage : {program} <cookie> <url_or_class_id>'.format(program=sys.argv[0]))

if re.match("^[0-9]+$", sys.argv[2]) is not None:
	dl.download_course_by_class_id(sys.argv[2])
else:
	dl.download_course_by_url(sys.argv[2])

