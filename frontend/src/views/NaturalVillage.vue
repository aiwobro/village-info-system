<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { naturalVillageApi } from '../api/naturalVillage'
import { adminVillageApi } from '../api/adminVillage'
import { ElMessage, ElMessageBox } from 'element-plus'
import ImportDialog from '../components/ImportDialog.vue'

const importDialogVisible = ref(false)
const importFields = [
  { label: '村名', field: 'name', required: true },
  { label: '所属行政村', field: 'admin_village_id', required: true },
  { label: '负责人', field: 'leader' },
  { label: '联系电话', field: 'phone' },
  { label: '描述', field: 'description' },
]

const importAdminVillages = ref<any[]>([])

const importTransform = (record: any) => {
  if (record.admin_village_id && typeof record.admin_village_id === 'string') {
    const found = importAdminVillages.value.find(
      (a: any) => a.name === record.admin_village_id || String(a.id) === record.admin_village_id
    )
    if (found) record.admin_village_id = found.id
  }
  return record
}

const openImport = async () => {
  importDialogVisible.value = true
  const avs = ((await adminVillageApi.getAll({ limit: 100 })) as any).items || []
  importAdminVillages.value = avs
}

const list = ref<any[]>([])
const adminVillages = ref<any[]>([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()
const loading = ref(false)

const form = ref({
  id: null as number | null,
  name: '',
  admin_village_id: null as number | null,
  leader: '',
  phone: '',
  description: '',
})

const rules = {
  name: [{ required: true, message: '请输入村名', trigger: 'blur' }],
  admin_village_id: [{ required: true, message: '请选择所属行政村', trigger: 'change' }],
}

const fetchList = async () => {
  loading.value = true
  try {
    const nvResult = (await naturalVillageApi.getAll({ limit: 1000 })) as any
    const avResult = (await adminVillageApi.getAll({ limit: 100 })) as any
    const villages = nvResult.items || []
    const admins = avResult.items || []
    list.value = villages.map((v: any) => ({
      ...v,
      admin_village_name: admins.find((a: any) => a.id === v.admin_village_id)?.name || '-',
    }))
    adminVillages.value = admins
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const openAdd = () => {
  isEdit.value = false
  form.value = { id: null, name: '', admin_village_id: null, leader: '', phone: '', description: '' }
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
        await naturalVillageApi.update(form.value.id, form.value)
        ElMessage.success('更新成功')
      } else {
        await naturalVillageApi.create(form.value)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      fetchList()
    } catch (e) {}
  })
}

const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm('确认删除该自然村？', '提示', { confirmButtonText: '确认', cancelButtonText: '取消', type: 'warning' })
    await naturalVillageApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchList()
  } catch (e) {}
}

onMounted(fetchList)
</script>

<template>
  <div class="page">
    <div class="toolbar">
      <h2>🏡 自然村管理</h2>
      <div style="display: flex; gap: 8px;">
        <el-button @click="openImport">批量导入</el-button>
        <el-button type="primary" @click="openAdd">新增自然村</el-button>
      </div>
    </div>

    <el-table :data="list" v-loading="loading">
      <el-table-column prop="name" label="村名" />
      <el-table-column prop="admin_village_name" label="所属行政村" />
      <el-table-column prop="leader" label="负责人" />
      <el-table-column prop="phone" label="联系电话" />
      <el-table-column prop="description" label="描述" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" @click="openEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑自然村' : '新增自然村'" width="600px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="村名" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="所属行政村" prop="admin_village_id">
          <el-select v-model="form.admin_village_id" style="width: 100%" placeholder="请选择">
            <el-option v-for="av in adminVillages" :key="av.id" :label="av.name" :value="av.id" />
          </el-select>
        </el-form-item>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="负责人">
              <el-input v-model="form.leader" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话">
              <el-input v-model="form.phone" />
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

    <ImportDialog
      v-model="importDialogVisible"
      title="批量导入自然村"
      :fields="importFields"
      :api="naturalVillageApi"
      :batch-api="naturalVillageApi.batchCreate"
      :transform="importTransform"
      @success="fetchList"
    />
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
