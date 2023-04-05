import os

from dotenv import load_dotenv
from pyaml_env import parse_config
from web3 import Web3
from abis.aave_abis import (
    v3_lending_pool_addresses_provider_abi,
    lending_pool_addresses_provider_abi,
    lending_pool_abi,
)

load_dotenv()

def get_health_stats(lending_pool, address):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        tlv,
        health_factor,
    )  = lending_pool.functions.getUserAccountData(address).call()
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    current_liquidation_threshold = Web3.fromWei(current_liquidation_threshold, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    health_factor = Web3.fromWei(health_factor, "ether")

    # print(f"User={address} have total_collateral_eth={total_collateral_eth} current_liquidation_threshold={current_liquidation_threshold} total_debt_eth={total_debt_eth} health_factor={health_factor}")
    return total_collateral_eth, current_liquidation_threshold, total_debt_eth, health_factor

def get_active_lending_pool_contracts():
    print("get_active_lending_pool_contracts")
    config = parse_config("./config.yaml")
    networks = config["networks"]["active"].split()
    result = {}
    for network in networks:
        w3 = Web3(Web3.HTTPProvider(config["networks"][network]["rpc_url"]))
        lending_pools = get_lending_pools(config, network, w3)
        result[network] = lending_pools
    return result
    # result looks like:
    # kovanTestnet: aave_lending_pool_v2: lp_contract
    # polygonMaticMainnet: aave_lending_pool_v2: lp_contract
    #                     aave_lending_pool_v3: lp_contract
    # ...

def get_lending_pools(config, network, w3):
    print("get_lending_pools", network, w3)
    result = {}
    if "aave_lending_pool_v2" in config["networks"][network]:
        result['aave_lending_pool_v2'] = _get_lending_pool(config, network, w3, 'aave_lending_pool_v2')
    if "aave_lending_pool_v3" in config["networks"][network]:
        result['aave_lending_pool_v3'] = _get_lending_pool(config, network, w3, 'aave_lending_pool_v3')
    return result

def _get_lending_pool(config, network, w3, protocol_and_version):
    print("_get_lending_pool", config, network, w3, protocol_and_version)
    lending_pool_addresses_provider_address = Web3.toChecksumAddress(
        config["networks"][network][protocol_and_version]
    )
    if protocol_and_version.split('_')[len(protocol_and_version.split('_'))-1] == 'v3':
        lending_pool_addresses_provider = w3.eth.contract(
            address=lending_pool_addresses_provider_address,
            abi=v3_lending_pool_addresses_provider_abi,
        )
        lending_pool_address = (
            lending_pool_addresses_provider.functions.getPool().call()
        )
    else: #v2 only i think
        lending_pool_addresses_provider = w3.eth.contract(
            address=lending_pool_addresses_provider_address,
            abi=lending_pool_addresses_provider_abi,
        )
        lending_pool_address = (
            lending_pool_addresses_provider.functions.getLendingPool().call()
        )
    lending_pool = w3.eth.contract(
        address=lending_pool_address, abi=lending_pool_abi)
    return lending_pool