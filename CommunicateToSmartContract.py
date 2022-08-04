import hashlib
import json
from web3 import Web3

f = open("Config.json", 'r', encoding='utf-8')
config = json.load(f)

class CommunicateToSmartContract:
    def __init__(self):
        self.__mySCAdress = config["config"]["blockchain"]["SENDER_ADDRESS"]
        self.abi = config["config"]["blockchain"]["abi"]
        self.ScAddress = config["config"]["blockchain"]["CREATED_CONTRACT_ADDRESS"]
        self.w3 = Web3(Web3.HTTPProvider(config["config"]["blockchain"]["RPC_SERVER"]))
        self.contract_instance = self.w3.eth.contract(address=self.ScAddress, abi=self.abi)

    def createHash(self, jsontohash):
        """
        Hashes a JSON with the Sha 256 hash.
        :param jsontohash: The file (dictionary) that needs to be hashed.
        :return:
        """
        # TODO somehow the hash online and the one created here is not the same
        return hashlib.sha256(json.dumps(jsontohash).encode('utf8')).hexdigest()

    def createNewFormSmartContract(self, id, data, name_of_file):
        """
        Creates a new instance on the Blockchain, with the given parameters.
        :param id: ID of the form
        :param data: The file itself
        :param name_of_file: Name of the local file. "ID-Unix timestamp"
        """
        self.contract_instance.functions.createForm(id, data["name"], 1391, name_of_file,
                                                    self.createHash(data), "").transact({'from': self.__mySCAdress})

    def uptateFormOnSmartContract(self, id, BackUpFileName, name_of_file):
        """
        Updates a form instance on the Blockchain, with the given parameters.
        :param id: ID of the form
        :param BackUpFileName: Name of the BackUpFile.
        :param name_of_file: Name of the local file. "ID-Unix timestamp"
        """
        with open(BackUpFileName, 'r', encoding='utf-8') as f:
            data = json.load(f)  # Todo 1391 ersetzen mit  data[id]["lastmodified by"]
        self.contract_instance.functions.updateForm(id, 1391,  # additional answers may be given
                                                    name_of_file, self.createHash(data),
                                                    "").transact({'from': self.__mySCAdress})

    def freezeForm(self, id):
        """
        Freezes a from on the Blockchain
        :param id: ID of the form that needs to be frozen.
        """
        self.contract_instance.functions.freezeForm(id).transact({'from': self.__mySCAdress})

    def sendTopublicBC(self):
        pass
        # TODO: implement the communication to the public BC
