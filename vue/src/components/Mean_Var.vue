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
        <p>
          Так как на объект воздействуют неуправляемые и неконтролируемые факторы, то
          отклик объекта имеет случайный То характер, поэтому в качестве значения отклика
          в каждой точке факторного пространства принимается случайная величина с
          математическим ожиданием, равным среднему значению отклика в параллельных
          опытах, и с дисперсией, вычисляемой также по параллельным опытам.
        </p>
        <p>
          Результаты вычислений оформляется в виде таблицы, строки которой соответствуют
          номерам точек плана, а столбцы - средним значениям и дисперсиям.
        </p>
        <p>
          Например, пусть в результате проведения эксперимента получены следующие значения
          отклика:
        </p>
        <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th rowspan="2">Точка ФП</th>
                  <th colspan="3" align="center">Параллельные опыты</th>
                </tr>
                <tr>
                  <th>1</th>
                  <th>2</th>
                  <th>3</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1</td>
                  <td>287.96</td>
                  <td>287.11</td>
                  <td>287.79</td>
                </tr>
                <tr>
                  <td>2</td>
                  <td>-149.15</td>
                  <td>-149.15</td>
                  <td>-147.69</td>
                </tr>
                <tr>
                  <td>3</td>
                  <td>-303.06</td>
                  <td>-302.36</td>
                  <td>-302.66</td>
                </tr>
                <tr>
                  <td>4</td>
                  <td>159.70</td>
                  <td>160.99</td>
                  <td>159.69</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
        <p>
          Тогда среднее значение в первой точке будет считаться так: y = ( 287.96 + 287.11
          + 287.79) / 3 = 287.62 <br />Дисперсия отклика в первой точке: D(y)=( (287.96 -
          287.62)^2 + (287.11 - 287.62)^2 + (287.79 - 287.62)^2)/(3-1) = 0.20<br />
          Остальные значения средних и дисперсий приведены в таблице:
        </p>
        <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Точка ФП</th>
                  <th>Среднее значение</th>
                  <th>Оценка дисперсии</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1</td>
                  <td>287.62</td>
                  <td>0.20</td>
                </tr>
                <tr>
                  <td>2</td>
                  <td>-148.62</td>
                  <td>0.65</td>
                </tr>
                <tr>
                  <td>3</td>
                  <td>-302.70</td>
                  <td>0.12</td>
                </tr>
                <tr>
                  <td>4</td>
                  <td>160.13</td>
                  <td>0.56</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
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
