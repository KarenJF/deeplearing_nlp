<template>
  <div class="home">
    <!--Example of text and size-->
    <h3 class='grey--text'>This is Homepage</h3>
    <p class="red white--text">
      Lorem ipsum dolor sit amet consectetur adipisicing elit. Rerum quam, non aliquam quas harum, sint placeat atque blanditiis qui inventore culpa. Omnis magni dignissimos voluptates quam iste sint facilis hic?
    </p>

    <p class="pink lighten-4 red--text text--darken-4">Lorem ipsum dolor sit amet consectetur, adipisicing elit. Provident fuga excepturi, facere magnam atque inventore, eius officia aliquid vel ratione omnis, porro commodi non impedit aliquam quo maxime eligendi est?</p>

    <h1 class="display-4 text-capitalize">massive Display</h1>
    <h4 class="display-1">small Display</h4>
    <p class="headline">This is a headline</p>
    <p class="subheading font-weight-bold">this is a subheading</p>
    <p class="cap">this is a caption</p>

    <!--Example of button and Icons-->
    <v-btn class="pink white--text">click me</v-btn>
    <v-btn dark depressed color="pink">click me again</v-btn>
    <v-btn plain :disabled="loading" color="pink">click me</v-btn>

    <v-btn depressed class="pink white--text mx-2">
      <v-icon left >mdi-email</v-icon>
      <span>Email Me</span>
    </v-btn>

    <v-btn depressed small class="pink white--text mx-2" >
      <v-icon left >mdi-email</v-icon>
      <span>Email Me</span>
    </v-btn>

    <v-btn depressed class="pink white--text mx-2">
      <v-icon left small >mdi-email</v-icon>
      <span>Email Me</span>
    </v-btn>

    <v-btn depressed large class="pink white--text mx-2">
      <span>Email Me</span>
      <v-icon right large >mdi-email</v-icon>
    </v-btn>

    <v-btn depressed small dark fab color="purple">
      <v-icon>mdi-heart</v-icon>
    </v-btn>

    <h1>Talk about breakpoints</h1>
    <v-btn class="d-none d-md-block">hide on screen smaller than md</v-btn>
    <v-btn class="d-md-none ">hide on screen wider than md</v-btn>
    <v-btn class="d-none d-sm-flex">hide on small screen only </v-btn>

  </div>

</template>

<script>

  export default {

  }
</script>
