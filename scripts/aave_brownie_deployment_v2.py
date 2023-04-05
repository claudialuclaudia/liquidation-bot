from brownie import FlashloanV2, accounts, config, network
from dotenv import load_dotenv
from pyaml_env import parse_config

load_dotenv()
config = parse_config("./config.yaml")

def main():
    """
    Deploy a `FlashloanV2` contract from `accounts[0]`.
    """

    acct = accounts.add(
        config["wallets"]["from_key"]
    )  # add your keystore ID as an argument to this call

    flashloan = FlashloanV2.deploy(
        config["networks"][network.show_active()]["aave_lending_pool_v2"],
        {"from": acct},
    )
    return flashloan
