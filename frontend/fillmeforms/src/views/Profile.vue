<template>
  <div class="Profile">
    <h3 class='grey--text'>This is a team page</h3>
    <v-container class="pa-15">
      <v-layout row wrap>
        <v-flex xs12 sm6 md4 lg3 v-for="person in team" :key="person.name">
          <v-card color = "grey lighten-4"
          flat class="text-center ma-4">
            <v-responsive class="pt-4">
              image goes here
            </v-responsive>
            <v-card-text>
              <h3>{{ person.name }}</h3>
              <div class="grey--text">{{ person.role}}</div>
            </v-card-text>
            <v-card-actions>
              <v-btn text dark color="grey">
                <v-icon small left>mdi-message</v-icon>
                <span>Message</span>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      team: [
        { name: 'Karen Fang', role: 'Data Scientist'},
        { name: 'Patrick Ho', role: 'Product Manager'},
        { name: 'Tester A', role: 'Tester'},
        { name: 'Tester B', role: 'Tester'}
      ]
    }
  }
}

</script>
