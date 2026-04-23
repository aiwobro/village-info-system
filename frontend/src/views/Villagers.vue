<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { villagerApi } from '../api/villager'
import { householdApi } from '../api/household'
import { naturalVillageApi } from '../api/naturalVillage'
import { adminVillageApi } from '../api/adminVillage'
import { contactApi } from '../api/contact'
import { bankAccountApi } from '../api/bankAccount'
import { ElMessage, ElMessageBox } from 'element-plus'
import ImportDialog from '../components/ImportDialog.vue'
import BatchActionBar from '../components/BatchActionBar.vue'
import ViewDialog from '../components/ViewDialog.vue'
import DeleteConfirmModal from '../components/DeleteConfirmModal.vue'
import { useSelectionStore } from '../stores/selection'

const importDialogVisible = ref(false)
const importFields = [
  { label: '姓名', field: 'name', required: true },
  { label: '身份证号', field: 'id_card' },
  { label: '性别', field: 'gender' },
  { label: '出生日期', field: 'birth_date' },
  { label: '民族', field: 'ethnicity' },
  { label: '文化程度', field: 'education' },
  { label: '职业', field: 'occupation' },
  { label: '所属户', field: 'household_id' },
  { label: '与户主关系', field: 'relation_to_head' },
  { label: '住址', field: 'address' },
  { label: '备注', field: 'remark' },
]

const importHouseholds = ref<any[]>([])
const adminVillages = ref<any[]>([])
const naturalVillages = ref<any[]>([])
const filterAdminVillage = ref<number | null>(null)
const filterNaturalVillage = ref<number | null>(null)
const filterLocked = ref<number | null>(null)

const importTransform = (record: any) => {
  if (record.household_id && typeof record.household_id === 'string') {
    const found = importHouseholds.value.find(
      (h: any) => h.household_no === record.household_id || String(h.id) === record.household_id
    )
    if (found) record.household_id = found.id
  }
  return record
}

const openImport = async () => {
  importDialogVisible.value = true
  const hhs = await householdApi.getAll({ limit: 5000 }) as any
  importHouseholds.value = hhs.items || []
}

