import re
import urllib.request

domain = 'https://hb.itslearning.com'
header = {'User-Agent': 'Mozilla/5.0'}

class VerifyLogin:
    @classmethod
    def get_sessionid(cls, username, password):
        req = urllib.request.Request(domain, headers=header)
        data = urllib.request.urlopen(req).read()
        print(data)


VerifyLogin.get_sessionid("admin", "admin")