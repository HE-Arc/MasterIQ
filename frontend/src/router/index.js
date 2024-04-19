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
      component: () => import('../views/CategoriesView.vue')
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
      path: '/login',
      name: 'Login',
      component: () => import('../views/Authentication/LoginView.vue')
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