const list = ref<any[]>([])
const households = ref<any[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const search = ref('')
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()
const selection = useSelectionStore()
const MODULE = 'villager'

// Batch action bar state
const viewDialogVisible = ref(false)
const viewRecord = ref<any>(null)
const editDialogVisible = ref(false)
const editRecord = ref<any>(null)
const deleteDialogVisible = ref(false)

const selectedCount = computed(() => selection.count(MODULE))
const selectedIds = computed(() => selection.getSelectedIds(MODULE))
const lockedCount = computed(() =>
  list.value.filter(r => selectedIds.value.includes(r.id) && r.is_locked).length
)

const handleBatchView = () => {
  const ids = selectedIds.value
  if (ids.length !== 1) { ElMessage.warning('请选择单条记录查看'); return }
  viewRecord.value = list.value.find(r => r.id === ids[0])
  viewDialogVisible.value = true
}

const handleBatchEdit = () => {
  const ids = selectedIds.value
  if (ids.length !== 1) { ElMessage.warning('请选择单条记录进行编辑'); return }
  editRecord.value = list.value.find(r => r.id === ids[0])
  editDialogVisible.value = true
}

const handleBatchDelete = () => { deleteDialogVisible.value = true }

const handleBatchLock = async () => {
  const ids = selectedIds.value
  if (!ids.length) return
  try {
    await ElMessageBox.confirm(`锁定选中的 ${ids.length} 条记录？`, '确认锁定', { confirmButtonText: '确认', cancelButtonText: '取消', type: 'warning' })
    await Promise.all(ids.map(id => villagerApi.lock(id)))
    ElMessage.success(`已锁定 ${ids.length} 条`)
    selection.clear(MODULE); fetchList()
  } catch (e: any) { if (e !== 'cancel') ElMessage.error(e?.response?.data?.detail || '锁定失败') }
}

const handleBatchUnlock = async () => {
  const ids = selectedIds.value
  if (!ids.length) return
  try {
    await ElMessageBox.confirm(`解锁选中的 ${ids.length} 条记录？`, '确认解锁', { confirmButtonText: '确认', cancelButtonText: '取消', type: 'info' })
    await Promise.all(ids.map(id => villagerApi.unlock(id)))
    ElMessage.success(`已解锁 ${ids.length} 条`)
    selection.clear(MODULE); fetchList()
  } catch (e: any) { if (e !== 'cancel') ElMessage.error(e?.response?.data?.detail || '解锁失败') }
}

const handleBatchExport = async () => {
  const ids = selectedIds.value
  if (!ids.length) return
  try {
    const res = await villagerApi.export(ids, 'villager') as any
    const blob = new Blob([res], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a'); a.href = url; a.download = `villager_${Date.now()}.xlsx`; a.click()
    URL.revokeObjectURL(url)
    ElMessage.success(`导出 ${ids.length} 条`)
  } catch (e: any) { ElMessage.error(e?.message || '导出失败') }
}

const handleDeleteConfirm = async () => {
  try {
    await Promise.all(selectedIds.value.map(id => villagerApi.delete(id)))
    ElMessage.success(`已删除 ${selectedIds.value.length} 条`)
    selection.clear(MODULE); deleteDialogVisible.value = false; fetchList()
  } catch (e: any) { ElMessage.error(e?.response?.data?.detail || '删除失败') }
}

const handleSelectionChange = (rows: any[]) => {
  const pageIds = list.value.map(r => r.id)
  selection.deselectAll(MODULE, pageIds)
  if (rows.length) selection.selectAll(MODULE, rows.map((r: any) => r.id))
}

const viewFields = [
  { label: '姓名', field: 'name' },
  { label: '性别', field: 'gender' },
  { label: '身份证号', field: 'id_card' },
  { label: '出生日期', field: 'birth_date' },
  { label: '民族', field: 'ethnicity' },
  { label: '文化程度', field: 'education' },
  { label: '职业', field: 'occupation' },
  { label: '户号', field: 'household_no' },
  { label: '与户主关系', field: 'relation_to_head' },
  { label: '行政村', field: 'admin_village_name' },
  { label: '自然村', field: 'natural_village_name' },
  { label: '电话', field: 'phones' },
  { label: '银行账号', field: 'bank_info' },
  { label: '住址', field: 'address' },
  { label: '备注', field: 'remark' },
]


// 编辑弹窗中的联系方式和银行账号
const editContacts = ref<any[]>([])
const editBanks = ref<any[]>([])
const newContact = ref({ type: '', value: '', is_primary: 0, remark: '' })
const newBank = ref({ bank_name: '', account_holder: '', account_number_encrypted: '', account_type: '', is_active: 1, remark: '' })

const form = ref({
  id: null as number | null,
  name: '',
  id_card: '',
  gender: '',
  birth_date: '',
  ethnicity: '',
  education: '',
  occupation: '',
  relation_to_head: '',
  household_id: null as number | null,
  address: '',
  remark: '',
})

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
}

const fetchList = async () => {
  loading.value = true
  try {
    const skip = (page.value - 1) * pageSize.value
    const [data, hhs, nvs, avs, contactsData, banksData] = await Promise.all([
      villagerApi.getAll({ skip, limit: pageSize.value, search: search.value, natural_village_id: filterNaturalVillage.value ?? undefined, is_locked: filterLocked.value ?? undefined }),
      householdApi.getAll({ limit: 5000 }) as Promise<any>,
      naturalVillageApi.getAll({ limit: 5000 }) as Promise<any>,
      adminVillageApi.getAll({ limit: 100 }) as Promise<any>,
      contactApi.getAll({ limit: 5000 }) as Promise<any>,
      bankAccountApi.getAll({ limit: 5000 }) as Promise<any>,
    ])
    adminVillages.value = avs.items || []
    naturalVillages.value = nvs.items || []
    households.value = hhs.items || []
    const contacts = contactsData.items || []
    const banks = banksData.items || []
    list.value = (data.items || []).map(v => {
      const hh = households.value.find((h: any) => h.id === v.household_id)
      const nv = hh ? (nvs.items || []).find((n: any) => n.id === hh.natural_village_id) : null
      const av = nv ? (avs.items || []).find((a: any) => a.id === nv.admin_village_id) : null
      const villagerContacts = contacts.filter((c: any) => c.villager_id === v.id)
      const villagerBanks = banks.filter((b: any) => b.villager_id === v.id)
      const phones = villagerContacts.map((c: any) => c.value).filter(Boolean).join('、')
      const bankInfo = villagerBanks.map((b: any) => b.bank_name + ' ' + b.account_number_encrypted?.slice(-4)).filter(Boolean).join('、')
      return {
        ...v,
        household_no: hh?.household_no || '-',
        natural_village_name: nv?.name || '-',
        admin_village_name: av?.name || '-',
        phones: phones || '-',
        bank_info: bankInfo || '-',
      }
    })
    total.value = data.total || 0
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  page.value = 1
  fetchList()
}

const openAdd = () => {
  isEdit.value = false
  form.value = { id: null, name: '', id_card: '', gender: '', birth_date: '', ethnicity: '', education: '', occupation: '', relation_to_head: '', household_id: null, address: '', remark: '' }
  dialogVisible.value = true
}

const openEdit = async (row: any) => {
  isEdit.value = true
  form.value = { ...row }
  // 加载该村民的联系方式和银行账号
  const [contactsRes, banksRes] = await Promise.all([
    contactApi.getAll({ villager_id: row.id, limit: 1000 }) as Promise<any>,
    bankAccountApi.getAll({ villager_id: row.id, limit: 1000 }) as Promise<any>,
  ])
  editContacts.value = contactsRes.items || []
  editBanks.value = banksRes.items || []
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid: boolean) => {
    if (!valid) return
    try {
      if (isEdit.value && form.value.id) {
        await villagerApi.update(form.value.id, form.value)
        ElMessage.success('更新成功')
      } else {
        await villagerApi.create(form.value)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      fetchList()
    } catch (e) {}
  })
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确认删除该村民？', '提示', { confirmButtonText: '确认', cancelButtonText: '取消', type: 'warning' })
    await villagerApi.delete(id)
    ElMessage.success('删除成功')
    fetchList()
  } catch (e) {}
}

