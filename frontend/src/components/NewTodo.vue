<script setup lang="ts">
import { type TaskOutput, type TaskInput, Status } from '@/lib/types'
import { addTask } from '@/lib/queries'
import ToasterBS from './ToasterBS.vue'
import { ref } from 'vue'

defineProps({
  modal_id: String
})

const createdTasks = ref<TaskInput[]>([])

const getFormElements = function (form: HTMLFormElement) {
  const title = form.elements.namedItem('title') as HTMLInputElement
  const description = form.elements.namedItem('description') as HTMLInputElement
  const date = form.elements.namedItem('date') as HTMLInputElement
  const start = form.elements.namedItem('start') as HTMLInputElement
  const end = form.elements.namedItem('end') as HTMLInputElement

  return {
    title,
    description,
    date,
    start,
    end
  }
}

const handleSubmit = async function (event: Event) {
  const form = event.target as HTMLFormElement
  const elements = getFormElements(form)

  const task: TaskOutput = {
    title: elements.title.value,
    description: elements.description.value,
    date: elements.date.valueAsDate || undefined,
    start_time: elements.start.value || undefined,
    end_time: elements.end.value || undefined,
    status: Status.OPEN
  }

  const added_task = await addTask('newTaskFromForm', task)

  if (added_task) {
    createdTasks.value.push({ title: added_task.title, id: added_task.id })
  } else {
    console.error('An error occured')
  }

  form.reset()
}
</script>

<template>
  <div class="modal fade" :id="modal_id" data-bs-backdrop="static" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title">Add a new task</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <form @submit.prevent="handleSubmit">
          <div class="modal-body">
            <div class="row">
              <div class="col-12">
                <label for="task_title" class="form-label">Title <span class="text-danger">*</span></label>
                <input type="text" name="title" class="form-control" id="task_title" required />
              </div>
            </div>
            <div class="row my-1">
              <div class="col-12">
                <label for="task_description" class="form-label">Description</label>
                <textarea type="text" name="description" class="form-control" id="task_description" />
              </div>
            </div>
            <hr />
            <div class="row my-1">
              <div class="col-4">
                <label for="task_date" class="form-label">Due date</label>
                <input type="date" name="date" class="form-control" id="task_date" />
              </div>
              <div class="col-4">
                <label for="task_start" class="form-label">Start time</label>
                <input type="time" name="start" class="form-control" id="task_start" />
              </div>
              <div class="col-4">
                <label for="task_end" class="form-label">End time</label>
                <input type="time" name="end" class="form-control" id="task_end" />
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="reset" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="submit" class="btn btn-primary">Add task</button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <div class="toast-container position-fixed top-0 end-0 p-3" id="newTaskToastContainer">
    <template v-for="task in createdTasks" v-bind:key="task.id">
      <ToasterBS title="New task added" :text="task.title" />
    </template>
  </div>
</template>
