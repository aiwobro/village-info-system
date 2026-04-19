<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { contactApi } from '../api/contact'
import { villagerApi } from '../api/villager'
import { adminVillageApi } from '../api/adminVillage'
import { naturalVillageApi } from '../api/naturalVillage'
import { ElMessage, ElMessageBox } from 'element-plus'
import ImportDialog from '../components/ImportDialog.vue'

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
      contactApi.getAll({ skip, limit: pageSize.value, search: search.value, natural_village_id: filterNaturalVillage.value ?? undefined }),
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
  await ElMessageBox.confirm('确定要删除这条联系方式吗？', '提示', { type: 'warning' })
  await contactApi.delete(id)
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
      <el-input v-model="search" placeholder="搜索村民/联系方式/备注" style="width: 280px" @keyup.enter="handleSearch" />
      <el-button type="primary" @click="handleSearch">搜索</el-button>
    </div>

    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column prop="villager_name" label="村民" width="100" />
      <el-table-column prop="type" label="类型" width="100" />
      <el-table-column prop="value" label="联系方式" />
      <el-table-column prop="is_primary" label="主联系方式" width="110">
        <template #default="{ row }">
          {{ row.is_primary === 1 ? '是' : '否' }}
        </template>
      </el-table-column>
      <el-table-column prop="remark" label="备注" />
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
