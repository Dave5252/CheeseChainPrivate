import json, time
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
import requests

class handleData:
    def __init__(self):
        self.cookies = {
        '_ga': 'GA1.2.409366753.1648130862',
        'csrftoken': '5fHZozvMhzSYQcJyb1nFg3PROGBrKe0gor7QAWM04ixsE2BeX71yMexcD2GmFIUu',
        'op_browser_state': '6dd3825f4c1719276a677a70bb1303f8ba9fcdb4ad5d0e9a4010c121',
        'sessionid': 'quhnvolzwxistj9rph9kohzhf4pjxqg5',
    }
        self.headers  = {
        'authority': 'qs.fromarte.ch',
        'accept': 'application/json',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,lb;q=0.6,id;q=0.5',
        # Requests sorts cookies= alphabetically
        # 'cookie': '_ga=GA1.2.409366753.1648130862; csrftoken=5fHZozvMhzSYQcJyb1nFg3PROGBrKe0gor7QAWM04ixsE2BeX71yMexcD2GmFIUu; op_browser_state=6dd3825f4c1719276a677a70bb1303f8ba9fcdb4ad5d0e9a4010c121; sessionid=quhnvolzwxistj9rph9kohzhf4pjxqg5',
        'origin': 'https://qs.fromarte.ch',
        'referer': 'https://qs.fromarte.ch/qs',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    }
        # insert refresh-token
        self.data  = {
        'refresh_token': 'f9817fc2559b4d0ebb041bc6fc647a1b',
        'client_id': 'pc',
        'grant_type': 'refresh_token',
        'redirect_uri': 'https://qs.fromarte.ch/login',
    }

    def getAuthToke(self):
        response = requests.post('https://qs.fromarte.ch/openid/token', headers=self.headers, cookies=self.cookies, data=self.data)
        time.sleep(2)
        response_data = response.json()
        #self.data['refresh_token']=response_data["refresh_token"]
        print(response_data["refresh_token"])
        return response_data["access_token"]

    def getAllWorkingItems(self):
        transport = AIOHTTPTransport(url="https://qs.fromarte.ch/graphql/",
                                     headers={"authorization": "Bearer "+self.getAuthToke()})
        client = Client(transport=transport)
        # Provide a GraphQL query
        query = gql("""{
           allWorkItems(status: READY, orderBy: CREATED_AT_DESC) {
             edges {
               node {
                 id
                 createdAt
                 createdByUser
                 task {
                   slug
                   __typename
                 }
                 case {
                   document {
                     id
                     form {
                       id
                       name
                       meta
                       source {
                         id
                         meta
                         __typename
                       }
                       __typename
                     }
                     __typename
                   }
                   __typename
                 }
                 __typename
               }
               __typename
             }
             __typename
           }
         }
         """)
        return client.execute(query)

    def saveAsJson(self, name):
        with open(name+'.json', 'w', encoding='utf-8') as f:
            json.dump(self.convertToJson(), f, ensure_ascii=False, indent=4)


d = handleData()
print(d.getAllWorkingItems())

