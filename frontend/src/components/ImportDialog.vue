<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import * as XLSX from 'xlsx'

interface Field {
  label: string
  field: string
  required?: boolean
}

const props = defineProps<{
  title: string
  fields: Field[]
  api: any
}>()

const emit = defineEmits<{
  success: [count: number]
}>()

const dialogVisible = defineModel<boolean>()

const loading = ref(false)
const previewData = ref<any[]>([])
const previewColumns = ref<string[]>([])
const fileName = ref('')
const errorRows = ref<{ row: number; msg: string }[]>([])

const downloadTemplate = () => {
  const headers = props.fields.map(f => f.label)
  const worksheet = XLSX.utils.aoa_to_sheet([headers])
  const workbook = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(workbook, worksheet, '导入模板')
  XLSX.writeFile(workbook, `${props.title}.xlsx`)
}

const handleFileChange = async (event: Event) => {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  fileName.value = file.name
  errorRows.value = []

  try {
    const buffer = await file.arrayBuffer()
    const workbook = XLSX.read(buffer, { type: 'array' })
    const sheetName = workbook.SheetNames[0]
    const sheet = workbook.Sheets[sheetName]
    const jsonData = XLSX.utils.sheet_to_json(sheet, { header: 1 }) as any[][]

    if (jsonData.length < 2) {
      ElMessage.warning('Excel 文件至少需要 1 行表头 + 1 行数据')
      return
    }

    previewColumns.value = jsonData[0].map((h: any) => String(h ?? '').trim())
    previewData.value = jsonData.slice(1).filter((row: any[]) => row.some((cell: any) => cell !== null && cell !== undefined && cell !== ''))
  } catch (e: any) {
    ElMessage.error('读取 Excel 文件失败: ' + e.message)
  }

  input.value = ''
}

const getCell = (row: any[], colIndex: number) => {
  return row[colIndex] ?? ''
}

const handleConfirm = async () => {
  if (previewData.value.length === 0) {
    ElMessage.warning('没有可导入的数据')
    return
  }

  loading.value = true
  let successCount = 0
  const errors: { row: number; msg: string }[] = []

  for (let i = 0; i < previewData.value.length; i++) {
    const row = previewData.value[i]
    const rowNum = i + 2 // Excel 行号（1是表头）
    const record: any = {}

    for (let j = 0; j < props.fields.length; j++) {
      const field = props.fields[j]
      const colIndex = previewColumns.value.findIndex(
        (h) => h === field.label || h.replace(/\s+/g, '') === field.label.replace(/\s+/g, '')
      )
      if (colIndex >= 0) {
        record[field.field] = row[colIndex]
      }
    }

    // 检查必填字段
    for (const f of props.fields) {
      if (f.required && !record[f.field]) {
        errors.push({ row: rowNum, msg: `缺少必填字段: ${f.label}` })
        continue
      }
    }

    if (errors.length > 0 && errors[errors.length - 1].row === rowNum) continue

    try {
      await (props as any).api.create(record)
      successCount++
    } catch (e: any) {
      const msg = e?.response?.data?.detail || e?.message || '导入失败'
      errors.push({ row: rowNum, msg })
    }
  }

  loading.value = false
  errorRows.value = errors

  if (successCount > 0) {
    ElMessage.success(`成功导入 ${successCount} 条数据`)
    emit('success', successCount)
    dialogVisible.value = false
    previewData.value = []
    previewColumns.value = []
    fileName.value = ''
  } else {
    ElMessage.error('导入失败，请检查数据')
  }
}

const handleClose = () => {
  previewData.value = []
  previewColumns.value = []
  fileName.value = ''
  errorRows.value = []
}
</script>

<template>
  <el-dialog
    v-model="dialogVisible"
    :title="title"
    width="900px"
    :before-close="handleClose"
  >
    <div class="upload-area">
      <div class="upload-actions">
        <input
          type="file"
          accept=".xlsx,.xls"
          @change="handleFileChange"
          style="display: none"
          id="import-file-input"
        />
        <label for="import-file-input" class="upload-label">
          <el-icon size="24"><Upload /></el-icon>
          <span>选择 Excel 文件</span>
          <span class="hint">支持 .xlsx .xls</span>
        </label>
        <el-button @click="downloadTemplate" type="info" plain>
          <el-icon><Download /></el-icon> 下载模板
        </el-button>
      </div>
      <div v-if="fileName" class="file-name">
        已选: {{ fileName }}
      </div>
    </div>

    <div v-if="previewData.length > 0" class="preview-section">
      <div class="preview-header">
        <span>预览 ({{ previewData.length }} 行)</span>
        <span v-if="errorRows.length > 0" class="error-hint">
          ⚠️ {{ errorRows.length }} 行有错误，错误行将被跳过
        </span>
      </div>
      <el-table :data="previewData" stripe max-height="400" size="small">
        <el-table-column
          v-for="(col, idx) in previewColumns"
          :key="idx"
          :label="col"
          min-width="120"
        >
          <template #default="{ row }">
            <span :class="{ 'cell-error': errorRows.some(e => e.row === row.__rowIdx + 2) }">
              {{ getCell(row, idx) }}
            </span>
          </template>
        </el-table-column>
      </el-table>

      <div v-if="errorRows.length > 0" class="error-list">
        <div class="error-title">错误列表：</div>
        <div v-for="err in errorRows" :key="err.row" class="error-item">
          第 {{ err.row }} 行: {{ err.msg }}
        </div>
      </div>
    </div>

    <div v-else class="template-hint">
      <div class="template-title">Excel 列名要求：</div>
      <div class="field-list">
        <div v-for="f in fields" :key="f.field" class="field-item">
          <el-tag v-if="f.required" type="danger" size="small">必填</el-tag>
          <el-tag v-else size="small">选填</el-tag>
          <span class="field-label">{{ f.label }}</span>
          <code class="field-key">{{ f.field }}</code>
        </div>
      </div>
    </div>

    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button
        type="primary"
        :loading="loading"
        :disabled="previewData.length === 0"
        @click="handleConfirm"
      >
        确认导入
      </el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.upload-area {
  margin-bottom: 16px;
}
.upload-actions {
  display: flex;
  gap: 16px;
  align-items: center;
}
.upload-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 32px;
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  cursor: pointer;
  color: #606266;
  transition: all 0.2s;
}
.upload-label:hover {
  border-color: #409eff;
  color: #409eff;
}
.upload-label .hint {
  font-size: 12px;
  color: #909399;
}
.file-name {
  margin-top: 8px;
  color: #67c23a;
  font-size: 14px;
}
.preview-section {
  margin-top: 8px;
}
.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-size: 14px;
  color: #606266;
}
.error-hint {
  color: #f56c6c;
}
.template-hint {
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}
.template-title {
  font-weight: bold;
  margin-bottom: 12px;
  color: #303133;
}
.field-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.field-item {
  display: flex;
  align-items: center;
  gap: 8px;
}
.field-label {
  color: #606266;
  min-width: 100px;
}
.field-key {
  background: #ebeef5;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
  color: #909399;
}
.error-list {
  margin-top: 12px;
  max-height: 150px;
  overflow-y: auto;
  padding: 8px 12px;
  background: #fef0f0;
  border-radius: 4px;
}
.error-title {
  color: #f56c6c;
  font-weight: bold;
  margin-bottom: 4px;
}
.error-item {
  color: #f56c6c;
  font-size: 13px;
}
.cell-error {
  color: #f56c6c;
}
</style>
