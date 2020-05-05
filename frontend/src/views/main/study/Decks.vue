<template>
  <div>
    <v-toolbar>
      <v-toolbar-title>
        Decks
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn to="/main/add/deck">Add New Deck</v-btn>
      <v-card-actions>
        <v-btn v-if="checkAllDecks()" to="/main/study/learn">Study All</v-btn>
        <v-btn v-else color="primary" @click="openDecks()">Study Selected</v-btn>
      </v-card-actions>
    </v-toolbar>
    <v-data-table
      v-model="selected"
      :headers="headers"
      item-key="id"
      :items="decks"
      show-select
      hide-default-footer
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

  @Component
  export default class Decks extends Vue {
    public headers = [
      {
        text: "Deck",
        sortable: false,
        value: "title",
        align: "left",
      },
    ];
    selected: IComponents["Deck"][] = [];

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
      this.$router.push({ path: "/main/study/learn", query: { deck: deck.id } });
    }
  }
</script>