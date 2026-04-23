<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterView } from 'vue-router'
import { ElConfigProvider } from 'element-plus'
import zhCn from 'element-plus/dist/locale/zh-cn.js'
import { useAuthStore } from './stores/auth'
import Sidebar from './components/Sidebar.vue'

const auth = useAuthStore()
const isMobile = ref(false)
const sidebarOpen = ref(false)

const checkMobile = () => {
  isMobile.value = window.innerWidth < 768
  if (!isMobile.value) sidebarOpen.value = false
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}
</script>

<template>
  <el-config-provider :locale="zhCn">
    <div class="app-container">
      <!-- 移动端顶部导航栏 -->
      <div v-if="isMobile && auth.token" class="mobile-header">
        <el-button :icon="sidebarOpen ? 'Close' : 'Menu'" @click="toggleSidebar" text />
        <span class="mobile-title">村庄信息管理系统</span>
      </div>

      <Sidebar v-if="auth.token" :is-mobile="isMobile" :open="sidebarOpen" @close="sidebarOpen = false" />

      <!-- 移动端遮罩层 -->
      <div v-if="isMobile && sidebarOpen && auth.token" class="sidebar-overlay" @click="sidebarOpen = false" />

      <main class="main-content" :class="{ 'full-width': !auth.token, 'mobile-main': isMobile }">
        <RouterView />
      </main>
    </div>
  </el-config-provider>
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
  background: var(--airtable-surface);
}

.main-content.full-width {
  max-width: 100%;
}

.main-content.mobile-main {
  padding: 12px;
}

/* 移动端顶部导航 */
.mobile-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 12px;
  height: 56px;
  background: var(--airtable-white);
  color: var(--airtable-navy);
  border-bottom: 1px solid var(--airtable-border);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.mobile-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--airtable-navy);
  letter-spacing: -0.01em;
}

/* 移动端遮罩层 */
.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 999;
}
</style>
