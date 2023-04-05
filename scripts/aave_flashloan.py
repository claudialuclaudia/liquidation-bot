from brownie import Contract, FlashloanV2, accounts, config, network
from eth_abi import encode

from helper import get_contract, build_and_sign_and_send_transaction

from dotenv import load_dotenv
from pyaml_env import parse_config
from web3 import Web3
from abis import comptroller_abi, cETH
import os

from scripts.helper import build_and_sign_and_send_transaction, get_contract

load_dotenv()
WETH_AMOUNT = 0.001
AMOUNT = int(WETH_AMOUNT * 10 ** 18)
NETWORK = "kovan"

def call_aave_flashloan(borrower_add, collateral_add):
    # Step 0: make sure there's enought WETH for transaction fee
    # Step 1: Deploy the FlashloanV2.sol contract.
    aave_lending_pool_v2= config["networks"][NETWORK]["aave_lending_pool_v2"]
    params = abi_encode_args(param1, param2) #TODO: figure out these params
    flashloan = FlashloanV2.deploy(aave_lending_pool_v2, {"from": accounts[0]})
    # Step 2: Perform our flash loan
    WETH = Contract(config["networks"][NETWORK]["weth"])
    tx = flashloan.flashloan(WETH, {"from": accounts[0]})

# params are: collateralAsset, borrowedAsset, user, debtToCover, useEthPath
def abi_encode_args(param1, param2):
    # const params = web3.eth.abi.encodeParameters(
    #     ["bytes32"],
    #     [
    #         web3.utils.utf8ToHex("some_value")
    #     ]
    # encode(['bytes32', 'bytes32'], [b'a', b'b'])
    encode(['bytes32', 'bytes32'], [param1, param2])

if __name__ == "__main__":
    call_aave_flashloan()