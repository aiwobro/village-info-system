<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { householdApi } from '../api/household'
import { naturalVillageApi } from '../api/naturalVillage'
import { adminVillageApi } from '../api/adminVillage'
import { villagerApi } from '../api/villager'
import { ElMessage, ElMessageBox } from 'element-plus'
import ImportDialog from '../components/ImportDialog.vue'
import BatchActionBar from '../components/BatchActionBar.vue'
import ViewDialog from '../components/ViewDialog.vue'
import EditDialog from '../components/EditDialog.vue'
import DeleteConfirmModal from '../components/DeleteConfirmModal.vue'
import { useSelectionStore } from '../stores/selection'

const importDialogVisible = ref(false)
const importFields = [
  { label: '户号', field: 'household_no', required: true },
  { label: '所属自然村', field: 'natural_village_id', required: true },
  { label: '地址', field: 'address' },
]

const importNaturalVillages = ref<any[]>([])

const importTransform = (record: any) => {
  if (record.natural_village_id && typeof record.natural_village_id === 'string') {
    const found = importNaturalVillages.value.find(
      (n: any) => n.name === record.natural_village_id || String(n.id) === record.natural_village_id
    )
    if (found) record.natural_village_id = found.id
  }
  return record
}

// 统计数据
const stats = ref({ household_count: 0, villager_count: 0 })

// 筛选
const adminVillages = ref<any[]>([])
const naturalVillages = ref<any[]>([])
const filterAdminVillage = ref<number | null>(null)
const filterNaturalVillage = ref<number | null>(null)
const filterLocked = ref<number | null>(null)
const filterSearch = ref('')

