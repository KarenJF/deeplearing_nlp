<template>
  <div class="MyForms">
    <h3 class='grey--text'>This is a projects page</h3>
    <v-container class="pa-15">
      <v-layout row wrap >
        <v-flex xs12 sm6 md4 lg3 v-for="person in team" :key="person.name">
          <v-card>Hello</v-card>
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
