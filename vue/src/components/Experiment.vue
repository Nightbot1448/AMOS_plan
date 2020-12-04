<template>
  <div>
  <div id="factor_points">
    <div v-for="(experiment, index) in number_of_experiments" :key="index">
      <h3>Опыт {{ index + 1 }}</h3>
      <p>
        <input type="number" v-model.number="factor_points[index][0]" />
        <input type="number" v-model.number="factor_points[index][1]" />
        <button @click="send_factor_point(index)">Сохранить</button> {{ answer }}
        <p>Результат: {{y_vals[index]}}</p>
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
  created() {},
  data() {
    return {
      endpoint: "http://127.0.0.1:5000/api/check/factor_point",
      number_of_experiments: 2,
      factor_points: [
        [10, 10],
        [10, 10],
        [10, 10],
      ],
      y_vals: [0, 0, 0],
      answer: "",
    };
  },
  props: {},
  methods: {
    send_factor_point: function (index) {
      axios
        .post(this.endpoint, {
          data: {
            factor_point: this.factor_points[index],
          },
        })
        .then((response) => {
          if (response.data.error) {
            this.answer = response.data.data.message;
          } else {
            this.y_vals[index] = Number(response.data.data.y.toFixed(2));
            this.$forceUpdate();
          }
          setTimeout(function (e) {
              document.getElementById("factor_points").style.display = "none";
              document.getElementById("text").style.display = "block";
            }, 2000);
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
    show_results: function (e) {
      axios
        .post(this.endpoint, {
          data: {
            factor_point: "",
          },
        })
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
