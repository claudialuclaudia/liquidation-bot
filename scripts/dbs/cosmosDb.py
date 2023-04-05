from dotenv import load_dotenv
import os
import pymongo
import datetime
# from bson.decimal128 import Decimal128

load_dotenv()
uri = os.getenv("COSMOS_DB_URI")
client = pymongo.MongoClient(uri)
try:
    client.server_info() # validate connection string
except pymongo.errors.ServerSelectionTimeoutError:
    raise TimeoutError("Invalid API for MongoDB connection string or timed out when attempting to connect")

def get_db_and_col(db, col):
    db = client[db]
    col = db[col]
    return db, col

def insert_liquidationEvents(event, total_collateral_eth, current_liquidation_threshold, total_debt_eth, health_factor, network):
    db = client["liquidationEvents"]
    col = db[network]

    args = event.args

    col.insert_one(args)
    # TODO: fill these args out & add hf variables

def insert_aave_borrowEvents(event, total_collateral_eth, current_liquidation_threshold, total_debt_eth, health_factor, network):
    db = client["borrowEvents"]
    col = db[network]

    args = event.args
    entry = {
        "reserve": args.reserve,
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
        "timestamp": datetime.datetime.now().timestamp()*1000,
        "currentTotalCollateralETH": str(total_collateral_eth),
        "currentLiquidationThreshold": str(current_liquidation_threshold),
        "currentTotalDebtETH": str(total_debt_eth),
        "currentHealthFactor": str(health_factor)
    }

    col.insert_one(entry)

def get_all(db, col):
    db, col = get_db_and_col(db, col)

    cursor = col.find({})
    return cursor