import request from './index'

export const bankAccountApi = {
  getAll: (params?: { skip?: number; limit?: number; villager_id?: number }) =>
    request.get('/bank-accounts', { params }) as Promise<any[]>,
  getById: (id: number) => request.get(`/bank-accounts/${id}`) as Promise<any>,
  create: (data: any) => request.post('/bank-accounts', data) as Promise<any>,
  update: (id: number, data: any) => request.put(`/bank-accounts/${id}`, data) as Promise<any>,
  delete: (id: number) => request.delete(`/bank-accounts/${id}`) as Promise<any>,
}
