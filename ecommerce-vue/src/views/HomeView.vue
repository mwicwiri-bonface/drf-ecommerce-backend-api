<template>
  <section class="hero is-medium is-dark mb-6">
    <div class="hero-body has-text-centered">
      <p class="title mb-6">
        Welcome to Djacket
      </p>
      <p class="subtitle">
        The Jacket Store Online
      </p>
    </div>
  </section>
  <div class="columns is-multiline">
    <div class="column is-12">
      <h2 class="is-size-2 has-text-centered"> Latests Products</h2>
    </div>
    <ProductBox v-for="product in latestProducts" :key="product.id" :product="product" />
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios'
import ProductBox from '@/components/ProductBox.vue'

export default {
  name: 'HomeView',
  data() {
    return {
      latestProducts: []
    }
  },
  components: {
    ProductBox
  },
  mounted() {
    this.getLatestProducts()

    document.title = 'Home | Djackets'
  },
  methods: {
    async getLatestProducts() {
      this.$store.commit('setIsLoading', true)


      await axios
        .get('/api/products/')
        .then(response => {
          let data = response.data
          this.latestProducts = data['results']
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
    }
  }

}
</script>

