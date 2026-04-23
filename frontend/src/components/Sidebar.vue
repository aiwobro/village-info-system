<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { DArrowLeft } from '@element-plus/icons-vue'

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
      <span v-if="!isCollapse" class="logo-text">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="flex-shrink:0">
          <path d="M3 21V9L12 3L21 9V21H15V14H9V21H3Z" fill="white" opacity="0.9"/>
        </svg>
        村庄管理
      </span>
      <span v-else class="logo-icon">🏘️</span>
      <button class="collapse-btn" :class="{ collapsed: isCollapse }" @click="isCollapse = !isCollapse" :title="isCollapse ? '展开侧边栏' : '收起侧边栏'">
        <el-icon><DArrowLeft /></el-icon>
      </button>
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
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="flex-shrink:0">
          <path d="M3 21V9L12 3L21 9V21H15V14H9V21H3Z" fill="white" opacity="0.9"/>
        </svg>
        <span class="logo-text">村庄管理</span>
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
/* ---- Corporate Deep Blue Sidebar ---- */

.sidebar {
  background: #1e3a5f;
  height: 100vh;
  transition: width 0.2s ease;
  flex-shrink: 0;
  border-right: none;
  display: flex;
  flex-direction: column;
}

/* Logo */
.logo {
  height: 56px;
  display: flex;
  align-items: center;
  gap: 10px;
  justify-content: center;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  flex-shrink: 0;
  position: relative;
  padding: 0 12px;
}

.logo-text {
  font-size: 14px;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: 0;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  font-size: 20px;
}

/* 折叠按钮 */
.collapse-btn {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  width: 28px;
  height: 28px;
  border: none;
  background: rgba(255,255,255,0.1);
  border-radius: var(--radius-sm);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255,255,255,0.7);
  transition: background 0.15s ease, color 0.15s ease;
  flex-shrink: 0;
}

.collapse-btn:hover {
  background: rgba(255,255,255,0.2);
  color: #ffffff;
}

.collapse-btn .el-icon {
  font-size: 13px;
  transition: transform 0.2s ease;
}

.collapse-btn.collapsed .el-icon {
  transform: rotate(180deg);
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
  height: 40px;
  line-height: 40px;
  margin: 2px 10px;
  border-radius: var(--radius-sm);
  color: rgba(255,255,255,0.7);
  font-size: 14px;
  font-weight: 500;
  transition: background 0.12s ease, color 0.12s ease;
}

:deep(.el-menu-item:hover) {
  background: rgba(255,255,255,0.1);
  color: #ffffff;
}

:deep(.el-menu-item.is-active) {
  background: rgba(37, 99, 235, 0.6);
  color: #ffffff;
  font-weight: 600;
}

/* 激活态左侧蓝色指示条 */
:deep(.el-menu-item.is-active)::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 24px;
  background: #60a5fa;
  border-radius: 0 2px 2px 0;
}

:deep(.el-menu-item .el-icon) {
  font-size: 16px;
}

/* 折叠状态 */
:deep(.el-menu--collapse) {
  padding: 8px 0;
}

:deep(.el-menu--collapse .el-menu-item) {
  margin: 2px 8px;
  justify-content: center;
}

/* ---- 移动端抽屉 ---- */
.mobile-drawer .logo {
  height: 56px;
  display: flex;
  align-items: center;
  gap: 8px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.mobile-drawer .logo-text {
  font-size: 14px;
  font-weight: 700;
  color: #ffffff;
}

:deep(.el-drawer__header) {
  padding: 0;
  margin: 0;
  background: #1e3a5f;
}

:deep(.el-drawer__body) {
  padding: 0;
  background: #1e3a5f;
}
</style>
