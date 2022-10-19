import base64
import http.client
import json
import ssl


class Api:
    def __init__(self, host='127.0.0.1', user="ers_admin", password='12345678'):
        self.__host = host.__str__()
        self.__user = user.__str__()
        self.__password = password.__str__()
        self.headers = {
            'content-type': "application/json; charset=utf-8",
            'accept': "application/json; charset=utf-8",
            'cache-control': "no-cache",
        }

    def __auth(self):
        self.__conn = http.client.HTTPSConnection("{}:9060".format(self.__host),
                                                  context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_1))
        creds = str.encode(':'.join((self.__user, self.__password)))
        encodedAuth = bytes.decode(base64.b64encode(creds))
        self.headers['authorization'] = " ".join(("Basic", encodedAuth))

    def __req(self, method, path, body=''):
        body = body.encode('utf-8')
        self.__auth()
        if body == '':
            self.__conn.request(method, path, headers=self.headers)
        else:
            self.__conn.request(method, path, headers=self.headers, body=body)
        return self.__conn.getresponse()

    def add_user(self, login, email, namefirst, namelast, description, identitygroups, password_id_store='AD'):
        if isinstance(identitygroups, list):
            buf = ''
            for gr in identitygroups:
                buf = buf + ',' + gr
            identitygroups = buf[1:]
        req_body_json = """  {{
                "InternalUser" : {{
                    "name" : "{}",
                    "email" : "{}",
                    "firstName" : "{}",
                    "lastName" : "{}",
                    "description" : "{}",
                    "identityGroups" : "{}",
                    "passwordIDStore" : "AD"
                }}
            }}
            """.format(login,
                       email,
                       namefirst,
                       namelast,
                       description,
                       identitygroups,
                       password_id_store)
        response = self.__req("POST", "/ers/config/internaluser/", req_body_json)
        return [response.status, response.read()]

    def find_userid_by_name(self, login):
        response = self.__req("GET",
                              "/ers/config/internaluser/?page=1&size=10&sortdsc=name&filter=name.EQ.{}".format(login))
        dataform = str(response.read().decode("utf-8")).strip("'<>() ").replace('\'', '\"')
        js = json.loads(dataform)
        user_data = js['SearchResult']['resources'][0]
        User_ID = user_data['id']
        return User_ID

    def find_user_profile_by_id(self, userid):
        response = self.__req("GET", "/ers/config/internaluser/{}".format(userid))
        dataform = str(response.read().decode("utf-8")).strip("'<>() ").replace('\'', '\"')
        js = json.loads(dataform)
        user_data = js['InternalUser']
        username = user_data['name']
        user_description = user_data['description']
        user_groups = user_data['identityGroups']
        return username, user_description, user_groups

    def modify_user(self, userid='', user_identity_groups='', username='', user_description=''):
        if (userid == '') and (username != ''):
            userid = self.find_userid_by_name(username)
            username, ud, uig = self.find_user_profile_by_id(userid)
        elif userid != '':
            username, ud, uig = self.find_user_profile_by_id(userid)
        else:
            return [404, '{"ERSError":"User not found"}']
        if user_description == '':
            user_description = ud
        if user_identity_groups == '':
            Groups = uig
        elif (len(uig) > 1) and (user_identity_groups != ''):
            if isinstance(user_identity_groups, str):
                Groups = uig + ',' + user_identity_groups
            else:
                Groups = uig + ',' + ','.join(user_identity_groups)
        else:
            Groups = user_identity_groups
        req_body_json_upd = """  {{
                    "InternalUser" : {{
                        "id" : "{}",
                        "name" : "{}",
                        "description" : "{}",
                        "identityGroups" : "{}",
                        "customAttributes" : {{
                        }}
                    }}
                }}
                """.format(userid, username, user_description, Groups)
        response = self.__req("PUT", "/ers/config/internaluser/" + userid, req_body_json_upd)
        return [response.status, response.read()]

    def delete_user(self, userid='', username=''):
        if (userid == '') and (username != ''):
            userid = self.find_userid_by_name(username)
        elif userid != '':
            pass
            # username, ud, uig = self.find_user_profile_by_id(userid)
        else:
            return [404, '{"ERSError":"User not found"}']
        response = self.__req("DELETE", "/ers/config/internaluser/" + userid)
        return [response.status, response.read()]
