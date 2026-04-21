<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { resourceApi } from '../api/resource'
import { adminVillageApi } from '../api/adminVillage'
import { naturalVillageApi } from '../api/naturalVillage'
import { ElMessage, ElMessageBox } from 'element-plus'
import ImportDialog from '../components/ImportDialog.vue'
import BatchActionBar from '../components/BatchActionBar.vue'
import ViewDialog from '../components/ViewDialog.vue'
import EditDialog from '../components/EditDialog.vue'
import DeleteConfirmModal from '../components/DeleteConfirmModal.vue'
import { useSelectionStore } from '../stores/selection'
import { useAuthStore } from '../stores/auth'

const importDialogVisible = ref(false)
const importFields = [
  { label: '资源名称', field: 'name', required: true },
  { label: '资源编码', field: 'code' },
  { label: '资源类型', field: 'resource_type' },
  { label: '位置', field: 'location' },
  { label: '面积', field: 'area' },
  { label: '储量', field: 'reserves' },
  { label: '状态', field: 'status' },
  { label: '开发利用情况', field: 'development' },
  { label: '描述', field: 'description' },
  { label: '备注', field: 'remark' },
]

const list = ref<any[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const search = ref('')
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()
const adminVillages = ref<any[]>([])
const naturalVillages = ref<any[]>([])
const filterAdminVillage = ref<number | null>(null)
const filterNaturalVillage = ref<number | null>(null)

const form = ref({
  id: null as number | null,
  name: '',
  code: '',
  resource_type: '',
  location: '',
  area: null as number | null,
  reserves: '',
  status: '可用',
  development: '',
  description: '',
  remark: '',
})

const rules = {
  name: [{ required: true, message: '请输入资源名称', trigger: 'blur' }],
}

const fetchList = async () => {
  loading.value = true
  try {
    const skip = (page.value - 1) * pageSize.value
    const [data, avs, nvs] = await Promise.all([
      resourceApi.getAll({ skip, limit: pageSize.value, search: search.value, natural_village_id: filterNaturalVillage.value ?? undefined }) as Promise<any>,
      adminVillageApi.getAll({ limit: 100 }) as Promise<any>,
      naturalVillageApi.getAll({ limit: 5000 }) as Promise<any>,
    ])
    adminVillages.value = avs.items || []
    naturalVillages.value = nvs.items || []
    list.value = data.items || []
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
  form.value = { id: null, name: '', code: '', resource_type: '', location: '', area: null, reserves: '', status: '可用', development: '', description: '', remark: '' }
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
        await resourceApi.update(form.value.id, form.value)
        ElMessage.success('更新成功')
      } else {
        await resourceApi.create(form.value)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      fetchList()
    } catch (e) {}
  })
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确认删除该资源？', '提示', { type: 'warning' })
    await resourceApi.delete(id)
    ElMessage.success('删除成功')
    fetchList()
  } catch (e) {}
}

watch([page, pageSize], () => fetchList())

