import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSelectionStore = defineStore('selection', () => {
  // 选中 ID 集合，key 为 "module:id"
  const selected = ref<Map<string, Set<number>>>(new Map())

  /** 切换单条选中状态 */
  const toggle = (module: string, id: number) => {
    if (!selected.value.has(module)) {
      selected.value.set(module, new Set())
    }
    const set = selected.value.get(module)!
    if (set.has(id)) {
      set.delete(id)
    } else {
      set.add(id)
    }
  }

  /** 全选当前页 */
  const selectAll = (module: string, ids: number[]) => {
    if (!selected.value.has(module)) {
      selected.value.set(module, new Set())
    }
    const set = selected.value.get(module)!
    ids.forEach(id => set.add(id))
  }

  /** 取消全选当前页 */
  const deselectAll = (module: string, ids: number[]) => {
    const set = selected.value.get(module)
    if (!set) return
    ids.forEach(id => set.delete(id))
  }

  /** 清空指定模块的选择 */
  const clear = (module: string) => {
    selected.value.set(module, new Set())
  }

  /** 是否选中 */
  const isSelected = (module: string, id: number) => {
    return selected.value.get(module)?.has(id) ?? false
  }

  /** 获取模块已选中的 ID 数组 */
  const getSelectedIds = (module: string): number[] => {
    return Array.from(selected.value.get(module) ?? [])
  }

  /** 获取模块已选中的数量 */
  const count = (module: string) => {
    return selected.value.get(module)?.size ?? 0
  }

  return { selected, toggle, selectAll, deselectAll, clear, isSelected, getSelectedIds, count }
})