const list = ref<any[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()
const selection = useSelectionStore()
const MODULE = 'household'

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

// Batch action handlers
const handleBatchView = () => {
  const ids = selectedIds.value
  if (ids.length !== 1) {
    ElMessage.warning('请选择单条记录查看')
    return
  }
  viewRecord.value = list.value.find(r => r.id === ids[0])
  viewDialogVisible.value = true
}

const handleBatchEdit = () => {
  const ids = selectedIds.value
  if (ids.length !== 1) {
    ElMessage.warning('请选择单条记录进行编辑')
    return
  }
  editRecord.value = list.value.find(r => r.id === ids[0])
  editDialogVisible.value = true
}

const handleBatchDelete = () => {
  deleteDialogVisible.value = true
}

const handleBatchLock = async () => {
  const ids = selectedIds.value
  if (!ids.length) return
  try {
    await ElMessageBox.confirm(`锁定选中的 ${ids.length} 条记录？锁定后无法编辑和删除。`, '确认锁定', { confirmButtonText: '确认', cancelButtonText: '取消', type: 'warning' })
    await Promise.all(ids.map(id => householdApi.lock(id)))
    ElMessage.success(`已锁定 ${ids.length} 条记录`)
    selection.clear(MODULE)
    fetchList()
  } catch (e: any) {
    if (e !== 'cancel') ElMessage.error(e?.response?.data?.detail || '锁定失败')
  }
}

const handleBatchUnlock = async () => {
  const ids = selectedIds.value
  if (!ids.length) return
  try {
    await ElMessageBox.confirm(`解锁选中的 ${ids.length} 条记录？`, '确认解锁', { confirmButtonText: '确认', cancelButtonText: '取消', type: 'info' })
    await Promise.all(ids.map(id => householdApi.unlock(id)))
    ElMessage.success(`已解锁 ${ids.length} 条记录`)
    selection.clear(MODULE)
    fetchList()
  } catch (e: any) {
    if (e !== 'cancel') ElMessage.error(e?.response?.data?.detail || '解锁失败')
  }
}

const handleBatchExport = async () => {
  const ids = selectedIds.value
  if (!ids.length) return
  try {
    const res = await householdApi.export(ids, 'household') as any
    const blob = new Blob([res], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a'); a.href = url; a.download = `household_${Date.now()}.xlsx`; a.click()
    URL.revokeObjectURL(url)
    ElMessage.success(`导出 ${ids.length} 条`)
  } catch (e: any) { ElMessage.error(e?.message || '导出失败') }
}

const handleDeleteConfirm = async () => {
  const ids = selectedIds.value
  try {
    await Promise.all(ids.map(id => householdApi.delete(id)))
    ElMessage.success(`已删除 ${ids.length} 条记录`)
    selection.clear(MODULE)
    deleteDialogVisible.value = false
    fetchList()
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '删除失败')
  }
}

// Table row selection
const handleSelectionChange = (rows: any[]) => {
  const pageIds = list.value.map(r => r.id)
  selection.deselectAll(MODULE, pageIds)
  if (rows.length) {
    selection.selectAll(MODULE, rows.map((r: any) => r.id))
  }
}

// View/Edit dialog fields
const viewFields = [
  { label: '户号', field: 'household_no' },
  { label: '户主姓名', field: 'head_name' },
  { label: '户内人数', field: 'member_count' },
  { label: '行政村', field: 'admin_village_name' },
  { label: '自然村', field: 'natural_village_name' },
  { label: '地址', field: 'address' },
]

const editFields = computed(() => [
  { label: '户号', field: 'household_no', type: 'input', required: true },
  { label: '所属自然村', field: 'natural_village_id', type: 'select', required: true,
    options: naturalVillages.value.map((n: any) => ({ label: n.name, value: n.id })) },
  { label: '地址', field: 'address', type: 'input' },
])

// 成员弹窗
const membersDialogVisible = ref(false)
const members = ref<any[]>([])
const membersLoading = ref(false)
const currentHousehold = ref('')

const openMembers = async (row: any) => {
  currentHousehold.value = row.household_no
  membersDialogVisible.value = true
  membersLoading.value = true
  try {
    const res = await villagerApi.getAll({ household_id: row.id, limit: 1000 }) as any
    members.value = res.items || []
  } catch (e) {
    members.value = []
  } finally {
    membersLoading.value = false
  }
}

// 编辑弹窗中的成员
const editMembers = ref<any[]>([])
const newMemberForm = ref({ name: '', gender: '', id_card: '', relation_to_head: '本人', occupation: '', address: '' })

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

const fetchStats = async () => {
  try {
    const res = await householdApi.getStats({ admin_village_id: filterAdminVillage.value ?? undefined, natural_village_id: filterNaturalVillage.value ?? undefined, is_locked: filterLocked.value ?? undefined }) as any
    stats.value = res
  } catch (e) {
    stats.value = { household_count: 0, villager_count: 0 }
  }
}

const fetchList = async () => {
  loading.value = true
  try {
    const skip = (page.value - 1) * pageSize.value
    const params: any = { skip, limit: pageSize.value }
    if (filterAdminVillage.value) params.admin_village_id = filterAdminVillage.value
    if (filterNaturalVillage.value) params.natural_village_id = filterNaturalVillage.value
    if (filterLocked.value !== null) params.is_locked = filterLocked.value
    if (filterSearch.value) params.search = filterSearch.value

    const [data, avs] = await Promise.all([
      householdApi.getAll(params) as Promise<any>,
      adminVillageApi.getAll({ limit: 100 }) as Promise<any>,
    ])
    adminVillages.value = avs.items || []

    // 过滤后的自然村列表
    let nvsForFilter = naturalVillages.value
    if (filterAdminVillage.value) {
      nvsForFilter = naturalVillages.value.filter((n: any) => n.admin_village_id === filterAdminVillage.value)
    }

    list.value = (data.items || []).map((h: any) => {
      const nv = nvsForFilter.find((n: any) => n.id === h.natural_village_id)
      const av = adminVillages.value.find((a: any) => a.id === (nv?.admin_village_id || h.natural_village_id))
      return {
        ...h,
        natural_village_name: nv?.name || '-',
        admin_village_name: av?.name || '-',
      }
    })
    total.value = data.total || 0
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const fetchAllVillages = async () => {
  const avs = await adminVillageApi.getAll({ limit: 100 }) as any
  adminVillages.value = avs.items || []
  const nvs = await naturalVillageApi.getAll({ limit: 5000 }) as any
  naturalVillages.value = nvs.items || []
}

// 切换行政村筛选 → 重置自然村筛选
watch(filterAdminVillage, () => {
  filterNaturalVillage.value = null
  page.value = 1
  fetchList()
  fetchStats()
})

watch(filterNaturalVillage, () => {
  page.value = 1
  fetchList()
  fetchStats()
})

watch(filterLocked, () => {
  page.value = 1
  fetchList()
  fetchStats()
})

const handleSearch = () => {
  page.value = 1
  fetchList()
  fetchStats()
}

const openAdd = () => {
  isEdit.value = false
  form.value = { id: null, household_no: '', natural_village_id: null, head_id: null, address: '' }
  dialogVisible.value = true
}

const openEdit = async (row: any) => {
  isEdit.value = true
  form.value = { ...row }
  // 加载该户成员
  const res = await villagerApi.getAll({ household_id: row.id ?? undefined, limit: 500 }) as any
  editMembers.value = res.items || []
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
      fetchStats()
    } catch (e) {}
  })
}

