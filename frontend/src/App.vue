<template>
  <div id="app">
    <v-app>
      <v-main v-if="loggedIn === null">
        <v-container class="fill-height">
          <v-row align="center" justify="center">
            <v-col>
              <div class="text-center">
                <div class="headline my-5">Loading...</div>
                <v-progress-circular
                  size="100"
                  indeterminate
                  color="primary"
                ></v-progress-circular>
              </div>
            </v-col>
          </v-row>
        </v-container>
      </v-main>
      <router-view v-else />
      <NotificationsManager></NotificationsManager>
      <ConnectionError></ConnectionError>
      <UpdateAvailable></UpdateAvailable>
    </v-app>
  </div>
</template>

<script lang="ts">
  import { Component, Vue } from "vue-property-decorator";
  import NotificationsManager from "@/components/NotificationsManager.vue";
  import { mainStore } from "@/store";
  import ConnectionError from "@/components/ConnectionError.vue";
  import UpdateAvailable from "@/components/UpdateAvailable.vue";

  @Component({
    components: {
      UpdateAvailable,
      NotificationsManager,
      ConnectionError,
    },
  })
  export default class App extends Vue {
    get loggedIn() {
      return mainStore.isLoggedIn;
    }

    public async created() {
      await mainStore.checkLoggedIn();
    }

    public async mounted() {
      setInterval(this.checkForUpdate, 1000);
    }

    checkForUpdate() {
      if (navigator.serviceWorker !== undefined) {
        navigator.serviceWorker.ready.then((reg) => {
          if (reg.installing === null) {
            console.log("checking for update");
            reg.update().catch();
          } else {
            console.log("installing");
          }
        });
      }
    }
  }
</script>
