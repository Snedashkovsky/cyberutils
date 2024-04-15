import json
import requests

from base64 import b64encode


def query_contract(
        contract_address: str,
        query: dict,
        node_lcd_url: str,
        display_query_url: bool = False) -> dict:
    """
    Query contract
    :param contract_address: contract address
    :param query: contract query
    :param node_lcd_url: node lcd url
    :param display_query_url: display a query url or not
    :return: query result
    """
    _query_msg = b64encode(json.dumps(query).encode("utf-8")).decode("utf-8")
    _query = f'{node_lcd_url}/cosmwasm/wasm/v1/contract/{contract_address}/smart/{_query_msg}'
    if display_query_url:
        print(_query)
    return requests.get(_query).json()
