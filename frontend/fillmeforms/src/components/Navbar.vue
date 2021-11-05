<template>
  <nav>
    <v-app-bar elevate-on-scroll app color="grey lighten-5" elevation="4" outlined>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-app-bar-title class="text-uppercase black--text">
        <span class="font-weight-light">fillme</span>
        <span>forms</span>
      </v-app-bar-title>

      <v-spacer></v-spacer>

      <v-btn text dark class="black--text">
        <span>Logout</span>
        <v-icon right>mdi-exit-to-app</v-icon>
      </v-btn>

    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app color="#9652ff">
      <v-list>
        <v-list-item v-for="link in links" :key="link.text" router :to="link.route">
          <v-list-item-action>
            <v-icon class="white--text">{{ link.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title class = "white--text">
              {{ link.text }}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>

    </v-navigation-drawer>
  </nav>
</template>

<script>
export default {
  data () {
    return {
      drawer: false,
      links: [
        { icon: 'mdi-view-dashboard', text: 'Dashboard', route: '/dashboard' },
        { icon: 'mdi-folder', text: 'My Forms', route: '/myforms' },
        { icon: 'mdi-account', text: 'Profile', route: '/profile' }
      ]
    }
  }

}
</script>