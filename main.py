import json
import os
import time

from CommunicateToSmartContract import CommunicateToSmartContract
from HandleData import HandleData

# make instances Global
d = HandleData()
c = CommunicateToSmartContract()

def main():
    d.refreshToken()
    d.saveAsJson(d.getAllWorkingItems(d.getAllWorkingItemsQuery), "AllWorkingItems")
    firstTimeRun()
    while True:
        updatedids = d.update()
        if updatedids != []:
            for ids in updatedids:
                pass

        time.sleep(250)

def firstTimeRun():

    backUpFileName = 'BackUp' + str(time.time()) + ".json"
    with open(r'C:\Users\David\Desktop\BA Code\AllWorkingItems.json', encoding='utf-8') as f:
        loaded = json.load(f)
        # save the relevant data inside a nested json called BackUp
        d.nameNewestBackupFile = backUpFileName
        with open(backUpFileName, 'w', encoding='utf-8') as jsonFile:
            final = {}
            currStringTime = str(time.time())
            for node in loaded["allCases"]["edges"]:
                nested = {}
                relevantData = d.getRelevantInfoAllWorkingItems(node)
                # sort by ID
                IDofCurrentNode = node["node"]["document"]["id"]
                os.chdir(r"C:\Users\David\Desktop\BA Code\Anwers")
                d.saveAsJson(d.getDocument(IDofCurrentNode, d.getAnswerQuery),
                             "Answer_" + IDofCurrentNode + currStringTime)
                relevantData["answer"] = d.getRelevantInfoFromJsonAnswers(
                    "Answer_" + IDofCurrentNode + currStringTime + ".json")
                nested[relevantData["id"]] = relevantData
                final.update(nested)
            json.dump(final, jsonFile, indent=2)
            os.chdir(r"C:\Users\David\Desktop\BA Code")
            print("ran for the fist time")
            # send the created BackUp JSON to the local BC
            for id, val in final.items():
                c.createNewFormSmartContract(id, val)

if __name__ == '__main__':
    main()
