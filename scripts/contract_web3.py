import json
from web3 import Web3, HTTPProvider
#from web3.auto.infura.ropsten import web3

# https://dev.to/gcrsaldanha/deploy-a-smart-contract-on-ethereum-with-python-truffle-and-web3py-5on

# Infura email & pw: fokeg20453@gilfun.com
# WEB3_INFURA_PROJECT_ID=762d1e31835940f992bb35954922c7d4



def CreateCall(compiled_contract_path = '../build/contracts/ETHOptionsFactory.json', deployed_contract_address = '0x9BB465b8080019CfA71b1a2AFA9970E0FbF2452c', expiry=10000000000000, strike=1):
    
    #blockchain_address = 'http://127.0.0.1:9545' # truffle development blockchain address
    
    #web3 = Web3(HTTPProvider(blockchain_address)) # Client instance to interact with the blockchain

    WEB3_INFURA_PROJECT_ID='21163b9559174609975c67d0188e36db'

    web3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/"+WEB3_INFURA_PROJECT_ID))

    # Set the default account (so we don't need to set the "from" for every transaction call)
    web3.eth.defaultAccount = '0xd919F0F0e45C57d520BE7BD155f84506C2Ca0131' # web3.eth.accounts[0]

    # Path to the compiled contract JSON file
    #compiled_contract_path = '../build/contracts/ETHOptionsFactory.json'
    
    # Deployed contract address (see `migrate` command output: `contract address`)
    #deployed_contract_address = '0x9BB465b8080019CfA71b1a2AFA9970E0FbF2452c'

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

    # Fetch deployed contract reference
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    # Call contract function (this is not persisted to the blockchain)
    message = contract.functions.createCallOptionContract(expiry, strike)#.call()

    print(message)


    return message

def RopstenTest():

    WEB3_INFURA_PROJECT_ID='21163b9559174609975c67d0188e36db'

    web3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/"+WEB3_INFURA_PROJECT_ID))

    return web3.isConnected()