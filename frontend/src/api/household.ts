import request from './index'

export const householdApi = {
  getAll: (params?: { skip?: number; limit?: number; natural_village_id?: number; admin_village_id?: number }) =>
    request.get('/households', { params }) as Promise<{ items: any[]; total: number }>,
  getStats: (params?: { natural_village_id?: number; admin_village_id?: number }) =>
    request.get('/households/stats', { params }) as Promise<{ household_count: number; villager_count: number }>,
  getById: (id: number) => request.get(`/households/${id}`) as Promise<any>,
  create: (data: any) => request.post('/households', data) as Promise<any>,
  update: (id: number, data: any) => request.put(`/households/${id}`, data) as Promise<any>,
  delete: (id: number) => request.delete(`/households/${id}`) as Promise<any>,
}
