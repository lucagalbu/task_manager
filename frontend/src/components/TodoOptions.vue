<script setup lang="ts">
import IconPlus from '@/icons/IconPlus.vue'
import NewTodo from './NewTodo.vue'

const modal_id = 'newTask'
</script>

<template>
  <button
    type="button"
    class="btn btn-light"
    data-bs-toggle="modal"
    :data-bs-target="`#${modal_id}`"
  >
    <IconPlus />
  </button>
  <NewTodo :modal_id="modal_id" />
</template>
