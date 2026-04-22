<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { adminVillageApi } from '../api/adminVillage'
import { naturalVillageApi } from '../api/naturalVillage'
import { ElMessage, ElMessageBox } from 'element-plus'
import ImportDialog from '../components/ImportDialog.vue'

const importDialogVisible = ref(false)
const importFields = [
  { label: '村名', field: 'name', required: true },
  { label: '村庄代码', field: 'code' },
  { label: '负责人', field: 'leader' },
  { label: '联系电话', field: 'phone' },
  { label: '地址', field: 'address' },
  { label: '描述', field: 'description' },
]

const list = ref<any[]>([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()
const loading = ref(false)

// 编辑弹窗中的自然村
const editNaturalVillages = ref<any[]>([])
const newNaturalVillageForm = ref({ name: '', leader: '', phone: '', description: '' })

const form = ref({
  id: null as number | null,
  name: '',
  code: '',
  leader: '',
  phone: '',
  address: '',
  description: '',
})

const rules = {
  name: [{ required: true, message: '请输入村名', trigger: 'blur' }],
}

const fetchList = async () => {
  loading.value = true
  try {
    const res = (await adminVillageApi.getAll({ limit: 100 })) as any
    list.value = res.items || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const openAdd = () => {
  isEdit.value = false
  form.value = { id: null, name: '', code: '', leader: '', phone: '', address: '', description: '' }
  dialogVisible.value = true
}

const openEdit = async (row: any) => {
  isEdit.value = true
  form.value = { ...row }
  // 加载该行政村下的自然村
  const res = await naturalVillageApi.getAll({ admin_village_id: row.id ?? undefined, limit: 500 }) as any
  editNaturalVillages.value = res.items || []
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid: boolean) => {
    if (!valid) return
    try {
      if (isEdit.value && form.value.id) {
        await adminVillageApi.update(form.value.id, form.value)
        ElMessage.success('更新成功')
      } else {
        await adminVillageApi.create(form.value)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      fetchList()
    } catch (e) {}
  })
}

const handleDelete = async (row: any) => {
  try {
    // 检查是否有关联的自然村
    const naturalVillages = ((await naturalVillageApi.getAll({ limit: 1000 })) as any).items || []
    const hasChildren = naturalVillages.some((v: any) => v.admin_village_id === row.id)
    if (hasChildren) {
      ElMessage.warning('该行政村下有自然村，无法删除')
      return
    }
    await ElMessageBox.confirm('确认删除？', '提示', { confirmButtonText: '确认', cancelButtonText: '取消', type: 'warning' })
    await adminVillageApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchList()
  } catch (e) {}
}

const handleAddNaturalVillage = async () => {
  if (!newNaturalVillageForm.value.name) {
    ElMessage.warning('请填写自然村名称')
    return
  }
  try {
    await naturalVillageApi.create({ ...newNaturalVillageForm.value, admin_village_id: form.value.id })
    const res = await naturalVillageApi.getAll({ admin_village_id: form.value.id ?? undefined, limit: 500 }) as any
    editNaturalVillages.value = res.items || []
    newNaturalVillageForm.value = { name: '', leader: '', phone: '', description: '' }
    fetchList()
    ElMessage.success('添加成功')
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '添加失败')
  }
}

const handleDeleteNaturalVillage = async (id: number) => {
  try {
    await ElMessageBox.confirm('确认删除该自然村？', '提示', { confirmButtonText: '确认', cancelButtonText: '取消', type: 'warning' })
    await naturalVillageApi.delete(id)
    editNaturalVillages.value = editNaturalVillages.value.filter(n => n.id !== id)
    ElMessage.success('删除成功')
  } catch (e: any) {
    if (e !== 'cancel') {
      ElMessage.error(e?.response?.data?.detail || '删除失败')
    }
  }
}

onMounted(fetchList)
</script>

<template>
  <div class="page">
    <div class="toolbar">
      <h2>🏘️ 行政村管理</h2>
      <div style="display: flex; gap: 8px;">
        <el-button @click="importDialogVisible = true">批量导入</el-button>
        <el-button type="primary" @click="openAdd">新增行政村</el-button>
      </div>
    </div>

    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column prop="name" label="村名" />
      <el-table-column prop="code" label="村庄代码" />
      <el-table-column prop="leader" label="负责人" />
      <el-table-column prop="phone" label="联系电话" />
      <el-table-column prop="address" label="地址" />
      <el-table-column prop="description" label="描述" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" @click="openEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑行政村' : '新增行政村'" width="600px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="村名" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="村庄代码">
          <el-input v-model="form.code" />
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
        <el-form-item label="地址">
          <el-input v-model="form.address" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>

        <!-- 下辖自然村区块 -->
        <el-divider content-position="left">下辖自然村</el-divider>
        <el-table :data="editNaturalVillages" size="small" stripe style="margin-bottom: 12px" max-height="250">
          <el-table-column prop="name" label="名称" />
          <el-table-column prop="leader" label="负责人" />
          <el-table-column prop="phone" label="联系电话" />
          <el-table-column prop="description" label="描述" />
          <el-table-column label="操作" width="80">
            <template #default="{ row }">
              <el-button size="small" type="danger" @click="handleDeleteNaturalVillage(row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-row :gutter="8">
          <el-col :span="6"><el-input v-model="newNaturalVillageForm.name" placeholder="自然村名称" size="small" /></el-col>
          <el-col :span="5"><el-input v-model="newNaturalVillageForm.leader" placeholder="负责人" size="small" /></el-col>
          <el-col :span="5"><el-input v-model="newNaturalVillageForm.phone" placeholder="联系电话" size="small" /></el-col>
          <el-col :span="5"><el-input v-model="newNaturalVillageForm.description" placeholder="描述" size="small" /></el-col>
          <el-col :span="3"><el-button size="small" type="primary" @click="handleAddNaturalVillage">添加</el-button></el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <ImportDialog
      v-model="importDialogVisible"
      title="批量导入行政村"
      :fields="importFields"
      :api="adminVillageApi"
      :batch-api="adminVillageApi.batchCreate"
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