const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm('确认删除该户？', '提示', { confirmButtonText: '确认', cancelButtonText: '取消', type: 'warning' })
    await householdApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchList()
    fetchStats()
  } catch (e: any) {
    if (e !== 'cancel') ElMessage.error(e?.response?.data?.detail || '删除失败')
  }
}

const handleAddMember = async () => {
  if (!newMemberForm.value.name) {
    ElMessage.warning('请填写成员姓名')
    return
  }
  try {
    await villagerApi.create({ ...newMemberForm.value, household_id: form.value.id })
    const res = await villagerApi.getAll({ household_id: form.value.id ?? undefined, limit: 500 }) as any
    editMembers.value = res.items || []
    newMemberForm.value = { name: '', gender: '', id_card: '', relation_to_head: '本人', occupation: '', address: '' }
    fetchList()
    ElMessage.success('添加成功')
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '添加失败')
  }
}

const handleDeleteMember = async (id: number) => {
  try {
    await ElMessageBox.confirm('确认删除该成员？', '提示', { confirmButtonText: '确认', cancelButtonText: '取消', type: 'warning' })
    await villagerApi.delete(id)
    editMembers.value = editMembers.value.filter(m => m.id !== id)
    fetchList()
    ElMessage.success('删除成功')
  } catch (e) {}
}

const openImport = async () => {
  importDialogVisible.value = true
  const nvs = await naturalVillageApi.getAll({ limit: 5000 }) as any
  importNaturalVillages.value = nvs.items || []
}

onMounted(async () => {
  await fetchAllVillages()
  fetchList()
  fetchStats()
})
</script>