const handleDeleteContact = async (id: number) => {
  try {
    await ElMessageBox.confirm('确认删除该联系方式？', '提示', { confirmButtonText: '确认', cancelButtonText: '取消', type: 'warning' })
    await contactApi.delete(id)
    editContacts.value = editContacts.value.filter(c => c.id !== id)
    fetchList()
    ElMessage.success('删除成功')
  } catch (e) {}
}

const handleAddContact = async () => {
  if (!newContact.value.type || !newContact.value.value) {
    ElMessage.warning('请填写类型和联系方式')
    return
  }
  try {
    await contactApi.create({ ...newContact.value, villager_id: form.value.id })
    const res = await contactApi.getAll({ villager_id: form.value.id ?? undefined, limit: 1000 }) as any
    editContacts.value = res.items || []
    newContact.value = { type: '', value: '', is_primary: 0, remark: '' }
    fetchList()
    ElMessage.success('添加成功')
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '添加失败')
  }
}

const handleDeleteBank = async (id: number) => {
  try {
    await ElMessageBox.confirm('确认删除该银行账号？', '提示', { confirmButtonText: '确认', cancelButtonText: '取消', type: 'warning' })
    await bankAccountApi.delete(id)
    editBanks.value = editBanks.value.filter(b => b.id !== id)
    fetchList()
    ElMessage.success('删除成功')
  } catch (e) {}
}

const handleAddBank = async () => {
  if (!newBank.value.bank_name || !newBank.value.account_holder) {
    ElMessage.warning('请填写开户行和开户名')
    return
  }
  try {
    await bankAccountApi.create({ ...newBank.value, villager_id: form.value.id })
    const res = await bankAccountApi.getAll({ villager_id: form.value.id ?? undefined, limit: 1000 }) as any
    editBanks.value = res.items || []
    newBank.value = { bank_name: '', account_holder: '', account_number_encrypted: '', account_type: '', is_active: 1, remark: '' }
    fetchList()
    ElMessage.success('添加成功')
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '添加失败')
  }
}

onMounted(fetchList)
</script>

