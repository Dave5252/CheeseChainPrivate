#Autorization
import json

import requests
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.requests import RequestsHTTPTransport

import requests

import requests

cookies = {
    '_ga': 'GA1.2.1564887654.1644181048',
    'csrftoken': 'z6wSeXULo4qT8NBDyNwoKj9nvtSZtbtvTPTjHc8SxAxKtu64TpnOTpq9M2xMO1ca',
    'op_browser_state': '884d8d3f0a32c2ccad65645bd282777765b42cbfef272ebc71f63a4d',
    'sessionid': '4etqe1944pg1p1ywfmf0qrkv9ct1awyd'
}

headers = {
    'authority': 'qs.fromarte.ch',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,lb;q=0.6,id;q=0.5',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': '_ga=GA1.2.1564887654.1644181048; csrftoken=z6wSeXULo4qT8NBDyNwoKj9nvtSZtbtvTPTjHc8SxAxKtu64TpnOTpq9M2xMO1ca; op_browser_state=884d8d3f0a32c2ccad65645bd282777765b42cbfef272ebc71f63a4d; sessionid=4etqe1944pg1p1ywfmf0qrkv9ct1awyd',
    'origin': 'https://qs.fromarte.ch',
    'referer': 'https://qs.fromarte.ch/openid/authorize?client_id=pc&redirect_uri=https://qs.fromarte.ch/login&response_type=code&state=1d6b9868-ad9a-4429-a063-58671c307307&scope=openid%20profile%20caluma',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
}

data = {
    'csrfmiddlewaretoken': 'h5AB9ntTugHp3mxOsreRgx66EMaichzWBOX2CCH0DMOgo32fN35hpDnSVlP5x7iB',
    'client_id': 'pc',
    'redirect_uri': 'https://qs.fromarte.ch/login',
    'response_type': 'code',
    'scope': 'openid profile caluma',
    'state': '1d6b9868-ad9a-4429-a063-58671c307307',
    'allow': 'Authorize'}





transport = AIOHTTPTransport(url="https://qs.fromarte.ch/graphql/",headers= {"authorization": "Bearer 4babc74f539f46829b17ff4807752759"})

# Create a GraphQL client using the defined transport
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


params = {"documentId": "RG9jdW1lbnQ6YTJmOGQwYTEtNWFhZS00MTM3LTkxZmMtYWViMjg5YTkzOWFh"}

response = requests.post('https://qs.fromarte.ch/openid/authorize', headers=headers, cookies=cookies, data=data)
print(response.status_code, response.text)
result = client.execute(query)

json_formatted_str = json.dumps(result, indent=2)
json_formatted_str

print(json_formatted_str)
# Execute the query on the transport