<template>
  <div class="page">
    <div class="toolbar">
      <h2>🏠 户管理</h2>
      <div style="display: flex; gap: 8px;">
        <el-button @click="openImport">批量导入</el-button>
        <el-button type="primary" @click="openAdd">新增户</el-button>
      </div>
    </div>

    <!-- 统计行 -->
    <div class="stats-bar">
      <div class="stat-item">
        <span class="stat-num">{{ stats.household_count }}</span>
        <span class="stat-text">户</span>
      </div>
      <div class="stat-divider" />
      <div class="stat-item">
        <span class="stat-num">{{ stats.villager_count }}</span>
        <span class="stat-text">人</span>
      </div>
    </div>

    <!-- 筛选行 -->
    <div class="filter-bar">
      <el-select v-model="filterAdminVillage" placeholder="按行政村筛选" clearable style="width: 200px">
        <el-option v-for="av in adminVillages" :key="av.id" :label="av.name" :value="av.id" />
      </el-select>
      <el-select v-model="filterNaturalVillage" placeholder="按自然村筛选" clearable style="width: 200px">
        <el-option v-for="nv in (filterAdminVillage ? naturalVillages.filter((n: any) => n.admin_village_id === filterAdminVillage) : naturalVillages)" :key="nv.id" :label="nv.name" :value="nv.id" />
      </el-select>
      <el-select v-model="filterLocked" placeholder="按锁定筛选" clearable style="width: 130px" @change="handleSearch">
        <el-option label="已锁定" :value="1" />
        <el-option label="未锁定" :value="0" />
      </el-select>
      <el-input v-model="filterSearch" placeholder="按姓名或身份证搜索" clearable style="width: 200px" @keyup.enter="handleSearch" />
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
      <el-table-column prop="household_no" label="户号" />
      <el-table-column prop="head_name" label="户主姓名" />
      <el-table-column prop="member_count" label="户内人数" width="90" />
      <el-table-column prop="admin_village_name" label="行政村" />
      <el-table-column prop="natural_village_name" label="自然村" />
      <el-table-column prop="address" label="地址" />
      <el-table-column label="锁定" width="70">
        <template #default="{ row }">
          <el-icon v-if="row.is_locked" style="color: var(--notion-orange)"><Lock /></el-icon>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="240">
        <template #default="{ row }">
          <el-button size="small" @click="openMembers(row)">成员</el-button>
          <el-button size="small" @click="openEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
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

        <!-- 家庭成员区块 -->
        <el-divider content-position="left">家庭成员</el-divider>
        <el-table :data="editMembers" size="small" stripe style="margin-bottom: 12px" max-height="250">
          <el-table-column prop="name" label="姓名" />
          <el-table-column prop="gender" label="性别" width="60" />
          <el-table-column prop="id_card" label="身份证号" width="180" />
          <el-table-column prop="relation_to_head" label="与户主关系" width="100" />
          <el-table-column prop="occupation" label="职业" />
          <el-table-column label="操作" width="80">
            <template #default="{ row }">
              <el-button size="small" type="danger" @click="handleDeleteMember(row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-row :gutter="8">
          <el-col :span="4"><el-input v-model="newMemberForm.name" placeholder="姓名" size="small" /></el-col>
          <el-col :span="3"><el-select v-model="newMemberForm.gender" size="small" style="width:100%">
            <el-option label="男" value="男" /><el-option label="女" value="女" />
          </el-select></el-col>
          <el-col :span="6"><el-input v-model="newMemberForm.id_card" placeholder="身份证号" size="small" /></el-col>
          <el-col :span="4"><el-input v-model="newMemberForm.relation_to_head" placeholder="与户主关系" size="small" /></el-col>
          <el-col :span="4"><el-input v-model="newMemberForm.occupation" placeholder="职业" size="small" /></el-col>
          <el-col :span="3"><el-button size="small" type="primary" @click="handleAddMember">添加</el-button></el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="membersDialogVisible" :title="'户 ' + currentHousehold + ' 的成员'" width="700px">
      <el-table :data="members" v-loading="membersLoading" stripe max-height="400">
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="gender" label="性别" width="60" />
        <el-table-column prop="id_card" label="身份证号" width="180" />
        <el-table-column prop="relation_to_head" label="与户主关系" width="100" />
        <el-table-column prop="phone" label="电话" />
        <el-table-column prop="occupation" label="职业" />
      </el-table>
      <div v-if="members.length === 0 && !membersLoading" style="text-align: center; color: #909399; padding: 20px;">
        暂无成员
      </div>
    </el-dialog>

    <ImportDialog
      v-model="importDialogVisible"
      title="批量导入户"
      :fields="importFields"
      :api="householdApi"
      :batch-api="householdApi.batchCreate"
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
      :title="`查看户 — ${viewRecord?.household_no ?? ''}`"
      :record="viewRecord"
      :fields="viewFields"
    />

    <!-- 编辑弹窗 -->
    <EditDialog
      v-model="editDialogVisible"
      :title="editRecord?.id ? '编辑户' : '新增户'"
      :record="editRecord"
      :fields="editFields"
      :api="householdApi"
      @success="() => { fetchList(); selection.clear(MODULE); }"
    />

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
.stats-bar {
  display: flex;
  align-items: center;
  background: var(--airtable-surface);
  border: 1px solid var(--airtable-border);
  border-radius: var(--radius-md);
  padding: 12px 24px;
  margin-bottom: 16px;
  gap: 16px;
}
.stat-item {
  display: flex;
  align-items: baseline;
  gap: 4px;
}
.stat-num {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
}
.stat-text {
  font-size: 14px;
  color: #606266;
}
.stat-divider {
  width: 1px;
  height: 24px;
  background: #dcdfe6;
}
.filter-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}
</style>
