<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { villageApi } from '../api/village'
import { ElMessage, ElMessageBox } from 'element-plus'

const list = ref<any[]>([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()
const loading = ref(false)

const form = ref({
  id: null as number | null,
  name: '',
  code: '',
  address: '',
  area: null as number | null,
  population: null as number | null,
  established_date: '',
  latitude: null as number | null,
  longitude: null as number | null,
  description: '',
})

const rules = {
  name: [{ required: true, message: '请输入村名', trigger: 'blur' }],
}

const fetchList = async () => {
  loading.value = true
  try {
    list.value = await villageApi.getAll({ limit: 100 }) as any[]
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const openAdd = () => {
  isEdit.value = false
  form.value = { id: null, name: '', code: '', address: '', area: null, population: null, established_date: '', latitude: null, longitude: null, description: '' }
  dialogVisible.value = true
}

const openEdit = (row: any) => {
  isEdit.value = true
  form.value = { ...row }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid: boolean) => {
    if (!valid) return
    try {
      if (isEdit.value && form.value.id) {
        await villageApi.update(form.value.id, form.value)
        ElMessage.success('更新成功')
      } else {
        await villageApi.create(form.value)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      fetchList()
    } catch (e) {}
  })
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确认删除？', '提示', { type: 'warning' })
    await villageApi.delete(id)
    ElMessage.success('删除成功')
    fetchList()
  } catch (e) {}
}

onMounted(fetchList)
</script>

<template>
  <div class="page">
    <div class="toolbar">
      <h2>🏘️ 村庄信息</h2>
      <el-button type="primary" @click="openAdd">新增村庄</el-button>
    </div>

    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column prop="name" label="村名" />
      <el-table-column prop="code" label="村庄代码" />
      <el-table-column prop="address" label="地址" />
      <el-table-column prop="area" label="面积(km²)" />
      <el-table-column prop="population" label="人口" />
      <el-table-column prop="established_date" label="成立时间" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" @click="openEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑村庄' : '新增村庄'" width="600px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="村名" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="村庄代码">
          <el-input v-model="form.code" />
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="form.address" />
        </el-form-item>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="面积(km²)">
              <el-input-number v-model="form.area" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="人口">
              <el-input-number v-model="form.population" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="成立时间">
          <el-input v-model="form.established_date" placeholder="如：1980-01-01" />
        </el-form-item>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="纬度">
              <el-input-number v-model="form.latitude" :precision="6" :step="0.000001" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="经度">
              <el-input-number v-model="form.longitude" :precision="6" :step="0.000001" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.page { padding: 0; }
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.toolbar h2 { margin: 0; }
</style>
