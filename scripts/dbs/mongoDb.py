from dotenv import load_dotenv
import os
from pymongo import MongoClient
import pymongo
import datetime
from pprint import pprint

load_dotenv()
uri = os.getenv("COSMOS_DB_URI")
client = MongoClient(os.getenv("MONGO_DB_URI"))

def insert_aave_borrowEvents(event, total_collateral_eth, current_liquidation_threshold, total_debt_eth, health_factor, network, protocol_and_version):
    print("insert_aave_borrowEvents", event, total_collateral_eth, current_liquidation_threshold, total_debt_eth, health_factor, network, protocol_and_version)
    db, col = _get_db_and_col(network, protocol_and_version)

    args = event.args
    entry = {
        "reserve": args.reserve,
        "eventType": 'Borrow',
        "onBehalfOf": args.onBehalfOf,
        "referral": args.referral,
        "user": args.user,
        "amount": str(args.amount),
        "borrowRateMode": args.borrowRateMode,
        "borrowRate": str(args.borrowRate),
        "logIndex": event.logIndex,
        "transactionIndex": event.transactionIndex,
        "transactionHash": event.transactionHash,
        "address": event.address,
        "blockHash": event.blockHash,
        "blockNumber": event.blockNumber,
        "createdAt": datetime.datetime.now().timestamp()*1000,
        "currentTotalCollateralETH": str(total_collateral_eth),
        "currentLiquidationThreshold": str(current_liquidation_threshold),
        "currentTotalDebtETH": str(total_debt_eth),
        "currentHealthFactor": str(health_factor)
    }

    col.insert_one(entry)

def insert_aave_liquidation_opportunity(
    network,
    lending_pool_contract,
    user,
    total_collateral_eth, 
    current_liquidation_threshold,
    total_debt_eth,
    health_factor
):
    db, col = _get_db_and_col(network, lending_pool_contract)
    entry = {
        "eventType": 'Liquidation Opportunity',
        "user": str(user),
        "createdAt": datetime.datetime.now().timestamp()*1000,
        "total_collateral_eth": str(total_collateral_eth),
        "current_liquidation_threshold": str(current_liquidation_threshold),
        "total_debt_eth": str(total_debt_eth),
        "health_factor": str(health_factor)
    }
    print("insert_aave_liquidation_opportunity", entry)

    col.insert_one(entry)
    # col.update_one({"user": user}, {"$set": entry}, upsert=False)

def get_all(network, protocol_and_version):
    db, col = _get_db_and_col(network, protocol_and_version)

    cursor = col.find({})
    return cursor

def _get_db_and_col(network, protocol_and_version):
    db = client[network]
    col = db[_get_col_name(protocol_and_version)]
    
    return db, col

def _get_col_name(protocol_and_version):
    if protocol_and_version == 'aave_lending_pool_v2':
        return 'aave_v2'
    elif protocol_and_version == 'aave_lending_pool_v3':
        return 'aave_v3'
    else:
        raise KeyError('no protocol known as ', protocol_and_version)