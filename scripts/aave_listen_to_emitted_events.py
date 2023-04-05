import asyncio
import datetime
from web3 import Web3

# import cosmosDb
from dbs import mongoDb
from aave_helper import get_health_stats, get_active_lending_pool_contracts

async def main():
    lp_contracts = get_active_lending_pool_contracts()

    coroutines = []
    for network in lp_contracts.keys():
        for protocol_and_version in lp_contracts.get(network).keys():
            lending_pool_contract = lp_contracts.get(network).get(protocol_and_version)
            borrow_filter = lending_pool_contract.events.Borrow.createFilter(fromBlock='latest')
            coroutines.append(insert_emitted_events_to_db(network, lending_pool_contract, borrow_filter, 1, protocol_and_version)) #TODO: poll intervel different for each networks??????

            #TODO: implement cosmosDB.insert for other type of events
            # liquidation_calls = lending_pool.events.LiquidationCall.createFilter(fromBlock='latest').get_new_entries()

    await asyncio.gather(*coroutines)

async def insert_emitted_events_to_db(network, lending_pool, event_filter, poll_interval, protocol_and_version):
    # TODO: potentially: for each of the new Borrow entries, calculate the user's health factor
    while True:
        # print("time rn is: ", datetime.datetime.now(), " network is: ", network)
        entries = event_filter.get_new_entries() # gets all the entries on the blockchain that fits the event_filter

        for entry in entries: 
            print('################################################')
            print(Web3.toJSON(entry))
            total_collateral_eth, current_liquidation_threshold, total_debt_eth, health_factor = get_health_stats(lending_pool, entry.args.user)
            # cosmosDb.insert_aave_borrowEvents(entry, total_collateral_eth, current_liquidation_threshold, total_debt_eth, health_factor, network)
            mongoDb.insert_aave_borrowEvents(entry, total_collateral_eth, current_liquidation_threshold, total_debt_eth, health_factor, network, protocol_and_version)

        await asyncio.sleep(poll_interval)

if __name__ == "__main__":
    asyncio.run(main())