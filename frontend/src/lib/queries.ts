import { GRAPHQL_QUERY_NAME, GRAPHQL_ADD_NAME, GRAPHQL_DELETE_NAME, API_URL } from './config'
import { graphqlToTaskInput } from './converters'
import type { TaskInput, graphQLTaskResponse } from './types'

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

export const queryAllTasks = async function (query_name: string): Promise<TaskInput[]> {
  const fields = [
    'id',
    'title',
    'status',
    'description',
    'dateTimestamp',
    'startTimestamp',
    'endTimestamp',
    'goal'
  ]
  const query = `query ${query_name} {
        ${GRAPHQL_QUERY_NAME} {
          ${fields.join('\n')}
        }
    }`
  const response = await makeGraphQLRequest(query)
  if (!response.ok) {
    return []
  }

  const response_json: GraphQLRespQuery = await response.json()
  const tasks_ql = response_json.data.queryTask
  const tasks_converted = tasks_ql.map((task) => graphqlToTaskInput(task))
  return tasks_converted
}
