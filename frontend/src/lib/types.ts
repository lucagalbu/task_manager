export enum Status {
  DONE = 'Done',
  OPEN = 'Open',
  PROGRESS = 'Progress'
}

export type TaskOutput = {
  title: string
  status?: Status
  description?: string
  date?: Date
  start_time?: string
  end_time?: string
  goal?: string
}

export type TaskInput = TaskOutput & { id: number }

export type graphQLTaskRequest = {
  title: string
  status: string
  description?: string
  dateTimestamp?: number
  startTimestamp?: string
  endTimestamp?: string
  goal?: string
}

export type graphQLTaskResponse = graphQLTaskRequest & { id: number }
