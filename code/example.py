from downloader import Downloader
from bs4 import BeautifulSoup as BS
import urllib.request

cookie = """
ADD YOUR COOKIE HERE
"""

dl = Downloader(cookie=cookie)


def download_course():
    # download individual class
    # # download by class URL:
    course_url = input("Enter class URL: ")
    dl.download_course_by_url(course_url)

    # # or by class ID:
    # course_url = input("Enter class ID: ")
    # # dl.download_course_by_class_id(input("Enter class ID"))

# download classes in a public list


def download_list():
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    list_url = input("Enter list URL: ")
    req = urllib.request.Request(list_url, headers=hdr)
    html = urllib.request.urlopen(req)
    soup = BS(html, features="html.parser")
    elem = soup.findAll('div', {'class': 'list-item'})

    for course in elem:
        course_url = course.find('a').attrs['href'].split('?')[0]
        dl.download_course_by_url(course_url)

# download multiple courses


def download_multiple_courses():
    count = int(input("Number of courses to download: "))
    course_list = []
    for i in range(count):
        course_list.append(input("Enter course URL: "))

    for course_url in course_list:
        dl.download_course_by_url(course_url)


download_multiple_courses()
