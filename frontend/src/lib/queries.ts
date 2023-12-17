import { GRAPHQL_QUERY_NAME, GRAPHQL_ADD_NAME, GRAPHQL_DELETE_NAME, API_URL } from './config'
import type { graphQLTaskResponse } from './types'

type GraphQLRespQuery = {
  data: {
    [GRAPHQL_QUERY_NAME]: graphQLTaskResponse[]
  }
}

type GraphQLRespMutation = {
  data: {
    [GRAPHQL_ADD_NAME]: graphQLTaskResponse
  }
}

type GraphQLRespDelete = {
  data: {
    [GRAPHQL_DELETE_NAME]: graphQLTaskResponse
  }
}


const makeGraphQLRequest = function (body: string) {
  const req_headers = new Headers()
  req_headers.append('Content-Type', 'application/json')

  const req_options: RequestInit = {
    method: 'POST',
    body: JSON.stringify({ query: body }),
    headers: req_headers
  }

  const response = fetch(API_URL, req_options)
  return response
}