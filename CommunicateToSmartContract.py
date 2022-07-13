import hashlib
import json
import time

from web3 import Web3


class CommunicateToSmartContract:
    def __init__(self):
        self.__mySCAdress = "0x97d2b9dc20Ab4fcb08b5fef882E1ffDA08567c10"
        self.abi = """[
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_userID",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_company",
				"type": "string"
			}
		],
		"name": "addParticipant",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_id",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_createdByUser",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_fileName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_fileHash",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_additionalData",
				"type": "string"
			}
		],
		"name": "createForm",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_id",
				"type": "string"
			}
		],
		"name": "freezeForm",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "string",
				"name": "_formID",
				"type": "string"
			}
		],
		"name": "FormFrozen",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_id",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_lastModifiedBy",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_fileName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_fileHash",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_additionalData",
				"type": "string"
			}
		],
		"name": "updateForm",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "administrator",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "amountForms",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "forms",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"components": [
					{
						"internalType": "string",
						"name": "name",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "company",
						"type": "string"
					}
				],
				"internalType": "struct CheeseChainPrivate.Participant",
				"name": "createdByUser",
				"type": "tuple"
			},
			{
				"components": [
					{
						"internalType": "string",
						"name": "name",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "company",
						"type": "string"
					}
				],
				"internalType": "struct CheeseChainPrivate.Participant",
				"name": "lastModifiedBy",
				"type": "tuple"
			},
			{
				"internalType": "uint256",
				"name": "createdAt",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "lastModifiedAt",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "frozen",
				"type": "bool"
			},
			{
				"internalType": "string",
				"name": "fileName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "fileHash",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "additionalData",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "previousFileName",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "formsList",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_address",
				"type": "address"
			}
		],
		"name": "isAdministrator",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "partipants",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "company",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]"""
        self.ScAddress = '0xb5aa162A774E5BA2722Fa7f0466130FbE13725CF'
        self.w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
        self.contract_instance = self.w3.eth.contract(address=self.ScAddress, abi=self.abi)

    def createHash(self, jsontohash):
        #TODO somehow the hash online and the one created here is not the same
        return hashlib.sha256(json.dumps(jsontohash).encode('utf8')).hexdigest()

    def createNewFormSmartContract(self, id, data):
        self.contract_instance.functions.createForm(id, data["name"], 1391, data["id"]+str(time.time()), self.createHash(data), "").transact({'from': self.__mySCAdress})

    def uptateFormOnSmartContract(self, id, BackUpFileName):
        with open(BackUpFileName, 'r', encoding='utf-8') as f:
            data = json.load(f) # Todo 1391 ersetzen mit  data[id]["lastmodified by"]
        self.contract_instance.functions.updateForm(id, 1391,# additional answers may be given
                                                        data[id]["id"] + str(time.time()), self.createHash(data), "").transact({'from': self.__mySCAdress})

    def freezeForm(self, id):
        self.contract_instance.functions.freezeForm(id).transact({'from': self.__mySCAdress})

    def sendTopublicBC(self):
        pass
        # TODO: implement the communication to the public BC
