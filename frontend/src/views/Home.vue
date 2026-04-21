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
  color: rgba(0, 0, 0, 0.95);
  letter-spacing: -0.02em;
  margin: 0;
}

.page-subtitle {
  font-size: 14px;
  color: #615d59;
  margin: 0;
}

.logout-btn {
  background: rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.08);
  color: #31302e;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
  padding: 6px 14px;
  height: auto;
  margin-top: 4px;
}

.logout-btn:hover {
  background: rgba(0, 0, 0, 0.08);
  border-color: rgba(0, 0, 0, 0.12);
  color: #31302e;
}

/* 统计区域 */
.stats-section {
  margin-bottom: 8px;
}

.stats-label {
  font-size: 13px;
  font-weight: 600;
  color: #a39e98;
  letter-spacing: 0.02em;
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
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03), 0 1px 8px rgba(0, 0, 0, 0.02);
  transition: box-shadow 0.15s ease, border-color 0.15s ease;
  min-height: 80px;
}

.stat-link:hover .stat-card {
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.06), 0 2px 6px rgba(0, 0, 0, 0.03);
  border-color: rgba(0, 0, 0, 0.15);
}

.stat-icon {
  font-size: 28px;
  flex-shrink: 0;
  color: #0075de;
  opacity: 0.85;
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
  color: rgba(0, 0, 0, 0.95);
  letter-spacing: -0.02em;
  line-height: 1.1;
}

.stat-label {
  color: #615d59;
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
