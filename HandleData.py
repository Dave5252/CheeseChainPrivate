import json, time
import os
from datetime import datetime
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
import requests


class handleData:
    def __init__(self):
        self.cookies = {
            '_ga': 'GA1.2.1564887654.1644181048',
            'csrftoken': 'YewbsaeZsQTbbUrSWw68XUhTOsnm3l9ez2sfXytUIrYcly33qgMHbc6Mr2iwM2r0',
            'op_browser_state': 'e1b5449746b83db4d810aa2100c5afc8c449baf9f03dc03cd65519ff',
            'sessionid': 'kacgu0pq36y7tq89vu16uw825rh3ub49',
        }

        self.headers = {
            'authority': 'beta.qs.fromarte.ch',
            'accept': 'application/json',
            'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,lb;q=0.6,id;q=0.5',
            # Requests sorts cookies= alphabetically
            # 'cookie': '_ga=GA1.2.1564887654.1644181048; csrftoken=YewbsaeZsQTbbUrSWw68XUhTOsnm3l9ez2sfXytUIrYcly33qgMHbc6Mr2iwM2r0; op_browser_state=e1b5449746b83db4d810aa2100c5afc8c449baf9f03dc03cd65519ff; sessionid=kacgu0pq36y7tq89vu16uw825rh3ub49',
            'origin': 'https://beta.qs.fromarte.ch',
            'referer': 'https://beta.qs.fromarte.ch/qs',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
        }

        self.data = {
            'refresh_token': '1ec92b1f5ffe45d8bddd5935f3f080d7',
            'client_id': 'pc',
            'grant_type': 'refresh_token',
            'redirect_uri': 'https://beta.qs.fromarte.ch/login',
        }


        self.authToken = "0"
        self.dateTimeIso = datetime.now().isoformat()
        self.getAnswerQuery = """
                  query DocumentAnswers($id: ID!) {
  allDocuments(filter: [{id: $id}]) {
    edges {
      node {
        id
        form {
          id
          slug
          __typename
        }
        workItem {
          id
          __typename
        }
        case {
          id
          workItems {
            edges {
              node {
                id
                task {
                  id
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
        answers {
          edges {
            node {
              ...FieldAnswer
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

fragment SimpleQuestion on Question {
  id
  slug
  label
  isRequired
  isHidden
  meta
  infoText
  ... on TextQuestion {
    textMinLength: minLength
    textMaxLength: maxLength
    textDefaultAnswer: defaultAnswer {
      id
      value
      __typename
    }
    placeholder
    __typename
  }
  ... on TextareaQuestion {
    textareaMinLength: minLength
    textareaMaxLength: maxLength
    textareaDefaultAnswer: defaultAnswer {
      id
      value
      __typename
    }
    placeholder
    __typename
  }
  ... on IntegerQuestion {
    integerMinValue: minValue
    integerMaxValue: maxValue
    integerDefaultAnswer: defaultAnswer {
      id
      value
      __typename
    }
    placeholder
    __typename
  }
  ... on FloatQuestion {
    floatMinValue: minValue
    floatMaxValue: maxValue
    floatDefaultAnswer: defaultAnswer {
      id
      value
      __typename
    }
    placeholder
    __typename
  }
  ... on ChoiceQuestion {
    choiceOptions: options {
      edges {
        node {
          id
          slug
          label
          isArchived
          __typename
        }
        __typename
      }
      __typename
    }
    choiceDefaultAnswer: defaultAnswer {
      id
      value
      __typename
    }
    __typename
  }
  ... on MultipleChoiceQuestion {
    multipleChoiceOptions: options {
      edges {
        node {
          id
          slug
          label
          isArchived
          __typename
        }
        __typename
      }
      __typename
    }
    multipleChoiceDefaultAnswer: defaultAnswer {
      id
      value
      __typename
    }
    __typename
  }
  ... on DateQuestion {
    dateDefaultAnswer: defaultAnswer {
      id
      value
      __typename
    }
    __typename
  }
  ... on StaticQuestion {
    staticContent
    __typename
  }
  ... on CalculatedFloatQuestion {
    calcExpression
    __typename
  }
  ... on ActionButtonQuestion {
    action
    color
    validateOnEnter
    __typename
  }
  __typename
}

fragment FieldTableQuestion on Question {
  id
  ... on TableQuestion {
    rowForm {
      id
      slug
      questions {
        edges {
          node {
            ...SimpleQuestion
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
    tableDefaultAnswer: defaultAnswer {
      id
      value {
        id
        answers {
          edges {
            node {
              id
              question {
                id
                slug
                __typename
              }
              ... on StringAnswer {
                stringValue: value
                __typename
              }
              ... on IntegerAnswer {
                integerValue: value
                __typename
              }
              ... on FloatAnswer {
                floatValue: value
                __typename
              }
              ... on ListAnswer {
                listValue: value
                __typename
              }
              ... on DateAnswer {
                dateValue: value
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
  __typename
}

fragment FieldQuestion on Question {
  id
  ...SimpleQuestion
  ...FieldTableQuestion
  ... on FormQuestion {
    subForm {
      id
      slug
      name
      questions {
        edges {
          node {
            id
            ...SimpleQuestion
            ...FieldTableQuestion
            ... on FormQuestion {
              subForm {
                id
                slug
                name
                questions {
                  edges {
                    node {
                      ...SimpleQuestion
                      ...FieldTableQuestion
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
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}

fragment SimpleAnswer on Answer {
  id
  question {
    id
    slug
    __typename
  }
  ... on StringAnswer {
    stringValue: value
    __typename
  }
  ... on IntegerAnswer {
    integerValue: value
    __typename
  }
  ... on FloatAnswer {
    floatValue: value
    __typename
  }
  ... on ListAnswer {
    listValue: value
    __typename
  }
  ... on FileAnswer {
    fileValue: value {
      id
      uploadUrl
      downloadUrl
      metadata
      name
      __typename
    }
    __typename
  }
  ... on DateAnswer {
    dateValue: value
    __typename
  }
  __typename
}

fragment FieldAnswer on Answer {
  id
  ...SimpleAnswer
  ... on TableAnswer {
    tableValue: value {
      id
      form {
        id
        slug
        questions {
          edges {
            node {
              ...FieldQuestion
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
      answers {
        edges {
          node {
            ...SimpleAnswer
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


                """
        self.getHistAnswerQuery = """query hsitData($id: ID!, $dateTime: DateTime!){
  documentAsOf(asOf: $dateTime, id:$id){
    historyUserId
    createdByUser
    createdAt
    modifiedByGroup
    historicalAnswers(asOf: $dateTime){
      edges{
        node{
          id
          createdAt
          historyDate
          meta
          historyUserId
          historyType
          createdByUser
          question{
            slug
            label
            
          }
        }
      }
    }
  }
}


"""
        self.searchFilterAllWorkingItems = ["createdByUser", "createdAt", "id", "name", "slug", "category"]
        self.searchFilterMilkRelated = ["833-10-milchmenge", "833-10-lab-lot-nummer", "833-10-kultur-lotnummer",
                                        "833-10-uhrzeit", "833-10-temperatur", "833-10-temperatur-gelagerte-milch",
                                        "833-10-stuckzahl-produzierte-kase", "833-10-datum", "833-10-kultur"]

    def refreshToken(self):
        response = requests.post('https://beta.qs.fromarte.ch/openid/token', headers=self.headers, cookies=self.cookies,
                                 data=self.data)
        time.sleep(2)
        response_data = response.json()
        self.authToken = response_data["access_token"]
        self.data['refresh_token'] = response_data["refresh_token"]

    def getAuthToekn(self):
        return self.authToken

    def getAllWorkingItems(self):
        transport = AIOHTTPTransport(url="https://beta.qs.fromarte.ch/graphql/",
                                     headers={"authorization": "Bearer " + self.getAuthToekn()})
        client = Client(transport=transport)
        # Provide a GraphQL query
        query = gql("""{
           allWorkItems(status: READY, orderBy: CREATED_AT_DESC) {
             edges {
               node {
                 createdAt
                 createdByUser
                 task {
                   slug
                 }
                 case {
                   document {
                     id
                     form {
                       name
                       meta
                       source {
                         meta
                       }
                     }
                   }
                 }
               }
             }
           }
         }
         """)
        response = client.execute(query)
        return response

    #save a doc as JSON
    def saveAsJson(self, responseJson, nameOfJson):
        with open(nameOfJson + '.json', 'w', encoding='utf-8') as f:
            json.dump(responseJson, f, ensure_ascii=False, indent=4)

    def getDocument(self, docID, query, dateTime=False):
        transport = AIOHTTPTransport(url="https://beta.qs.fromarte.ch/graphql/",
                                     headers={"authorization": "Bearer " + self.getAuthToekn()})
        client = Client(transport=transport)
        # Provide a GraphQL query with th docID
        query = gql(query)
        params = {"id": docID}
        if dateTime:
            params['dateTime'] = self.dateTimeIso
        response = client.execute(query, variable_values=params)
        return response

    # only works if there are not more than one k, v pair wih the same key
    def getRelevantInfoFromJsonAllWorkingItems(self, json):
        final = {}
        if type(json) == dict:
            for k, v in json.items():
                if type(v) == dict or type(v) == list:
                    final = final | self.getRelevantInfoFromJsonAllWorkingItems(v)
                if k in self.searchFilterAllWorkingItems:
                    final[k] = v
        elif type(json) == list:
            for element in json:
                final = final | self.getRelevantInfoFromJsonAllWorkingItems(element)
        return final

    # check if a relevant answer was altered
    def update(self):
        with open("BackUp.json", encoding='utf-8') as f:
            for node in json.load(f).items():
                returnedJson = self.getDocument(node[0], self.getHistAnswerQuery, dateTime=True)
                #check if something was changed with "~" and if the answer is relevant
                newanswers = []
                for historicalAnswer in returnedJson["documentAsOf"]["historicalAnswers"]['edges']:
                    question = historicalAnswer["node"]["question"]["slug"]
                    if historicalAnswer["node"]["historyType"] == "~" and question in self.searchFilterMilkRelated:
                        # something was altered or deleted
                        newanswers.append(question)
                    elif question in self.searchFilterMilkRelated and question not in node[1]['answer']:
                        #check if a new relevant aswer was given
                        newanswers.append(question)
                # check if new answers were found
                if newanswers:
                    print(self.getRelevantInfoFromJsonAnswers(self.getDocument(node[0], self.getAnswerQuery), newanswers))





    # May need some rework
    def getRelevantInfoFromJsonAnswers(self, jsonname, searchwords=None):
        if searchwords is None:
            searchwords = self.searchFilterMilkRelated
        final = {}
        if type(jsonname) == str:
            with open(jsonname, encoding='utf-8') as f:
                loaded = json.load(f)
        else:loaded = jsonname

            # check all answer nodes
        for node in loaded["allDocuments"]["edges"][0]["node"]["answers"]["edges"]:
            if node['node']['question']['slug'] in searchwords:
                for k in node['node']:
                    if "Value" in k:
                        final[node['node']["question"]["slug"]] = node['node'][k]

            # check all the tables
            try:
                if node['node']['tableValue']:
                    for awnserNode in node['node']["tableValue"][0]["answers"]["edges"]:
                        if awnserNode['node']['question']['slug'] in searchwords:
                            for k in awnserNode['node']:
                                if "Value" in k:
                                    final[awnserNode['node']["question"]["slug"]] = awnserNode['node'][k]
            except:
                pass

        return final
