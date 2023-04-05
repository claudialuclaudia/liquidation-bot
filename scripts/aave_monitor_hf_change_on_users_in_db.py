import asyncio
import datetime

# from cosmosDb import get_all, get_db_and_col
from dbs.mongoDb import get_all, insert_aave_liquidation_opportunity
from aave_helper import get_health_stats, get_active_lending_pool_contracts

async def main():
    lp_contracts = get_active_lending_pool_contracts()

    coroutines = []
    for network in lp_contracts.keys():
        for protocol_and_version in lp_contracts.get(network).keys():
            lending_pool_contract = lp_contracts.get(network).get(protocol_and_version)
            coroutines.append(get_all_borrowers_in_db_hf(network, lending_pool_contract, protocol_and_version))
    
    await asyncio.gather(*coroutines)

async def get_all_borrowers_in_db_hf(network, lending_pool_contract, protocol_and_version):
    while True:
        print("Time is ", datetime.datetime.now())
        print("Getting all borrow events for network=", network, "protocol_and_version=", protocol_and_version, "...")
        # documents = get_all("borrowEvents", network) <<< cosmosDB
        documents = get_all(network, protocol_and_version) # mongoDB
        update_user_tasks = [_check_user_stats(doc['user'], network, lending_pool_contract, protocol_and_version) for doc in documents]
        await asyncio.gather(*update_user_tasks)
        await asyncio.sleep(1)


async def _check_user_stats(user, network, lending_pool_contract, protocol_and_version):
    # db, col = get_db_and_col("monitorUsers", network) <<< cosmos

    total_collateral_eth, current_liquidation_threshold, total_debt_eth, health_factor = get_health_stats(lending_pool_contract, user)
    if health_factor < 1:
        print("A user's hf just dropped below 1:")
        insert_aave_liquidation_opportunity(network, protocol_and_version, user, total_collateral_eth, current_liquidation_threshold, total_debt_eth, health_factor)

if __name__ == "__main__":    
    asyncio.run(main())