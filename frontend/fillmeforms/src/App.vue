<template>
  <v-app class="grey darken-2">
    <Navbar />

    <v-main >
    <v-divider></v-divider>
      <router-view class="mx-4 mb-4"/>
    </v-main>
  </v-app>
</template>

<script>
import Navbar from './components/Navbar.vue';

export default {
  name: 'App',
  components: { Navbar },

  data: () => ({
    //
  })

};
</script>
