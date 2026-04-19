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
      (v: any) => v.name === record.villager_id || String(v.id) === record.villager_id || String(v.id_card) === record.villager_id
    )
    if (found) record.villager_id = found.id
  }
  if (record.account_number_encrypted !== undefined && record.account_number_encrypted !== null) {
    record.account_number_encrypted = String(record.account_number_encrypted)
  }
  if (record.is_active !== undefined) {
    if (String(record.is_active).toLowerCase() === '是' || String(record.is_active) === '1' || String(record.is_active).toLowerCase() === 'true' || String(record.is_active) === '正常' || String(record.is_active) === '激活') {
      record.is_active = 1
    } else if (String(record.is_active).toLowerCase() === '否' || String(record.is_active) === '0' || String(record.is_active).toLowerCase() === 'false' || String(record.is_active) === '停用' || String(record.is_active) === '注销') {
      record.is_active = 0
    }
  }
  return record
}

const openImport = async () => {
  importDialogVisible.value = true
  const res = await villagerApi.getAll({ limit: 5000 }) as any
  importVillagers.value = res.items || []
}

const list = ref<any[]>([])
const villagers = ref<any[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const loading = ref(false)
const search = ref('')
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
    const skip = (page.value - 1) * pageSize.value
    const [data, villagerData] = await Promise.all([
      bankAccountApi.getAll({ skip, limit: pageSize.value, search: search.value }),
      villagerApi.getAll({ limit: 5000 }) as Promise<any>,
    ])
    villagers.value = villagerData.items || []
    list.value = (data.items || []).map(b => ({
      ...b,
      villager_name: villagers.value.find((v: any) => v.id === b.villager_id)?.name || '-',
    }))
    total.value = data.total || 0
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
  await ElMessageBox.confirm('确定要删除这条账号吗？', '提示', { type: 'warning' })
  await bankAccountApi.delete(id)
  ElMessage.success('删除成功')
  fetchList()
}

const handleSearch = () => {
  page.value = 1
  fetchList()
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

    <div class="search-bar">
      <el-input v-model="search" placeholder="搜索村民/卡号/开户行/备注" style="width: 280px" @keyup.enter="handleSearch" />
      <el-button type="primary" @click="handleSearch">搜索</el-button>
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

    <el-pagination
      v-model:current-page="page"
      v-model:page-size="pageSize"
      :total="total"
      :page-sizes="[10, 20, 50, 100]"
      layout="total, sizes, prev, pager, next"
      @current-change="fetchList"
      @size-change="() => { page = 1; fetchList(); }"
      style="margin-top: 16px;"
    />

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
      :batch-api="bankAccountApi.batchCreate"
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
