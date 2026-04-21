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
  <el-aside v-if="!isMobile" :width="isCollapse ? '64px' : '220px'" class="sidebar">
    <div class="logo">
      <span v-if="!isCollapse" class="logo-text">🏘️ 村庄管理</span>
      <span v-else class="logo-icon">🏘️</span>
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
  <el-drawer v-else :model-value="open" direction="ltr" :show-close="false" size="220px" @close="emit('close')" class="mobile-drawer">
    <template #title>
      <div class="logo">
        <span class="logo-text">🏘️ 村庄管理</span>
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
/* ---- Notion Style Sidebar ---- */

/* 桌面端侧边栏 */
.sidebar {
  background: #f6f5f4;
  height: 100vh;
  transition: width 0.2s ease;
  flex-shrink: 0;
  border-right: 1px solid rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
}

/* Logo */
.logo {
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  flex-shrink: 0;
}

.logo-text {
  font-size: 15px;
  font-weight: 600;
  color: #31302e;
  letter-spacing: -0.01em;
  white-space: nowrap;
}

.logo-icon {
  font-size: 20px;
}

/* 菜单 */
.sidebar-menu {
  border-right: none;
  background: transparent;
  flex: 1;
  padding: 8px 0;
}

:deep(.el-menu) {
  background: transparent;
  border: none;
}

:deep(.el-menu-item) {
  height: 38px;
  line-height: 38px;
  margin: 1px 8px;
  border-radius: 6px;
  color: #31302e;
  font-size: 14px;
  font-weight: 450;
  transition: background 0.12s ease, color 0.12s ease;
}

:deep(.el-menu-item:hover) {
  background: rgba(0, 0, 0, 0.06);
  color: #31302e;
}

:deep(.el-menu-item.is-active) {
  background: rgba(0, 117, 222, 0.1);
  color: #0075de;
  font-weight: 600;
  position: relative;
}

/* 激活态左侧蓝色指示条 */
:deep(.el-menu-item.is-active)::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 20px;
  background: #0075de;
  border-radius: 0 2px 2px 0;
}

:deep(.el-menu-item .el-icon) {
  font-size: 15px;
}

/* 折叠状态 */
:deep(.el-menu--collapse) {
  padding: 8px 0;
}

:deep(.el-menu--collapse .el-menu-item) {
  margin: 1px 6px;
  justify-content: center;
}

/* ---- 移动端抽屉 ---- */
.mobile-drawer .logo {
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.mobile-drawer .logo-text {
  font-size: 15px;
  font-weight: 600;
  color: #31302e;
}

:deep(.el-drawer__header) {
  padding: 0;
  margin: 0;
  background: #f6f5f4;
}

:deep(.el-drawer__body) {
  padding: 0;
  background: #f6f5f4;
}
</style>
