<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const auth = useAuthStore()

const form = ref({ username: '', password: '' })
const loading = ref(false)

const handleLogin = async () => {
  if (!form.value.username || !form.value.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }
  loading.value = true
  try {
    await auth.login(form.value.username, form.value.password)
    ElMessage.success('登录成功')
    router.push('/')
  } catch (e) {
    // Error handled by interceptor
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-card">
      <!-- Logo & Title -->
      <div class="login-header">
        <div class="login-logo">🏘️</div>
        <h1 class="login-title">村庄信息管理系统</h1>
        <p class="login-subtitle">请登录以继续</p>
      </div>

      <!-- Form -->
      <el-form class="login-form">
        <el-form-item>
          <el-input
            v-model="form.username"
            placeholder="用户名"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>
        <el-form-item>
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            size="large"
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <el-form-item class="login-btn-item">
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            class="login-btn"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<style scoped>
/* ---- Notion Style Login ---- */

.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--airtable-surface);
  padding: 24px;
}

.login-card {
  width: 100%;
  max-width: 380px;
  background: var(--airtable-white);
  border: 1px solid var(--airtable-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--airtable-shadow-hover);
  padding: 40px 36px;
}

/* Header */
.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-logo {
  font-size: 40px;
  margin-bottom: 16px;
  line-height: 1;
}

.login-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--airtable-navy);
  letter-spacing: -0.025em;
  margin: 0 0 8px;
}

.login-subtitle {
  font-size: 14px;
  color: var(--airtable-text-muted);
  margin: 0;
  font-weight: 500;
}

/* Form */
.login-form {
  margin-top: 0;
}

.login-form .el-form-item {
  margin-bottom: 16px;
}

/* Airtable-style input override */
.login-form :deep(.el-input__wrapper) {
  border-radius: var(--radius-sm);
  padding: 4px 12px;
  box-shadow: 0 0 0 1px var(--airtable-border) !important;
  background: var(--airtable-white);
}

.login-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px var(--airtable-border-strong) !important;
}

.login-form :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px var(--airtable-focus) !important;
}

.login-form :deep(.el-input__inner) {
  font-family: var(--airtable-font);
  font-size: 14px;
  color: var(--airtable-text-primary);
  letter-spacing: 0.01em;
}

.login-form :deep(.el-input__inner::placeholder) {
  color: var(--airtable-text-muted);
}

.login-form :deep(.el-input__prefix .el-icon) {
  color: var(--airtable-text-muted);
}

/* Login button */
.login-btn-item {
  margin-bottom: 0;
  margin-top: 8px;
}

.login-btn {
  width: 100%;
  height: 40px;
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 700;
  font-family: var(--airtable-font);
  background: var(--airtable-blue);
  border-color: var(--airtable-blue);
  letter-spacing: 0.02em;
}

.login-btn:hover {
  background: var(--airtable-blue-dark);
  border-color: var(--airtable-blue-dark);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(27, 97, 201, 0.3);
}

.login-btn:active {
  transform: translateY(0);
}
</style>
