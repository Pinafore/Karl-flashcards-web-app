<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <v-card class="ma-3 pa-3">
          <v-card-title>
            <h2>Contact Us</h2>
          </v-card-title>
          <v-card-text>
            Do you have bugs to report or comments for the developers? Join the official
            KAR³L Discord, comment on our quizbowl forum post, or contact us through
            email!
          </v-card-text>
          <v-card-actions class="pt-0">
            <v-row>
              <v-spacer></v-spacer>
              <v-btn color="primary" text href="https://discord.gg/PTfEmHd">
                Join Discord </v-btn
              ><v-spacer></v-spacer>
              <v-btn
                color="primary"
                text
                href="https://hsquizbowl.org/forums/viewtopic.php?f=123&p=379140&sid=1edf62c02b590220bc42d0104791bca6#p379140"
              >
                Forum Post
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn color="primary" text href="mailto:learningwithkarl@gmail.com">
                Email Us
              </v-btn>
              <v-spacer></v-spacer>
            </v-row>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
  import { Component, Vue } from "vue-property-decorator";

  @Component
  export default class Contact extends Vue {}
</script>

<style></style>
