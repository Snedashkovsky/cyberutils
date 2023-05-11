from typing import Optional, Dict, List

from .execution import execute_graphql


async def get_messages_by_address_and_type(address: str,
                                           msg_type: str,
                                           graphql_url: str,
                                           limit: int = 100,
                                           offset: int = 0) -> Optional[List[Dict]]:
    """
    get messages with a given address and type
    :param address: network address
    :param msg_type: type of message, ex. `cosmos.bank.v1beta1.MsgSend`
    :param graphql_url: The GraphQL server URL. Example: 'https://server.com:PORT/path'.
    :param limit: limit of entities
    :param offset: where in the list the server should start when returning items for a query
    :return: dict with messages
    """
    _res = await execute_graphql(
        request="""
            query MessagesByAddressAndType($address: _text, $types: _text, $limit: bigint, $offset: bigint) {
              messages_by_address(
                args: {addresses: $address, limit: $limit, offset: $offset, types: $types}
                order_by: {transaction: {block: {height: desc}}}
              ) {
                    message_type: type
                    message_value: value
                    message_involved_addresses: involved_accounts_addresses
                    transaction_hash
                    transaction {
                      success
                      memo
                      signer_infos
                    }
                }
            }
            """,
        variable_values={
            "address": f"{{{address}}}",
            "types": f"{{{msg_type}}}",
            "limit": str(limit),
            "offset": str(offset)
        },
        graphql_url=graphql_url)
    try:
        return _res['messages_by_address']
    except KeyError:
        return
