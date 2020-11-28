from downloader import Downloader

cookie = """
device_session_id=4acc568f-f0b3-451a-85fb-297e1d1abfce; show-like-copy=0; visitor_tracking=utm_campaign%3D%26utm_source%3D%28direct%29%26utm_medium%3D%28none%29%26utm_term%3D%26referrer%3D%26referring_username%3D; first_landing=utm_campaign%3D%26utm_source%3D%28direct%29%26utm_medium%3D%28none%29%26utm_term%3D%26referrer%3D%26referring_username%3D; _gcl_au=1.1.1950218587.1604020908; _ga=GA1.2.2045758321.1604020908; __utmz=99704988.1604020908.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); sm_uuid=1604021102735; __pdst=8100281ef18b4f348dd1aa273e2b517e; _scid=047ff7da-fb05-4a2b-bdb6-5c99972c9466; G_ENABLED_IDPS=google; __stripe_mid=2b9a646b-98b7-4ecb-8dca-30c5aa386479d936e4; __qca=P0-1398544483-1604020912937; __ssid=752b9b455e2f6440164dbece83c9c4e; __utmv=99704988.|1=visitor-type=user=1; _pin_unauth=dWlkPU9HUm1NbUl6TlRZdE5qQTVNeTAwTlRZMkxUazVOalV0TXpNMk1EUmhNalV3WXpFMA; _sctr=1|1604687400000; _gid=GA1.2.1873554925.1604747554; PHPSESSID=e7893ff62deff7ba19b6004bf909ef0f; YII_CSRF_TOKEN=cUZnamtOcW5KTUt0TFVmMU95NHBYQ0N3aWE1b0tBQWki4NsXBwG94kYQPwkXjVaX33VMqbKp_LhkMdVxI8V6nA%3D%3D; __utma=99704988.2045758321.1604020908.1604823462.1604845330.13; __utmc=99704988; IR_gbd=skillshare.com; _uetsid=d30ca7b020e911eb83c00dc58fad8b67; _uetvid=48cea4201a4e11eb9a214798457677ae; __utmt=1; __utmb=99704988.2.10.1604845330; IR_4650=1604846369742%7C0%7C1604845331485%7C%7C; IR_PI=85b477ae-1a4e-11eb-980c-0abbe301118c%7C1604932769742; skillshare_user_=3469a6a5a13e5be3415618dbfcfb73fc219ec61ba%3A4%3A%7Bi%3A0%3Bs%3A8%3A%2215795041%22%3Bi%3A1%3Bs%3A16%3A%22t11%40k4anubhav.cf%22%3Bi%3A2%3Bi%3A2592000%3Bi%3A3%3Ba%3A3%3A%7Bs%3A8%3A%22username%22%3Bs%3A9%3A%22424290711%22%3Bs%3A10%3A%22login_time%22%3Bs%3A19%3A%222020-10-30%2001%3A23%3A27%22%3Bs%3A10%3A%22touch_time%22%3Bs%3A19%3A%222020-11-08%2014%3A39%3A30%22%3B%7D%7D; __stripe_sid=ad6b63a2-72a8-443f-9e20-9237195cc9f29b5cf1
"""

dl = Downloader(cookie=cookie)

# download by class URL:
dl.download_course_by_url('https://www.skillshare.com/classes/Art-Fundamentals-in-One-Hour/189505397')

# or by class ID:
# dl.download_course_by_class_id(189505397)
