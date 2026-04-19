<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { bankAccountApi } from '../api/bankAccount'
import { villagerApi } from '../api/villager'
import { ElMessage, ElMessageBox } from 'element-plus'
import ImportDialog from '../components/ImportDialog.vue'

const importDialogVisible = ref(false)
const importFields = [
  { label: '村民', field: 'villager_id', required: true },
  { label: '开户行', field: 'bank_name', required: true },
  { label: '开户名', field: 'account_holder', required: true },
  { label: '卡号', field: 'account_number_encrypted' },
  { label: '账户类型', field: 'account_type' },
  { label: '状态', field: 'is_active' },
  { label: '备注', field: 'remark' },
]

const importVillagers = ref<any[]>([])

const importTransform = (record: any) => {
  if (record.villager_id && typeof record.villager_id === 'string') {
    const found = importVillagers.value.find(
      (v: any) => v.name === record.villager_id || String(v.id) === record.villager_id
    )
    if (found) record.villager_id = found.id
  }
  // 把"状态"的文字转成布尔值
  if (record.is_active !== undefined) {
    if (String(record.is_active).toLowerCase() === '是' || String(record.is_active) === '1' || String(record.is_active).toLowerCase() === 'true' || String(record.is_active) === '正常' || String(record.is_active) === '激活') {
      record.is_active = true
    } else if (String(record.is_active).toLowerCase() === '否' || String(record.is_active) === '0' || String(record.is_active).toLowerCase() === 'false' || String(record.is_active) === '停用' || String(record.is_active) === '注销') {
      record.is_active = false
    }
  }
  return record
}

const openImport = async () => {
  importDialogVisible.value = true
  const vs = await villagerApi.getAll({ limit: 1000 }) as any[]
  importVillagers.value = vs
}

const list = ref<any[]>([])
const villagers = ref<any[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()

const form = ref({
  id: null as number | null,
  villager_id: null as number | null,
  bank_name: '',
  account_holder: '',
  account_number_encrypted: '',
  account_type: '',
  is_active: 1,
  remark: '',
})

const rules = {
  villager_id: [{ required: true, message: '请选择村民', trigger: 'change' }],
  bank_name: [{ required: true, message: '请输入开户行', trigger: 'blur' }],
  account_holder: [{ required: true, message: '请输入开户名', trigger: 'blur' }],
}

const fetchList = async () => {
  loading.value = true
  try {
    const [accounts, villagerList] = await Promise.all([
      bankAccountApi.getAll({ limit: 1000 }) as Promise<any[]>,
      villagerApi.getAll({ limit: 1000 }) as Promise<any[]>,
    ])
    villagers.value = villagerList
    list.value = accounts.map(b => ({
      ...b,
      villager_name: villagerList.find((v: any) => v.id === b.villager_id)?.name || '-',
    }))
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const openAdd = () => {
  isEdit.value = false
  form.value = { id: null, villager_id: null, bank_name: '', account_holder: '', account_number_encrypted: '', account_type: '', is_active: 1, remark: '' }
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
        await bankAccountApi.update(form.value.id, form.value)
        ElMessage.success('更新成功')
      } else {
        await bankAccountApi.create(form.value)
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
    await bankAccountApi.delete(id)
    ElMessage.success('删除成功')
    fetchList()
  } catch (e) {}
}

onMounted(fetchList)
</script>

<template>
  <div class="page">
    <div class="toolbar">
      <h2>💳 银行账号</h2>
      <div style="display: flex; gap: 8px;">
        <el-button @click="openImport">批量导入</el-button>
        <el-button type="primary" @click="openAdd">新增账号</el-button>
      </div>
    </div>

    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column prop="villager_name" label="村民" width="100" />
      <el-table-column prop="account_holder" label="开户名" />
      <el-table-column prop="bank_name" label="开户行" />
      <el-table-column prop="account_number_encrypted" label="卡号" />
      <el-table-column prop="account_type" label="账户类型" />
      <el-table-column prop="is_active" label="状态" width="80">
        <template #default="{ row }">
          {{ row.is_active === 1 ? '有效' : '无效' }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" @click="openEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑账号' : '新增账号'" width="600px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="村民" prop="villager_id">
          <el-select v-model="form.villager_id" style="width: 100%" placeholder="请选择村民" filterable>
            <el-option v-for="v in villagers" :key="v.id" :label="v.name" :value="v.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="开户名" prop="account_holder">
          <el-input v-model="form.account_holder" />
        </el-form-item>
        <el-form-item label="开户行" prop="bank_name">
          <el-input v-model="form.bank_name" />
        </el-form-item>
        <el-form-item label="卡号">
          <el-input v-model="form.account_number_encrypted" />
        </el-form-item>
        <el-form-item label="账户类型">
          <el-select v-model="form.account_type" style="width: 100%">
            <el-option label="个人账户" value="个人账户" />
            <el-option label="对公账户" value="对公账户" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="form.is_active">
            <el-radio :label="1">有效</el-radio>
            <el-radio :label="0">无效</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.remark" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <ImportDialog
      v-model="importDialogVisible"
      title="批量导入银行账号"
      :fields="importFields"
      :api="bankAccountApi"
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
