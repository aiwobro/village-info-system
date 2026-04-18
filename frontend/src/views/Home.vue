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
        <span>欢迎，{{ auth.user?.full_name || auth.user?.username }}</span>
        <el-button type="danger" size="small" @click="auth.logout(); $router.push('/login')">
          退出
        </el-button>
      </div>
    </div>
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <el-icon class="stat-icon" color="#409eff"><User /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ dataStore.stats.villagers }}</div>
              <div class="stat-label">村民总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <el-icon class="stat-icon" color="#67c23a"><Box /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ dataStore.stats.assets }}</div>
              <div class="stat-label">资产数量</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <el-icon class="stat-icon" color="#e6a23c"><Grid /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ dataStore.stats.resources }}</div>
              <div class="stat-label">资源数量</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <el-icon class="stat-icon" color="#f56c6c"><LocationInformation /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ dataStore.stats.villages }}</div>
              <div class="stat-label">村庄数量</div>
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
  margin-bottom: 24px;
}
.header h1 {
  color: #303133;
  margin: 0;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #606266;
}
.stats-row {
  margin-bottom: 20px;
}
.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
}
.stat-icon {
  font-size: 48px;
}
.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
}
.stat-label {
  color: #909399;
  font-size: 14px;
}
</style>
