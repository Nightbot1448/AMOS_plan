<template>
  <div>
  <div id="alerts"></div>
  <div id="factor_points">
  <div id="experiment_0">
      <h3>Опыт 1</h3>
      <p>
        <input type="number" v-model.number="factor_points[0][0]" />
        <input type="number" v-model.number="factor_points[0][1]" />
        <button id="button_0" @click="send_factor_point(0)">Сохранить</button> <p id="text_0"></p>
        <p>Результат: {{y_vals[0]}}</p>
      </p>
    </div>
    <div id="experiment_1" style="display: none">
      <h3>Опыт 2</h3>
      <p>
        <input type="number" v-model.number="factor_points[1][0]" />
        <input type="number" v-model.number="factor_points[1][1]" />
        <button id="button_1" @click="send_factor_point(1)">Сохранить</button> <p id="text_1"></p>
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
    <div class="documentation">
      <p>
        Результатом проведения основного эксперимента является получение значений отклика во всех точках плана, которые заносятся в таблицу, строки которой соответствуют номерам точек плана, а столбцы - номерам параллельных опытов.
      </p>
      <p>
        *Здесь должна быть таблица с примером того как оно выглядит*
      </p>
      <p>
        Для проведения опыта Вам необходимо задать точку плана, в которой будет проведен опыт с указанным номером. Причем требуется ввести значения факторов реальном масштабе. Значение фактора в реальном масштабе вычисляется с помощью основного фактора и фактора.
      </p>
      <p>
        Так как на объект воздействуют неуправляемые и неконтролируемые факторы, то отклик объекта имеет случайный То характер, поэтому в качестве значения отклика в каждой точке факторного пространства принимается случайная величина с математическим ожиданием, равным среднему значению отклика в параллельных опытах, и с дисперсией, вычисляемой также по параллельным опытам.
      </p>
      <p>
        Результаты вычислений оформляется в виде таблицы, строки которой соответствуют номерам точек плана, а столбцы - средним значениям и дисперсиям.
      </p>
      <p>
        Например, пусть в результате проведения эксперимента получены следующие значения отклика
      </p>
      <p>
        *здесь должен быть пример таблицы с дисперсиями и средними*
      </p>
      <p>
        Тогда среднее значение в первой точке будет считаться так:
y = ( 287.96 + 287.11 + 287.79) / 3 = 287.62
Дисперсия отклика в первой точке:
D(y)=( (287.96 - 287.62)^2 + (287.11 - 287.62)^2 + (287.79 - 287.62)^2)/(3-1) = 0.20

      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  mounted() {
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
            if (index == 0){
              document.getElementById("text_0").innerText = response.data.message;
            }
            else {
              document.getElementById("text_1").innerText = response.data.message;
            }
          } else {
            this.number_of_saved_points++;
            this.save_number_of_points()
            this.y_vals[index] = Number(response.data.data.y.toFixed(2));
            this.$forceUpdate();
            document.getElementById("button_"+index).disabled = true;
            setTimeout(function (e) {
                if (index == 0){
                  document.getElementById("experiment_0").style.display = "none";
                  document.getElementById("experiment_1").style.display = "block";
                  this.message = ""
                }
                else{
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