<template>
  <div class="page">
    <div class="toolbar">
      <h2>👥 村民管理</h2>
      <div style="display: flex; gap: 8px;">
        <el-button @click="openImport">批量导入</el-button>
        <el-button type="primary" @click="openAdd">新增村民</el-button>
      </div>
    </div>

    <div class="filter-bar">
      <el-select v-model="filterAdminVillage" placeholder="按行政村筛选" clearable style="width: 200px" @change="() => { filterNaturalVillage = null; handleSearch(); }">
        <el-option v-for="av in adminVillages" :key="av.id" :label="av.name" :value="av.id" />
      </el-select>
      <el-select v-model="filterNaturalVillage" placeholder="按自然村筛选" clearable style="width: 200px" @change="handleSearch">
        <el-option v-for="nv in (filterAdminVillage ? naturalVillages.filter((n: any) => n.admin_village_id === filterAdminVillage) : naturalVillages)" :key="nv.id" :label="nv.name" :value="nv.id" />
      </el-select>
      <el-select v-model="filterLocked" placeholder="按锁定筛选" clearable style="width: 130px" @change="handleSearch">
        <el-option label="已锁定" :value="1" />
        <el-option label="未锁定" :value="0" />
      </el-select>
      <el-input v-model="search" placeholder="搜索姓名/身份证" style="width: 280px" @keyup.enter="handleSearch" />
      <el-button type="primary" @click="handleSearch">搜索</el-button>
    </div>

    <el-table
      :data="list"
      v-loading="loading"
      stripe
      row-class-name="row-selected"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="40" />
      <el-table-column prop="name" label="姓名" />
      <el-table-column prop="gender" label="性别" width="60" />
      <el-table-column prop="id_card" label="身份证号" width="180" />
      <el-table-column prop="household_no" label="户号" />
      <el-table-column prop="relation_to_head" label="与户主关系" width="100" />
      <el-table-column prop="phones" label="电话" />
      <el-table-column prop="bank_info" label="银行账号" min-width="180" />
      <el-table-column prop="occupation" label="职业" />
      <el-table-column label="锁定" width="70">
        <template #default="{ row }">
          <el-icon v-if="row.is_locked" style="color: var(--notion-orange)"><Lock /></el-icon>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
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
      :page-sizes="[20, 50, 100]"
      layout="total, sizes, prev, pager, next"
      style="margin-top: 16px"
      @current-change="fetchList"
      @size-change="() => { page = 1; fetchList(); }"
    />

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑村民' : '新增村民'" width="700px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="form.name" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别">
              <el-select v-model="form.gender" style="width: 100%">
                <el-option label="男" value="男" />
                <el-option label="女" value="女" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="身份证号">
              <el-input v-model="form.id_card" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="出生日期">
              <el-input v-model="form.birth_date" placeholder="如：1990-01-01" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="民族">
              <el-input v-model="form.ethnicity" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="文化程度">
              <el-input v-model="form.education" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="职业">
              <el-input v-model="form.occupation" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="所属户">
              <el-select v-model="form.household_id" style="width: 100%" placeholder="请选择户" clearable>
                <el-option v-for="hh in households" :key="hh.id" :label="hh.household_no" :value="hh.id" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="与户主关系">
              <el-input v-model="form.relation_to_head" placeholder="如：本人、配偶、子女" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="住址">
          <el-input v-model="form.address" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.remark" type="textarea" :rows="2" />
        </el-form-item>

        <!-- 联系方式区块 -->
        <el-divider content-position="left">联系方式</el-divider>
        <el-table :data="editContacts" size="small" stripe style="margin-bottom: 12px">
          <el-table-column prop="type" label="类型" width="100" />
          <el-table-column prop="value" label="联系方式" />
          <el-table-column prop="is_primary" label="主联系" width="80">
            <template #default="{ row }">{{ row.is_primary === 1 ? '是' : '否' }}</template>
          </el-table-column>
          <el-table-column prop="remark" label="备注" />
          <el-table-column label="操作" width="80">
            <template #default="{ row }">
              <el-button size="small" type="danger" @click="handleDeleteContact(row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-row :gutter="8" style="margin-bottom: 12px">
          <el-col :span="6"><el-input v-model="newContact.type" placeholder="类型" size="small" /></el-col>
          <el-col :span="8"><el-input v-model="newContact.value" placeholder="联系方式" size="small" /></el-col>
          <el-col :span="4"><el-select v-model="newContact.is_primary" size="small" style="width:100%">
            <el-option label="主" :value="1" /><el-option label="副" :value="0" />
          </el-select></el-col>
          <el-col :span="6"><el-button size="small" type="primary" @click="handleAddContact">添加</el-button></el-col>
        </el-row>

        <!-- 银行账号区块 -->
        <el-divider content-position="left">银行账号</el-divider>
        <el-table :data="editBanks" size="small" stripe style="margin-bottom: 12px">
          <el-table-column prop="bank_name" label="开户行" />
          <el-table-column prop="account_holder" label="开户名" />
          <el-table-column prop="account_number_encrypted" label="卡号" />
          <el-table-column prop="is_active" label="状态" width="70">
            <template #default="{ row }">{{ row.is_active === 1 ? '有效' : '无效' }}</template>
          </el-table-column>
          <el-table-column label="操作" width="80">
            <template #default="{ row }">
              <el-button size="small" type="danger" @click="handleDeleteBank(row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-row :gutter="8">
          <el-col :span="7"><el-input v-model="newBank.bank_name" placeholder="开户行" size="small" /></el-col>
          <el-col :span="5"><el-input v-model="newBank.account_holder" placeholder="开户名" size="small" /></el-col>
          <el-col :span="7"><el-input v-model="newBank.account_number_encrypted" placeholder="卡号" size="small" /></el-col>
          <el-col :span="5"><el-button size="small" type="primary" @click="handleAddBank">添加</el-button></el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <ImportDialog
      v-model="importDialogVisible"
      title="批量导入村民"
      :fields="importFields"
      :api="villagerApi"
      :batch-api="villagerApi.batchCreate"
      :transform="importTransform"
      @success="fetchList"
    />

    <!-- 批量操作栏 -->
    <BatchActionBar
      :count="selectedCount"
      :module="MODULE"
      :locked-count="lockedCount"
      @view="handleBatchView"
      @edit="handleBatchEdit"
      @delete="handleBatchDelete"
      @lock="handleBatchLock"
      @unlock="handleBatchUnlock"
      @export="handleBatchExport"
    />

    <!-- 查看弹窗 -->
    <ViewDialog
      v-model="viewDialogVisible"
      :title="`查看村民 — ${viewRecord?.name ?? ''}`"
      :record="viewRecord"
      :fields="viewFields"
    />

    <!-- 编辑弹窗（批量操作用 ViewDialog + EditDialog 替代内置表单） -->
    <el-dialog v-model="editDialogVisible" :title="editRecord?.id ? '编辑村民' : '新增村民'" width="700px">
      <el-form ref="formRef" :model="editRecord ?? {}" :rules="rules" label-width="100px">
        <el-row :gutter="16">
          <el-col :span="12"><el-form-item label="姓名" prop="name"><el-input v-model="editRecord.name" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="性别"><el-select v-model="editRecord.gender" style="width:100%"><el-option label="男" value="男" /><el-option label="女" value="女" /></el-select></el-form-item></el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12"><el-form-item label="身份证号"><el-input v-model="editRecord.id_card" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="出生日期"><el-input v-model="editRecord.birth_date" /></el-form-item></el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12"><el-form-item label="民族"><el-input v-model="editRecord.ethnicity" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="文化程度"><el-input v-model="editRecord.education" /></el-form-item></el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12"><el-form-item label="职业"><el-input v-model="editRecord.occupation" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="所属户"><el-select v-model="editRecord.household_id" style="width:100%" placeholder="请选择户" clearable><el-option v-for="hh in households" :key="hh.id" :label="hh.household_no" :value="hh.id" /></el-select></el-form-item></el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12"><el-form-item label="与户主关系"><el-input v-model="editRecord.relation_to_head" /></el-form-item></el-col>
        </el-row>
        <el-form-item label="住址"><el-input v-model="editRecord.address" /></el-form-item>
        <el-form-item label="备注"><el-input v-model="editRecord.remark" type="textarea" :rows="2" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="async () => {
          try {
            await villagerApi.update(editRecord.id, editRecord)
            ElMessage.success('更新成功')
            editDialogVisible = false
            selection.clear(MODULE)
            fetchList()
          } catch(e: any) { ElMessage.error(e?.response?.data?.detail || '更新失败') }
        }">保存</el-button>
      </template>
    </el-dialog>

    <!-- 删除确认弹窗 -->
    <DeleteConfirmModal
      v-model="deleteDialogVisible"
      :count="selectedCount"
      @confirm="handleDeleteConfirm"
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
.filter-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  align-items: center;
}
</style>
