import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/Login.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/village',
    name: 'Village',
    component: () => import('../views/Village.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/natural-village',
    name: 'NaturalVillage',
    component: () => import('../views/NaturalVillage.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/household',
    name: 'Household',
    component: () => import('../views/Household.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/villagers',
    name: 'Villagers',
    component: () => import('../views/Villagers.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('../views/Contact.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/bank',
    name: 'Bank',
    component: () => import('../views/Bank.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/assets',
    name: 'Assets',
    component: () => import('../views/Assets.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/resources',
    name: 'Resources',
    component: () => import('../views/Resources.vue'),
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.token) {
    next('/login')
  } else if (to.path === '/login' && auth.token) {
    next('/')
  } else {
    next()
  }
})

export default router
