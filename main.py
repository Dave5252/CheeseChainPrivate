import json
import time

from HandleData import handleData


def main():
    d = handleData()

    while True:
        d.refreshToken()
        d.saveAsJson(d.getAllWorkingItems(), "AllWorkingItems")
        # d.saveAsJson(d.getDocument("f4f0d363-960f-4561-8de5-0dbd51669901"),"DocAnswer")

        with open('AllWorkingItems.json', encoding='utf-8') as f:
            loaded = json.load(f)
            # save the relevant data inside a nested json called BackUp
            with open('BackUp.json', 'w', encoding='utf-8') as jsonFile:
                final = {}
                for node in loaded["allWorkItems"]["edges"]:
                    nested = {}
                    relData = d.getRelevantInfoFromJsonAllWorkingItems(node)
                    # sort by ID
                    nested[relData["id"]] = relData
                    d.saveAsJson(d.getDocument("f4f0d363-960f-4561-8de5-0dbd51669901"), "DocAnswer")
                    nested["awsners"] = d.getRelevantInfoFromJsonAnswers('DocAnswer.json')

                    final.update(nested)
                json.dump(final, jsonFile, indent=2)



        #print(d.getRelevantInfoFromJsonAnswers('DocAnswer.json'))

        time.sleep(250)
main()