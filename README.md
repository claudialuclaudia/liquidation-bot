# Aave
1. listen to events emitted from aave (Borrow, LiquidationCall, etc.) and save them to cosmosDB (`python ./scripts/aave_listen_to_emitted_events.py`)
2. monitor health factor change on users that have a borrow recorded in the db (`python ./scripts/aave_monitor_hf_change_on_users_in_db.py`)

# Compound
1. listen to events emitted from compound (MarketEntered, MarketExited) (`python ./scripts/compound_listen_to_emitted_events.py`)
2. compound library (cTokens, comptroller) (`python ./scripts/compound_wrapper.py`)
# Other
1. liquidate using [ftx's liquidations algorithm](https://help.ftx.com/hc/en-us/articles/360027668712-Liquidations) (`./scripts/ftx_liquidation_execution.py`)
2. `IN PROGRESS:` upload past borrows from tenderly so we can backfill them into our db (`./scripts/upload_past_borrows_from_tenderly.py`)
3. `IN PROGRESS:` Borrow from aave flash loan and liquidate account on compound(`aave_flashloan.py` `./contracts/v2/FlashloanV2.sol`)
- `brownie run scripts/deployment_v2.py --network kovan`
- `brownie run scripts/run_flash_loan_v2.py --network kovan`

# Setup
`pip install -r requirements.txt`

# How to run brownie scripts
[Aave Brownie Mix](https://github.com/brownie-mix/aave-flashloan-mix)