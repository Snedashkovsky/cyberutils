# cyberutils

<p>
    <img alt="GitHub" src="https://img.shields.io/github/license/Snedashkovsky/cyberutils">
    <img alt="Python" src="https://img.shields.io/pypi/pyversions/cyberutils">
    <img alt="pip" src="https://img.shields.io/pypi/v/cyberutils">
</p>
<p>
    <a href="https://pypi.org/project/cyberutils/">PyPI Package</a>
    ·
    <a href="https://github.com/Snedashkovsky/cyberutils">GitHub Repository</a>
</p>

## usage

### execute bash query
get bash query result and error
```python
from cyberutils.bash import execute_bash

execute_bash(
    bash_command='cyber status --node https://rpc.bostrom.cybernode.ai:443')
```
get json from bash query result
```python
from cyberutils.bash import get_json_from_bash_query

get_json_from_bash_query(
    bash_command='cyber status --node https://rpc.bostrom.cybernode.ai:443')
```

### execute a cosmwasm contract

```python
from cyber_sdk.client.lcd import LCDClient
from cyber_sdk.key.mnemonic import MnemonicKey

from cyberutils.contract import execute_contract

WALLET_SEED = 'rack canyon puzzle grow afford faint heavy kick furnace economy change loop debate tip acquire render rib truth bachelor monster page range wine measure'
CONTRACT_ADDRESS = 'bostrom1nwm9pjmfgmxgc4euyfps05p9pfde8vd4sm8pavy93eu9xquz27dsgyxtml'

# initiate lcd client and wallet
mk = MnemonicKey(mnemonic=WALLET_SEED)
lcd_client = LCDClient(
    url='https://lcd.bostrom.cybernode.ai/',
    chain_id='bostrom',
    prefix='bostrom'
)
wallet = lcd_client.wallet(mk)

# the execution message in a contract must match its schema
execute_msg = {
    "transfer" :  {
        "recipient": "bostrom1xszmhkfjs3s00z2nvtn7evqxw3dtus6yr8e4pw",
        "amount": "1000000"
    }
}

# execution of a contract
execute_contract(
    execute_msgs=[execute_msg],
    wallet=wallet,
    contract_address=CONTRACT_ADDRESS,
    lcd_client=lcd_client,
    gas=500_000,
    fee_amount=0,
    fee_denom='boot',
    memo='the first transfer')
```

### execute a graphql query

```python
import pandas as pd

from cyberutils.graphql import execute_graphql

res = await execute_graphql(
    request="""
        query AllContracts {
          contracts(order_by: {tx: desc_nulls_last}) {
            address
            admin
            code_id
            creation_time
            creator
            fees
            gas
            height
            label
            tx
          }
        }
        """,
    graphql_url='https://index.bostrom.cybernode.ai/v1/graphql')

pd.DataFrame(res['contracts'])
```