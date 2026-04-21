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
      <el-form @submit.prevent="handleLogin" class="login-form">
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
            native-type="submit"
            class="login-btn"
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
  background: #f6f5f4;
  padding: 24px;
}

.login-card {
  width: 100%;
  max-width: 380px;
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  box-shadow:
    0 4px 18px rgba(0, 0, 0, 0.04),
    0 2px 6px rgba(0, 0, 0, 0.025),
    0 0.5px 2px rgba(0, 0, 0, 0.015);
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
  color: rgba(0, 0, 0, 0.95);
  letter-spacing: -0.02em;
  margin: 0 0 8px;
}

.login-subtitle {
  font-size: 14px;
  color: #a39e98;
  margin: 0;
}

/* Form */
.login-form {
  margin-top: 0;
}

.login-form .el-form-item {
  margin-bottom: 16px;
}

/* Notion-style input override */
.login-form :deep(.el-input__wrapper) {
  border-radius: 4px;
  padding: 4px 12px;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.1) !important;
  background: #ffffff;
}

.login-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.2) !important;
}

.login-form :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px #097fe8 !important;
}

.login-form :deep(.el-input__inner) {
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 15px;
  color: rgba(0, 0, 0, 0.95);
}

.login-form :deep(.el-input__inner::placeholder) {
  color: #a39e98;
}

.login-form :deep(.el-input__prefix .el-icon) {
  color: #a39e98;
}

/* Login button */
.login-btn-item {
  margin-bottom: 0;
  margin-top: 8px;
}

.login-btn {
  width: 100%;
  height: 40px;
  border-radius: 4px;
  font-size: 15px;
  font-weight: 600;
  font-family: 'Inter', system-ui, sans-serif;
  background: #0075de;
  border-color: #0075de;
  letter-spacing: 0;
}

.login-btn:hover {
  background: #005bab;
  border-color: #005bab;
  transform: none;
}

.login-btn:active {
  transform: scale(0.98);
}
</style>
