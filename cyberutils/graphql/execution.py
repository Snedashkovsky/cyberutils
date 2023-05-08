from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


async def execute_graphql(request: str, graphql_url: str) -> dict:
    """
    Execute a GraphQL query
    :param request: the GraphQL request as a String
    :param graphql_url: The GraphQL server URL. Example: 'https://server.com:PORT/path'.
    :return: GraphQL result
    """
    # Select your transport with a defined url endpoint
    _transport = AIOHTTPTransport(url=graphql_url)
    # Create a GraphQL client using the defined transport
    async with Client(
        transport=_transport, fetch_schema_from_transport=True,
    ) as _session:
        # Execute a query
        _gql_query = gql(request_string=request)
        return await _session.execute(_gql_query)
