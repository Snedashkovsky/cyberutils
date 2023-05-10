from typing import Union, Optional, Dict, Any

from graphql import ExecutionResult
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


async def execute_graphql(request: str,
                          graphql_url: str,
                          variable_values: Optional[Dict[str, Any]] = None,
                          operation_name: Optional[str] = None,
                          serialize_variables: Optional[bool] = None,
                          parse_result: Optional[bool] = None,
                          get_execution_result: bool = False,
                          **kwargs,
                          ) -> Union[Dict[str, Any], ExecutionResult]:
    """
    Execute a GraphQL query
    :param request: the GraphQL request as a String
    :param graphql_url: The GraphQL server URL. Example: 'https://server.com:PORT/path'.
    :param variable_values: Dictionary of input parameters.
    :param operation_name: Name of the operation that shall be executed.
    :param serialize_variables: whether the variable values should be
            serialized. Used for custom scalars and/or enums.
            By default, use the serialize_variables argument of the client.
    :param parse_result: Whether gql will unserialize the result.
            By default, use the parse_results argument of the client.
    :param get_execution_result: return the full ExecutionResult instance instead of
            only the "data" field. Necessary if you want to get the "extensions" field.
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
        return await _session.execute(
            document=_gql_query,
            variable_values=variable_values,
            operation_name=operation_name,
            serialize_variables=serialize_variables,
            parse_result=parse_result,
            get_execution_result=get_execution_result,
            **kwargs,
        )
