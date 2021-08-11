<template>
  <div>
    <h1>Joukkuenäkymä</h1>
    <v-row align="center">
      <v-col class="d-flex" cols="12" sm="3">
        <v-select
          :items=seriesList
          v-on:change="seriesChanged"
          label="Sarja"
        ></v-select>
      </v-col>
      <v-col class="d-flex" cols="12" sm="3">
        <v-select
          :items=seasonList
          v-on:change="seasonChanged"
          label="Kausi"
        ></v-select>
      </v-col>
      <v-col class="d-flex" cols="12" sm="3">
        <v-select
          :items=teams
          :disabled="teams.length == 0"
          v-on:change="teamChanged"
          label="Joukkue"
        ></v-select>
      </v-col>
      <v-col class="d-flex" cols="12" sm="3">
        <v-select
          :items=outcomeList
          :disabled="teams.length == 0"
          v-on:change="outcomeChanged"
          label="Tapahtuma"
        ></v-select>
      </v-col>
    </v-row>
    <div id="shotmap_container">
      <img id="shotmap_img" class="shotmap_layer" alt="Vue logo" src="../assets/rink.png"/>
      <canvas id="shotmap_canvas" class="shotmap_layer" width="1262" height="633"></canvas>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import * as Heatimage from 'heatimage';
import simpleheat from 'simpleheat';

export default {
  data() {
    return {
      shots: [],
      teams: [],
      seriesList: ["Mestis", "Nuorten SM-Liiga"],
      seasonList: ["2019-2020", "2018-2019"],
      outcomeList: ["Kaikki", "Maalit", "Torjunnat", "Peitetyt", "Ohilaukaukset"],
      outcome: "Kaikki",
      series: null,
      season: null,
      team: null,
    };
  },
  methods: {
    getShots(team, outcome) {
      console.log(this.$data);
      console.log(team);
      console.log(outcome);
      if (this.$data.series == null || this.$data.season == null) {
        return;
      }
      const path = 'http://localhost:5000/shots/team';
      /*if (team === undefined) {
        const path = 'http://localhost:5000/shots';
      }
      else {
        const path = 'http://localhost:5000/shots';
      }*/
      axios.get(path, {
        params: {
          team: team,
          outcome: outcome,
        }
      })
        .then((res) => {
          const shotList = res.data.shots;
          this.shots = [];
          shotList.forEach((shotStr) => {
            this.shots.push(JSON.parse(shotStr));
          });
          this.initHeatmap();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getTeams() {
      if (this.$data.series == null || this.$data.season == null) {
        return;
      }
      console.log(this.$data);
      const path = 'http://localhost:5000/teams';
      axios.get(path)
        .then((res) => {
          this.teams = res.data.teams;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    seriesChanged(series) {
      console.log(series);
      this.series = series;
      this.getTeams();
    },
    seasonChanged(season) {
      console.log(season);
      this.season = season;
      this.getTeams();
    },
    teamChanged(team) {
      console.log(team);
      this.team = team;
      this.getShots(team, this.$data.outcome);
    },
    outcomeChanged(outcome) {
      console.log(outcome);
      this.outcome = outcome;
      this.getShots(this.$data.team, outcome);
    },
    initHeatmap() {
      const element = document.querySelector('#shotmap_img');
      console.log(element);
      let heatData = this.createHeatData(element.height, element.width);
      console.log(heatData);
      let heat = simpleheat('shotmap_canvas').data(heatData);
      heat.radius(15, 25);
      heat.max(heatData.length/400);
      console.log(heat);
      heat.draw();
      console.log(heat);
      /*let heatOptions = {
        heatValue: 0.05,
        heatRadius: 15,
        heatBlur: 25,
        colorGradient: 'Visible Spectrum',
        exporting: false,
        edit: false,
        keys: false,
        visibleCanvas: true,
        defaultData: heatData,
      };
      Heatimage.heatimage(element, heatOptions);*/
    },
    createHeatData(canvasHeight, canvasWidth) {
      const heatData = [];
      this.$data.shots.forEach((shot) => {
        /*heatData.push({
          x: (shot['ShotX'] * canvasWidth / 1024),
          y: (shot['ShotY'] * canvasHeight / 514),
          value: 1,
        });*/
        let x = shot['ShotX'] * canvasWidth / 1024;
        let y = shot['ShotY'] * canvasHeight / 514;
        heatData.push([x, y, 1]);
      });
      return heatData;
    },
  },
  created() {
    //this.getSeries();
    //this.getSeasons();
    // this.getShots();
    // this.getTeams();
  },
  mounted() {
    //this.initHeatmap();
  },
  updated() {
    /*this.getTeams();
    this.getShots();
    this.initHeatmap();*/
  },
  name: 'Shotmap',
};
</script>

<style>
  #shotmap_container{
    display: grid;
  }
  .shotmap_layer{
    grid-column: 1;
    grid-row: 1;
  }
  /*canvas {
    display: inline-block !important;
  }*/
</style>
