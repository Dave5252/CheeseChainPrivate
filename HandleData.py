import json, time
from datetime import datetime
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
import requests

class HandleData:
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
            'refresh_token': '9f2ae9e03ecc448e9de3e828ffc0928b',
            'client_id': 'pc',
            'grant_type': 'refresh_token',
            'redirect_uri': 'https://beta.qs.fromarte.ch/login',
        }

        self.authToken = "0"
        self.lastChecked = 0
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
        self.getAllWorkingItemsQuery = """ {allCases(orderBy: CREATED_AT_DESC, status: [RUNNING,COMPLETED]) {
                     edges {
                       node {
                         createdAt
                         createdByUser
                        document{
                          id
                          form{
                            name

                          }
                          
                        }
                        status
                        
                         }
                        
                         }
                       }
                     }
                 """
        self.getAllWorkingItemsAfterQuery = """query allWorkItemsAfter($dateTime: DateTime!){
                   {allCases(orderBy: CREATED_AT_DESC, status: [RUNNING,COMPLETED], createdAfter: $dateTime) {
                     edges {
                       node {
                         createdAt
                         createdByUser
                        document{
                          id
                          form{
                            name

                          }
                          
                        }
                        status
                        
                         }
                        
                         }
                       }
                     }
                   
                 }"""
        self.searchFilterAllWorkingItems = ["createdByUser", "createdAt", "id", "name", "slug", "status"]
        self.searchFilterMilkRelated = ["833-10-milchmenge", "833-10-lab-lot-nummer", "833-10-kultur-lotnummer",
                                        "833-10-uhrzeit", "833-10-temperatur", "833-10-temperatur-gelagerte-milch",
                                        "833-10-stuckzahl-produzierte-kase", "833-10-datum", "833-10-kultur"]
        self.nameNewestBackupFile = "BackUp1657132756.8715763.json"

    def refreshToken(self):
        response = requests.post('https://beta.qs.fromarte.ch/openid/token', headers=self.headers, cookies=self.cookies,
                                 data=self.data)
        time.sleep(2)
        response_data = response.json()
        self.authToken = response_data["access_token"]
        self.data['refresh_token'] = response_data["refresh_token"]

    def getAuthToekn(self):
        return self.authToken

    def getAllWorkingItems(self, query, dateTime=None):
        """
        Returns a JSON with all the open forms and corresponding information (i.e. UserID of creator, creation date)
        :return: Returns the received JSON.
        """
        transport = AIOHTTPTransport(url="https://beta.qs.fromarte.ch/graphql/",
                                     headers={"authorization": "Bearer " + self.getAuthToekn()})
        client = Client(transport=transport)
        query = gql(query)
        # Set the time to the time that was last checked
        params = {"dateTime": self.lastChecked}
        # Update the last checked tim to the current time
        self.lastChecked = datetime.now().isoformat()
        if dateTime:
            response = client.execute(query,variable_values=params)
        else:response = client.execute(query)
        return response

    def saveAsJson(self, responseJson, nameOfJson):
        """
        Saves a response as a JSON to the directory.
        :param responseJson: JSON which should be saved
        :param nameOfJson: The name the JSON should get.
        """
        with open(nameOfJson + '.json', 'w', encoding='utf-8') as f:
            json.dump(responseJson, f, ensure_ascii=False, indent=4)

    def getDocument(self, docID, query, dateTime=False):
        """
        Through a provided query and document ID this function fetches the associated JSON and return the received file.
        Namely: "createdByUser", "createdAt", "id", "name", "slug", "status".
        :param docID: Id of the document
        :param query: GraphQL query
        :param dateTime: Relevant when fetching historical answers. Default is false (=not relevant).
        :return: Received JSON file
        """
        transport = AIOHTTPTransport(url="https://beta.qs.fromarte.ch/graphql/",
                                     headers={"authorization": "Bearer " + self.getAuthToekn()})
        client = Client(transport=transport)
        # Provide a GraphQL query with the docID
        query = gql(query)
        params = {"id": docID}
        # DateTime may be relevant when fetching historical answers
        if dateTime:
            params['dateTime'] = datetime.now().isoformat()
        response = client.execute(query, variable_values=params)
        return response

    # only works if there are not more than one k, v pair wih the same key
    def getRelevantInfoAllWorkingItems(self, json):
        """
        This function is designed to extract relevant information from the JSON with all the open forms.
        :param json: Passing the JSON into the function.
        :return: Return a dict with the extracted fields.
        """
        final = {}
        if type(json) == dict:
            for k, v in json.items():
                if type(v) == dict or type(v) == list:
                    final = final | self.getRelevantInfoAllWorkingItems(v)
                if k in self.searchFilterAllWorkingItems:
                    final[k] = v
        elif type(json) == list:
            for element in json:
                final = final | self.getRelevantInfoAllWorkingItems(element)
        #set the lastUpdated variable = 0
        final["lastUpdated"] = 0
        final["lastModifiedBy"] = ""
        return final

    def update(self):
        """
        This is the core function of the script. It fetches the "historical answers" of unfinished forms.
        If something was deleted or altered it will be indicated with a "~", a "+" indicate that an new answer was given.
        The Functions then updates the new or altered answers on the JSON. XXXXXXXXXXXXXXXXXXXXXX
        :return: The IDs of the Files that were altered/updated.
        """
        idsofupdatedfiles = []
        with open(self.nameNewestBackupFile, encoding='utf-8') as f:
            data = json.load(f)
            changes = 0
            # loop through all stored documents
            for node in data.items():
                # check if the document is already frozen
                if node[1]['status'] != 'RUNNING':
                    continue
                returnedJson = self.getDocument(node[0], self.getHistAnswerQuery, dateTime=True)
                # check if something was changed with "~" and if the answer is relevant
                newanswers = []
                for historicalAnswer in returnedJson["documentAsOf"]["historicalAnswers"]['edges']:
                    question = historicalAnswer["node"]["question"]["slug"]
                    if historicalAnswer["node"]["historyType"] == "~" and question in self.searchFilterMilkRelated and node[1]["lastUpdated"] != historicalAnswer["node"]["historyDate"]:
                        # something was altered or deleted and is new
                        newanswers.append(question)
                        # update the lastUpdated time
                        data[node[0]]["lastUpdated"] = historicalAnswer["node"]["historyDate"]
                        # save the Username
                        modifiedByWho = historicalAnswer["node"]["historyUserId"]
                    elif question in self.searchFilterMilkRelated and question not in node[1]['answer']:
                        # check if a new relevant answer was given
                        newanswers.append(question)

                if newanswers:
                    # check if the new answers are really new maybe the historical answer is the same. This makes sure no unnecessary transaction will me triggered.
                    newFetchedAnswers = self.getRelevantInfoFromJsonAnswers(self.getDocument(node[0], self.getAnswerQuery), newanswers)
                    # TODO: Save the new fetched answerfile??? maybe false
                    for question, newVal in newFetchedAnswers.items():
                        if node[1]["answer"][question] != newVal:
                            # the new value was really new
                            changes+=1
                            data[node[0]][question] = newVal
                            data[node[0]]["lastModifiedBy"] = modifiedByWho
                            idsofupdatedfiles.append(node[0])
        # update the new BackupJSON with the new time
        if changes !=0:
            with open("BackUp"+str(time.time())+".json", "w", encoding='utf-8') as f:
                json.dump(data,f, indent=2)
                print(changes, " files were updated")
                return idsofupdatedfiles




    def checkForNewFiles(self):
        with open("AllWorkingItems.json", "r", encoding='utf-8') as f:
            newitems = self.getAllWorkingItems(query=self.getAllWorkingItemsAfterQuery)
            # If there are no new entries the length of the JSON will be 65
            if len(newitems) == 65:
                return
            else:pass


      # May need some rework
    def getRelevantInfoFromJsonAnswers(self, jsonname, searchwords=None):
        """
        Extracts certain variables from a JSON containing the answers to a filled out from.
        :param jsonname: Name of the (JSON) file that needs to be searched.
        :param searchwords: The variables that are relevant and need to be extracted.
        :return:
        """
        if searchwords is None:
            searchwords = self.searchFilterMilkRelated
        final = {}
        if type(jsonname) == str:
            with open(jsonname, encoding='utf-8') as f:
                loaded = json.load(f)
        else:
            loaded = jsonname

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
