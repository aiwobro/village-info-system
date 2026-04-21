<script setup lang="ts">
import { computed, ref } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps<{
  modelValue: boolean
  title?: string
  count: number   // number of selected records to delete
}>()

const emit = defineEmits<{
  'update:modelValue': [val: boolean]
  'confirm': []
}>()

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const confirmText = ref('')
const loading = ref(false)

const handleConfirm = async () => {
  if (confirmText.value !== '确认删除') {
    ElMessage.warning('请输入"确认删除"')
    return
  }
  loading.value = true
  try {
    emit('confirm')
    dialogVisible.value = false
    confirmText.value = ''
  } finally {
    loading.value = false
  }
}

const handleClosed = () => {
  confirmText.value = ''
}
</script>

<template>
  <el-dialog
    v-model="dialogVisible"
    :title="title ?? '确认删除'"
    width="420px"
    :close-on-click-modal="false"
    @closed="handleClosed"
  >
    <div style="line-height: 1.7; color: var(--notion-black);">
      <p style="margin-bottom: 12px;">
        确认删除选中的 <strong>{{ count }}</strong> 条记录？
      </p>
      <p style="font-size: 13px; color: var(--notion-gray-500); margin-bottom: 16px;">
        此操作不可恢复，请输入 <strong>确认删除</strong> 以继续：
      </p>
      <el-input
        v-model="confirmText"
        placeholder="请输入 确认删除"
        @keyup.enter="handleConfirm"
      />
    </div>

    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button
        type="danger"
        :loading="loading"
        :disabled="confirmText !== '确认删除'"
        @click="handleConfirm"
      >
        确认删除
      </el-button>
    </template>
  </el-dialog>
</template>
