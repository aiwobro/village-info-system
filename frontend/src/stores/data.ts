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
      const [hhData, villagerData, assetData, resourceData] = await Promise.all([
        householdApi.getAll({ limit: 1 }) as Promise<any>,
        villagerApi.getAll({ limit: 1 }) as Promise<any>,
        assetApi.getAll({ limit: 1, search: undefined }) as Promise<any>,
        resourceApi.getAll({ limit: 1, search: undefined }) as Promise<any>,
      ])
      const [avAll, nvAll] = await Promise.all([
        adminVillageApi.getAll({ limit: 1 }) as Promise<any>,
        naturalVillageApi.getAll({ limit: 1 }) as Promise<any>,
      ])
      stats.value.adminVillages = avAll.total
      stats.value.naturalVillages = nvAll.total
      stats.value.households = hhData.total
      stats.value.villagers = villagerData.total
      stats.value.assets = assetData.total
      stats.value.resources = resourceData.total
    } catch (e) {
      console.error('Failed to fetch stats', e)
    }
  }

  return { stats, fetchStats }
})
