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

### execute bash queries

```python
from cyberutils.bash import execute_bash

execute_bash(
    bash_command='cyber status --node https://rpc.bostrom.cybernode.ai:443')
```

```bash
{"NodeInfo":{"protocol_version":{"p2p":"8","block":"11","app":"0"},"id":"6546edd90cfa8e33753653ef5048e2242686ad76","listen_addr":"tcp://88.198.18.156:26656","network":"bostrom","version":"v0.34.21","channels":"40202122233038606100","moniker":"85491d1cbf43","other":{"tx_index":"on","rpc_address":"tcp://0.0.0.0:26657"}},"SyncInfo":{"latest_block_hash":"17C750DF078141AA30A2428ABDB06E117D236B9971E1E06DDFAA8DCEB5203751","latest_app_hash":"A4FEFCEC8028BA9B1812FCD13BE5449D6F2E673FCBD7E98283DDD4CB534D6F13","latest_block_height":"8010914","latest_block_time":"2023-05-03T03:30:12.631211969Z","earliest_block_hash":"3C6BEA9792C0E70B6A1F29D9B75A0A4387195C86185EAA9BF44C27F19FB799D0","earliest_app_hash":"E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855","earliest_block_height":"1","earliest_block_time":"2021-11-05T13:22:42Z","catching_up":false},"ValidatorInfo":{"Address":"2E036BC5B3476FABE0DCBF841DB4F5FCF978A089","PubKey":{"type":"tendermint/PubKeyEd25519","value":"110HUJd7XFqWhXbE/nF1D4pFcM/vQ8D9yOJbyQF6gsc="},"VotingPower":"0"}}
(b'', None)
```

```python
from cyberutils.bash import get_json_from_bash_query

get_json_from_bash_query(
    bash_command='cyber status --node https://rpc.bostrom.cybernode.ai:443')
```

```json
{
  "NodeInfo": {
    "protocol_version": {
      "p2p": "8",
      "block": "11",
      "app": "0"
    },
    "id": "d0518ce9881a4b0c5872e5e9b7c4ea8d760dad3f",
    "listen_addr": "tcp://85.10.207.173:26656",
    "network": "bostrom",
    "version": "v0.34.21",
    "channels": "40202122233038606100",
    "moniker": "c83b0d17224c",
    "other": {
      "tx_index": "on",
      "rpc_address": "tcp://0.0.0.0:26657"
    }
  },
  "SyncInfo": {
    "latest_block_hash": "FB3119D7749688DF9DBFD52307C68C9AAB6725CFBFF59988841C67E4627A1A8C",
    "latest_app_hash": "3E54DEE032E43B865EE1B4AF68FBE7B77BCC3F3DD052EEEF58C0EA3CA4D8E747",
    "latest_block_height": "8010938",
    "latest_block_time": "2023-05-03T03:32:37.631562092Z",
    "earliest_block_hash": "3C6BEA9792C0E70B6A1F29D9B75A0A4387195C86185EAA9BF44C27F19FB799D0",
    "earliest_app_hash": "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855",
    "earliest_block_height": "1",
    "earliest_block_time": "2021-11-05T13:22:42Z",
    "catching_up": false
  },
  "ValidatorInfo": {
    "Address": "9473DC9D965766118B258B54A5187A1BC06D3481",
    "PubKey": {
      "type": "tendermint/PubKeyEd25519",
      "value": "c7DPxofO6ijIQ1aTs0MMhjLGX9PNzikGEDe/Eiammv4="
    },
    "VotingPower": "0"
  }
}
```

### execute cosmwasm contracts

