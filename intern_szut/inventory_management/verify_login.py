from re import findall
from gzip import decompress
from urllib import request, parse, error


class VerifyLogin:
    domain = 'https://hb.itslearning.com/'
    api_token = '10ae9d30-1853-48ff-81cb-47b58a325685'  # itslearning-app api token
    hierarchy_id = 2  # school hierarchy id
    parent_hierarchy_id = 12724  # school parent (city) hierarchy id

    @classmethod
    def get_access_token(cls, username: str, password: str):
        try:
            header = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8', 'Accept-Encoding': 'gzip, deflate', 'User-Agent': 'itslearningintapp/3.5 (com.itslearning.itslearningintapp; build:22; iOS 15.4.1) Alamofire/3.5'}
            req = request.Request(f'{cls.domain}restapi/oauth2/token', headers=header)
            post_data = parse.urlencode({'client_id': cls.api_token, 'grant_type': 'password', 'password': password, 'username': username}).encode('utf-8')
            response = request.urlopen(req, post_data)
            response_data = decompress(response.read()).decode('utf-8')
            access_token = str(findall(r'"access_token":"(.*?)"', response_data)[0])
            return response.getcode(), None, access_token
        except error.HTTPError as e:
            # print(e.code, e.read().decode('utf-8'))
            return e.code, e.read().decode('utf-8'), False

    @classmethod
    def get_user_data(cls, access_token: str):
        try:
            header = {'User-Agent': 'itslearningintapp/3.5 (com.itslearning.itslearningintapp; build:22; iOS 15.4.1) Alamofire/3.5', 'Accept-Encoding': 'gzip, deflate'}
            req = request.Request(f'{cls.domain}restapi/personal/person/v1?access_token={access_token}', headers=header)
            response = request.urlopen(req)
            response_data = decompress(response.read()).decode('utf-8')

            user_data = {
                'PersonId': int(findall(r'"PersonId":(.*?),', response_data)[0]),
                'FirstName': str(findall(r'"FirstName":"(.*?)"', response_data)[0]),
                'LastName': str(findall(r'"LastName":"(.*?)"', response_data)[0]),
                'Language': str(findall(r'"Language":"(.*?)"', response_data)[0]),
                'ProfileImageUrl': (str(findall(r'"ProfileImageUrl":"(.*?)"', response_data)[0]) if findall(r'"ProfileImageUrl":"(.*?)"', response_data) else None),
                'Use12HTimeFormat': (True if findall(r'"Use12HTimeFormat":true', response_data) else False)
            }
            return response.getcode(), None, user_data
        except error.HTTPError as e:
            # print(e.code, e.read().decode('utf-8'))
            return e.code, e.read().decode('utf-8'), False

    @classmethod
    def get_user_role(cls, access_token: str):
        try:
            header = {'User-Agent': 'itslearningintapp/3.5 (com.itslearning.itslearningintapp; build:22; iOS 15.4.1) Alamofire/3.5', 'Accept-Encoding': 'gzip, deflate'}
            for role_id in [2, 1, 3]:
                """ 1: Teachers, 2: Students, 3: Admins? """
                req = request.Request(f'{cls.domain}restapi/personal/hierarchies/organisations/v1?role={role_id}&access_token={access_token}', headers=header)
                response = request.urlopen(req)
                response_data = decompress(response.read()).decode('utf-8')
                if findall(rf'"HierarchyId":{cls.hierarchy_id},"ParentHierarchyId":{cls.parent_hierarchy_id}', response_data):
                    return response.getcode(), None, role_id
            return response.getcode(), None, 4  # 4: Guest (not in organization)
        except error.HTTPError as e:
            # print(e.code, e.read().decode('utf-8'))
            return e.code, e.read().decode('utf-8'), False


# http_code, error_message, token = VerifyLogin.get_access_token(username, password)  # get token
# http_code, error_message, user_data = VerifyLogin.get_user_data(token)  # get user data
# http_code, error_message, user_role = VerifyLogin.get_user_role(token)  # get user role
