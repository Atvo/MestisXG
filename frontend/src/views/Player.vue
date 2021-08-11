<template>
  <div class="about">
    <h1>Pelaaja</h1>
    <v-row align="center" justify="center">
    	<v-col class="d-flex" cols="12" sm="5">
    		<Shotmap title="Laukaukset tasakentällisin"/>
    	</v-col>
    	<v-col class="d-flex" cols="12" sm="5">
    		<Shotmap title="Laukaukset ylivoimalla"/>
    	</v-col>
    </v-row>
    <v-row align="center" justify="center">
    	<v-col class="d-flex" cols="12" sm="5">
    		<Shotmap title="Maalit tasakentällisin"/>
    	</v-col>
    	<v-col class="d-flex" cols="12" sm="5">
    		<Shotmap title="Maalit ylivoimalla"/>
    	</v-col>
    </v-row>
    <v-row align="center" justify="center">
    	<v-col class="d-flex" cols="12" sm="5">
    		<Shotmap title="Blokit tasakentällisin"/>
    	</v-col>
    	<v-col class="d-flex" cols="12" sm="5">
    		<Shotmap title="Blokit alivoimalla"/>
    	</v-col>
    </v-row>
  </div>
</template>

<script>
import Shotmap from '../components/Shotmap.vue';

export default {
  name: 'PlayerView',
  components: {
  	'Shotmap': Shotmap
  }
};
</script>