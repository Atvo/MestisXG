<template>
<div id="app">
  <v-app id="inspire">
    <v-navigation-drawer
      v-model="drawer"
      app
      right
    >
      <v-list dense>
        <v-list-item to="/">
          <v-list-item-action>
            <v-icon>home</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Joukkuenäkymä</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item to="/player">
          <v-list-item-action>
            <v-icon>home</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Pelaajanäkymä</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item to="/about">
          <v-list-item-action>
            <v-icon>contact_mail</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Tietoja</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar
      app
      color="cyan"
      dark
    >
      <v-spacer></v-spacer>
      <v-toolbar-title>Valikko</v-toolbar-title>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
    </v-app-bar>

    <v-content>
      <router-view/>
    </v-content>

    <v-footer
      color="cyan"
      app
    >
      <v-spacer></v-spacer>
      <span class="white--text">&copy; 2020</span>
    </v-footer>
  </v-app>
</div>
</template>

<script>

export default {
  name: 'App',

  components: {
  },

  data: () => ({
    drawer: false,
  }),
};
</script>