const selection = useSelectionStore()
const auth = useAuthStore()
const MODULE = 'resource'

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
    await ElMessageBox.confirm(`锁定选中的 ${selectedIds.value.length} 条？`, '确认锁定', { type: 'warning' })
    await Promise.all(selectedIds.value.map(id => resourceApi.lock(id)))
    ElMessage.success('已锁定'); selection.clear(MODULE); fetchList()
  } catch (e: any) { if (e !== 'cancel') ElMessage.error(e?.response?.data?.detail || '锁定失败') }
}
const handleBatchUnlock = async () => {
  try {
    await ElMessageBox.confirm(`解锁选中的 ${selectedIds.value.length} 条？`, '确认解锁', { type: 'info' })
    await Promise.all(selectedIds.value.map(id => resourceApi.unlock(id)))
    ElMessage.success('已解锁'); selection.clear(MODULE); fetchList()
  } catch (e: any) { if (e !== 'cancel') ElMessage.error(e?.response?.data?.detail || '解锁失败') }
}
const handleBatchExport = async () => {
  const ids = selectedIds.value
  if (!ids.length) return
  try {
    const res = await resourceApi.export(ids, 'resource') as any
    const blob = new Blob([res], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a'); a.href = url; a.download = `resource_${Date.now()}.xlsx`; a.click()
    URL.revokeObjectURL(url)
    ElMessage.success(`导出 ${ids.length} 条`)
  } catch (e: any) { ElMessage.error(e?.message || '导出失败') }
}
const handleDeleteConfirm = async () => {
  try {
    await Promise.all(selectedIds.value.map(id => resourceApi.delete(id)))
    ElMessage.success('已删除'); selection.clear(MODULE); deleteDialogVisible.value = false; fetchList()
  } catch (e: any) { ElMessage.error(e?.response?.data?.detail || '删除失败') }
}
const handleSelectionChange = (rows: any[]) => {
  const pageIds = list.value.map(r => r.id)
  selection.deselectAll(MODULE, pageIds)
  if (rows.length) selection.selectAll(MODULE, rows.map((r: any) => r.id))
}

const viewFields = [
  { label: '资源名称', field: 'name' },
  { label: '资源编码', field: 'code' },
  { label: '资源类型', field: 'resource_type' },
  { label: '位置', field: 'location' },
  { label: '面积(亩)', field: 'area' },
  { label: '储量', field: 'reserves' },
  { label: '状态', field: 'status' },
  { label: '开发利用情况', field: 'development' },
  { label: '描述', field: 'description' },
  { label: '备注', field: 'remark' },
]

const editFields = [
  { label: '资源名称', field: 'name', type: 'input', required: true },
  { label: '资源编码', field: 'code', type: 'input' },
  { label: '资源类型', field: 'resource_type', type: 'select',
    options: [{ label: '森林', value: '森林' }, { label: '水源', value: '水源' }, { label: '矿产', value: '矿产' }, { label: '农田', value: '农田' }, { label: '草地', value: '草地' }, { label: '水面', value: '水面' }] },
  { label: '位置', field: 'location', type: 'input' },
  { label: '面积(亩)', field: 'area', type: 'input' },
  { label: '储量/产量', field: 'reserves', type: 'input' },
  { label: '状态', field: 'status', type: 'select',
    options: [{ label: '可用', value: '可用' }, { label: '开发中', value: '开发中' }, { label: '已开发', value: '已开发' }, { label: '保护', value: '保护' }] },
  { label: '开发利用情况', field: 'development', type: 'input' },
  { label: '描述', field: 'description', type: 'textarea' },
  { label: '备注', field: 'remark', type: 'textarea' },
]

onMounted(fetchList)
</script>

<template>
  <div class="page">
    <div class="toolbar">
      <h2>🌲 资源管理</h2>
      <div style="display: flex; gap: 8px;">
        <el-button @click="importDialogVisible = true">批量导入</el-button>
        <el-button type="primary" @click="openAdd">新增资源</el-button>
      </div>
    </div>

    <div class="filter-bar">
      <el-select v-model="filterAdminVillage" placeholder="按行政村筛选" clearable style="width: 200px" @change="() => { filterNaturalVillage = null; handleSearch(); }">
        <el-option v-for="av in adminVillages" :key="av.id" :label="av.name" :value="av.id" />
      </el-select>
      <el-select v-model="filterNaturalVillage" placeholder="按自然村筛选" clearable style="width: 200px" @change="handleSearch">
        <el-option v-for="nv in (filterAdminVillage ? naturalVillages.filter((n: any) => n.admin_village_id === filterAdminVillage) : naturalVillages)" :key="nv.id" :label="nv.name" :value="nv.id" />
      </el-select>
      <el-input v-model="search" placeholder="搜索名称/编码" style="width: 240px" @keyup.enter="handleSearch" />
      <el-button type="primary" @click="handleSearch">搜索</el-button>
    </div>

    <el-table :data="list" v-loading="loading" stripe row-class-name="row-selected" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="40" />
      <el-table-column prop="name" label="资源名称" />
      <el-table-column prop="code" label="编码" />
      <el-table-column prop="resource_type" label="类型" />
      <el-table-column prop="location" label="位置" />
      <el-table-column prop="area" label="面积(亩)" />
      <el-table-column prop="reserves" label="储量" />
      <el-table-column prop="status" label="状态" />
      <el-table-column prop="development" label="开发利用情况" />
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
      :page-sizes="[20, 50, 100]"
      layout="total, sizes, prev, pager, next"
      @current-change="fetchList"
      @size-change="fetchList"
      style="margin-top: 16px"
    />

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑资源' : '新增资源'" width="700px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="资源名称" prop="name">
              <el-input v-model="form.name" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="资源编码">
              <el-input v-model="form.code" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="资源类型">
              <el-select v-model="form.resource_type" style="width: 100%">
                <el-option label="森林" value="森林" />
                <el-option label="水源" value="水源" />
                <el-option label="矿产" value="矿产" />
                <el-option label="农田" value="农田" />
                <el-option label="草地" value="草地" />
                <el-option label="水面" value="水面" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态">
              <el-select v-model="form.status" style="width: 100%">
                <el-option label="可用" value="可用" />
                <el-option label="开发中" value="开发中" />
                <el-option label="已开发" value="已开发" />
                <el-option label="保护" value="保护" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="位置">
          <el-input v-model="form.location" />
        </el-form-item>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="面积(亩)">
              <el-input-number v-model="form.area" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="储量/产量">
              <el-input v-model="form.reserves" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="开发利用情况">
          <el-input v-model="form.development" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="2" />
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
      title="批量导入资源"
      :fields="importFields"
      :api="resourceApi"
      :batch-api="resourceApi.batchCreate"
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

    <ViewDialog v-model="viewDialogVisible" title="查看资源" :record="viewRecord" :fields="viewFields" />

    <EditDialog
      v-model="editDialogVisible"
      title="编辑资源"
      :record="editRecord"
      :fields="editFields"
      :api="resourceApi"
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
