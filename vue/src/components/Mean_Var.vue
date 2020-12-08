<template>
  <div>
    <div id="data">
      <input v-model.number="means[0]" type="number" />
      <input v-model.number="vars[0]" type="number" />
      <button @click="send_mean_var">Проверить</button>
    </div>
    <p id="data_p" style="display: none">Не верно.</p>
    <div>
      <p id="correct_data" style="display: none">
        Данные верны. Показать остальные значения?
      </p>
      <button id="show_result" @click="show_results" style="display: none">
        Показать
      </button>
    </div>
    <div id="mean_var_table" style="display: none">
      <table border="2" class="table table-responsive">
        <thead>
          <tr>
            <th scope="col">Точка ФП</th>
            <th scope="col">Среднее значение</th>
            <th scope="col">Оценка дисперсии</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(n, index) in means.length" :key="index">
            <th scope="row">Точка {{ index + 1 }}</th>
            <td>{{ Number(means[index].toFixed(2)) }}</td>
            <td>{{ Number(means[index].toFixed(2)) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  created() {},
  data() {
    return {
      means: [0],
      vars: [0],
      endpoints: [
        "http://127.0.0.1:5000/api/check/mean_var",
        "http://127.0.0.1:5000/api/get/means_vars",
      ],
    };
  },
  props: {},
  methods: {
    send_mean_var: function (e) {
      axios
        .post(this.endpoints[0], {
          data: {
            mean: this.means[0],
            var: this.vars[0],
          },
        })
        .then((response) => {
          if (response.data.message === "") {
            document.getElementById("data").style.display = "none";
            document.getElementById("data_p").style.display = "none";
            document.getElementById("correct_data").style.display = "block";
            document.getElementById("show_result").style.display = "block";
          } else {
            document.getElementById("data_p").style.display = "block";
          }
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
          if (response.data.message === "") {
            this.means = response.data.data.means;
            this.vars = response.data.data.vars;
            document.getElementById("mean_var_table").style.display = "block";
          } else {
            //document.getElementById("data_p").style.display = "block";
          }
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
