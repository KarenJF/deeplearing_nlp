<template>
  <div class="dashboard">
    <h3 class='grey--text'>Dashboard</h3>

    <v-container class="pa-15">

      <v-layout row class="mb-10 pa-3">
        <v-tooltip top>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              small
              depressed
              class="grey grey--text lighten-3 mx-2"
              v-bind="attrs"
              v-on="on"
              @click="sortBy('title')"
            >
              <v-icon left small>mdi-folder</v-icon>
              <span class="caption text-lowercase">By project name</span>
            </v-btn>
          </template>
          <span>Sort projects by project name</span>
        </v-tooltip>

        <v-tooltip top>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              small
              depressed
              class="grey grey--text lighten-3 mx-2"
              v-bine="attrs"
              v-on="on"
              @click="sortBy('person')"
            >
              <v-icon left small>mdi-account</v-icon>
              <span class="caption text-lowercase">By Person</span>
            </v-btn>
          </template>
          <span>Sort project by person</span>

        </v-tooltip>

      </v-layout>


      <v-card flat color='grey lighten-4' v-for="project in projects" :key="project.title">
        <v-layout row wrap :class="`pa-3 project ${project.status}`">
          <v-flex xs12 md6>
            <div class="caption grey--text">Project Title</div>
            <div>{{ project.title }}</div>
          </v-flex>
          <v-flex xs6 sm4 md2>
            <div class="caption grey--text">Person</div>
            <div>{{ project.person }}</div>
          </v-flex>
          <v-flex xs6 sm4 md2>
            <div class="caption grey--text">Due By</div>
            <div>{{ project.due }}</div>
          </v-flex>
          <v-flex xs2 sm2 md2>
            <div class="d-flex justify-space-around">
              <v-chip id="chip" small :class="`${project.status} white--text caption my-2`">{{ project.status }}</v-chip>
            </div>
          </v-flex>
        </v-layout>
        <v-divider class="my-3"></v-divider>
      </v-card>
    </v-container>

  </div>
</template>

<script>
export default {
  data () {
    return {
      projects: [
        { title: 'Design a new website', person: 'Karen Fang', due: '11/1/2021', status: 'ongoing' },
        { title: 'Code up the homepage', person: 'Karen Fang', due: '11/15/2021', status: 'pending' },
        { title: 'Design vedeo thumbnails', person: 'Karen Fang', due: '11/30/2021', status: 'pending' },
        { title: 'Create database', person: 'Patrick Ho', due: '11/30/2021', status: 'ongoing' },
        { title: 'Build APIs', person: 'Patrick Ho', due: '11/30/2021', status: 'complete' }
      ]
    }
  },
  methods: {
    sortBy(prop) {
      this.projects.sort((a,b) => a[prop] < b[prop] ? -1 : 1)
    }
  }

}
</script>

<style>
.project.complete {
  border-left: 4px solid #3cd1c2;
}

.project.ongoing {
  border-left: 4px solid orange;
}

.project.pending {
  border-left: 4px solid grey;
}

#chip.v-chip.complete{
  background:  #3cd1c2;
}

#chip.v-chip.ongoing {
  background: orange;
}
#chip.v-chip.pending {
  background: grey;
}

</style>
