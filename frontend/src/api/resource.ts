import request from './index'

export const resourceApi = {
  getAll: (params?: { skip?: number; limit?: number; search?: string; natural_village_id?: number; is_locked?: number }) =>
    request.get('/resources', { params }) as Promise<{ items: any[]; total: number }>,
  getById: (id: number) => request.get(`/resources/${id}`) as Promise<any>,
  create: (data: any) => request.post('/resources', data) as Promise<any>,
  update: (id: number, data: any) => request.put(`/resources/${id}`, data) as Promise<any>,
  batchCreate: (items: any[]) => request.post("/resources/batch", { items }) as Promise<any>,
  delete: (id: number) => request.delete(`/resources/${id}`) as Promise<any>,
  lock: (id: number) => request.post(`/resources/${id}/lock`) as Promise<any>,
  unlock: (id: number) => request.post(`/resources/${id}/unlock`) as Promise<any>,
  export: (ids: number[], module: string) =>
    request.post('/export', { ids, module }, { responseType: 'blob' }) as Promise<any>,
}
