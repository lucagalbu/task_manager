<script setup lang="ts">
import { deleteTask, queryAllTasks } from '@/lib/queries'
import type { TaskInput } from '@/lib/types'
import ToasterBS from './ToasterBS.vue'
import IconTrash from "@/icons/IconTrash.vue"
import { onMounted, ref, computed } from 'vue'

const tasks = ref<TaskInput[]>([])
const deleted_tasks = ref<TaskInput[]>([])

const dates = computed(() => {
  const found_dates = tasks.value
    .map((task) => task.date)
    .filter((el): el is Date => el !== undefined)
    .sort((a, b) => a.getTime() - b.getTime())
    .filter((value, index, array) => value.getTime() !== array[index - 1]?.getTime())
  return found_dates
})

onMounted(async () => {
  tasks.value = await queryAllTasks('TodoList')
})

const deleteHandler = async (id: Number) => {
  const deleted_task = await deleteTask("deleteTask", id);

  if (deleted_task) {
    deleted_tasks.value.push(deleted_task)
    tasks.value = await queryAllTasks('TodoList')
  } else {
    console.error('An error occured')
  }
}
</script>

<template>
  <div class="accordion" id="todo-list-accordion-container">
    <div class="accordion-item">
      <h2 class="accordion-header">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
          data-bs-target="#date-list-no-date">
          No date
        </button>
      </h2>
      <div id="date-list-no-date" class="accordion-collapse collapse">
        <div class="accordion-body">
          <table class="table">
            <thead>
              <tr>
                <th>Completed</th>
                <th>Time</th>
                <th>Title</th>
                <th>Actions</th>
              </tr>
            </thead>
            <template v-for="task in tasks.filter((task) => task.date === undefined)" :key="task.id">
              <tr>
                <td>{{ task.status }}</td>
                <td>
                  {{ `${task.start_time} - ${task.end_time}` }}
                </td>
                <td>{{ task.title }}</td>
                <td>
                  <div class="trash-icon" @click="deleteHandler(task.id)">
                    <IconTrash />
                  </div>
                </td>
              </tr>
            </template>
          </table>
        </div>
      </div>
    </div>

    <div class="accordion-item" v-for="date in dates" :key="date.getTime()">
      <h2 class="accordion-header">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
          :data-bs-target="`#date-list-${date.getTime()}`">
          {{ date.toDateString() }}
        </button>
      </h2>
      <div :id="`date-list-${date.getTime()}`" class="accordion-collapse collapse">
        <div class="accordion-body">
          <table class="table">
            <thead>
              <tr>
                <th>Completed</th>
                <th>Time</th>
                <th>Title</th>
                <th>Actions</th>
              </tr>
            </thead>
            <template v-for="task in tasks.filter((task) => task.date?.getTime() === date.getTime())" :key="task.id">
              <tr>
                <td>{{ task.status }}</td>
                <td>
                  {{ `${task.start_time} - ${task.end_time}` }}
                </td>
                <td>{{ task.title }}</td>
                <td>
                  <div class="trash-icon" @click="deleteHandler(task.id)">
                    <IconTrash />
                  </div>
                </td>
              </tr>
            </template>
          </table>
        </div>
      </div>
    </div>
  </div>

  <div class="toast-container position-fixed top-0 end-0 p-3" id="deletedTaskToastContainer">
    <template v-for="task in deleted_tasks" v-bind:key="task.id">
      <ToasterBS title="Task deleted" :text="task.title" />
    </template>
  </div>
</template>

<style scoped lang="scss">
.trash-icon {
  fill: var(--bs-danger);
  width: fit-content;
  cursor: pointer;
}
</style>