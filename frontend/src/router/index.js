import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Categories',
      component: HomeView
    },
    {
      path: '/quiz/:id_category',
      name: 'Quiz',
      component: () => import('../views/QuizView.vue')
    },
    {
      path: '/add-question',
      name: 'Add question',
      component: () => import('../views/AddQuestionView.vue')
    },
    {
      path: 'Authentication/login',
      name: 'Login',
      component: () => import('../views/Authentication/LoginView.vue')
    },
    {
      path: 'Authentication/logout',
      name: 'Logout',
      component: () => import('../views/Authentication/LogoutView.vue')
    },
    {
      path: 'Authentication/Signup',
      name: 'Signup',
      component: () => import('../views/Authentication/SignUpView.vue')
    }
  ]
})

export default router
