<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { householdApi } from '../api/household'
import { naturalVillageApi } from '../api/naturalVillage'
import { adminVillageApi } from '../api/adminVillage'
import { villagerApi } from '../api/villager'
import { ElMessage, ElMessageBox } from 'element-plus'
import ImportDialog from '../components/ImportDialog.vue'

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

const list = ref<any[]>([])
const naturalVillages = ref<any[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()

// 成员弹窗
const membersDialogVisible = ref(false)
const members = ref<any[]>([])
const membersLoading = ref(false)
const currentHousehold = ref('')
const currentHouseholdId = ref<number | null>(null)
const currentHeadId = ref<number | null>(null)

const openMembers = async (row: any) => {
  currentHousehold.value = row.household_no
  currentHouseholdId.value = row.id
  currentHeadId.value = row.head_id
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

const handleSetHead = async (villager: any) => {
  try {
    await householdApi.update(currentHouseholdId.value!, { head_id: villager.id })
    currentHeadId.value = villager.id
    ElMessage.success('已将 ' + villager.name + ' 设为户主')
    fetchList()
  } catch (e) {
    ElMessage.error('设置失败')
  }
}

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

const fetchList = async () => {
  loading.value = true
  try {
    const skip = (page.value - 1) * pageSize.value
    const [data, nvs, avs] = await Promise.all([
      householdApi.getAll({ skip, limit: pageSize.value }),
      naturalVillageApi.getAll({ limit: 1000 }) as Promise<any>,
      adminVillageApi.getAll({ limit: 100 }) as Promise<any>,
    ])
    naturalVillages.value = nvs.items || []
    list.value = (data.items || []).map(h => {
      const nv = naturalVillages.value.find((n: any) => n.id === h.natural_village_id)
      const av = nv ? (avs.items || []).find((a: any) => a.id === nv.admin_village_id) : null
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

const openAdd = () => {
  isEdit.value = false
  form.value = { id: null, household_no: '', natural_village_id: null, head_id: null, address: '' }
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
        await householdApi.update(form.value.id, form.value)
        ElMessage.success('更新成功')
      } else {
        await householdApi.create(form.value)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      fetchList()
    } catch (e) {}
  })
}

const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm('确认删除该户？', '提示', { type: 'warning' })
    await householdApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchList()
  } catch (e) {}
}

const openImport = async () => {
  importDialogVisible.value = true
  const nvs = await naturalVillageApi.getAll({ limit: 1000 }) as any
  importNaturalVillages.value = nvs.items || []
}

onMounted(fetchList)
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

    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column prop="household_no" label="户号" />
      <el-table-column prop="head_name" label="户主姓名" />
      <el-table-column prop="member_count" label="户内人数" width="90" />
      <el-table-column prop="admin_village_name" label="行政村" />
      <el-table-column prop="natural_village_name" label="自然村" />
      <el-table-column prop="address" label="地址" />
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
