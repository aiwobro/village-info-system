<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps<{
  isMobile?: boolean
  open?: boolean
}>()

const emit = defineEmits<{
  close: []
}>()

const route = useRoute()

const menuItems = [
  { path: '/', label: '首页', icon: 'HomeFilled' },
  { path: '/village', label: '行政村', icon: 'LocationInformation' },
  { path: '/natural-village', label: '自然村', icon: 'OfficeBuilding' },
  { path: '/household', label: '户管理', icon: 'House' },
  { path: '/villagers', label: '村民管理', icon: 'User' },
  { path: '/contact', label: '联系方式', icon: 'Phone' },
  { path: '/bank', label: '银行账号', icon: 'CreditCard' },
  { path: '/assets', label: '资产管理', icon: 'Box' },
  { path: '/resources', label: '资源管理', icon: 'Grid' },
]

const isCollapse = ref(false)

const handleSelect = () => {
  if (props.isMobile) emit('close')
}
</script>

<template>
  <!-- 桌面端：固定侧边栏 -->
  <el-aside v-if="!isMobile" :width="isCollapse ? '64px' : '200px'" class="sidebar">
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

  <!-- 移动端：弹出抽屉 -->
  <el-drawer v-else :model-value="open" direction="ltr" :show-close="false" size="200px" @close="emit('close')" class="mobile-drawer">
    <template #title>
      <div class="logo">
        <span>🏘️ 村庄管理</span>
      </div>
    </template>
    <el-menu
      :default-active="route.path"
      router
      class="sidebar-menu"
      @select="handleSelect"
    >
      <el-menu-item v-for="item in menuItems" :key="item.path" :index="item.path">
        <el-icon><component :is="item.icon" /></el-icon>
        <template #title>{{ item.label }}</template>
      </el-menu-item>
    </el-menu>
  </el-drawer>
</template>

<style scoped>
/* 桌面端 */
.sidebar {
  background: #304156;
  height: 100vh;
  transition: width 0.3s;
  flex-shrink: 0;
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

/* 移动端抽屉 */
.mobile-drawer .logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  background: #263445;
}

:deep(.el-drawer__header) {
  padding: 0;
  margin: 0;
  background: #263445;
}
</style>
