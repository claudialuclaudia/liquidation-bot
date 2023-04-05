import os

from dotenv import load_dotenv
from pyaml_env import parse_config
from web3 import Web3
from helper import build_and_sign_and_send_transaction, get_contract
from abis.compound_abis import cETH, comptroller_abi

config = parse_config("./config.yaml")
NETWORK = config["networks"]["active"]

def mint(address_name, abi): #transfers an asset into the protocol (and mints equivalent cToken)
    function = get_contract(NETWORK, address_name, abi).functions.mint()
    build_and_sign_and_send_transaction(NETWORK, function)

def getAccountLiquidity(account_add):
    tx = get_contract(NETWORK, "compound_comptroller", comptroller_abi).functions.getAccountLiquidity(account_add).call()
    print("tx is:", tx)

def exchangeRateCurrent(address_name, abi):
    exchangeRate = get_contract(NETWORK, address_name, abi).functions.exchangeRateCurrent().call() 
    scaled = exchangeRate / (10 ** 18)
    print("exchangeRate is:", exchangeRate)
    print("scaled is:", scaled)

# mint("compound_cETH", cETH)
exchangeRateCurrent("compound_cETH", cETH)