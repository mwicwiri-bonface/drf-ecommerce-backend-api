<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>MaliSafi</strong></router-link>
        <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu"
          @click="showMobileMenu = !showMobileMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>
      <div class="navbar-menu" id="navbar-menu" v-bind:class="{ 'is-active': showMobileMenu }">

        <div class="navbar-start">
          <div class="navbar-item">
            <Search />
          </div>
        </div>

        <div class="navbar-end">
          <router-link v-bind:to="'/categories/' + category.slug + '/'" class="navbar-item"
            v-for="category in categories" v-bind:key="category.slug">
            {{ category.name }}
          </router-link>
          <div class="navbar-item">
            <div class="buttons">
              <template v-if="$store.state.isAuthenticated">
                <router-link to="/my-account" class="button is-light">My Account</router-link>
              </template>
              <template v-else>
                <router-link to="/log-in" class="button is-light">Login</router-link>
              </template>
              <router-link to="/cart" class="button is-success">
                <span class="icon"><i class="fa fa-shopping-cart" aria-hidden="true"></i></span>
                <span>Cart ({{ cartTotalLength }})</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <div class="is-loading-bar has-text-centered" :class="{ 'is-loading': $store.state.isLoading }">
      <div class="lds-dual-ring"></div>
    </div>

    <section class="section">
      <router-view />
    </section>

    <footer class="footer">
      <p class="has-text-centered"><i class="fa fa-copyright" aria-hidden="true"></i> 2022</p>
    </footer>
  </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
import Search from './views/SearchFunctionality.vue'

export default {
  components: {
    Search
  },
  data() {
    return {
      showMobileMenu: false,
      cart: {
        items: []
      },
      categories: []
    }
  },
  beforeCreate() {
    this.$store.commit('initializeStore')
    const token = this.$store.state.token
    if (token) {
      axios.defaults.headers.common['Authorization'] = 'Token ' + token
    } else {
      axios.defaults.headers.common['Authorization'] = ''
    }
  },
  mounted() {
    this.cart = this.$store.state.cart
    this.getCategories()
  },
  methods: {
    async getCategories() {
      this.$store.commit('setIsLoading', true)

      await axios
        .get('/api/v1/categories/')
        .then(response => {
          this.categories = response.data
        })
        .catch(error => {
          console.log(error)
          toast({
            message: 'Something went wrong, please try again',
            type: 'is-danger',
            dismissible: true,
            pauseOnHover: true,
            duration: 2000,
            position: 'bottom-right',
          })
        })
      this.$store.commit('setIsLoading', false)
    },
  },
  computed: {
    cartTotalLength() {
      let totalLength = 0

      for (let i = 0; i < this.cart.items.length; i++) {
        totalLength += this.cart.items[i].quantity
      }

      return totalLength
    },
  },
}
</script>
<style lang="scss">
@import '../node_modules/bulma';

.lds-dual-ring {
  display: inline-block;
  width: 80px;
  height: 80px;
}

.lds-dual-ring::after {
  content: "";
  display: block;
  width: 64px;
  height: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid #ccc;
  border-color: #ccc transparent #ccc transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}

@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.is-loading-bar {
  height: 0;
  overflow: hidden;
  -webkit-transition: all 0.3s;
  transition: all 0.3s;

  &.is-loading {
    height: 80px;
  }
}
</style>
