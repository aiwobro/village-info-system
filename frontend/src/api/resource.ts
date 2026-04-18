import request from './index'

export const resourceApi = {
  getAll: (params?: { skip?: number; limit?: number; search?: string }) =>
    request.get('/resources', { params }) as Promise<any[]>,
  getCount: (search?: string) => request.get('/resources/count', { params: { search } }) as Promise<any>,
  getById: (id: number) => request.get(`/resources/${id}`) as Promise<any>,
  create: (data: any) => request.post('/resources', data) as Promise<any>,
  update: (id: number, data: any) => request.put(`/resources/${id}`, data) as Promise<any>,
  delete: (id: number) => request.delete(`/resources/${id}`) as Promise<any>,
}
