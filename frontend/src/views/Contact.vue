<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { contactApi } from '../api/contact'
import { villagerApi } from '../api/villager'
import { adminVillageApi } from '../api/adminVillage'
import { naturalVillageApi } from '../api/naturalVillage'
import { ElMessage, ElMessageBox } from 'element-plus'
import ImportDialog from '../components/ImportDialog.vue'
import BatchActionBar from '../components/BatchActionBar.vue'
import ViewDialog from '../components/ViewDialog.vue'
import EditDialog from '../components/EditDialog.vue'
import DeleteConfirmModal from '../components/DeleteConfirmModal.vue'
import { useSelectionStore } from '../stores/selection'

const importDialogVisible = ref(false)
const importFields = [
  { label: '村民', field: 'villager_id', required: true },
  { label: '类型', field: 'type', required: true },
  { label: '联系方式', field: 'value', required: true },
  { label: '主联系方式', field: 'is_primary' },
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
  if (record.value !== undefined && record.value !== null) {
    record.value = String(record.value)
  }
  if (record.is_primary !== undefined) {
    if (String(record.is_primary).toLowerCase() === '是' || String(record.is_primary) === '1' || String(record.is_primary).toLowerCase() === 'true') {
      record.is_primary = 1
    } else if (String(record.is_primary).toLowerCase() === '否' || String(record.is_primary) === '0' || String(record.is_primary).toLowerCase() === 'false') {
      record.is_primary = 0
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
const adminVillages = ref<any[]>([])
const naturalVillages = ref<any[]>([])
const filterAdminVillage = ref<number | null>(null)
const filterNaturalVillage = ref<number | null>(null)
const filterLocked = ref<number | null>(null)

const form = ref({
  id: null as number | null,
  villager_id: null as number | null,
  type: '',
  value: '',
  is_primary: 0,
  remark: '',
})

const contactTypes = [
  { label: '手机', value: '手机' },
  { label: '固定电话', value: '固定电话' },
  { label: '微信', value: '微信' },
  { label: 'QQ', value: 'QQ' },
  { label: '邮箱', value: '邮箱' },
  { label: '紧急联系人', value: '紧急联系人' },
]

const rules = {
  villager_id: [{ required: true, message: '请选择村民', trigger: 'change' }],
  type: [{ required: true, message: '请选择联系方式类型', trigger: 'change' }],
  value: [{ required: true, message: '请输入联系方式', trigger: 'blur' }],
}

const fetchList = async () => {
  loading.value = true
  try {
    const skip = (page.value - 1) * pageSize.value
    const [data, villagerData, avs, nvs] = await Promise.all([
      contactApi.getAll({ skip, limit: pageSize.value, search: search.value, natural_village_id: filterNaturalVillage.value ?? undefined, is_locked: filterLocked.value ?? undefined }),
      villagerApi.getAll({ limit: 5000 }) as Promise<any>,
      adminVillageApi.getAll({ limit: 100 }) as Promise<any>,
      naturalVillageApi.getAll({ limit: 5000 }) as Promise<any>,
    ])
    adminVillages.value = avs.items || []
    naturalVillages.value = nvs.items || []
    villagers.value = villagerData.items || []
    list.value = (data.items || []).map(c => ({
      ...c,
      villager_name: villagers.value.find((v: any) => v.id === c.villager_id)?.name || '-',
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
  form.value = { id: null, villager_id: null, type: '', value: '', is_primary: 0, remark: '' }
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
        await contactApi.update(form.value.id, form.value)
        ElMessage.success('更新成功')
      } else {
        await contactApi.create(form.value)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      fetchList()
    } catch (e) {}
  })
}

const handleDelete = async (id: number) => {
  await ElMessageBox.confirm('确定要删除这条联系方式吗？', '提示', { confirmButtonText: '确认', cancelButtonText: '取消', type: 'warning' })
  await contactApi.delete(id)
  ElMessage.success('删除成功')
  fetchList()
}

const handleSearch = () => {
  page.value = 1
  fetchList()
}

const selection = useSelectionStore()
const MODULE = 'contact'

const viewDialogVisible = ref(false)
const viewRecord = ref<any>(null)
const editDialogVisible = ref(false)
const editRecord = ref<any>(null)
const deleteDialogVisible = ref(false)

const selectedCount = computed(() => selection.count(MODULE))
const selectedIds = computed(() => selection.getSelectedIds(MODULE))
const lockedCount = computed(() => list.value.filter(r => selectedIds.value.includes(r.id) && r.is_locked).length)

const handleBatchView = () => {
  if (selectedIds.value.length !== 1) { ElMessage.warning('请选择单条记录查看'); return }
  viewRecord.value = list.value.find(r => r.id === selectedIds.value[0])
  viewDialogVisible.value = true
}
const handleBatchEdit = () => {
  if (selectedIds.value.length !== 1) { ElMessage.warning('请选择单条记录进行编辑'); return }
  editRecord.value = list.value.find(r => r.id === selectedIds.value[0])
  editDialogVisible.value = true
}
const handleBatchDelete = () => { deleteDialogVisible.value = true }
const handleBatchLock = async () => {
  try {
    await ElMessageBox.confirm(`锁定选中的 ${selectedIds.value.length} 条？`, '确认锁定', { confirmButtonText: '确认', cancelButtonText: '取消', type: 'warning' })
    await Promise.all(selectedIds.value.map(id => contactApi.lock(id)))
    ElMessage.success('已锁定'); selection.clear(MODULE); fetchList()
  } catch (e: any) { if (e !== 'cancel') ElMessage.error(e?.response?.data?.detail || '锁定失败') }
}
const handleBatchUnlock = async () => {
  try {
    await ElMessageBox.confirm(`解锁选中的 ${selectedIds.value.length} 条？`, '确认解锁', { confirmButtonText: '确认', cancelButtonText: '取消', type: 'info' })
    await Promise.all(selectedIds.value.map(id => contactApi.unlock(id)))
    ElMessage.success('已解锁'); selection.clear(MODULE); fetchList()
  } catch (e: any) { if (e !== 'cancel') ElMessage.error(e?.response?.data?.detail || '解锁失败') }
}
const handleBatchExport = async () => {
  const ids = selectedIds.value
  if (!ids.length) return
  try {
    const res = await contactApi.export(ids, 'contact') as any
    const blob = new Blob([res], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a'); a.href = url; a.download = `contact_${Date.now()}.xlsx`; a.click()
    URL.revokeObjectURL(url)
    ElMessage.success(`导出 ${ids.length} 条`)
  } catch (e: any) { ElMessage.error(e?.message || '导出失败') }
}
const handleDeleteConfirm = async () => {
  try {
    await Promise.all(selectedIds.value.map(id => contactApi.delete(id)))
    ElMessage.success('已删除'); selection.clear(MODULE); deleteDialogVisible.value = false; fetchList()
  } catch (e: any) { ElMessage.error(e?.response?.data?.detail || '删除失败') }
}
const handleSelectionChange = (rows: any[]) => {
  const pageIds = list.value.map(r => r.id)
  selection.deselectAll(MODULE, pageIds)
  if (rows.length) selection.selectAll(MODULE, rows.map((r: any) => r.id))
}

const viewFields = [
  { label: '村民', field: 'villager_name' },
  { label: '类型', field: 'type' },
  { label: '联系方式', field: 'value' },
  { label: '主联系方式', field: 'is_primary', type: 'boolean', trueLabel: '是', falseLabel: '否' },
  { label: '备注', field: 'remark' },
]

const editFields = computed(() => [
  { label: '村民', field: 'villager_id', type: 'select', required: true,
    options: villagers.value.map((v: any) => ({ label: v.name, value: v.id })) },
  { label: '类型', field: 'type', type: 'select', required: true,
    options: contactTypes.map(t => ({ label: t.label, value: t.value })) },
  { label: '联系方式', field: 'value', type: 'input', required: true },
  { label: '主联系方式', field: 'is_primary', type: 'select',
    options: [{ label: '是', value: 1 }, { label: '否', value: 0 }] },
  { label: '备注', field: 'remark', type: 'textarea' },
])

onMounted(fetchList)
</script>

<template>
  <div class="page">
    <div class="toolbar">
      <h2>📞 联系方式</h2>
      <div style="display: flex; gap: 8px;">
        <el-button @click="openImport">批量导入</el-button>
        <el-button type="primary" @click="openAdd">新增联系方式</el-button>
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
      <el-input v-model="search" placeholder="搜索村民/联系方式/备注" style="width: 280px" @keyup.enter="handleSearch" />
      <el-button type="primary" @click="handleSearch">搜索</el-button>
    </div>

    <el-table :data="list" v-loading="loading" stripe row-class-name="row-selected" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="40" />
      <el-table-column prop="villager_name" label="村民" width="100" />
      <el-table-column prop="type" label="类型" width="100" />
      <el-table-column prop="value" label="联系方式" />
      <el-table-column prop="is_primary" label="主联系方式" width="110">
        <template #default="{ row }">{{ row.is_primary === 1 ? '是' : '否' }}</template>
      </el-table-column>
      <el-table-column prop="remark" label="备注" />
      <el-table-column label="锁定" width="70">
        <template #default="{ row }"><el-icon v-if="row.is_locked" style="color: var(--notion-orange)"><Lock /></el-icon></template>
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

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑联系方式' : '新增联系方式'" width="500px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="110px">
        <el-form-item label="村民" prop="villager_id">
          <el-select v-model="form.villager_id" style="width: 100%" placeholder="请选择村民" filterable>
            <el-option v-for="v in villagers" :key="v.id" :label="v.name" :value="v.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="form.type" style="width: 100%" placeholder="请选择">
            <el-option v-for="t in contactTypes" :key="t.value" :label="t.label" :value="t.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="联系方式" prop="value">
          <el-input v-model="form.value" />
        </el-form-item>
        <el-form-item label="主联系方式">
          <el-radio-group v-model="form.is_primary">
            <el-radio :label="1">是</el-radio>
            <el-radio :label="0">否</el-radio>
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
      title="批量导入联系方式"
      :fields="importFields"
      :api="contactApi"
      :batch-api="contactApi.batchCreate"
      :transform="importTransform"
      @success="fetchList"
    />

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

    <ViewDialog v-model="viewDialogVisible" :title="`查看联系方式`" :record="viewRecord" :fields="viewFields" />

    <EditDialog
      v-model="editDialogVisible"
      title="编辑联系方式"
      :record="editRecord"
      :fields="editFields"
      :api="contactApi"
      @success="() => { selection.clear(MODULE); fetchList() }"
    />

    <DeleteConfirmModal v-model="deleteDialogVisible" :count="selectedCount" @confirm="handleDeleteConfirm" />
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
