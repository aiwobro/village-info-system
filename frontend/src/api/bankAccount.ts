import request from './index'

export const bankAccountApi = {
  getAll: (params?: { skip?: number; limit?: number; villager_id?: number; search?: string; natural_village_id?: number; is_locked?: number }) =>
    request.get('/bank-accounts', { params }) as Promise<{ items: any[]; total: number }>,
  getById: (id: number) => request.get(`/bank-accounts/${id}`) as Promise<any>,
  create: (data: any) => request.post('/bank-accounts', data) as Promise<any>,
  update: (id: number, data: any) => request.put(`/bank-accounts/${id}`, data) as Promise<any>,
  batchCreate: (items: any[]) => request.post("/bank-accounts/batch", { items }) as Promise<any>,
  delete: (id: number) => request.delete(`/bank-accounts/${id}`) as Promise<any>,
  lock: (id: number) => request.post(`/bank-accounts/${id}/lock`) as Promise<any>,
  unlock: (id: number) => request.post(`/bank-accounts/${id}/unlock`) as Promise<any>,
  export: (ids: number[], module: string) =>
    request.post('/export', { ids, module }, { responseType: 'blob' }) as Promise<any>,
}
