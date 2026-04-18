<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const stats = ref({
  villagers: 0,
  assets: 0,
  resources: 0,
})

onMounted(async () => {
  try {
    const res = await axios.get('/api/v1/health')
    console.log('API connected:', res.data)
  } catch (e) {
    console.log('API not yet connected')
  }
})
</script>

<template>
  <div class="home">
    <h1>🏘️ 村庄信息管理系统</h1>
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <el-icon class="stat-icon" color="#409eff"><User /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ stats.villagers }}</div>
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
              <div class="stat-value">{{ stats.assets }}</div>
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
              <div class="stat-value">{{ stats.resources }}</div>
              <div class="stat-label">资源数量</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <el-icon class="stat-icon" color="#f56c6c"><UserFilled /></el-icon>
            <div class="stat-info">
              <div class="stat-value">0</div>
              <div class="stat-label">银行账号</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.home h1 {
  margin-bottom: 24px;
  color: #303133;
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
