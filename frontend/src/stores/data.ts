import { defineStore } from 'pinia'
import { ref } from 'vue'
import { villageApi } from '../api/village'
import { villagerApi } from '../api/villager'
import { assetApi } from '../api/asset'
import { resourceApi } from '../api/resource'

export const useDataStore = defineStore('data', () => {
  const stats = ref({
    villagers: 0,
    assets: 0,
    resources: 0,
    villages: 0,
  })

  const fetchStats = async () => {
    try {
      const [vCount, aCount, rCount, vData] = await Promise.all([
        villagerApi.getCount(),
        assetApi.getCount(),
        resourceApi.getCount(),
        villageApi.getAll({ limit: 100 }),
      ])
      stats.value.villagers = (vCount as any).count
      stats.value.assets = (aCount as any).count
      stats.value.resources = (rCount as any).count
      stats.value.villages = ((vData as any)).length
    } catch (e) {
      console.error('Failed to fetch stats', e)
    }
  }

  return { stats, fetchStats }
})
