from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport


# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://qs.fromarte.ch/graphql/",headers= {"authorization": "Bearer ae6d61b9faea4153a9ec062fa1101c39"})

# Create a GraphQL client using the defined transport
client = Client(transport=transport,fetch_schema_from_transport=True)

# Provide a GraphQL query
query = gql(
    """query ($documentId: ID!) {
  node(id: $documentId) {
    ... on Document {
      id
      case {
        id
        workItems(status: READY) {
          edges {
            node {
              id
              task {
                id
                slug
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}
"""
)

params = {"documentId": "RG9jdW1lbnQ6YTJmOGQwYTEtNWFhZS00MTM3LTkxZmMtYWViMjg5YTkzOWFh"}

# Execute the query on the transport
result = client.execute(query, variable_values=params)
print(result)