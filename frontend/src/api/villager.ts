import request from './index'

export const villagerApi = {
  getAll: (params?: { skip?: number; limit?: number; search?: string; household_id?: number }) =>
    request.get('/villagers', { params }) as Promise<{ items: any[]; total: number }>,
  getById: (id: number) => request.get(`/villagers/${id}`) as Promise<any>,
  create: (data: any) => request.post('/villagers', data) as Promise<any>,
  update: (id: number, data: any) => request.put(`/villagers/${id}`, data) as Promise<any>,
  delete: (id: number) => request.delete(`/villagers/${id}`) as Promise<any>,
}
