import json
import time

from CommunicateToSmartContract import CommunicateToSmartContract
from HandleData import HandleData

# make instances Global
d = HandleData()
c = CommunicateToSmartContract()


def main():
    global st
    st = time.time()
    d.refreshToken()
    d.saveAsJson(d.getAllWorkingItems(d.getAllWorkingItemsQuery), "AllWorkingItems")
    firstTimeRun()
    et = time.time()
    print('Execution time (Fetching, data parsing and BC interaction 1):', et - st, 'seconds')
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
            c.uptateFormOnSmartContract(id, d.nameNewestBackupFile,
                                        [item for item in local_names if item.startswith(id)][0])
    else:
        print("nothing to update")
    if ids_to_freeze:
        d.freezeForm(ids_to_freeze)
        st = time.time()
        [c.freezeForm(id) for id in ids_to_freeze]
        et = time.time()
        print('Execution time (cfreezing all COMPLETED forms 7):', et - st, 'seconds')



def creteNewFormOnSC(newFiles, local_names):
    if newFiles:
        for id, new_file in newFiles.items():
            c.createNewFormSmartContract(id, new_file, [item for item in local_names if item.startswith(id)][0])


def firstTimeRun():
    back_up_file_name = 'BackUp' + str(time.time()) + ".json"
    stt = time.time()
    with open(r'AllWorkingItems.json', encoding='utf-8') as f:
        loaded = json.load(f)
        # save the relevant data inside a nested json called BackUp
        d.nameNewestBackupFile = back_up_file_name
        with open(back_up_file_name, 'w', encoding='utf-8') as jsonFile:
            final, local_names = d.helperFunctionForExtractionAndSaving(loaded)
            json.dump(final, jsonFile, indent=2)
            ett = time.time()
            print('Execution time (extracting and fetching each form separately 4):', ett - stt, 'seconds')
            print('Execution time (Mirror the DB onto the host 2):', ett - stt, 'seconds')
            print("ran for the fist time")
            # send the created BackUp JSON to the local BC
            stBC = time.time()
            for id, val in final.items():
                c.createNewFormSmartContract(id, val, [item for item in local_names if item.startswith(id)][0])
            et = time.time()
            print('Execution time (creating SC on BC 3):', et - stBC, 'seconds')


if __name__ == '__main__':
    main()
