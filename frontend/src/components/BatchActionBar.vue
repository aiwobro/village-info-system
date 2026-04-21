<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  count: number
  module: string
  lockedCount?: number  // 选中的锁定记录数
}>()

const emit = defineEmits<{
  view: []
  edit: []
  delete: []
  lock: []
  unlock: []
  export: []
}>()

// 全部选中项都是锁定状态时，禁用解锁按钮
const allLocked = computed(() => {
  // lockedCount 有值且等于 count 时，全部是锁定的
  return props.lockedCount !== undefined && props.count > 0 && props.lockedCount === props.count
})

// 全部选中项都是非锁定状态时，禁用锁定按钮
const allUnlocked = computed(() => {
  return props.lockedCount !== undefined && props.count > 0 && props.lockedCount === 0
})
</script>

<template>
  <Teleport to="body">
    <div v-if="count > 0" class="batch-action-bar">
      <span class="batch-action-bar__count">{{ count }} 条已选</span>

      <el-button @click="emit('view')">
        <el-icon style="margin-right: 4px"><View /></el-icon>
        查看
      </el-button>

      <el-button @click="emit('edit')">
        <el-icon style="margin-right: 4px"><Edit /></el-icon>
        编辑
      </el-button>

      <el-button type="danger" @click="emit('delete')">
        <el-icon style="margin-right: 4px"><Delete /></el-icon>
        删除
      </el-button>

      <div style="width: 1px; height: 20px; background: rgba(255,255,255,0.2); margin: 0 4px;" />

      <el-button :disabled="allLocked" @click="emit('lock')">
        <el-icon style="margin-right: 4px"><Lock /></el-icon>
        锁定
      </el-button>

      <el-button :disabled="allUnlocked" @click="emit('unlock')">
        <el-icon style="margin-right: 4px"><Unlock /></el-icon>
        解锁
      </el-button>

      <div style="width: 1px; height: 20px; background: rgba(255,255,255,0.2); margin: 0 4px;" />

      <el-button @click="emit('export')">
        <el-icon style="margin-right: 4px"><Download /></el-icon>
        导出
      </el-button>
    </div>
  </Teleport>
</template>

<script lang="ts">
import { View, Edit, Delete, Lock, Unlock, Download } from '@element-plus/icons-vue'
export default {
  components: { View, Edit, Delete, Lock, Unlock, Download }
}
</script>
