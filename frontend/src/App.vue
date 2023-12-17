<script setup lang="ts">
import TodoList from '@/components/TodoList.vue'
import TodoOptions from './components/TodoOptions.vue'
</script>

<template>
    <div class="container-md">
        <div class="card">
            <div class="card-header">
                <TodoOptions />
            </div>
            <div class="card-body">
                <TodoList />
            </div>
        </div>
    </div>
</template>
