import json
import os
import time

from HandleData import handleData


def main():
    d = handleData()
    d.refreshToken()



    while True:
        d.refreshToken()
        d.saveAsJson(d.getAllWorkingItems(), "AllWorkingItems")

        with open(r'C:\Users\David\Desktop\BA Code\AllWorkingItems.json', encoding='utf-8') as f:
            loaded = json.load(f)
            # save the relevant data inside a nested json called BackUp
            with open('BackUp.json', 'w', encoding='utf-8') as jsonFile:
                final = {}
                for node in loaded["allWorkItems"]["edges"]:
                    nested = {}
                    relevantData = d.getRelevantInfoFromJsonAllWorkingItems(node)
                    # sort by ID
                    IDofCurrentNode = node["node"]["case"]["document"]["id"]
                    os.chdir(r"C:\Users\David\Desktop\BA Code\Anwers")
                    d.saveAsJson(d.getDocument(IDofCurrentNode, d.getAnswerQuery), "Answer_"+ IDofCurrentNode)
                    relevantData["answer"] = d.getRelevantInfoFromJsonAnswers("Answer_"+IDofCurrentNode+".json")
                    nested[relevantData["id"]] = relevantData
                    final.update(nested)
                json.dump(final, jsonFile, indent=2)
                os.chdir(r"C:\Users\David\Desktop\BA Code")
                print("done")
            print(d.update())
        time.sleep(250)
if __name__ == '__main__':
    main()
