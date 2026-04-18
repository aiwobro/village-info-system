import request from './index'

export const authApi = {
  login: (username: string, password: string) =>
    request.post('/auth/login', { username, password }, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      transformRequest: [(data: any) => {
        const params = new URLSearchParams()
        params.append('username', data.username)
        params.append('password', data.password)
        return params
      }]
    }) as Promise<any>,
  register: (data: { username: string; password: string; full_name?: string }) =>
    request.post('/auth/register', data) as Promise<any>,
  getMe: () => request.get('/auth/me') as Promise<any>,
}
