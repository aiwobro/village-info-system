import request from './index'

export const contactApi = {
  getAll: (params?: { skip?: number; limit?: number; villager_id?: number; search?: string; natural_village_id?: number }) =>
    request.get('/contacts', { params }) as Promise<{ items: any[]; total: number }>,
  getById: (id: number) => request.get(`/contacts/${id}`) as Promise<any>,
  create: (data: any) => request.post('/contacts', data) as Promise<any>,
  update: (id: number, data: any) => request.put(`/contacts/${id}`, data) as Promise<any>,
  batchCreate: (items: any[]) => request.post("/contacts/batch", { items }) as Promise<any>,
  delete: (id: number) => request.delete(`/contacts/${id}`) as Promise<any>,
  lock: (id: number) => request.post(`/contacts/${id}/lock`) as Promise<any>,
  unlock: (id: number) => request.post(`/contacts/${id}/unlock`) as Promise<any>,
  export: (ids: number[], module: string) =>
    request.post('/export', { ids, module }, { responseType: 'blob' }) as Promise<any>,
}
