import {
  createRouter,
  createWebHistory
} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProductView from '../views/ProductView.vue'
import CategoryView from '../views/CategoryView.vue'

const routes = [{
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/products/:slug/',
    name: 'product-details',
    component: ProductView
  },
  {
    path: '/categories/:slug/',
    name: 'category-details',
    component: CategoryView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router