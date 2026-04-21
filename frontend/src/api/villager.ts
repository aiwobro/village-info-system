import request from './index'

export const villagerApi = {
  getAll: (params?: { skip?: number; limit?: number; search?: string; household_id?: number; natural_village_id?: number }) =>
    request.get('/villagers', { params }) as Promise<{ items: any[]; total: number }>,
  getById: (id: number) => request.get(`/villagers/${id}`) as Promise<any>,
  create: (data: any) => request.post('/villagers', data) as Promise<any>,
  update: (id: number, data: any) => request.put(`/villagers/${id}`, data) as Promise<any>,
  batchCreate: (items: any[]) => request.post("/villagers/batch", { items }) as Promise<any>,
  delete: (id: number) => request.delete(`/villagers/${id}`) as Promise<any>,
  lock: (id: number) => request.post(`/villagers/${id}/lock`) as Promise<any>,
  unlock: (id: number) => request.post(`/villagers/${id}/unlock`) as Promise<any>,
  export: (ids: number[], module: string) =>
    request.post('/export', { ids, module }, { responseType: 'blob' }) as Promise<any>,
}
