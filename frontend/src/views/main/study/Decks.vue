<template>
  <div>
    <Onboard></Onboard>
    <v-toolbar style="position: sticky; top: 0; z-index: 10;">
      <v-toolbar-title>
        Decks
      </v-toolbar-title>
      <v-spacer class="hidden-xs-only"></v-spacer>

      <v-card-actions class="px-0 px-sm-auto">
        <v-btn v-show="!checkAllDecks()" @click="deleteDecks">Delete</v-btn>
        <v-btn to="/main/add/deck">Add Deck</v-btn>
        <v-btn v-if="checkAllDecks()" to="/main/study/learn">Study All</v-btn>
        <v-btn v-else color="primary" @click="openDecks()"
          >Study<span class="hidden-xs-only"> Selected</span></v-btn
        >
      </v-card-actions>
    </v-toolbar>
    <v-data-table
      v-model="selected"
      :headers="headers"
      item-key="id"
      :items="decks"
      :items-per-page="15"
      show-select
      :style="{ cursor: 'pointer' }"
      @click:row="openDeck"
    >
    </v-data-table>
  </div>
</template>

<script lang="ts">
  import { Component, Vue } from "vue-property-decorator";
  import { mainStore } from "@/utils/store-accessor";
  import { IComponents } from "@/interfaces";
  import Onboard from "@/views/Onboard.vue";

  @Component({
    components: { Onboard },
  })
  export default class Decks extends Vue {
    public headers = [
      {
        text: "Deck",
        sortable: true,
        value: "title",
        align: "left",
      },
    ];
    selected: IComponents["Deck"][] = [];

    async mounted() {
      await mainStore.getUserProfile();
    }

    get decks() {
      const userProfile = mainStore.userProfile;
      return userProfile && userProfile.decks ? userProfile.decks : [];
    }

    public checkAllDecks() {
      return this.selected.length == 0 || this.selected.length == this.decks.length;
    }

    public openDecks() {
      // Vue router takes in arrays only as strings
      const selectedIds = this.selected.map((a) => String(a.id));
      this.$router.push({
        path: "/main/study/learn",
        query: { deck: selectedIds },
      });
    }

    public openDeck(deck) {
      this.$router.push({
        path: "/main/study/learn",
        query: { deck: String(deck.id) },
      });
    }

    public async deleteDecks() {
      const selectedIds = this.selected.map((a) => a.id);
      if (selectedIds.length > 0) {
        await mainStore.deleteDecks({ ids: selectedIds });
        this.selected = [];
        await mainStore.getUserProfile();
      }
    }
  }
</script>
