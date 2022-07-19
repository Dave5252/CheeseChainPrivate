import json, time
import dateutil.parser
import os
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
            'refresh_token': '7a1d967f2e0843918d6ffa3f091eae46',
            'client_id': 'pc',
            'grant_type': 'refresh_token',
            'redirect_uri': 'https://beta.qs.fromarte.ch/login',
        }

        self.authToken = "0"
        self.lastChecked = '2022-12-14T15:46:19.944445' # when running first time needs to be changed
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
  allDocuments(id:$id){
    edges{
      node{
       case{
        status
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
                   allCases(orderBy: CREATED_AT_DESC, status: [RUNNING,COMPLETED], createdAfter: $dateTime) {
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
        self.searchFilterAllWorkingItems = ["createdByUser", "createdAt", "id", "name", "slug", "status"]
        self.searchFilterMilkRelated = ["833-10-milchmenge", "833-10-lab-lot-nummer", "833-10-kultur-lotnummer",
                                        "833-10-uhrzeit", "833-10-temperatur", "833-10-temperatur-gelagerte-milch",
                                        "833-10-stuckzahl-produzierte-kase", "833-10-datum", "833-10-kultur"]
        self.nameNewestBackupFile = ""

    def refreshToken(self):
        """
        Sends a request to the GQL endpoint of fromarte to refresh the authorization and refresh token.
        """
        gotnewtoken = False
        tries = 0
        # If the request gets denied or it is delayed, try it again (max 5 times).
        while gotnewtoken == False or tries == 5:
            try:
                response = requests.post('https://beta.qs.fromarte.ch/openid/token', headers=self.headers, cookies=self.cookies,
                                     data=self.data)
                gotnewtoken = True
            except requests.exceptions.ConnectionError:
                response.status_code = "Connection refused"
                tries += 1
        response_data = response.json()
        self.authToken = response_data["access_token"]
        self.data['refresh_token'] = response_data["refresh_token"]


    def getAllWorkingItems(self, query, dateTime=None):
        """
        Returns a JSON with all the open forms and corresponding information (i.e. UserID of creator, creation date)
        :return: Returns the received JSON.
        """
        transport = AIOHTTPTransport(url="https://beta.qs.fromarte.ch/graphql/",
                                     headers={"authorization": "Bearer " + self.authToken})
        client = Client(transport=transport)
        query = gql(query)
        # Set the time to the time that was last checked
        params = {"dateTime": self.lastChecked}
        # If the dateTime is needed (when checking for new forms), execute with the params.
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

    def getDocument(self, document_id, query, date_time=None):
        """
        Through a provided query and document ID this function fetches the associated JSON and returns the received file.
        :param document_id: Id of the document
        :param query: GraphQL query
        :param date_time: Relevant when fetching historical answers. Default is false (=not relevant).
        :return: Received JSON file
        """
        transport = AIOHTTPTransport(url="https://beta.qs.fromarte.ch/graphql/",
                                     headers={"authorization": "Bearer " + self.authToken})
        client = Client(transport=transport)
        # Provide a GraphQL query with the docID
        query = gql(query)
        params = {"id": document_id}
        # DateTime may be relevant when fetching historical answers
        if date_time:
            params['dateTime'] = datetime.now().isoformat()
        got_connection = False
        tries = 0
        while got_connection == False or tries == 5:
            try:
                response = client.execute(query, variable_values=params)
                got_connection = True
            except requests.exceptions.ConnectionError:
                response.status_code = "Connection refused"
                tries += 1
        return response

    # only works if there are not more than one k, v pair wih the same key
    def getRelevantInfoAllWorkingItems(self, json):
        """
        This function is designed to extract relevant information from the JSON with all the open forms.
        :param json: Passing the JSON into the function.
        :return: Return a dict with the extracted fields.
        """
        final = {}
        # Check if it is dict or a list
        if type(json) == dict:
            for k, v in json.items():
                if type(v) == dict or type(v) == list:
                    # If the value is still a dict or a list, call itself again (recursion).
                    final = final | self.getRelevantInfoAllWorkingItems(v)
                # append the key value pair, if they are of relevance.
                if k in self.searchFilterAllWorkingItems:
                    final[k] = v

        elif type(json) == list:
            for element in json:
                final = final | self.getRelevantInfoAllWorkingItems(element)
        # set the lastUpdated variable = 0 and lastModifiedBy to an empty string
        final["lastUpdated"] = 0
        final["lastModifiedBy"] = ""
        return final

    def updateFiles(self):
        """
        This is the core function of the script. It fetches the "historical answers" of unfinished forms.
        If something was deleted or altered it will be indicated with a "~", a "+" indicate that an new answer was given.
        The Functions then updates the new or altered answers on the JSON. XXXXXXXXXXXXXXXXXXXXXX
        :return: The IDs of the Files that were altered/updated.
        """
        ids_of_updated_files = []
        ids_to_freeze = []
        with open(self.nameNewestBackupFile, encoding='utf-8') as f:
            data = json.load(f)
            # used to see if a new file needs to be saved to BackUpFile
            total_changes = 0
            # loop through all stored documents
            for node in data.items():
                changes_to_current_file = 0
                # Initiate a random date.
                newest_history_date = "2000-07-19T19:27:19.121610"
                # check if the document is already frozen after first fetching
                if node[1]['status'] != 'RUNNING':
                    ids_to_freeze.append(node[0])
                    continue
                returnedJson = self.getDocument(node[0], self.getHistAnswerQuery, date_time=True)
                # chek if it got frozen in the meantime
                if returnedJson['allDocuments']["edges"][0]["node"]["case"]["status"] != 'RUNNING':
                    ids_to_freeze.append(node[0])
                    print(node[0], "Will be frozen")
                    continue
                # check if something was changed with "~" and if the answer is relevant
                new_answers = []
                for historical_answer in returnedJson["documentAsOf"]["historicalAnswers"]['edges']:
                    question = historical_answer["node"]["question"]["slug"]
                    hist_date = historical_answer["node"]["historyDate"]
                    if historical_answer["node"]["historyType"] == "~" and question in self.searchFilterMilkRelated and node[1]["lastUpdated"] != hist_date[:(hist_date.index("+"))]:
                        # something was altered or deleted and is new
                        new_answers.append(question)
                        if dateutil.parser.parse(newest_history_date) < dateutil.parser.parse(hist_date[:(hist_date.index("+"))]):
                            newest_history_date = hist_date[:(hist_date.index("+"))]
                        # save the Username
                        modifiedByWho = historical_answer["node"]["historyUserId"]
                    elif question in self.searchFilterMilkRelated and question not in node[1]['answer']:
                        # check if a new relevant answer was given
                        new_answers.append(question)
                        if dateutil.parser.parse(newest_history_date) < dateutil.parser.parse(
                                hist_date[:(hist_date.index("+"))]):
                            newest_history_date = hist_date[:(hist_date.index("+"))]
                    # "Kultur" related variables need to be handled differently, 833-10-kultur-lotnummer and 833-10-kultur variables need to be appended m.anually
                    if historical_answer["node"]["question"]["label"] == "Kulturen" and node[1]["lastUpdated"] != historical_answer["node"]["historyDate"]:
                        new_answers.extend(["833-10-kultur", "833-10-kultur-lotnummer"])
                if new_answers:
                    # check if the new answers are really new maybe the historical answer is the same. This makes sure no unnecessary transaction will me triggered.
                    newFetchedAnswers = {key:val for key, val in self.getRelevantInfoFromJsonAnswers(self.getDocument(node[0], self.getAnswerQuery), new_answers).items() if val != "tbt"}
                    for question, newVal in newFetchedAnswers.items():
                        try:
                            if node[1]["answer"][question] or node[1]["answer"][question] == None:
                                if node[1]["answer"][question] != newVal:
                                    # the new value was really new
                                    data[node[0]]["lastModifiedBy"] = modifiedByWho
                                    data[node[0]]["answer"][question] = newVal
                                    # update the lastUpdated time
                                    data[node[0]]["lastUpdated"] = newest_history_date
                                    total_changes += 1
                                    changes_to_current_file += 1
                                    if node[0] not in ids_of_updated_files:
                                        ids_of_updated_files.append(node[0])
                        except:
                            # Catch if it does not exist
                            data[node[0]]["answer"][question] = newVal
                            total_changes += 1
                            data[node[0]]["lastUpdated"] = newest_history_date
                            changes_to_current_file += 1
                            if node[0] not in ids_of_updated_files:
                                ids_of_updated_files.append(node[0])
                    # check if a given value was deleted
                    for quest in new_answers:
                        if quest not in newFetchedAnswers and quest in data[node[0]]["answer"].keys():
                            data[node[0]]["answer"].update({quest: None})
                            total_changes += 1
                            changes_to_current_file += 1
                            data[node[0]]["lastUpdated"] = newest_history_date
                            if node[0] not in ids_of_updated_files:
                                ids_of_updated_files.append(node[0])

                    # create new BackupFile if changes to current file were made
                    if changes_to_current_file != 0:
                        os.chdir("BackupFiles")
                        to_save = {}
                        to_save[node[0]] = data[node[0]]
                        self.saveAsJson(to_save, node[0] + r"-" + str(time.time()))
                        os.chdir("..")


        # update the new BackupJSON with the new time
        if total_changes !=0:
            # Update nameNewestBackupFile variable
            print(total_changes," were made")
            new_name = "BackUp"+str(time.time())+".json"
            self.nameNewestBackupFile = new_name
            with open(new_name, "w", encoding='utf-8') as f:
                json.dump(data,f, indent=2)
        return ids_of_updated_files, ids_to_freeze


    def mostRecentFileByID(self, id):
        """
        Gets the most recent file by ID.
        :param id: A ID of a file.
        :return: Return the newest file.
        """
        return max([int(x[x.index("-")+1:x.index(".json")+1]) for x in os.listdir("BackupFiles") if x.startswith(id)])


    def checkForNewFiles(self):
        """
        Fetches all the working items again and checks if they are new, if yes it appends to the current BackUp file
        :return: Returns the new forms.
        """
        new_items = self.getAllWorkingItems(query=self.getAllWorkingItemsAfterQuery, dateTime=self.lastChecked)
        # Update the last checked time to the current UCT time, as the server runs on UCT time.
        self.lastChecked = datetime.now().utcnow().isoformat()
        new_forms = self.helperFunctionForExtracionAndSaving(new_items)
        if new_forms:
            self.writeOnCurrentBackUpFile(new_forms)
            print("new item", new_forms)
            return new_forms
        else:return


    def helperFunctionForExtracionAndSaving(self, allWorkItemsJson):
        """
        Helps extracting and organizing relevant info from all the forms from the digitalQM. Fetches the corresponding
        answer JSON from each form.
        :return: Returns the BackUp file with all nodes and all its relevant variables.
        """
        final = {}
        curr_string_time = str(time.time())
        # Loop trough the file with all the forms.
        for node in allWorkItemsJson["allCases"]["edges"]:
            nested = {}
            # Feed each node into getRelevantInfoAllWorkingItems, to extract the relevant information.
            relevant_data = self.getRelevantInfoAllWorkingItems(node)
            id_of_current_node = node["node"]["document"]["id"]
            os.chdir("Answers")
            # Save the new fetched answer file from the forms inside the Answers directory.
            self.saveAsJson(self.getDocument(id_of_current_node, self.getAnswerQuery),
                            "Answer_" + id_of_current_node + curr_string_time)
            # Call getRelevantInfoFromJsonAnswers to extract all the relevant variables from the new
            # fetched answer file.
            relevant_data["answer"] = {key:val for key, val in self.getRelevantInfoFromJsonAnswers(
                "Answer_" + id_of_current_node + curr_string_time + ".json").items() if val != "tbt"}
            nested[relevant_data["id"]] = relevant_data
            final.update(nested)
            os.chdir("..")
            os.chdir("BackupFiles")
            # Save the new organized JSON with the extracted variables also to the BackupFiles folder.
            if nested:
                self.saveAsJson(nested,(relevant_data["id"] + r"-" + str(time.time())))
            os.chdir("..")
        return final

    def freezeForm(self, ids):
        """
        Freezes completed forms. Frozen forms are extracted from the BackUp file and moved into a FrozenIDs.json.
        :param ids: Takes a list with IDs a parameter.
        :return Returns nothing, but if we have an empty list the function does not need to run, or empty files
        may be created.
        """
        # May be called with an empty list.
        if not ids:
            return
        with open(self.nameNewestBackupFile, "r+", encoding='utf-8') as f:
            data = json.load(f)
            # check if the file where all the frozen files are saved already exists.
            if os.path.exists(r"FrozenIDs.json"):
                frozen = open("FrozenIDs.json", "r+", encoding='utf-8')
                alredy_frozen = json.load(frozen)
            else:
                frozen = open("FrozenIDs.json", "w", encoding='utf-8')
                alredy_frozen = {}
            # Iterate through the ids of the files which need to be frozen.
            for id in ids:
                # create the same data structure as in the BackUp file, and add to the alreadyFrozen file.
                popped = data.pop(id)
                alredy_frozen[popped["id"]] = popped
                alredy_frozen[popped["id"]]["status"] = "COMPLETED"
            # Overwrite the old file with the new appended JSON file
            frozen.seek(0)
            json.dump(alredy_frozen,frozen, indent=2)
            frozen.truncate()
            frozen.close()
            print("new frozenIDs file: ", alredy_frozen)
            print("new backup file without any frozenfiles file: ", data)
            # Save the BackUp file with the RUNNING files, as all COMPLETED ones were frozen.
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()





    def writeOnCurrentBackUpFile(self, fileToAppend):
        """
        Writes a JSON onto the currents BackUp JSON.
        """
        with open(self.nameNewestBackupFile, "r+", encoding='utf-8') as f:
            curr_data = json.loads(f.read())
            # Appends to the current file and overwrites the outdated data
            curr_data.update(fileToAppend)
            f.seek(0)
            json.dump(curr_data, f, indent=2)
            f.truncate()


    # May need some rework
    def getRelevantInfoFromJsonAnswers(self, jsonname, search_words=None):
        """
        Extracts certain variables from a JSON containing the answers to a filled out from.
        :param jsonname: Name of the (JSON) file that needs to be searched.
        :param search_words: The variables that are relevant and need to be extracted.
        :return:
        """
        # take the predefined searchwords, if the variable is not defined.
        if search_words is None:
            search_words = self.searchFilterMilkRelated
        final = {}
        # check if a name of a file is given, or a whole file is passed in the function
        if type(jsonname) == str:
            with open(jsonname, encoding='utf-8') as f:
                loaded = json.load(f)
        else:
            loaded = jsonname

        # check all answer nodes for relevant variables
        if type(loaded) == dict:
            for k, v in loaded.items():
                if type(v) == dict or type(v) == list:
                    final = final | self.getRelevantInfoFromJsonAnswers(v, search_words)
                if "tbt" in final.values():
                    if "Value" in k:
                        final.update({ke: v for ke, val in final.items() if type(v) in [str, float, int]})
                if v in search_words:
                    final[v] = "tbt"
        elif type(loaded) == list:
            for element in loaded:
                final = final | self.getRelevantInfoFromJsonAnswers(element, search_words)

        return final
