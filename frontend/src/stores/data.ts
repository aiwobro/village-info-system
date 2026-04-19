import { defineStore } from 'pinia'
import { ref } from 'vue'
import { adminVillageApi } from '../api/adminVillage'
import { naturalVillageApi } from '../api/naturalVillage'
import { householdApi } from '../api/household'
import { villagerApi } from '../api/villager'
import { assetApi } from '../api/asset'
import { resourceApi } from '../api/resource'

export const useDataStore = defineStore('data', () => {
  const stats = ref({
    adminVillages: 0,
    naturalVillages: 0,
    households: 0,
    villagers: 0,
    assets: 0,
    resources: 0,
  })

  const fetchStats = async () => {
    try {
      const [vCount, aCount, rCount] = await Promise.all([
        villagerApi.getCount(),
        assetApi.getCount(),
        resourceApi.getCount(),
      ])
      // 获取总数需要单独查
      const [avAll, nvAll, hhAll] = await Promise.all([
        adminVillageApi.getAll({ limit: 1000 }) as Promise<any[]>,
        naturalVillageApi.getAll({ limit: 1000 }) as Promise<any[]>,
        householdApi.getAll({ limit: 1000 }) as Promise<any[]>,
      ])
      stats.value.adminVillages = avAll.length
      stats.value.naturalVillages = nvAll.length
      stats.value.households = hhAll.length
      stats.value.villagers = (vCount as any).count
      stats.value.assets = (aCount as any).count
      stats.value.resources = (rCount as any).count
    } catch (e) {
      console.error('Failed to fetch stats', e)
    }
  }

  return { stats, fetchStats }
})
