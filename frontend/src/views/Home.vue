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
        <h1 class="page-title">🏘️ 村庄信息管理系统</h1>
        <p class="page-subtitle">欢迎，{{ auth.user?.full_name || auth.user?.username }}</p>
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
      <el-row :gutter="12" class="stats-row">
        <el-col :xs="12" :sm="8" :md="4" :lg="4">
          <router-link to="/village" class="stat-link">
            <div class="stat-card">
              <el-icon class="stat-icon"><LocationInformation /></el-icon>
              <div class="stat-info">
                <div class="stat-value">{{ dataStore.stats.adminVillages }}</div>
                <div class="stat-label">行政村</div>
              </div>
            </div>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="8" :md="4" :lg="4">
          <router-link to="/natural-village" class="stat-link">
            <div class="stat-card">
              <el-icon class="stat-icon"><OfficeBuilding /></el-icon>
              <div class="stat-info">
                <div class="stat-value">{{ dataStore.stats.naturalVillages }}</div>
                <div class="stat-label">自然村</div>
              </div>
            </div>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="8" :md="4" :lg="4">
          <router-link to="/household" class="stat-link">
            <div class="stat-card">
              <el-icon class="stat-icon"><House /></el-icon>
              <div class="stat-info">
                <div class="stat-value">{{ dataStore.stats.households }}</div>
                <div class="stat-label">户</div>
              </div>
            </div>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="8" :md="4" :lg="4">
          <router-link to="/villagers" class="stat-link">
            <div class="stat-card">
              <el-icon class="stat-icon"><User /></el-icon>
              <div class="stat-info">
                <div class="stat-value">{{ dataStore.stats.villagers }}</div>
                <div class="stat-label">村民</div>
              </div>
            </div>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="8" :md="4" :lg="4">
          <router-link to="/assets" class="stat-link">
            <div class="stat-card">
              <el-icon class="stat-icon"><Box /></el-icon>
              <div class="stat-info">
                <div class="stat-value">{{ dataStore.stats.assets }}</div>
                <div class="stat-label">资产</div>
              </div>
            </div>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="8" :md="4" :lg="4">
          <router-link to="/resources" class="stat-link">
            <div class="stat-card">
              <el-icon class="stat-icon"><Grid /></el-icon>
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
/* ---- Notion Style Home ---- */

.home {
  padding: 0;
}

/* 页面头部 */
.home-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  padding-top: 56px; /* 移动端顶部导航栏高度 */
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--airtable-text-primary);
  letter-spacing: -0.025em;
  margin: 0;
}

.page-subtitle {
  font-size: 14px;
  color: var(--airtable-text-secondary);
  margin: 0;
  font-weight: 500;
}

.logout-btn {
  background: var(--airtable-white);
  border: 1px solid var(--airtable-border);
  color: var(--airtable-text-secondary);
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 600;
  padding: 6px 14px;
  height: auto;
  margin-top: 4px;
  letter-spacing: 0.02em;
}

.logout-btn:hover {
  background: var(--airtable-surface);
  border-color: var(--airtable-border-strong);
  color: var(--airtable-text-primary);
}

/* 统计区域 */
.stats-section {
  margin-bottom: 8px;
}

.stats-label {
  font-size: 12px;
  font-weight: 700;
  color: var(--airtable-text-muted);
  letter-spacing: 0.06em;
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
  background: var(--airtable-white);
  border: 1px solid var(--airtable-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--airtable-shadow-card);
  transition: box-shadow 0.15s ease, border-color 0.15s ease, transform 0.15s ease;
  min-height: 80px;
}

.stat-link:hover .stat-card {
  box-shadow: var(--airtable-shadow-hover);
  border-color: var(--airtable-border-strong);
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 26px;
  flex-shrink: 0;
  color: var(--airtable-blue);
  opacity: 0.9;
}

.stat-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 0;
  gap: 2px;
}

.stat-value {
  font-size: 26px;
  font-weight: 700;
  color: var(--airtable-text-primary);
  letter-spacing: -0.025em;
  line-height: 1.1;
  font-variant-numeric: tabular-nums;
}

.stat-label {
  color: var(--airtable-text-secondary);
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
    font-size: 1.75rem;
  }

  .stat-card {
    padding: 20px 18px;
    min-height: 88px;
    gap: 16px;
  }

  .stat-icon {
    font-size: 32px;
  }

  .stat-value {
    font-size: 30px;
  }
}

/* 大屏幕 */
@media (min-width: 1200px) {
  .stat-card {
    padding: 22px 20px;
  }
}
</style>
