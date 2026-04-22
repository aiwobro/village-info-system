<script setup lang="ts">
import { computed, watch, ref } from 'vue'
import { ElMessage } from 'element-plus'

export interface EditField {
  label: string
  field: string
  type: string  // 'input' | 'select' | 'number' | 'date' | 'textarea'
  required?: boolean
  options?: { label: string; value: any }[]
  rules?: any[]
  placeholder?: string
}

const props = defineProps<{
  modelValue: boolean
  title: string
  record: Record<string, any> | null   // null = new record
  fields: EditField[]
  api: any         // { create, update }
  transform?: (data: Record<string, any>) => Record<string, any>  // before save
}>()

const emit = defineEmits<{
  'update:modelValue': [val: boolean]
  'success': []
}>()

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

// Local form copy
const form = ref<Record<string, any>>({})
const loading = ref(false)
const formRef = ref()

watch(dialogVisible, (val) => {
  if (val) {
    if (props.record) {
      form.value = { ...props.record }
    } else {
      form.value = {}
      props.fields.forEach(f => {
        if (f.type === 'select') form.value[f.field] = null
        else if (f.type === 'number') form.value[f.field] = null
        else form.value[f.field] = ''
      })
    }
  }
})

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid: boolean) => {
    if (!valid) return
    loading.value = true
    try {
      const data = props.transform ? props.transform({ ...form.value }) : { ...form.value }
      if (form.value.id) {
        await props.api.update(form.value.id, data)
        ElMessage.success('更新成功')
      } else {
        await props.api.create(data)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      emit('success')
    } catch (e: any) {
      ElMessage.error(e?.response?.data?.detail || e?.message || '操作失败')
    } finally {
      loading.value = false
    }
  })
}
</script>

<template>
  <el-dialog
    v-model="dialogVisible"
    :title="title"
    width="560px"
    :close-on-click-modal="false"
    @closed="formRef?.resetFields()"
  >
    <el-form
      ref="formRef"
      :model="form"
      label-width="110px"
      label-position="left"
    >
      <el-form-item
        v-for="field in fields"
        :key="field.field"
        :label="field.label"
        :prop="field.field"
        :rules="field.rules"
      >
        <!-- select -->
        <el-select
          v-if="field.type === 'select'"
          v-model="form[field.field]"
          :placeholder="field.placeholder || `请选择${field.label}`"
          style="width: 100%"
          clearable
        >
          <el-option
            v-for="opt in field.options"
            :key="opt.value"
            :label="opt.label"
            :value="opt.value"
          />
        </el-select>

        <!-- textarea -->
        <el-input
          v-else-if="field.type === 'textarea'"
          v-model="form[field.field]"
          type="textarea"
          :rows="3"
          :placeholder="field.placeholder || `请输入${field.label}`"
        />

        <!-- number -->
        <el-input-number
          v-else-if="field.type === 'number'"
          v-model="form[field.field]"
          :placeholder="field.placeholder || `请输入${field.label}`"
          controls-position="right"
          style="width: 100%"
        />

        <!-- date -->
        <el-date-picker
          v-else-if="field.type === 'date'"
          v-model="form[field.field]"
          type="date"
          value-format="YYYY-MM-DD"
          :placeholder="field.placeholder || `请选择${field.label}`"
          style="width: 100%"
        />

        <!-- default: text input -->
        <el-input
          v-else
          v-model="form[field.field]"
          :placeholder="field.placeholder || `请输入${field.label}`"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" :loading="loading" @click="handleSubmit">
        {{ form.id ? '保存' : '创建' }}
      </el-button>
    </template>
  </el-dialog>
</template>
