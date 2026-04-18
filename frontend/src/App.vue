<script setup lang="ts">
import { RouterView } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
</script>

<template>
  <div class="app-container">
    <Sidebar />
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
  font-family: 'Microsoft YaHei', sans-serif;
}

.app-container {
  display: flex;
  height: 100%;
}

.main-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  background: #f5f7fa;
}
</style>
