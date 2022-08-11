import json
import time

from CommunicateToSmartContract import CommunicateToSmartContract
from HandleData import HandleData

# make instances Global
d = HandleData()
c = CommunicateToSmartContract()


def main():
    """
    Main function, calling the most important functions. Everything before the the while true loop is executed only
    once. The while true loop is a infinite loop, meaning the DigitalQM is always checked for new forms and the RUNNING
    ones are updated.

    """
    global st
    st = time.time()
    d.refreshToken()
    d.saveAsJson(d.getAllWorkingItems(d.getAllWorkingItemsQuery), "AllWorkingItems")
    firstTimeRun()
    et = time.time()
    print('Execution time (Fetching, data parsing and BC interaction 2):', et - st, 'seconds')
    while True:
        d.refreshToken()
        refetchingFreezingAndUpdating()
        new_files, local_names = d.checkForNewFiles()
        creteNewFormOnSC(new_files, local_names)
        et = time.time()
        print('Execution time (Fetching, data parsing and BC interaction& updatign freezing 1):', et - st, 'seconds')
        # time.sleep(200)
        time.sleep(10)


def refetchingFreezingAndUpdating():
    """
    Calls the updateFiles function, which returns a list of the forms that need to be updated and the ones that need to be
    frozen. The local names are also returned by the update function, as the names need to bed the same in the local BC.
    The updateFiles function already saved the files locally, only the BC need to updated.
    """
    updated_ids, ids_to_freeze, local_names = d.updateFiles()
    # If there are forms to update: Iterate, and call the function updateFormOnSmartContract to update the BC.
    if updated_ids:
        print("to update: ", updated_ids)
        for id in updated_ids:
            c.updateFormOnSmartContract(id, d.nameNewestBackupFile,
                                        [item for item in local_names if item.startswith(id)][0])
    else:
        print("nothing to update")
    # If there are forms that got frozen: Freeze on the BC and locally.
    if ids_to_freeze:
        # Freeze locally
        d.freezeForm(ids_to_freeze)
        st = time.time()
        # Freeze on BC
        [c.freezeForm(id) for id in ids_to_freeze]
        et = time.time()
        print('Execution time (cfreezing all COMPLETED forms 7):', et - st, 'seconds')



def creteNewFormOnSC(newFiles, local_names):
    """
    Creates new instance on the BC.
    :param newFiles: A dict with the new form that need to be created on the BC. Key is the ID and val the content.
    :param local_names: Their local names, to have constant naming on the BC and the host.
    """
    if newFiles:
        for id, new_file in newFiles.items():
            c.createNewFormSmartContract(id, new_file, [item for item in local_names if item.startswith(id)][0])


def firstTimeRun():
    """
    Helper function when the script is first ran. Creating the Backup file, saving the forms and their answers locally.
    """
    back_up_file_name = 'BackUp' + str(int(time.time())) + ".json"
    stt = time.time()
    with open(r'AllWorkingItems.json', encoding='utf-8') as f:
        loaded = json.load(f)
        # save the relevant data inside a nested json called BackUp
        d.nameNewestBackupFile = back_up_file_name
        with open(back_up_file_name, 'w', encoding='utf-8') as jsonFile:
            # Pass the json with AllWorkingItems into the helperFunctionForExtractionAndSaving to first save and
            # extract. The Returns the local names and the json for the BackUp file.
            final, local_names = d.helperFunctionForExtractionAndSaving(loaded)
            json.dump(final, jsonFile, indent=2)
            ett = time.time()
            print('Execution time (Mirror the DB onto the host 2):', ett - stt, 'seconds')
            print("ran for the fist time")
            # send the created BackUp JSON to the local BC
            stBC = time.time()
            for id, val in final.items():
                # For each form create an instance on the BC
                c.createNewFormSmartContract(id, val, [item for item in local_names if item.startswith(id)][0])
            et = time.time()
            print('Execution time (creating SC on BC 3):', et - stBC, 'seconds')


if __name__ == '__main__':
    main()
