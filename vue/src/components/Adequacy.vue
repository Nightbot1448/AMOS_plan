<template>
  <div>
    <b-container>
      <b-row>
        <b-col cols="1"></b-col>
        <b-col cols="9" align="center">
          <b-card class="mb-2 mt-2">
            <h2>Адекватность модели</h2>
            <div id="significance">
              <label for="significance">Уровень значимости</label>
              <b-form-select id="significance" v-model.number="significance" type="number">
                <option>0.01</option>
                <option>0.05</option>
              </b-form-select>
              <b-button @click="send_significance" variant="primary" class="mt-4" id="send_sign">Сохранить</b-button>
            </div>
            <div id="var_adequacy" style="display: none">
              <label for="var_adequacy"
                >Чему равна дисперсия адекватности:</label
              >
              <b-form-input v-model.number="var_adequacy" type="number" />
              <b-button class="mt-4" id="ade_var" @click="send_var_adequacy" variant="primary">Проверить</b-button>
            </div>
            <div id="adequacy_prac" style="display: none">
              <label for="adequacy_prac">Введите наблюдаемое значение критерия Фишера:</label>
              <b-form-input v-model.number="adequacy_prac" type="number" />
              <b-button class="mt-4" id="ade_prac" @click="send_adequacy_prac" variant="primary">Проверить</b-button>
            </div>
            <div id="fisher_table" style="display: none">
              <table class="table table-bordered">
                <thead>
                  <tr>
                    <th rowspan="2">Степени свободы знаменателя</th>
                    <th :colspan="numerators.length">Число степеней свободы числителя</th>
                  </tr>
                  <tr>
                      <th v-for="(n,i) in numerators.length" :key="i">
                          {{ numerators[i] }}
                      </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(n, j) in vals.length" :key="j">
                    <td>{{ denominators[j] }}</td>
                    <td v-for="(n, k) in vals[j].length" :key="k">{{ vals[j][k] }}</td>
                  </tr>
                </tbody>
              </table>
              <label for="df_num_fisher">Введите число степеней свободы числителя критерия Фишера:</label>
              <b-form-input v-model.number="df_num_fisher" type="number" />
              <label for="df_den_fisher">Введите число степеней свободы знаменателя критерия Фишера:</label>
              <b-form-input v-model.number="df_den_fisher" type="number" />
              <b-button class="mt-4" id="df_fisher" @click="send_df_fisher" variant="primary">Проверить</b-button>
            </div>
            <div id="adequacy_check" style="display: none">
                <p>Наблюдаемое значение критерия: {{ Number(prac_value.toFixed(2)) }}</p>
                <p>Критическое значение критерия: {{ Number(crit_value.toFixed(2)) }}</p>
                <p>Модель адекватна?</p>
                <b-button @click="is_adeq(true)" variant="primary">Да</b-button>
              <b-button @click="is_adeq(false)" variant="primary">Нет</b-button>
            </div>
            <div id="fisher_results" style="display: none">
                <p>Проверка проводилась по критерию Фишера на уровне значимости {{ significance }}.</p>
                <p>Наблюдаемое значение критерия: {{ Number(prac_value.toFixed(3)) }}</p>
                <p>Критическое значение критерия: {{ Number(crit_value.toFixed(3)) }}</p>
                <p>Вывод: Модель <span v-if="!is_adeq_model">не</span>адекватна.</p>
            </div>
          </b-card>
          <b-alert class="mt-2" variant="danger" :show="significance_answer ? true : false">
            {{ significance_answer }}</b-alert
          >
          <b-alert class="mt-2" variant="danger" :show="var_adequacy_answer ? true : false">
            {{ var_adequacy_answer }}</b-alert
          >
          <b-alert class="mt-2" variant="danger" :show="adequacy_prac_answer ? true : false">
            {{ adequacy_prac_answer }}</b-alert
          >
          <b-alert class="mt-2" variant="danger" :show="adequacy_check_answer ? true : false">
            {{ adequacy_check_answer }}</b-alert
          >
          <b-alert class="mt-2" variant="success" :show="adequacy_true_answer ? true : false">
            {{ adequacy_true_answer }}</b-alert
          >
          <b-alert class="mt-2" variant="danger" :show="adequacy_false_answer ? true : false">
            {{ adequacy_false_answer }}</b-alert
          >
        </b-col>
      </b-row>
    </b-container>
    <div class="documentation">
      <b-card bg-variant="info">
        <p>Число степеней свободы дисперсии адекватности число точек спектра плана N минус количество измерений, использованных для вычисления значимых коэффициентов: для N-d.</p>
        <p>Значение отклика по модели в некоторой точки ФП - численное значение, полученное в результате подстановки в уравнении регрессии значений факторов, соответствующих указанной точке плана.</p>
        <p>В работе рассматривается нормированная модель, т.е. модель, параметры которой рассчитаны для нормированных значений факторов.</p>
        <p>Например, пусть требуется вычислить значения отклика по модели двухфакторного объекта ( n = 2 ) первого порядка, имеющего следующий список существенных переменнных:</p>
        <p>1, Х1, Х2, Х1*Х2 .</p>
        <p>Дана матрица спектра плана:<br>ПФЭ, m=2, N=4</p>
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
        <p>Параметры нормированной модели имеют следующие значения:</p>
        <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Обозначение</th>
                  <th>Оценка</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>B0</td>
                  <td>-0.891</td>
                </tr>
                <tr>
                  <td>B1</td>
                  <td>-6.647</td>
                </tr>
                <tr>
                  <td>B2</td>
                  <td>70.393</td>
                </tr>
                <tr>
                  <td>B12</td>
                  <td>224.764</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
        <p>Тогда значение отклика по модели в третьей точке плана считается так:</p>
        <p>y = - 0.891 - 6.647*1 + 70.393*(-1) + 224.764 * 1 * (-1) = -302.70</p>
        <p>Для остальных точек спектра плана:</p>
        <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Точка плана</th>
                  <th>Отклик по модели</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1</td>
                  <td>287.63</td>
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
        <p>Средние значения отклика, полученные экспериментальным путем, вообще говоря, могут не совпадать со значениями отклика, вычисленными по модели, следовательно разности среднего значения и предсказанного значения отклика несут информации об ошибках предсказания по уравнению регрессии.</p>
        <p>Для анализа свойств полученной модели вычисляется дисперсия адекватности, которая интегрально оценивает степень рассеяния экспериментальных данных относительно линии регрессии.</p>
        <p>Если число степеней свободы дисперсии адекватности равно нулю, то вычисление дисперсии адекватности оказывается невозможным. Возникновение такой ситуации возможно для насыщенных планов - планов, у которых число точек спектра равно количеству параметров модели, которые требуется оценить, когда все вычисляемые коэффициенты оказываются значимыми.</p>
        <p>В этом случае необходимо провести дополнительные опыты в некоторой точке факторного пространства, тем самым увеличив число точек спектра плана по сравнению с количеством значимых коэффициентов d.</p>
        <p>Проведение нескольких параллельных опытов в дополнительной точке дает 1 степень свободы для дисперсии адекватности.</p>
        <p>Например, пусть для исследования двухфакторного объекта n = 2 используется ПФЭ; рассматриваются две ситуации:
          <ol>
            <li>все параметры модели оказались значимыми;</li>
            <li>параметр ВО был признан незначимым и исключен из модели.</li>
          </ol><br>Требуется найти дисперсию адекватности для обоих случаев.
        </p>
        <p>1. Все параметры модели значимы.<br>Т.к. для ПФР N = 4 и все параметры модели двухфакторного объекта ( BO, B1, B2, B12 ) оказались значимыми - d = 4, то количество степеней свободы дисперсии адекватности N - d равно нулю. Следовательно для вычисления дисперсии адекватности придется провести дополнительный эксперимент, что добавит одну степень свободы; тогда дисперсия адекватности рассчитывается по формуле:</p>
        <p>Дисп_адекв = m(у -B0)^2</p>
        <p>Пусть в дополнительном эксперименте получены значения отклика:</p>
        <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th rowspan="2">Точка ФП</th>
                  <th colspan="3">Паралелльные опыты</th>
                </tr>
                <tr>
                  <th>1</th>
                  <th>2</th>
                  <th>3</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>5</td>
                  <td>-0.42</td>
                  <td>-0.42</td>
                  <td>-0.42</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
        <p>Найдена оценка параметра B0:</p>
        <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <tr>
                <th>Обозначение</th>
                <th>Оценка</th>
              </tr>
              <tr>
                <td>В0</td>
                <td>-0.891</td>
              </tr>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
        <p>Для расчета потребуется найти среднее значение отклика в дополнительном эксперименте:</p>
        <p>y = (-0.42 - 0.42 - 0.42)/3 = -0.42</p>
        <p>Тогда дисперсия адекватности будет рассчитываться так:</p>
        <p>Дисп_адекв = 3*(-0,42-(-0,891))^2 = 0.66</p>
        <p>2. Параметр ВО незначим.<br>В этом случае для расчета дисперсии адекватности понадобятся следующие данные: средние значения отклика во всех точках спектра плана и значения отклика, полученные по модели, и дисперсия адекватности будет вычисляться по формуле:
        </p>
        <p>Дисп_адекв = (m / (N - d)) × Сумма,</p>
        <p>где Сумма - это сумма квадратов разностей средних значений отклика, полученных в эксперименте, и значений отклика, полученных по модели.</p>
        <p>Пусть имеются следующие данные (отклик рассчитан по приведенной здесь уточненной модели - с исключенным параметров В0)</p>
        <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <tr>
                <th>Обозначение</th>
                <th>Оценка</th>
              </tr>
              <tr>
                <td>В1</td>
                <td>-6.647</td>
              </tr>
              <tr>
                <td>B2</td>
                <td>70.393</td>
              </tr>
              <tr>
                <td>B12</td>
                <td>224.764</td>
              </tr>
            </table>
          </b-col>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Точка плана</th>
                  <th>Среднее значение</th>
                  <th>Отклик по модели</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1</td>
                  <td>287.62</td>
                  <td>288.62</td>
                </tr>
                <tr>
                  <td>2</td>
                  <td>-148.62</td>
                  <td>-147.72</td>
                </tr>
                <tr>
                  <td>3</td>
                  <td>-302.70</td>
                  <td>-301.80</td>
                </tr>
                <tr>
                  <td>4</td>
                  <td>160.13</td>
                  <td>161.02</td>
                </tr>
              </tbody>
            </table>
          </b-col>
        </b-row>
        <p>Число параллельных опытов = 3.<br>Число точек спектра плана N = 4.<br>Число значимых параметров d = 3.
        </p>
        <p>Дисп_адекв = ( 3 / (4 - 3) ) * 2<br>* ( (287.62 - 288.62)^2 + (-148.62 + 147.72)^2 +<br>+ (-302.70 + 301.80)^2 + (160.13 - 161.02)^2 ) =<br>= 9.60
        </p>
        <p>Наблюдаемое значение критерия Фишера - отношение дисперсии адекватности к дисперсии воспроизводимости.</p>
        <p>Например, пусть:<br>Дисп_адекв = 0.66,<br>Дисп_воспр = 0.39,
        </p>
        <p>тогда наблюдаемое значение критерия Фишера:<br>Набл_Фиш = 0.66 / 0.39 = 1.707
        </p>
        <p>Число степеней свободы числителя критерия Фишера - число степеней свободы, связанных с дисперсией адекватности: 
          <ol>
            <li>разность числа точек спектра плана N и количества измерений, потребовавшихся для вычисления значимых параметров модели d: N-d;</li>
            <li>в случае, если N-d = 0, то для вычисления дисперсии адекватности проводится дополнительный эксперимент, что добавляет одну степень свободы, т.о. в этом случае число степеней свободы числителя критерия Фишера - 1</li>
          </ol>
        </p>
        <p>Число степеней свободы знаменателя критерия Фишера - число степеней свободы, связанных с дисперсией воспроизводимости:</p>
        <p>N * (m-1).</p>
        <p>Проверка адекватности осуществляется путем сопоставления выборочных дисперсий адекватности и воспроизводимости. Для модели, адекватной реальному объекту, единственная причина, по которой дисперсия адекватности может отличаться от нуля, - это воздействие шума.</p>
        <p>При этом проверка адекватности сводится к проверке гипотез вида:
          <ol start="0">
            <li>“Дисперсии воспроизводимости и адекватности оценивают одну и ту же величину - дисперсию шума”,</li>
            <li>“Дисперсия адекватности систематически превышает дисперсию воспроизводимости”</li>
          </ol>
        </p>
        <p>Проверку адекватности проводят с помощью критерия Фишера:<br>если наблюдаемое значение критерия Фишера меньше критического значения критерия Фишера, то принимается нулевая гипотеза об однородности дисперсий адекватности и воспроизводимости и модель считается адекватной на выбранном уровне значимости.
        </p>
        <p>В противном случае модель считается неадекватной отклику объекта, вследствие наличия дополнительного рассеяния, обусловленного несоответствием модели и реального объекта.</p>
        <p>Например, если наблюдаемое значение критерия Фишера:<br>Набл_Фиш = 1.707,<br>а критическое: Крит_Фиш(1, 8, 0.05) = 5.035,<br>то гипотеза об адекватности модели принимается на уровне значимости а = 0.05.</p>
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
      significance: 0.01,
      significance_answer: "",
      var_adequacy: 0,
      var_adequacy_answer: "",
      adequacy_prac: 0,
      adequacy_prac_answer: "",
      vals: [[]],
      numerators: [],
      denominators: [],
      df_num_fisher: 0,
      df_den_fisher: 0,
      adequacy_check_answer: "",
      crit_value: 0,
      prac_value: 0,
      is_adeq_model: false,
      adequacy_true_answer: "",
      adequacy_false_answer: "",
      endpoints: [
        "http://127.0.0.1:5000/api/set/significance_level_fisher",
        "http://127.0.0.1:5000/api/check/adequacy_var", 
        "http://127.0.0.1:5000/api/check/prac_fisher", 
        "http://127.0.0.1:5000/api/get/fisher_table", 
        "http://127.0.0.1:5000/api/check/fisher_freedom_degree", 
        "http://127.0.0.1:5000/api/check/is_adequacy"]
    };
  },
  props: {},
  methods: {
    send_significance: function (e) {
      axios
        .post(this.endpoints[0], { data: { significance: this.significance } })
        .then((response) => {
          if (!response.data.error) {
            document.getElementById("send_sign").disabled = true;
            document.getElementById("significance").style.display = "none";
            document.getElementById("var_adequacy").style.display = "block";
          } else {
            this.significance_answer = response.data.message
          }
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
    send_var_adequacy: function (e) {
      axios
        .post(this.endpoints[1], { data: { adequacy_var: this.var_adequacy } })
        .then((response) => {
          if (!response.data.error) {
            document.getElementById("ade_var").disabled = true;
            document.getElementById("var_adequacy").style.display = "none";
            document.getElementById("adequacy_prac").style.display = "block";
          } else {
            this.var_adequacy_answer = response.data.message
          }
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
    send_adequacy_prac: function (e) {
      axios
        .post(this.endpoints[2], { data: { prac_fisher: this.adequacy_prac } })
        .then((response) => {
          if (!response.data.error) {
            document.getElementById("ade_prac").disabled = true;
            document.getElementById("adequacy_prac").style.display = "none";
            axios
            .get(this.endpoints[3])
            .then((response) => {
                if (!response.data.error) {
                    this.vals = response.data.data.vals;
                    this.numerators = response.data.data.numerators;
                    this.denominators = response.data.data.denominators;
                    document.getElementById("fisher_table").style.display = "block";
              } else {
                this.adequacy_prac_answer = response.data.message
              }
            })
            .catch((error) => {
              console.log("-----error-------");
              console.log(error);
            });
          } else {
            this.adequacy_prac_answer = response.data.message
          }
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
    send_df_fisher: function (e) {
      axios
        .post(this.endpoints[4], { data: { df_numerator: this.df_num_fisher, df_denominator: this.df_den_fisher, } })
        .then((response) => {
          if (!response.data.error) {
            this.crit_value = response.data.data.crit_value
            this.prac_value = response.data.data.prac_value
            document.getElementById("df_fisher").disabled = true;
            document.getElementById("fisher_table").style.display = "none";
            document.getElementById("adequacy_check").style.display = "block";
          } else {
            this.adequacy_check_answer = response.data.message
          }
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
    is_adeq: function (answer) {
      this.is_adeq_model = answer;
      axios
        .post(this.endpoints[5], { data: { is_adequacy: answer } })
        .then((response) => {
          if (!response.data.error) {
            this.adequacy_true_answer = response.data.message
            document.getElementById("adequacy_check").style.display = "none";
            document.getElementById("fisher_results").style.display = "block";
          } else {
            this.adequacy_false_answer = response.data.message
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
