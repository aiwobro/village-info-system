<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { villagerApi } from '../api/villager'
import { householdApi } from '../api/household'
import { naturalVillageApi } from '../api/naturalVillage'
import { adminVillageApi } from '../api/adminVillage'
import { ElMessage, ElMessageBox } from 'element-plus'
import ImportDialog from '../components/ImportDialog.vue'

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
  const hhs = await householdApi.getAll({ limit: 1000 }) as any
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
    const [data, hhs, nvs, avs] = await Promise.all([
      villagerApi.getAll({ skip, limit: pageSize.value, search: search.value }),
      householdApi.getAll({ limit: 1000 }) as Promise<any>,
      naturalVillageApi.getAll({ limit: 1000 }) as Promise<any>,
      adminVillageApi.getAll({ limit: 100 }) as Promise<any>,
    ])
    households.value = hhs.items || []
    list.value = (data.items || []).map(v => {
      const hh = households.value.find((h: any) => h.id === v.household_id)
      const nv = hh ? (nvs.items || []).find((n: any) => n.id === hh.natural_village_id) : null
      const av = nv ? (avs.items || []).find((a: any) => a.id === nv.admin_village_id) : null
      return {
        ...v,
        household_no: hh?.household_no || '-',
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

const handleSearch = () => {
  page.value = 1
  fetchList()
}

const openAdd = () => {
  isEdit.value = false
  form.value = { id: null, name: '', id_card: '', gender: '', birth_date: '', ethnicity: '', education: '', occupation: '', relation_to_head: '', household_id: null, address: '', remark: '' }
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
    await ElMessageBox.confirm('确认删除该村民？', '提示', { type: 'warning' })
    await villagerApi.delete(id)
    ElMessage.success('删除成功')
    fetchList()
  } catch (e) {}
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

    <div class="search-bar">
      <el-input v-model="search" placeholder="搜索姓名/身份证" style="width: 280px" @keyup.enter="handleSearch" />
      <el-button type="primary" @click="handleSearch">搜索</el-button>
    </div>

    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column prop="name" label="姓名" />
      <el-table-column prop="gender" label="性别" width="60" />
      <el-table-column prop="id_card" label="身份证号" width="180" />
      <el-table-column prop="household_no" label="户号" />
      <el-table-column prop="relation_to_head" label="与户主关系" width="100" />
      <el-table-column prop="phone" label="电话" />
      <el-table-column prop="occupation" label="职业" />
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
.search-bar {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}
</style>
