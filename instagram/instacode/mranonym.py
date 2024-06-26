# import requests
# import socks
# import socket
# import time
# from stem import Signal
# from stem.control import Controller
# from fake_useragent import UserAgent
# import subprocess
# from datetime import datetime

# timestamp = int(datetime.now().timestamp())
# link = 'https://www.instagram.com/accounts/login/'
# login_url = 'https://www.instagram.com/accounts/login/ajax/'
# UserAgent = UserAgent().random
# user = 'asilxon.o2.24'
# passw = f'09062007'
# print(passw)

# payload = {
#     'username': user,
#     'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{passw}',
#     'queryParams': '{}',
#     'optIntoOneTap': 'false'
# }

# response =  requests.get(link)
# csrf = response.cookies['csrftoken']

# response = requests.post(login_url, data=payload, headers={
#     "User-Agent": UserAgent,
#     "X-Requested-With": "XMLHttpRequest",
#     "Referer": "https://www.instagram.com/",
#     "X-CSRFToken": csrf,
#     "Content-Type": "application/x-www-form-urlencoded",
#     "Host": "www.instagram.com",
#     "Origin": "https://www.instagram.com"
# })
# print(response.text)