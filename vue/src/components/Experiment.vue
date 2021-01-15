<template>
  <div>
    <b-container>
      <b-row>
        <b-col cols="2"></b-col>
        <b-col cols="8" align="center">
          <b-card class="mb-2 mt-2">
            <div id="factor_points">
              <h2>Проведение эксперимента</h2>
              <div id="experiment_0">
                <h3>Опыт 1</h3>
                <b-container>
                  <b-row class="ml-5">
                    <b-col cols="4">
                      <b-form-input type="number" v-model.number="factor_points[0][0]" />
                    </b-col>
                    <b-col cols="4">
                      <b-form-input type="number" v-model.number="factor_points[0][1]" />
                    </b-col>
                    <b-col cols="3">
                      <b-button
                        id="button_0"
                        @click="send_factor_point(0)"
                        variant="primary"
                        >Сохранить</b-button
                      >
                      <p id="text_0"></p>
                    </b-col>
                  </b-row>
                  <p>Результат: {{ y_vals[0] }}</p>
                </b-container>
              </div>
              <div id="experiment_1" style="display: none">
                <h3>Опыт 2</h3>
                <b-container>
                  <b-row class="ml-5">
                    <b-col cols="4">
                      <b-form-input type="number" v-model.number="factor_points[1][0]" />
                    </b-col>
                    <b-col cols="4">
                      <b-form-input type="number" v-model.number="factor_points[1][1]" />
                    </b-col>
                    <b-col cols="3">
                      <b-button
                        id="button_1"
                        @click="send_factor_point(1)"
                        variant="primary"
                        >Сохранить</b-button
                      >
                      <p id="text_1"></p>
                    </b-col>
                  </b-row>
                  <p>Результат: {{ y_vals[1] }}</p>
                </b-container>
              </div>
            </div>
            <div id="text" style="display: none">
              <p>Дальше эксперимент выполняется в автоматическом режиме.</p>
              <b-button id="show_res" @click="show_results()" variant="primary"
                >Показать результаты</b-button
              >
            </div>
            <div id="results" style="display: none" class="mt-4 table-responsive">
              <table class="table table-bordered">
                <thead>
                  <tr>
                    <th rowspan="2">Точка ФП</th>
                    <th :colspan="res[0].length" align="center">Параллельные опыты</th>
                  </tr>
                  <tr>
                    <th v-for="(n, j) in res[0].length" :key="j">{{ j + 1 }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(n, i) in res.length" :key="i">
                    <td>{{ i + 1 }}</td>
                    <td v-for="(n, j) in res[0].length" :key="j">
                      {{ Number(res[i][j].toFixed(2)) }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </b-card>
          <b-alert class="mt-2" variant="danger" :show="alert_new_exp">
            Точки уже были заданы ранее. Ввод новых точек приведет к пересчету основного
            эксперимента.</b-alert
          >
          <b-alert class="mt-2" variant="danger" :show="error ? true : false">
            {{ error }}</b-alert
          >
          <b-alert class="mt-2" variant="danger" :show="error2 ? true : false">
            {{ error2 }}</b-alert
          >
          <div class="mb-5 mt-5">
            <b-button variant="secondary" to="/mean_var">Далее</b-button>
          </div>
        </b-col>
      </b-row>
    </b-container>
    <div class="documentation">
      <b-card bg-variant="info">
        <p>
          Для проведения опыта Вам необходимо задать точку плана, в которой будет проведен
          опыт с указанным номером. Причем требуется ввести значения факторов реальном
          масштабе. Значение фактора в реальном масштабе вычисляется с помощью основного
          уровня фактора и его интервала варьирования.
        </p>
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
  mounted() {
    if (this.$store.state.experiments_data != undefined) {
      this.number_of_saved_points = this.$store.state.experiments_data;
    }
    if (this.number_of_saved_points >= 2) {
      this.alert_new_exp = true;
      this.number_of_saved_points = 0;
    }
  },
  data() {
    return {
      endpoints: [
        "http://127.0.0.1:5000/api/check/factor_point",
        "http://127.0.0.1:5000/api/get/factor_points",
      ],
      number_of_experiments: 2,
      factor_points: [
        [10, 10],
        [10, 10],
        [10, 10],
      ],
      y_vals: [0, 0, 0],
      res: [0, 0, 0],
      answer: "",
      number_of_saved_points: 0,
      alert_new_exp: false,
      error: "",
      error2: "",
    };
  },
  props: {},
  methods: {
    save_number_of_points: function (e) {
      this.$store.dispatch("changeExpData", this.number_of_saved_points);
    },
    send_factor_point: function (index) {
      document.getElementById("text_0").innerText = "";
      document.getElementById("text_1").innerText = "";
      axios
        .post(this.endpoints[0], {
          data: {
            factor_point: this.factor_points[index],
          },
        })
        .then((response) => {
          if (response.data.error) {
            if (index == 0) {
              this.error = "Ошибка в опыте 1: " + response.data.message;
            } else {
              this.error2 = "Ошибка в опыте 2: " + response.data.message;
            }
          } else {
            this.number_of_saved_points++;
            this.save_number_of_points();
            this.y_vals[index] = Number(response.data.data.y.toFixed(2));
            this.$forceUpdate();
            document.getElementById("button_" + index).disabled = true;
            if (index == 1) {
              axios
                .get(this.endpoints[1])
                .then((response) => {
                  if (response.data.error) {
                    this.answer = response.data.data.message;
                  } else {
                    this.res = response.data.data.y_vals;
                  }
                })
                .catch((error) => {
                  console.log("-----error-------");
                  console.log(error);
                });
            }
            setTimeout(function (e) {
              if (index == 0) {
                document.getElementById("experiment_0").style.display = "none";
                document.getElementById("experiment_1").style.display = "block";
                this.message = "";
              } else {
                document.getElementById("experiment_1").style.display = "none";
                document.getElementById("text").style.display = "block";
              }
            }, 1500);
            this.$forceUpdate();
          }
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
    show_results: function (e) {
      if (document.getElementById("results").style.display === "none")
        document.getElementById("results").style.display = "block";
      else document.getElementById("results").style.display = "none";
    },
  },
};
</script>

<style scoped></style>
