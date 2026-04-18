<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { resourceApi } from '../api/resource'
import { ElMessage, ElMessageBox } from 'element-plus'

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
    const [data, countData] = await Promise.all([
      resourceApi.getAll({ skip, limit: pageSize.value, search: search.value }),
      resourceApi.getCount(search.value),
    ])
    list.value = data as any[]
    total.value = (countData as any).count
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
onMounted(fetchList)
</script>

<template>
  <div class="page">
    <div class="toolbar">
      <h2>🌲 资源管理</h2>
      <el-button type="primary" @click="openAdd">新增资源</el-button>
    </div>

    <div class="search-bar">
      <el-input v-model="search" placeholder="搜索名称/编码" style="width: 240px" @keyup.enter="handleSearch" />
      <el-button type="primary" @click="handleSearch">搜索</el-button>
    </div>

    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column prop="name" label="资源名称" />
      <el-table-column prop="code" label="编码" />
      <el-table-column prop="resource_type" label="类型" />
      <el-table-column prop="location" label="位置" />
      <el-table-column prop="area" label="面积(亩)" />
      <el-table-column prop="reserves" label="储量" />
      <el-table-column prop="status" label="状态" />
      <el-table-column prop="development" label="开发利用情况" />
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
