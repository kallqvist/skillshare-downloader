# Skillshare video downloader in python

### Support your content creators, do NOT use this for piracy!

You will need a skillshare premium account to access premium content.
This script will not handle login for you.

1. Log-in to skillshare in your browser and open up the developer console.
(cmd-shift-c for chrome on mac)

2. Use it to grab your cookie by typing:
```
document.cookie
```

3. Copy-paste cookie from developer console (without " if present) into example script.

#### Example:
```
from downloader import Downloader

cookie = """
ADD YOUR COOKIE HERE
"""

4. Run the script and enter the number of courses you want to download. Then enter the URL of each of the courses.

    If you choose to download all classes in a public list (for example: https://www.skillshare.com/lists/Classes-for-Getting-Creative-Indoors/1347947), use the
    download_list() function and enter the URL of the list.

5. (Optionally) run with docker and docker-compose:
```
docker-compose build
docker-compose run --rm ssdl python example.py
```
