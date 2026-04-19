import request from './index'

export const adminVillageApi = {
  getAll: (params?: { skip?: number; limit?: number }) =>
    request.get('/admin-villages', { params }) as Promise<any[]>,
  getById: (id: number) => request.get(`/admin-villages/${id}`) as Promise<any>,
  create: (data: any) => request.post('/admin-villages', data) as Promise<any>,
  update: (id: number, data: any) => request.put(`/admin-villages/${id}`, data) as Promise<any>,
  delete: (id: number) => request.delete(`/admin-villages/${id}`) as Promise<any>,
}
