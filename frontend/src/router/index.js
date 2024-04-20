import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView
    },
    {
      path: '/categories',
      name: 'Categories',
      meta: {
        requiresAuth: true
      },
      component: () => import('../views/CategoriesView.vue')
    },
    {
      path: '/quiz/:id_category',
      name: 'Quiz',
      meta: {
        requiresAuth: true
      },
      component: () => import('../views/QuizView.vue')
    },
    {
      path: '/add-question',
      name: 'Add question',
      meta: {
        requiresAuth: true
      },
      component: () => import('../views/AddQuestionView.vue')
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/Authentication/LoginView.vue')
    },
    {
      path: '/logout',
      name: 'Logout',
      component: () => import('../views/Authentication/LogoutView.vue')
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('../views/Authentication/RegisterView.vue')
    },
    // path for unknown urls
    {
      path: '/:pathMatch(.*)',
      name: 'NotFound',
      component: () => import('../views/NotFoundView.vue')
    }
  ]
})

export default router
