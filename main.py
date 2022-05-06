import json
import time

from HandleData import handleData


def main():
    d = handleData()

    while True:
        d.refreshToken()
        d.saveAsJson(d.getAllWorkingItems(), "AllWorkingItems")


        with open(r'C:\Users\ddien\SOPRA\BA-Code\AllWorkingItems.json', encoding='utf-8') as f:
            loaded = json.load(f)
            # save the relevant data inside a nested json called BackUp
            with open('BackUp.json', 'w', encoding='utf-8') as jsonFile:
                final = {}
                for node in loaded["allWorkItems"]["edges"]:
                    nested = {}
                    relevantData = d.getRelevantInfoFromJsonAllWorkingItems(node)
                    # sort by ID
                    IDofCurrentNode = node["node"]["case"]["document"]["id"]
                    d.saveAsJson(d.getDocument(IDofCurrentNode), "Answer_"+ IDofCurrentNode)
                    relevantData["answer"] = d.getRelevantInfoFromJsonAnswers("Answer_"+IDofCurrentNode+".json")
                    nested[relevantData["id"]] = relevantData
                    final.update(nested)
                json.dump(final, jsonFile, indent=2)
                print("done")



        #print(d.getRelevantInfoFromJsonAnswers('DocAnswer.json'))

        time.sleep(250)
main()