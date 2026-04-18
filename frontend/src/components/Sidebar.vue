<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const menuItems = [
  { path: '/', label: '首页', icon: 'HomeFilled' },
  { path: '/village', label: '村庄信息', icon: 'LocationInformation' },
  { path: '/villagers', label: '村民管理', icon: 'User' },
  { path: '/contact', label: '联系方式', icon: 'Phone' },
  { path: '/bank', label: '银行账号', icon: 'BankCard' },
  { path: '/assets', label: '资产管理', icon: 'Box' },
  { path: '/resources', label: '资源管理', icon: 'Grid' },
]

const isCollapse = ref(false)
</script>

<template>
  <el-aside :width="isCollapse ? '64px' : '200px'" class="sidebar">
    <div class="logo">
      <span v-if="!isCollapse">🏘️ 村庄管理</span>
      <span v-else>🏘️</span>
    </div>
    <el-menu
      :default-active="route.path"
      :collapse="isCollapse"
      router
      class="sidebar-menu"
    >
      <el-menu-item v-for="item in menuItems" :key="item.path" :index="item.path">
        <el-icon><component :is="item.icon" /></el-icon>
        <template #title>{{ item.label }}</template>
      </el-menu-item>
    </el-menu>
  </el-aside>
</template>

<style scoped>
.sidebar {
  background: #304156;
  height: 100vh;
  transition: width 0.3s;
}

.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  background: #263445;
}

.sidebar-menu {
  border-right: none;
  background: #304156;
}

:deep(.el-menu) {
  background: transparent;
}

:deep(.el-menu-item) {
  color: #bfcbd9;
}

:deep(.el-menu-item:hover),
:deep(.el-menu-item.is-active) {
  background: #263445 !important;
  color: #409eff;
}
</style>
