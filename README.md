
# CheeseChainPrivate

Design and Implementation of a Database-to-Blockchain Data Gathering Solution for Cheese Tracking

## Authors

- [@Dave5252](https://github.com/Dave5252)


## Installation

Note that for different operating systems the commands are slightly different.


Download Ganache from the truffle website: https://trufflesuite.com/ganache/
Clone the project from: 


```bash
  git clone https://github.com/Dave5252/CheeseChainPrivate.git
  pip install -r requirements.txt
```


 Copy paste the Smart Contract from the CheeseChainPrivate directory into the remix online IDE <https://remix.ethereum.org/>

To run the main file the the SC needs to be deployed and the refresh token needs to be extracted from the fromarte webpage.

 1. Quickstart a Etherium BC on Ganache
 2. Copy the **RPC SERVER** address
 3. Compile the SC on remix
 4. Select Ganache as an Environment, paste in the **RPC SERVER** address.
 5. Deploy the SC
 6. On Ganache in transactions select the deployed SC and copy the **SENDER ADDRESS** and **CREATED CONTRACT ADDRESS** into the corresponding variables in the `config.json` `["config"]["blockchain"]` file in the directory.
 7. (Only if the refresh token is invalid. I.e., after logging in with the account on a different host) Login into Fromarte, with the Developer Tools Interface (F12) open on the network tab and copy the refresh token from the `token` into the `config.json file`  `["config"]["fromarte"]`.
 8. Run the `main.py` file

## Synchronization
The files are synchronized onto the host and the BC, with the ID (e.g. RG9jdW1lbnQ6MDg2Yzc3ODAtNDZlYS00Y2IyLThlMWQtMjliZmU0MzQ2NWYy) forms can be fetched form the BC trough the remix IDE. 
In the folder `BackupFiles` the corresponding files with the relevant information can be found, aswell as all **RUNNING** forms in the `BackUp.json` file in the main directory.


    
