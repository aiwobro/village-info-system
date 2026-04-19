import request from './index'

export const assetApi = {
  getAll: (params?: { skip?: number; limit?: number; search?: string }) =>
    request.get('/assets', { params }) as Promise<{ items: any[]; total: number }>,
  getById: (id: number) => request.get(`/assets/${id}`) as Promise<any>,
  create: (data: any) => request.post('/assets', data) as Promise<any>,
  update: (id: number, data: any) => request.put(`/assets/${id}`, data) as Promise<any>,
  batchCreate: (items: any[]) => request.post("/assets/batch", { items }) as Promise<any>,
  delete: (id: number) => request.delete(`/assets/${id}`) as Promise<any>,
}
