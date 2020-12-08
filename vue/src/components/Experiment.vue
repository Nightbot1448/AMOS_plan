<template>
  <div>
  <div id="alerts"></div>
  <div id="factor_points">
  <div id="experiment_0">
      <h3>Опыт 1</h3>
      <p>
        <input type="number" v-model.number="factor_points[0][0]" />
        <input type="number" v-model.number="factor_points[0][1]" />
        <button id="button_0" @click="send_factor_point(0)">Сохранить</button> {{ answer }}
        <p>Результат: {{y_vals[0]}}</p>
      </p>
    </div>
    <div id="experiment_1" style="display: none">
      <h3>Опыт 2</h3>
      <p>
        <input type="number" v-model.number="factor_points[1][0]" />
        <input type="number" v-model.number="factor_points[1][1]" />
        <button id="button_1" @click="send_factor_point(1)">Сохранить</button> {{ answer }}
        <p>
          Результат: {{y_vals[1]}}
        </p>
      </p>
    </div>
  </div>
    <div>
      <p id="text" style="display: none">Дальше эксперимент выполняется в автоматическом режиме.</p>
      <button @click="show_results()">Показать результаты</button>
    </div>
    <div id="results" style="display: none">
      <table border="2">
      <thead>
      <tr>
      <th rowspan="2">Точка ФП</th>
      <th :colspan="y_vals[0].length" align="center">Параллельные опыты</th>
      </tr>
      <tr>
      <th v-for="(n, j) in y_vals[0].length" :key="j"> {{ j+1 }}</th>
      </tr>
      </thead>
      <tbody>
        <tr v-for="(n, i) in y_vals.length" :key="i">
          <td>{{ i+1 }}</td>
          <td v-for="(n, j) in y_vals[0].length" :key="j">
            {{ Number(y_vals[i][j].toFixed(2)) }}
          </td>
        </tr>
      </tbody>
      </table>
    </div>
    <router-link class="nav-link" to="/planning">Далее</router-link>
  </div>
</template>

<script>
import axios from "axios";
export default {
  mounted() {
    console.log(this.$store.state.experiments_data)
    if (this.$store.state.experiments_data != undefined){
      this.number_of_saved_points = this.$store.state.experiments_data;
      
    }
    if (this.number_of_saved_points >= 2){
      document.getElementById("alerts").innerHTML += "<h2>Точки уже были заданы ранее. Ввод новых точек приведет к пересчету основного эксперимента.</h2>"
      this.number_of_saved_points = 0
    }
  },
  data() {
    return {
      endpoints: ["http://127.0.0.1:5000/api/check/factor_point", "http://127.0.0.1:5000/api/get/factor_points"],
      number_of_experiments: 2,
      factor_points: [
        [10, 10],
        [10, 10],
        [10, 10],
      ],
      y_vals: [0, 0, 0],
      answer: "",
      number_of_saved_points: 0,
    };
  },
  props: {},
  methods: {
    save_number_of_points: function (e) {
      this.$store.dispatch("changeExpData", this.number_of_saved_points);
    },
    send_factor_point: function (index) {
      axios
        .post(this.endpoints[0], {
          data: {
            factor_point: this.factor_points[index],
          },
        })
        .then((response) => {
          if (response.data.error) {
            this.answer = response.data.data.message;
          } else {
            this.number_of_saved_points++;
            this.save_number_of_points()
            this.y_vals[index] = Number(response.data.data.y.toFixed(2));
            this.$forceUpdate();
          }
          document.getElementById("button_"+index).disabled = true;
          setTimeout(function (e) {
              if (index == 0){
                document.getElementById("experiment_0").style.display = "none";
                document.getElementById("experiment_1").style.display = "block";
              }
              else{
                document.getElementById("experiment_1").style.display = "none";
                document.getElementById("text").style.display = "block";
              }
            }, 1500);
            this.$forceUpdate();
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
    show_results: function (e) {
      axios
        .get(this.endpoints[1])
        .then((response) => {
          if (response.data.error) {
            this.answer = response.data.data.message;
          } else {
            this.y_vals = response.data.data.y_vals;
          }
          document.getElementById("factor_points").style.display = "none";
          document.getElementById("results").style.display = "block";
          this.$forceUpdate();
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
  },
};
</script>

<style scoped></style>
