import {
  createRouter,
  createWebHistory
} from 'vue-router'
import store from '../store'
import HomeView from '../views/HomeView.vue'
import ProductView from '../views/ProductView.vue'
import CategoryView from '../views/CategoryView.vue'
import SearchView from '../views/SearchView.vue'
import CartView from '../views/CartView.vue'
import SignUp from '../views/SignUp.vue'
import LogIn from '../views/LogIn.vue'
import MyAccount from '../views/MyAccount.vue'
import CheckoutView from '../views/CheckoutView.vue'
import SuccessView from '../views/SuccessView.vue'

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
  },
  {
    path: '/search',
    name: 'SearchView',
    component: SearchView
  },
  {
    path: '/cart',
    name: 'cart',
    component: CartView
  },
  {
    path: '/sign-up',
    name: 'sign-up',
    component: SignUp
  },
  {
    path: '/log-in',
    name: 'LogIn',
    component: LogIn
  },
  {
    path: '/my-account',
    name: 'MyAccount',
    component: MyAccount,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/checkout/',
    name: 'checkout',
    component: CheckoutView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/success/',
    name: 'success',
    component: SuccessView,
    meta: {
      requireLogin: true
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next({
      name: 'LogIn',
      query: {
        to: to.path
      }
    })
  } else {
    next()
  }
})

export default router