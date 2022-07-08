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
        d.refreshToken()
        refetchingFreezingAndUpdating()
        time.sleep(25)
        d.checkForNewFiles()
        time.sleep(200)

def refetchingFreezingAndUpdating():
    updatedids, idstofreeze = d.update()
    if updatedids:
        print("to update: ",updatedids)
        for id in updatedids:
            c.uptateFormOnSmartContract(id, d.nameNewestBackupFile)
    else: print("nothing to update")
    if idstofreeze:
        d.freezeForm(idstofreeze)
        [c.freezeForm(id) for id in idstofreeze]


def firstTimeRun():

    backUpFileName = 'BackUp' + str(time.time()) + ".json"
    with open(r'C:\Users\David\Desktop\BA Code\AllWorkingItems.json', encoding='utf-8') as f:
        loaded = json.load(f)
        # save the relevant data inside a nested json called BackUp
        d.nameNewestBackupFile = backUpFileName
        with open(backUpFileName, 'w', encoding='utf-8') as jsonFile:
            final = d.helperFunctionForExtracionAndSaving(loaded)
            json.dump(final, jsonFile, indent=2)
            print("ran for the fist time")
            # send the created BackUp JSON to the local BC
            for id, val in final.items():
                c.createNewFormSmartContract(id, val)

if __name__ == '__main__':
    main()
