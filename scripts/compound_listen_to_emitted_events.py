from pyaml_env import parse_config
from web3 import Web3
from abis.compound_abis import comptroller_abi
import os

from helper import get_contract

def main():
    contract = get_contract("kovan", "compound_comptroller", comptroller_abi)
    event_filter = contract.events.MarketEntered.createFilter(fromBlock='latest')
    while True:
        market_entrances = event_filter.get_new_entries()
        for market_entrance in market_entrances:
            print('################################################')
            print(Web3.toJSON(market_entrance))
# ex.: {"args": {"cToken": "0x41B5844f4680a8C38fBb695b7F9CFd1F64474a72", "account": "0x93Ef9C5A0C82804241BFf9E41EC57E36498A49fb"}, "event": "MarketEntered", "logIndex": 2, "transactionIndex": 5, "transactionHash": "0x1b64bc8e2edec63934e2f920bb372989e63a38131204675121029d6c435ed683", "address": "0x5eAe89DC1C671724A672ff0630122ee834098657", "blockHash": "0x07c87ae91214dd72dd3f56073232ddf845e1f322f78b52b9b831b8eff00f16c8", "blockNumber": 31976251}
#TODO: implement listening to more then one network
#TODO: save to db
#TODO: listen to MarketExited as well

if __name__ == "__main__":
    main()