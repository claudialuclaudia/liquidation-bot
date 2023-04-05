from dotenv import load_dotenv
from pyaml_env import parse_config
from web3 import Web3
import os

load_dotenv()
my_address = Web3.toChecksumAddress(os.getenv("MY_ADDRESS"))
config = parse_config("./config.yaml")    

def get_contract(network, address_name, abi):
    print("Getting contract for: ", network, address_name)

    w3 = Web3(Web3.HTTPProvider(config["networks"][network]["rpc_url"]))
    add = Web3.toChecksumAddress(config["networks"][network][address_name])
    contract = w3.eth.contract(address=add, abi=abi)
    return contract

def build_and_sign_and_send_transaction(network, function, amount):
    print("Building and signing transaction:")

    w3 = Web3(Web3.HTTPProvider(config["networks"][network]["rpc_url"]))
    nonce = w3.eth.getTransactionCount(my_address)
    transaction = function.buildTransaction(
        {
            "chainId": config["networks"][network]["chain_id"],
            "from": my_address,
            "nonce": nonce,
            "value": amount,
        }
    )
    signed_txn = w3.eth.account.sign_transaction(
        transaction, private_key=os.getenv("PRIVATE_KEY")
    )
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Here is the tx hash: {tx_hash.hex()}")
    print("waiting for transaction receipt...")
    whatsthis = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Done. whatsthis is: ", whatsthis)