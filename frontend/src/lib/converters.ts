import type { graphQLTaskResponse, TaskInput } from './types'
import { Status } from './types'

export const statusToInternal = function (graphql_status: string | undefined): Status {
  if (graphql_status === 'DONE') return Status.DONE
  if (graphql_status === 'PROGRESS') return Status.PROGRESS
  if (graphql_status === 'OPEN') return Status.OPEN

  return Status.OPEN
}

export const statusToGraphQL = function (status_internal: Status | undefined): string {
  if (status_internal === Status.DONE) return 'DONE'
  if (status_internal === Status.PROGRESS) return 'PROGRESS'
  if (status_internal === Status.OPEN) return 'OPEN'
  return 'OPEN'
}

export const graphqlToTaskInput = function (graphql_task: graphQLTaskResponse): TaskInput {
  const start_time = graphql_task.startTimestamp?.split(":").splice(0, 2).join(":")
  const end_time = graphql_task.endTimestamp?.split(":").splice(0, 2).join(":")

  const task: TaskInput = {
    id: graphql_task.id,
    title: graphql_task.title,
    description: graphql_task.description,
    status: statusToInternal(graphql_task.status),
    goal: graphql_task.goal,
    start_time: start_time,
    end_time: end_time
  }

  if (graphql_task.dateTimestamp) task['date'] = new Date(graphql_task.dateTimestamp)

  return task
}
