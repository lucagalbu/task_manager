import { GRAPHQL_QUERY_NAME, GRAPHQL_ADD_NAME, GRAPHQL_DELETE_NAME } from './config'
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
