import request from './index'

export const naturalVillageApi = {
  getAll: (params?: { skip?: number; limit?: number; admin_village_id?: number }) =>
    request.get('/natural-villages', { params }) as Promise<any[]>,
  getById: (id: number) => request.get(`/natural-villages/${id}`) as Promise<any>,
  create: (data: any) => request.post('/natural-villages', data) as Promise<any>,
  update: (id: number, data: any) => request.put(`/natural-villages/${id}`, data) as Promise<any>,
  delete: (id: number) => request.delete(`/natural-villages/${id}`) as Promise<any>,
}
