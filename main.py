import json
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
        time.sleep(10)
        new_files, local_names = d.checkForNewFiles()
        creteNewFormOnSC(new_files, local_names)
        # time.sleep(200)
        time.sleep(10)


def refetchingFreezingAndUpdating():
    updated_ids, ids_to_freeze, local_names = d.updateFiles()
    if updated_ids:
        print("to update: ", updated_ids)
        for id in updated_ids:
            c.uptateFormOnSmartContract(id, d.nameNewestBackupFile, [item for item in local_names if item.startswith(id)][0])
    else:
        print("nothing to update")
    if ids_to_freeze:
        d.freezeForm(ids_to_freeze)
        [c.freezeForm(id) for id in ids_to_freeze]


def creteNewFormOnSC(newFiles, local_names):
    if newFiles:
        for id, new_file in newFiles.items():
            c.createNewFormSmartContract(id, new_file,[item for item in local_names if item.startswith(id)][0])


def firstTimeRun():
    back_up_file_name = 'BackUp' + str(time.time()) + ".json"
    with open(r'AllWorkingItems.json', encoding='utf-8') as f:
        loaded = json.load(f)
        # save the relevant data inside a nested json called BackUp
        d.nameNewestBackupFile = back_up_file_name
        with open(back_up_file_name, 'w', encoding='utf-8') as jsonFile:
            final, local_names = d.helperFunctionForExtractionAndSaving(loaded)
            json.dump(final, jsonFile, indent=2)
            print("ran for the fist time")
            # send the created BackUp JSON to the local BC
            for id, val in final.items():
                c.createNewFormSmartContract(id, val, [item for item in local_names if item.startswith(id)][0])


if __name__ == '__main__':
    main()
