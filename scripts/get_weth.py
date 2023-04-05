from web3 import Web3
from abis import weth_abi
from pyaml_env import parse_config
from dotenv import load_dotenv
import os

from scripts.helper import build_and_sign_and_send_transaction, get_contract

load_dotenv()

config = parse_config("./config.yaml")
network = config["networks"]["active"]
WETH_AMOUNT = 0.001
AMOUNT = int(WETH_AMOUNT * 10 ** 18)

def main():
    """
    Runs the get_weth function to get WETH
    """
    get_weth()


def get_weth():
    """
    Mints WETH by depositing ETH.
    """
    print("Getting WETH!")

    function = get_contract(network, "weth", weth_abi).functions.deposit()
    build_and_sign_and_send_transaction("kovan", function, AMOUNT)


if __name__ == "__main__":
    main()
