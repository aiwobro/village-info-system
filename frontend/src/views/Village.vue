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
    await ElMessageBox.confirm('确认删除？', '提示', { type: 'warning' })
    await adminVillageApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchList()
  } catch (e) {}
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
