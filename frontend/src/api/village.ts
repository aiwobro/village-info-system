import request from './index'

export const villageApi = {
  getAll: (params?: { skip?: number; limit?: number }) =>
    request.get('/villages', { params }) as Promise<any[]>,
  getById: (id: number) => request.get(`/villages/${id}`) as Promise<any>,
  create: (data: any) => request.post('/villages', data) as Promise<any>,
  update: (id: number, data: any) => request.put(`/villages/${id}`, data) as Promise<any>,
  delete: (id: number) => request.delete(`/villages/${id}`) as Promise<any>,
}
