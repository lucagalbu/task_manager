import { GRAPHQL_QUERY_NAME, GRAPHQL_ADD_NAME, GRAPHQL_DELETE_NAME, API_URL } from './config'
import { graphqlToTaskInput, statusToGraphQL } from './converters'
import type { TaskInput, TaskOutput, graphQLTaskResponse } from './types'

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

export const addTask = async function (
  mutation_name: string,
  task: TaskOutput
): Promise<TaskInput | null> {
  let mutation = `mutation ${mutation_name} {
    ${GRAPHQL_ADD_NAME}(
      title: "${task.title}"
      status: ${statusToGraphQL(task.status)}`
  if (task.description) {
    mutation = mutation.concat(`\ndescription: "${task.description}"`)
  }
  if (task.date) {
    mutation = mutation.concat(`\ndateTimestamp: "${task.date.toISOString().split("T")[0]}"`)
  }
  if (task.start_time) {
    mutation = mutation.concat(`\nstartTimestamp: "${task.start_time}"`)
  }
  if (task.end_time) {
    mutation = mutation.concat(`\nendTimestamp: "${task.end_time}"`)
  }
  if (task.goal) {
    mutation = mutation.concat(`\ngoal: "${task.goal}"`)
  }

  mutation = mutation.concat(`
            ) {
                id,
                title
            }
        }`)

  const response = await makeGraphQLRequest(mutation)
  if (!response.ok) {
    return null
  }

  const response_json: GraphQLRespMutation = await response.json()
  const added_task_ql = response_json.data[GRAPHQL_ADD_NAME]
  const converted_task = graphqlToTaskInput(added_task_ql)
  return converted_task
}

export const deleteTask = async function (mutation_name: string, id: Number): Promise<TaskInput | null> {
  const mutation = `mutation ${mutation_name} {
    ${GRAPHQL_DELETE_NAME}(
      taskId:${id}
    ) {
      id
      title
    } 
  }`
  const response = await makeGraphQLRequest(mutation)
  if (!response.ok) {
    return null
  }

  const response_json: GraphQLRespDelete = await response.json()
  const tasks_ql = response_json.data[GRAPHQL_DELETE_NAME]
  const converted_task = graphqlToTaskInput(tasks_ql)
  return converted_task
}
