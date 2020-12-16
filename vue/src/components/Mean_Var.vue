<template>
  <div>
    <b-container>
      <b-row>
        <b-col cols="2"></b-col>
        <b-col cols="8" align="center">
          <b-card class="mb-2 mt-2">
            <div id="data">
              <h3>Средние и дисперсии</h3>
              <p>
                Введите среднее значение отклика и оценку дисперсии отклика для точки 1.
              </p>
              <b-container>
                <b-row class="ml-5">
                  <b-col cols="4">
                    <b-form-input v-model.number="means[0]" type="number" />
                  </b-col>
                  <b-col cols="4">
                    <b-form-input v-model.number="vars[0]" type="number" />
                  </b-col>
                  <b-col cols="3">
                    <b-button id="check_mean_var" @click="send_mean_var" variant="primary"
                      >Проверить</b-button
                    >
                  </b-col>
                </b-row>
              </b-container>
            </div>
            <div>
              <p id="correct_data" style="display: none">
                Данные верны. Показать остальные значения?
              </p>
              <b-button
                id="show_result"
                @click="show_results"
                style="display: none"
                variant="primary"
              >
                Показать
              </b-button>
            </div>
            <div id="mean_var_table" style="display: none" class="table-responsive mt-4">
              <table class="table table-bordered">
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
                    <td>{{ Number(vars[index].toFixed(2)) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </b-card>
          <b-alert class="mt-2" variant="danger" :show="data_p ? true : false">
            {{ data_p }}</b-alert
          >
          <div class="mb-5 mt-5">
            <b-button variant="secondary" to="/reproducibility">Далее</b-button>
          </div>
        </b-col>
      </b-row>
    </b-container>
    <div class="documentation">
      <b-card bg-variant="info">
        <p>См. Таблица с результатами отклика</p>
      </b-card>
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
      data_p: "",
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
            document.getElementById("correct_data").style.display = "block";
            document.getElementById("show_result").style.display = "block";
            document.getElementById("check_mean_var").disabled = true;
          } else {
            this.data_p = response.data.message;
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
            document.getElementById("show_result").disabled = true;
          } else {
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
