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
    <div class="header">
      <h1>🏘️ 村庄信息管理系统</h1>
      <div class="user-info">
        <span class="username">欢迎，{{ auth.user?.full_name || auth.user?.username }}</span>
        <el-button type="danger" size="small" @click="auth.logout(); $router.push('/login')">
          退出
        </el-button>
      </div>
    </div>
    <el-row :gutter="16" class="stats-row">
      <el-col :xs="12" :sm="8" :md="4" :lg="4">
        <el-card shadow="hover">
          <div class="stat-card">
            <el-icon class="stat-icon" color="#409eff"><LocationInformation /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ dataStore.stats.adminVillages }}</div>
              <div class="stat-label">行政村</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="8" :md="4" :lg="4">
        <el-card shadow="hover">
          <div class="stat-card">
            <el-icon class="stat-icon" color="#909399"><OfficeBuilding /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ dataStore.stats.naturalVillages }}</div>
              <div class="stat-label">自然村</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="8" :md="4" :lg="4">
        <el-card shadow="hover">
          <div class="stat-card">
            <el-icon class="stat-icon" color="#67c23a"><House /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ dataStore.stats.households }}</div>
              <div class="stat-label">户</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="8" :md="4" :lg="4">
        <el-card shadow="hover">
          <div class="stat-card">
            <el-icon class="stat-icon" color="#e6a23c"><User /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ dataStore.stats.villagers }}</div>
              <div class="stat-label">村民</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="8" :md="4" :lg="4">
        <el-card shadow="hover">
          <div class="stat-card">
            <el-icon class="stat-icon" color="#f56c6c"><Box /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ dataStore.stats.assets }}</div>
              <div class="stat-label">资产</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="8" :md="4" :lg="4">
        <el-card shadow="hover">
          <div class="stat-card">
            <el-icon class="stat-icon" color="#909399"><Grid /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ dataStore.stats.resources }}</div>
              <div class="stat-label">资源</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-top: 56px; /* 移动端顶部导航栏高度 */
}
.header h1 {
  color: #303133;
  margin: 0;
  font-size: 20px;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #606266;
}
.username {
  font-size: 13px;
  white-space: nowrap;
}
.stats-row {
  margin-bottom: 16px;
}
.stat-card {
  display: flex;
  align-items: center;
  gap: 12px;
  min-height: 72px;
}
.stat-icon {
  font-size: 32px;
  flex-shrink: 0;
}
.stat-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 0;
}
.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  line-height: 1.2;
}
.stat-label {
  color: #909399;
  font-size: 13px;
  white-space: nowrap;
}

/* 平板及以上 */
@media (min-width: 768px) {
  .header {
    padding-top: 0;
  }
  .header h1 {
    font-size: 24px;
  }
  .stat-card {
    min-height: 80px;
    gap: 16px;
  }
  .stat-icon {
    font-size: 40px;
  }
  .stat-value {
    font-size: 28px;
  }
  .stat-label {
    font-size: 14px;
  }
}
</style>
