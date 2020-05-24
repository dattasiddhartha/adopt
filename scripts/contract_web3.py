import json
import cryptocompare
from web3 import Web3, HTTPProvider
#from web3.auto.infura.ropsten import web3

# https://dev.to/gcrsaldanha/deploy-a-smart-contract-on-ethereum-with-python-truffle-and-web3py-5on

# Infura email & pw: fokeg20453@gilfun.com
# WEB3_INFURA_PROJECT_ID=762d1e31835940f992bb35954922c7d4

#TODO: Refactor (Don't repeat yourself)

private_key = '7D89E06EEEA913ECAF2752CF689F89931DEE8FDDF7D6A641A498FCA3C0CA5F1D'

def OptionInTheMoney(strike_price, option_type):
    #get price at expiry
    spot_price = cryptocompare.get_price('BTC',curr='USD')['BTC']['USD']
    if option_type == "CALL":
        #calls are in the money if strike <= spot
        return (strike_price <= spot_price)
    elif option_type == "PUT":
        #puts are in the money if strike >= spot
        return (strike_price >= spot_price)
    else:
        print("Invalid input provided")

#need to look up option address that corresponds to the desired strike and expiry  
def SellCall(deployed_contract_address, token_amount): 
    token_amount = int(amount*10**18)
    # should not be doing te same things we did in CreateCall. Needs refactor
    compiled_contract_path = '../build/contracts/ETHCallOption.json'
    WEB3_INFURA_PROJECT_ID='21163b9559174609975c67d0188e36db'
    web3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/"+WEB3_INFURA_PROJECT_ID))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    message = contract.functions.writeOption(token_amount) #should return true if successful
    return message

def SellPut(deployed_contract_address, token_amount): 
    token_amount = int(amount*10**18)
    compiled_contract_path = '../build/contracts/ETHPutOption.json'
    WEB3_INFURA_PROJECT_ID='21163b9559174609975c67d0188e36db'
    web3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/"+WEB3_INFURA_PROJECT_ID))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    message = contract.functions.writeOption(token_amount) #should return true if successful
    return message


def ExerciseCall(deployed_contract_address, token_amount):
    token_amount = int(amount*10**18)
    compiled_contract_path = '../build/contracts/ETHCallOption.json'
    WEB3_INFURA_PROJECT_ID='21163b9559174609975c67d0188e36db'
    web3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/"+WEB3_INFURA_PROJECT_ID))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    message = contract.functions.exerciseOption(token_amount) #should return true if successful
    return message

def ExercisePut(deployed_contract_address, token_amount):
    token_amount = int(amount*10**18)
    compiled_contract_path = '../build/contracts/ETHPutOption.json'
    WEB3_INFURA_PROJECT_ID='21163b9559174609975c67d0188e36db'
    web3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/"+WEB3_INFURA_PROJECT_ID))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    message = contract.functions.exerciseOption(token_amount) #should return true if successful
    return message



def CreateCall(compiled_contract_path = '../build/contracts/ETHOptionsFactory.json', deployed_contract_address = '0x9BB465b8080019CfA71b1a2AFA9970E0FbF2452c', expiry=10000000000000, strike=1):
    
    #blockchain_address = 'http://127.0.0.1:9545' # truffle development blockchain address
    
    #web3 = Web3(HTTPProvider(blockchain_address)) # Client instance to interact with the blockchain

    WEB3_INFURA_PROJECT_ID='21163b9559174609975c67d0188e36db'

    web3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/"+WEB3_INFURA_PROJECT_ID))

    # Set the default account (so we don't need to set the "from" for every transaction call)
    #web3.eth.defaultAccount = '0xd919F0F0e45C57d520BE7BD155f84506C2Ca0131' # web3.eth.accounts[0]
    web3.eth.defaultAccount = '0xf4F808E0509c9942153557A6CFDcE9639C0EC69F'
    #web3.eth.defaultAccount = web3.eth.accounts[0]
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
    #message = contract.functions.createCallOptionContract(expiry, strike)#.call()

    create_call_txn = contract.functions.createCallOptionContract(expiry, strike).buildTransaction({
        'chainId': 3,
        'gas': 70000,
        'gasPrice': web3.toWei('1', 'gwei'), 
        'nonce': 90001,
    })

    signed_create_call_txn = web3.eth.account.sign_transaction(create_call_txn, private_key=private_key)

    message = web3.eth.sendRawTransaction(signed_create_call_txn.rawTransaction)  

#     >>> unicorn_txn = unicorns.functions.transfer(
# ...     '0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359',
# ...     1,
# ... ).buildTransaction({
# ...     'chainId': 1,
# ...     'gas': 70000,
# ...     'gasPrice': w3.toWei('1', 'gwei'),
# ...     'nonce': nonce,
# ... })

    print(message)

    return message

def RopstenTest():

    WEB3_INFURA_PROJECT_ID='21163b9559174609975c67d0188e36db'

    web3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/"+WEB3_INFURA_PROJECT_ID))

    return web3.isConnected()