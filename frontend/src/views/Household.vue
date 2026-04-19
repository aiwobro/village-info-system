<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { householdApi } from '../api/household'
import { naturalVillageApi } from '../api/naturalVillage'
import { adminVillageApi } from '../api/adminVillage'
import { ElMessage, ElMessageBox } from 'element-plus'
import ImportDialog from '../components/ImportDialog.vue'

const importDialogVisible = ref(false)
const importFields = [
  { label: '户号', field: 'household_no', required: true },
  { label: '所属自然村', field: 'natural_village_id', required: true },
  { label: '地址', field: 'address' },
]

const list = ref<any[]>([])
const naturalVillages = ref<any[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()

const form = ref({
  id: null as number | null,
  household_no: '',
  natural_village_id: null as number | null,
  head_id: null as number | null,
  address: '',
})

const rules = {
  household_no: [{ required: true, message: '请输入户号', trigger: 'blur' }],
  natural_village_id: [{ required: true, message: '请选择所属自然村', trigger: 'change' }],
}

const fetchList = async () => {
  loading.value = true
  try {
    const [households, naturalVills, adminVills] = await Promise.all([
      householdApi.getAll({ limit: 1000 }) as Promise<any[]>,
      naturalVillageApi.getAll({ limit: 1000 }) as Promise<any[]>,
      adminVillageApi.getAll({ limit: 100 }) as Promise<any[]>,
    ])
    naturalVillages.value = naturalVills
    list.value = households.map(h => {
      const nv = naturalVills.find((n: any) => n.id === h.natural_village_id)
      const av = nv ? adminVills.find((a: any) => a.id === nv.admin_village_id) : null
      return {
        ...h,
        natural_village_name: nv?.name || '-',
        admin_village_name: av?.name || '-',
      }
    })
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const openAdd = () => {
  isEdit.value = false
  form.value = { id: null, household_no: '', natural_village_id: null, head_id: null, address: '' }
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
        await householdApi.update(form.value.id, form.value)
        ElMessage.success('更新成功')
      } else {
        await householdApi.create(form.value)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      fetchList()
    } catch (e) {}
  })
}

const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm('确认删除该户？', '提示', { type: 'warning' })
    await householdApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchList()
  } catch (e) {}
}

onMounted(fetchList)
</script>

<template>
  <div class="page">
    <div class="toolbar">
      <h2>🏠 户管理</h2>
      <div style="display: flex; gap: 8px;">
        <el-button @click="importDialogVisible = true">批量导入</el-button>
        <el-button type="primary" @click="openAdd">新增户</el-button>
      </div>
    </div>

    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column prop="household_no" label="户号" />
      <el-table-column prop="admin_village_name" label="行政村" />
      <el-table-column prop="natural_village_name" label="自然村" />
      <el-table-column prop="address" label="地址" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" @click="openEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑户' : '新增户'" width="600px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="户号" prop="household_no">
          <el-input v-model="form.household_no" />
        </el-form-item>
        <el-form-item label="所属自然村" prop="natural_village_id">
          <el-select v-model="form.natural_village_id" style="width: 100%" placeholder="请选择">
            <el-option v-for="nv in naturalVillages" :key="nv.id" :label="nv.name" :value="nv.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="form.address" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <ImportDialog
      v-model="importDialogVisible"
      title="批量导入户"
      :fields="importFields"
      :api="householdApi"
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
