<template>
  <div>
    <b-container>
      <b-row>
        <b-col cols="2"></b-col>
        <b-col cols="8" align="center">
          <b-card class="mb-2 mt-2">
            <h2>Оценка параметров</h2>
            <div id="set_parameters_num">
              <label for="params_num">Сколько параметров содержит модель?</label>
              <b-form-input v-model.number="params_num" type="number" />
              <b-button id="send_params_num" @click="send_params_num()" class="mt-4" variant="primary">Сохранить</b-button>
            </div>
            <div id="set_const_param" style="display: none">
              <label for="const_param">Чему равна постоянная составляющая модели?</label>
              <b-form-input v-model.number="const_param" type="number" />
              <label for="var_const_param">Чему равна дисперсия этого параметра?</label>
              <b-form-input v-model.number="var_const_param" type="number" />
              <b-button id="send_const_param" @click="send_const_param()" class="mt-4" variant="primary">Сохранить</b-button>
            </div>
            <div id="set_next_param" style="display: none">
              <label for="next_param">Чему равен параметр В12?</label>
              <b-form-input v-model.number="next_param" type="number" />
              <label for="var_b12_param">Чему равна его дисперсия?</label>
              <b-form-input v-model.number="var_b12_param" type="number" />
              <b-button id="send_next_param" @click="send_next_param()" class="mt-4" variant="primary">Сохранить</b-button>
            </div>
            <div id="get_params" style="display: none">
              <h3>Оценки параметров модели объекта:</h3>
              <table class="table table-bordered">
                <thead>
                  <tr>
                    <th>Обозначение</th>
                    <th>Оценка</th>
                    <th>Дисперсия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(n, i) in notation.length" :key="i">
                    <td>{{ notation[i] }}</td>
                    <td> {{ Number(model_params[i].toFixed(3)) }}</td>
                    <td> {{ Number(model_params_var.toFixed(3)) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </b-card>
          <b-alert class="mt-2" variant="danger" :show="params_num_answer ? true : false">
            {{ params_num_answer }}</b-alert
          >
          <b-alert class="mt-2" variant="danger" :show="const_param_answer ? true : false">
            {{ const_param_answer }}</b-alert
          >
          <b-alert class="mt-2" variant="danger" :show="next_param_answer ? true : false">
            {{ next_param_answer }}</b-alert
          >
          <div class="mb-5 mt-5">
            <b-button variant="secondary" to="/significance">Далее</b-button>
          </div>
        </b-col>
      </b-row>
    </b-container>
    <div class="documentation">
      <b-card bg-variant="info">
      <p>
        Уточните по списку существующих переменных, сколько параметром должно присутствовать в модели объекта.
      </p>
      <p>
        Для вычисления оценок параметров модели используется метод наименьших квадратов (МНК)
Исходными данными для вычисления являются:
<ol>
<li>матрица спектра плана</li>
<li>средние значения отклика в эксперименте, записанные в виде вектора, номера строк которого соответствуют номерам точек плана</li>
<li>матрица численных значений базисных функций</li>
</ol>
      </p>
      <p>
        Оценивается вектор параметров модели, номера строк этого вектора - порядковые номера базисных функций ( имеется в виду тот порядок, в котором базисные функции воли в матрицу численных значений базисных функций
      </p>
      <p>
        Поскольку результаты измерения отклика сопровождается случайными ошибками, оценки параметров модели будут случайными величинами.
      </p>
      <p>
        При использовании МНК неизвестный вектор коэффициентов находится из условия минимизации суммы квадратов отклонений измеренных значений отклика от от получаемых по модели.
      </p>
      <p>
        Например, пусть требуется оценить параметры модели для объекта со следующим списком существенных переменных:<br> 1, X1, X2, X1*X2<br>
      </p>
      <p>
        Дана матрица спектра плана: ПФЭ, n=2, m=4. 
      </p>
      <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Точка плана</th>
                  <th>Х1</th>
                  <th>Х2</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1</td>
                  <td>+1</td>
                  <td>+1</td>
                </tr>
                <tr>
                  <td>2</td>
                  <td>-1</td>
                  <td>+1</td>
                </tr>
                <tr>
                  <td>3</td>
                  <td>+1</td>
                  <td>-1</td>
                </tr>
                <tr>
                  <td>4</td>
                  <td>-1</td>
                  <td>-1</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
      <p>
        Известно, что в результате проведения эксперимента получены средние значения отклика:
      </p>
      <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Точка ФП</th>
                  <th>Среднее значение</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1</td>
                  <td>287.62</td>
                </tr>
                <tr>
                  <td>2</td>
                  <td>-148.62</td>
                </tr>
                <tr>
                  <td>3</td>
                  <td>-302.70</td>
                </tr>
                <tr>
                  <td>4</td>
                  <td>160.13</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
      <p>
        Построим матрицу численных значений базисных функций:
      </p>
      <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <td rowspan="2">Точка плана</td>
                  <td colspan="3">Сущ. переменные</td>
                </tr>
                <tr>
                  <td>X1</td>
                  <td>X2</td>
                  <td>X1*X2</td>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1</td>
                  <td>+1</td>
                  <td>+1</td>
                  <td>+1</td>
                </tr>
                <tr>
                  <td>2</td>
                  <td>-1</td>
                  <td>+1</td>
                  <td>-1</td>
                </tr>
                <tr>
                  <td>3</td>
                  <td>+1</td>
                  <td>-1</td>
                  <td>-1</td>
                </tr>
                <tr>
                  <td>4</td>
                  <td>-1</td>
                  <td>-1</td>
                  <td>+1</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
      <p>
        Тогда расчет параметров модели будет проводиться так:<br>
В0 = (287.62 + (-148.62) + (-302.70) + 160. 13) / 4 = -0.891<br>
B1 = (1×287.62 + (-1)*(-148.62) + 1*(-302.70) + (-1)*160.13) / 4 = -6.647<br>
B2 = (1*287.62 + 1×(-148.62) + (-1)*(-302.70) + (-1)*160.13) / 4 = 70.393<br>
B12 = (1*287.62 + (-1)*(-148.62) + (-1)*(-302.70) + 1*160.13) / 4 = 224. 764<br>
      </p>
      <p>Это получены параметры для нормированной модели:<br>
у = -0.891 -6.647 * ((X1 - 1)/ 9) + 70.393*((X2 - 0)/ 20.0) + 225. 764 ( ((X1 - 1)/9)*((X2 - 0)/ 20.0),
</p>
<p>где область планирования определена следующим образом.</p>
<b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <td>Факторы</td>
                  <td>X1</td>
                  <td>X2</td>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Основной уровень</td>
                  <td>1</td>
                  <td>0</td>
                </tr>
                <tr>
                  <td>Интервал варьирования</td>
                  <td>9</td>
                  <td>20</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
        <p>Оценка дисперсии параметра модели производится на основе вычисленной ранее дисперсии воспроизводимости. </p>
        <p>Для планов первого порядка дисперсия оценок параметров модели постоянна:</p>
        <p>Дисп_оц = Дисп_воспр / (N * m),</p>
        <p>где N - число точек спектра плана,<br>
	      m - число параллельных опытов.</p>
        <p>Для планов второго порядка различные группы параметров имеют различные дисперсии:
          <ul>
            <li>Свободный член</li>
            <li>Параметры при факторах</li>
            <li>Параметры при парных взаимодействиях факторов</li>
            <li>Параметры при квадратах факторов</li>
          </ul>
        </p>
        <p>Например, для ПФЭ n=2 при m=3, если получена дисперсия воспроизводимости:<br>Дисп_воспр = 0.39,<br> то дисперсия оценок параметров модели:<br>Дисп_оц = 0.39 / (4 * 3) = 0.032.</p>
        <p></p>
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
      params_num: 0,
      params_num_answer: "",
      const_param: 0,
      var_const_param: 0,
      const_param_answer: "",
      next_param: 0,
      var_b12_param: 0,
      next_param_answer: "",
      notation: ["B0", "B1", "B2","B12"],
      model_params: [0,0,0,0],
      model_params_var: 0,
      endpoints: ["http://127.0.0.1:5000/api/check/param_num", "http://127.0.0.1:5000/api/check/const_param", "http://127.0.0.1:5000/api/check/next_param", "http://127.0.0.1:5000/api/get/params"]
    };
  },
  props: {},
  methods: {
    send_params_num: function (e) {
      axios
        .post(this.endpoints[0], { data: { param_num: this.params_num } })
        .then((response) => {
          if (!response.data.error){
            document.getElementById("set_parameters_num").style.display = "none";
            document.getElementById("set_const_param").style.display = "block";
          }
          else {
            this.params_num_answer = response.data.message;
          }
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
    send_const_param: function (e) {
      axios
        .post(this.endpoints[1], { data: { const_param: this.const_param, var_const_param: this.var_const_param } })
        .then((response) => {
          if (!response.data.error){
            document.getElementById("set_next_param").style.display = "block"
            document.getElementById("set_const_param").style.display = "none"
          }
          else {
            this.const_param_answer = response.data.message;
          }
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
    send_next_param: function (e) {
      axios
        .post(this.endpoints[2], { data: { next_param: this.next_param, var_b12_param: this.var_b12_param } })
        .then((response) => {
          if (!response.data.error){
            document.getElementById("set_next_param").style.display = "none"
            document.getElementById("get_params").style.display = "block"
            axios
              .get(this.endpoints[3])
              .then((response) => {
                if (!response.data.error){
                  this.model_params = response.data.data.params
                  this.model_params_var = response.data.data.var
                }
                else {
                  this.const_param_answer = response.data.message;
                }
              })
              .catch((error) => {
                console.log("-----error-------");
                console.log(error);
              });
          }
          else {
            this.const_param_answer = response.data.message;
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
