<script setup lang="ts">
import { computed } from 'vue'

export interface ViewField {
  label: string
  field: string
  type?: string  // 'text' | 'select' | 'boolean' | 'number' | 'date'
  options?: { label: string; value: any }[]
  trueLabel?: string
  falseLabel?: string
  format?: (val: any, row: any) => string
}

const props = defineProps<{
  modelValue: boolean
  title: string
  record: Record<string, any> | null
  fields: ViewField[]
}>()

const emit = defineEmits<{
  'update:modelValue': [val: boolean]
}>()

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const formatValue = (field: ViewField, value: any): string => {
  if (value === null || value === undefined || value === '') return '—'

  if (field.format) return field.format(value, props.record!)

  switch (field.type) {
    case 'boolean':
      return value ? (field.trueLabel ?? '是') : (field.falseLabel ?? '否')
    case 'select':
      if (field.options) {
        const opt = field.options.find(o => o.value === value)
        return opt ? opt.label : String(value)
      }
      return String(value)
    case 'date':
      return value ? String(value).slice(0, 10) : '—'
    case 'number':
      return typeof value === 'number' ? value.toLocaleString() : String(value)
    default:
      return String(value)
  }
}
</script>

<template>
  <el-dialog
    v-model="dialogVisible"
    :title="title"
    width="560px"
    :close-on-click-modal="false"
  >
    <div v-if="record" class="view-grid">
      <div
        v-for="field in fields"
        :key="field.field"
        class="view-row"
      >
        <span class="view-label">{{ field.label }}</span>
        <span class="view-value">
          <template v-if="field.type === 'boolean'">
            <el-tag :type="record[field.field] ? 'success' : 'info'" size="small" round>
              {{ formatValue(field, record[field.field]) }}
            </el-tag>
          </template>
          <template v-else>
            {{ formatValue(field, record[field.field]) }}
          </template>
        </span>
      </div>
    </div>

    <template #footer>
      <el-button @click="dialogVisible = false">关闭</el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.view-grid {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.view-row {
  display: flex;
  align-items: flex-start;
  padding: 10px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.view-row:last-child {
  border-bottom: none;
}

.view-label {
  width: 120px;
  flex-shrink: 0;
  font-size: 13px;
  color: var(--notion-gray-500);
  font-weight: 500;
  padding-top: 2px;
}

.view-value {
  flex: 1;
  font-size: 14px;
  color: var(--notion-black);
  word-break: break-all;
}
</style>
