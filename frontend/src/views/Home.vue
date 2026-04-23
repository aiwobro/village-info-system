<script setup lang="ts">
import { onMounted } from 'vue'
import { useDataStore } from '../stores/data'
import { useAuthStore } from '../stores/auth'

const dataStore = useDataStore()
const auth = useAuthStore()

onMounted(() => {
  dataStore.fetchStats()
})
</script>

<template>
  <div class="home">
    <!-- 页面头部 -->
    <div class="home-header">
      <div class="header-left">
        <h1 class="page-title">村庄信息管理系统</h1>
        <p class="page-subtitle">欢迎回来，{{ auth.user?.full_name || auth.user?.username }}</p>
      </div>
      <el-button
        class="logout-btn"
        @click="auth.logout(); $router.push('/login')"
      >
        退出登录
      </el-button>
    </div>

    <!-- 数据统计 -->
    <div class="stats-section">
      <div class="stats-label">数据概览</div>
      <el-row :gutter="16" class="stats-row">
        <el-col :xs="12" :sm="8" :md="4" :lg="4">
          <router-link to="/village" class="stat-link">
            <div class="stat-card stat-card--blue">
              <div class="stat-icon-wrap">
                <el-icon class="stat-icon"><LocationInformation /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ dataStore.stats.adminVillages }}</div>
                <div class="stat-label">行政村</div>
              </div>
            </div>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="8" :md="4" :lg="4">
          <router-link to="/natural-village" class="stat-link">
            <div class="stat-card stat-card--cyan">
              <div class="stat-icon-wrap">
                <el-icon class="stat-icon"><OfficeBuilding /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ dataStore.stats.naturalVillages }}</div>
                <div class="stat-label">自然村</div>
              </div>
            </div>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="8" :md="4" :lg="4">
          <router-link to="/household" class="stat-link">
            <div class="stat-card stat-card--indigo">
              <div class="stat-icon-wrap">
                <el-icon class="stat-icon"><House /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ dataStore.stats.households }}</div>
                <div class="stat-label">户</div>
              </div>
            </div>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="8" :md="4" :lg="4">
          <router-link to="/villagers" class="stat-link">
            <div class="stat-card stat-card--teal">
              <div class="stat-icon-wrap">
                <el-icon class="stat-icon"><User /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ dataStore.stats.villagers }}</div>
                <div class="stat-label">村民</div>
              </div>
            </div>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="8" :md="4" :lg="4">
          <router-link to="/assets" class="stat-link">
            <div class="stat-card stat-card--amber">
              <div class="stat-icon-wrap">
                <el-icon class="stat-icon"><Box /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ dataStore.stats.assets }}</div>
                <div class="stat-label">资产</div>
              </div>
            </div>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="8" :md="4" :lg="4">
          <router-link to="/resources" class="stat-link">
            <div class="stat-card stat-card--emerald">
              <div class="stat-icon-wrap">
                <el-icon class="stat-icon"><Grid /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ dataStore.stats.resources }}</div>
                <div class="stat-label">资源</div>
              </div>
            </div>
          </router-link>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<style scoped>
.home {
  padding: 0;
}

/* 页面头部 */
.home-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  padding-top: 56px;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.page-title {
  font-size: 1.375rem;
  font-weight: 700;
  color: var(--corp-text-primary);
  letter-spacing: -0.02em;
  margin: 0;
}

.page-subtitle {
  font-size: 14px;
  color: var(--corp-text-secondary);
  margin: 0;
  font-weight: 400;
}

.logout-btn {
  background: var(--corp-white);
  border: 1px solid var(--corp-border);
  color: var(--corp-text-secondary);
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 500;
  padding: 6px 14px;
  height: auto;
  margin-top: 4px;
}

.logout-btn:hover {
  background: var(--corp-surface);
  border-color: var(--corp-border-strong);
  color: var(--corp-text-primary);
}

/* 统计区域 */
.stats-section {
  margin-bottom: 8px;
}

.stats-label {
  font-size: 12px;
  font-weight: 700;
  color: var(--corp-text-muted);
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 12px;
}

.stats-row {
  margin-bottom: 8px;
}

/* 统计卡片 */
.stat-link {
  display: block;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px 16px;
  background: var(--corp-white);
  border: 1px solid var(--corp-border);
  border-radius: var(--radius-md);
  box-shadow: var(--corp-shadow-card);
  transition: box-shadow 0.15s ease, border-color 0.15s ease, transform 0.15s ease;
  min-height: 80px;
  border-left: 3px solid transparent;
}

.stat-link:hover .stat-card {
  box-shadow: var(--corp-shadow-hover);
  border-color: var(--corp-border-strong);
  border-left-color: transparent;
  transform: translateY(-2px);
}

/* 卡片色彩变体 */
.stat-card--blue   { border-left-color: #2563eb; }
.stat-card--cyan   { border-left-color: #0891b2; }
.stat-card--indigo { border-left-color: #4f46e5; }
.stat-card--teal   { border-left-color: #0d9488; }
.stat-card--amber  { border-left-color: #d97706; }
.stat-card--emerald{ border-left-color: #059669; }

.stat-icon-wrap {
  width: 42px;
  height: 42px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-card--blue .stat-icon-wrap   { background: #eff6ff; }
.stat-card--cyan .stat-icon-wrap   { background: #ecfeff; }
.stat-card--indigo .stat-icon-wrap { background: #eef2ff; }
.stat-card--teal .stat-icon-wrap   { background: #f0fdfa; }
.stat-card--amber .stat-icon-wrap  { background: #fffbeb; }
.stat-card--emerald .stat-icon-wrap{ background: #ecfdf5; }

.stat-icon {
  font-size: 22px;
}

.stat-card--blue .stat-icon   { color: #2563eb; }
.stat-card--cyan .stat-icon   { color: #0891b2; }
.stat-card--indigo .stat-icon { color: #4f46e5; }
.stat-card--teal .stat-icon   { color: #0d9488; }
.stat-card--amber .stat-icon  { color: #d97706; }
.stat-card--emerald .stat-icon{ color: #059669; }

.stat-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 0;
  gap: 2px;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--corp-text-primary);
  letter-spacing: -0.02em;
  line-height: 1.1;
  font-variant-numeric: tabular-nums;
}

.stat-label {
  color: var(--corp-text-secondary);
  font-size: 13px;
  font-weight: 500;
  white-space: nowrap;
}

/* 平板及以上 */
@media (min-width: 768px) {
  .home-header {
    padding-top: 0;
    align-items: center;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .stat-card {
    padding: 20px 18px;
    min-height: 88px;
    gap: 16px;
  }

  .stat-icon-wrap {
    width: 48px;
    height: 48px;
  }

  .stat-icon {
    font-size: 26px;
  }

  .stat-value {
    font-size: 28px;
  }
}

/* 大屏幕 */
@media (min-width: 1200px) {
  .stat-card {
    padding: 22px 20px;
  }
}
</style>
