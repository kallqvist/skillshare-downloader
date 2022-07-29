from downloader import Downloader

cookie = ''
dl = Downloader(cookie=cookie)

# download by class URL:
dl.download_course_by_url('https://www.skillshare.com/classes/Learning-Voice-Acting-Voice-Impressions-For-Beginners/1775383577')

# or by class ID:
#dl.download_course_by_class_id(1296169637)
