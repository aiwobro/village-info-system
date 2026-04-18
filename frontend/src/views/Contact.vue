<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { contactApi } from '../api/contact'
import { ElMessage, ElMessageBox } from 'element-plus'

const list = ref<any[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()

const form = ref({
  id: null as number | null,
  villager_id: null as number | null,
  phone: '',
  backup_phone: '',
  wechat: '',
  qq: '',
  email: '',
  emergency_contact: '',
  emergency_phone: '',
  remark: '',
})

const rules = {
  villager_id: [{ required: true, message: '请选择关联村民', trigger: 'change' }],
}

const fetchList = async () => {
  loading.value = true
  try {
    list.value = await contactApi.getAll({ limit: 100 }) as any[]
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const openAdd = () => {
  isEdit.value = false
  form.value = { id: null, villager_id: null, phone: '', backup_phone: '', wechat: '', qq: '', email: '', emergency_contact: '', emergency_phone: '', remark: '' }
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
  try {
    await ElMessageBox.confirm('确认删除？', '提示', { type: 'warning' })
    await contactApi.delete(id)
    ElMessage.success('删除成功')
    fetchList()
  } catch (e) {}
}

onMounted(fetchList)
</script>

<template>
  <div class="page">
    <div class="toolbar">
      <h2>📞 联系方式</h2>
      <el-button type="primary" @click="openAdd">新增联系方式</el-button>
    </div>

    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column prop="villager_id" label="村民ID" width="100" />
      <el-table-column prop="phone" label="手机号" />
      <el-table-column prop="backup_phone" label="备用电话" />
      <el-table-column prop="wechat" label="微信" />
      <el-table-column prop="qq" label="QQ" />
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="emergency_contact" label="紧急联系人" />
      <el-table-column prop="emergency_phone" label="紧急联系人电话" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" @click="openEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑联系方式' : '新增联系方式'" width="600px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
        <el-form-item label="村民ID" prop="villager_id">
          <el-input-number v-model="form.villager_id" :min="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="备用电话">
          <el-input v-model="form.backup_phone" />
        </el-form-item>
        <el-form-item label="微信号">
          <el-input v-model="form.wechat" />
        </el-form-item>
        <el-form-item label="QQ号">
          <el-input v-model="form.qq" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="紧急联系人">
          <el-input v-model="form.emergency_contact" />
        </el-form-item>
        <el-form-item label="紧急联系人电话">
          <el-input v-model="form.emergency_phone" />
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
</style>
