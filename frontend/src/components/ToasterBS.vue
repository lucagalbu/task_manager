<script setup lang="ts">
import { onMounted, ref } from 'vue'

defineProps({
  title: String,
  text: String
})

const toastRef = ref<HTMLInputElement | null>()

onMounted(() => {
  if (toastRef.value) {
    toastRef.value.addEventListener('hidden.bs.toast', () => {
      toastRef.value?.remove()
    })
    const toastInstance = bootstrap.Toast.getOrCreateInstance(toastRef.value)
    toastInstance.show()
  }
})
</script>

<template>
  <div class="toast" role="alert" ref="toastRef">
    <div class="toast-header">
      <strong class="me-auto">{{ title }}</strong>
      <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast-body">
      {{ text }}
    </div>
  </div>
</template>
