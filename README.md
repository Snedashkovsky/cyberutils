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
import requests

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

# an execution message in a contract must match its schema
execute_msg = {
    "transfer" :  {
        "recipient": "bostrom1xszmhkfjs3s00z2nvtn7evqxw3dtus6yr8e4pw",
        "amount": "1000000"
    }
}

# load a contract schema for an execute message validation
contract_schema_json = \
    requests.get(
        url='https://raw.githubusercontent.com/Snedashkovsky/cw-plus/main/contracts/cw20-base/schema/cw20-base.json'
    ).json()

# execution of a contract
execute_contract(
    execute_msgs=[execute_msg],
    wallet=wallet,
    contract_address=CONTRACT_ADDRESS,
    lcd_client=lcd_client,
    gas=500_000,
    fee_amount=0,
    fee_denom='boot',
    contract_execute_schema=contract_schema_json['execute'],
    memo='the first transfer')
```

### query a cosmwasm contract

```python
from cyberutils.contract import query_contract

query_contract(
    query={
        'get_asset': {
            'chain_name': 'osmosis',
            'base': 'ibc/FE2CD1E6828EC0FAB8AF39BAC45BC25B965BA67CCBC50C13A14BD610B0D1E2C4'
        }
    },
    contract_address='bostrom1w33tanvadg6fw04suylew9akcagcwngmkvns476wwu40fpq36pms92re6u',
    node_lcd_url='https://lcd.bostrom.cybernode.ai'
)
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
a query with variable values
```python
import pandas as pd

from cyberutils.graphql import execute_graphql

res = await execute_graphql(
    request="""
        query ContractsCodeID($code_id: bigint) {
            contracts(order_by: {tx: desc_nulls_last}, where: {code_id: {_eq: $code_id}}) {
                address
                admin
                creation_time
                creator
                fees
                gas
                height
                label
                tx
                code_id
            }
        }
        """,
    variable_values={"code_id": "3"},
    graphql_url='https://index.bostrom.cybernode.ai/v1/graphql')

pd.DataFrame(res['contracts'])
```
get messages with a given address and type
```python
import pandas as pd

from cyberutils.graphql import get_messages_by_address_and_type


res = await get_messages_by_address_and_type(
    address='bostrom1xszmhkfjs3s00z2nvtn7evqxw3dtus6yr8e4pw',
    msg_type='cosmos.bank.v1beta1.MsgSend',
    graphql_url='https://index.bostrom.cybernode.ai/v1/graphql')

pd.DataFrame(res)
```