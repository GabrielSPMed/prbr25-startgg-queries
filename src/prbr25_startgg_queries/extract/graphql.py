from importlib import resources
from typing import Dict

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from prbr25_startgg_queries.common.logger import setup_logger

logger = setup_logger(__name__)


class GraphQL:
    """
    GraphQL client for interacting with the StartGG API using GraphQL queries.

    Attributes:
        transport (RequestsHTTPTransport): HTTP transport for GraphQL requests.
        client (Client): GraphQL client instance.

    Methods:
        __init__(bearer_token: str):
            Initializes the GraphQL client with the provided bearer token.

        _load_query(query_name: str) -> str:
            Loads a GraphQL query from the queries resource folder by name.

        execute_query(query_name: str, query_parameters: Dict):
            Executes a GraphQL query with the given parameters and returns the response.

        query_all_pages_tournaments(query_name: str, query_parameters: Dict):
            Queries all pages of tournaments, handling pagination, and returns a list of tournaments.

        query_tournament(query_name: str, query_parameters: Dict):
            Queries a single tournament and returns it in a list.
    """

    def __init__(self, bearer_token: str):
        logger.info("Initializing GraphQL client class")
        logger.debug("Initializing GrapqhQL Transport")
        self.transport = RequestsHTTPTransport(
            url="https://api.start.gg/gql/alpha",
            headers={"Authorization": "Bearer " + bearer_token},
            verify=True,
            retries=3,
        )
        logger.debug("Initializing GraphQL client")
        self.client = Client(
            transport=self.transport, fetch_schema_from_transport=False
        )

    def _load_query(self, query_name: str) -> str:
        with (
            resources.files("prbr25_startgg_queries.queries")
            .joinpath(f"{query_name}.graphql")
            .open("r") as f
        ):
            return f.read()

    def execute_query(self, query_name: str, query_parameters: Dict):
        query_string = self._load_query(query_name)
        query = gql(query_string)
        query.variable_values = query_parameters
        return self.client.execute(query)

    def query_all_pages_tournaments(self, query_name: str, query_parameters: Dict):
        tournaments = []
        page_number = 1
        logger.info("Starting StartGG queries")
        while True:
            logger.debug(f"Querying page {page_number}")
            response = self.execute_query(query_name, query_parameters)
            logger.debug(f"Finished page {page_number}")
            tournaments.extend(response["tournaments"]["nodes"])
            if page_number == response["tournaments"]["pageInfo"]["totalPages"]:
                break
            page_number += 1
            query_parameters["cPage"] = page_number
        logger.info("All queries finished successfully")
        return tournaments

    def query_tournament(self, query_name: str, query_parameters: Dict):
        logger.info("Querying tournament")
        response = self.execute_query(query_name, query_parameters)
        logger.info("Query successful")
        return [response["tournament"]]
