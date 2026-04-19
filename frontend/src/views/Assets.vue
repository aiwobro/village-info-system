<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { assetApi } from '../api/asset'
import { ElMessage, ElMessageBox } from 'element-plus'
import ImportDialog from '../components/ImportDialog.vue'

const importDialogVisible = ref(false)
const importFields = [
  { label: '资产名称', field: 'name', required: true },
  { label: '资产编码', field: 'code' },
  { label: '资产类型', field: 'asset_type' },
  { label: '位置', field: 'location' },
  { label: '面积', field: 'area' },
  { label: '数量', field: 'quantity' },
  { label: '单位', field: 'unit' },
  { label: '购置日期', field: 'purchase_date' },
  { label: '购置价格', field: 'purchase_price' },
  { label: '当前估值', field: 'current_value' },
  { label: '状态', field: 'status' },
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

const form = ref({
  id: null as number | null,
  name: '',
  code: '',
  asset_type: '',
  description: '',
  location: '',
  area: null as number | null,
  quantity: 1,
  unit: '',
  purchase_date: '',
  purchase_price: null as number | null,
  current_value: null as number | null,
  status: '正常使用',
  villager_id: null as number | null,
  remark: '',
})

const rules = {
  name: [{ required: true, message: '请输入资产名称', trigger: 'blur' }],
}

const fetchList = async () => {
  loading.value = true
  try {
    const skip = (page.value - 1) * pageSize.value
    const data: any = await assetApi.getAll({ skip, limit: pageSize.value, search: search.value })
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
  form.value = { id: null, name: '', code: '', asset_type: '', description: '', location: '', area: null, quantity: 1, unit: '', purchase_date: '', purchase_price: null, current_value: null, status: '正常使用', villager_id: null, remark: '' }
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
        await assetApi.update(form.value.id, form.value)
        ElMessage.success('更新成功')
      } else {
        await assetApi.create(form.value)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      fetchList()
    } catch (e) {}
  })
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确认删除该资产？', '提示', { type: 'warning' })
    await assetApi.delete(id)
    ElMessage.success('删除成功')
    fetchList()
  } catch (e) {}
}

watch([page, pageSize], () => fetchList())
onMounted(fetchList)
</script>

<template>
  <div class="page">
    <div class="toolbar">
      <h2>📦 资产管理</h2>
      <div style="display: flex; gap: 8px;">
        <el-button @click="importDialogVisible = true">批量导入</el-button>
        <el-button type="primary" @click="openAdd">新增资产</el-button>
      </div>
    </div>

    <div class="search-bar">
      <el-input v-model="search" placeholder="搜索名称/编码" style="width: 240px" @keyup.enter="handleSearch" />
      <el-button type="primary" @click="handleSearch">搜索</el-button>
    </div>

    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column prop="name" label="资产名称" />
      <el-table-column prop="code" label="编码" />
      <el-table-column prop="asset_type" label="类型" />
      <el-table-column prop="location" label="位置" />
      <el-table-column prop="area" label="面积(m²)" />
      <el-table-column prop="quantity" label="数量" />
      <el-table-column prop="current_value" label="当前估值" />
      <el-table-column prop="status" label="状态" />
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
      style="margin-top: 16px"
    />

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑资产' : '新增资产'" width="700px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="资产名称" prop="name">
              <el-input v-model="form.name" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="资产编码">
              <el-input v-model="form.code" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="资产类型">
              <el-select v-model="form.asset_type" style="width: 100%">
                <el-option label="土地" value="土地" />
                <el-option label="建筑" value="建筑" />
                <el-option label="设备" value="设备" />
                <el-option label="设施" value="设施" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态">
              <el-select v-model="form.status" style="width: 100%">
                <el-option label="正常使用" value="正常使用" />
                <el-option label="报废" value="报废" />
                <el-option label="出租" value="出租" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="位置">
          <el-input v-model="form.location" />
        </el-form-item>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="面积(m²)">
              <el-input-number v-model="form.area" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="数量">
              <el-input-number v-model="form.quantity" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="购置价格">
              <el-input-number v-model="form.purchase_price" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="当前估值">
              <el-input-number v-model="form.current_value" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
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
      title="批量导入资产"
      :fields="importFields"
      :api="assetApi"
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
.search-bar {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}
</style>
